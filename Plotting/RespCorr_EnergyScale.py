# Program to find an approximate energy threshold required to reach the given occupancy (https://cds.cern.ch/record/2891496 page 21, fig 17 a)
# Arguments: <histogram root file> <histogram name> <RefVal text file> <output folder>
import ROOT as rt
import numpy as np
from sys import argv
from array import array as ar
rt.gROOT.SetBatch(True)
rt.gStyle.SetOptStat(0)
rt.gStyle.SetOptTitle(0)

tf = rt.TFile(argv[1],'READ')
hAll = tf.Get(argv[2])
# hAll = tf.Get('hRespCorrData')
InTXT = argv[3]
OutFolder = argv[4]
# OutFolder = '/eos/home-n/ngogate/www/HCAL_DPG/PhaseScan_2024/'

# root file to store the resp. corrections.
OutROOT = InTXT.split('.txt')[0]+'.root'

# 2024 phase scan lumi info
LumiInfo = {"379349":46.48,
            "379350":38.75,
            "Full"  :85.23}

# Get hits over 4GeV
Rechit_energy_thr = 4.0

# Get total no. of bins along all axes
nTotalBins = [hAll.GetAxis(ii).GetNbins() for ii in range(hAll.GetNdimensions())]

# A dictionary of histograms for effective plotting
hNewScale = {}
hNewOccup = {}

for ee in range(-29,30):
    for dd in range(1,8):
        # hNewScale[f'{ee}_{dd}'] = rt.TH1F(f'hNewScale_{ee}_{dd}',f'depth {dd};QIE Phase Offset [ns];Energy Scale',11,-6.5,4.5)
        # hNewOccup[f'{ee}_{dd}'] = rt.TH1F(f'hNewOccup_{ee}_{dd}',f'depth {dd};QIE Phase Offset [ns];Fraction of hits over scaled 4 GeV',11,-6.5,4.5)
        hNewScale[f'{ee}_{dd}'] = rt.TH1F(f'hNewScale_{ee}_{dd}',f'depth {dd};QIE Phase Offset [ns];Energy Scale',31,-10.5,20.5)
        hNewOccup[f'{ee}_{dd}'] = rt.TH1F(f'hNewOccup_{ee}_{dd}',f'depth {dd};QIE Phase Offset [ns];Fraction of hits over scaled 4 GeV',31,-10.5,20.5)

def DrawCMSHeading(opt=1,lumi_pb=300,ycoord=0.91,xleft=0.12,xright=0.7):
    textOnTop = rt.TLatex()
    intLumiE = rt.TLatex()
    textOnTop.SetTextSize(0.04)
    intLumiE.SetTextSize(0.04)
    if opt==1:
        textOnTop.DrawLatexNDC(xleft,ycoord,"CMS #it{#bf{Simulation Supplementary}}")
    if opt==2:
        textOnTop.DrawLatexNDC(xleft,ycoord,"CMS #it{#bf{Simulation Preliminary}}")
    if opt==3:
        textOnTop.DrawLatexNDC(xleft,ycoord,"CMS #it{#bf{Preliminary}}")
    intLumiE.DrawLatexNDC(xright,ycoord,"#bf{"+str(lumi_pb)+" pb^{-1} (13 TeV)}")
    return

# with open('RefVal.txt','r') as f:
with open(InTXT,'r') as f:

    # Loop over each entry (one ieta ring)
    for gg in f.readlines():
        data = gg.split('\t')
        ieta = int(data[0])
        depth = int(data[1])
        ref_occup = float(data[2].split('\n')[0])

        hAll.GetAxis(0).SetRangeUser(depth-.1,depth+.1)
        hAll.GetAxis(1).SetRangeUser(ieta-.1,ieta+.1)

        # Loop over time shift
        for tt in range(1,nTotalBins[2]+1):
            timeshift = hAll.GetAxis(2).GetBinCenter(tt)

            hAll.GetAxis(2).SetRangeUser(timeshift-.1,timeshift+.1)
            hist = hAll.Projection(3)
            hist.SetName(f'h_{depth}_{ieta}_{timeshift}')

            nevt = hist.Integral(0,nTotalBins[3]+1)
            if nevt ==0: continue
            
            bin_id = nTotalBins[3]+1
            Occup = hist.GetBinContent(bin_id)/nevt
            NewThr = hist.GetBinLowEdge(bin_id)

            while Occup < ref_occup:
                bin_id -=1
                Occup += hist.GetBinContent(bin_id)/nevt
                NewThr = hist.GetBinLowEdge(bin_id)

            hNewScale[f'{ieta}_{depth}'].Fill(timeshift,NewThr/Rechit_energy_thr)
            hNewOccup[f'{ieta}_{depth}'].Fill(timeshift,Occup)

def WriteRespCorr():
    # Prepare root file, TTree to store the values
    OutFile = rt.TFile(OutROOT,'RECREATE')
    OutTree = rt.TTree('RespCorrData','compensating response corrections')
    Data = [np.array([0],np.int_),
            np.array([0],np.int_),
            np.array([0],np.int_),
            np.array([0],np.int_),
            np.array([0],np.float64)]
    
    for ii,vv in enumerate([['ieta','I'],
                            ['depth','I'],
                            ['InitialPhase','I'],
                            ['FinalPhase','I'],
                            ['RespCorr','D']]):
        OutTree.Branch(vv[0],Data[ii],vv[0]+'/'+vv[1])

    # Loop over histograms for each ieta ring
    for nn,hh in hNewScale.items():
        if hh.GetEntries() == 0: continue
        ieta_,depth_ = nn.split('_')
        Data[0][0] = int(ieta_)
        Data[1][0] = int(depth_)
        nBins = hh.GetNbinsX()
        for ii in range(nBins):
            Data[2][0] = hh.GetBinCenter(ii+1)
            for jj in range(ii,nBins):
                if hh.GetBinContent(jj+1) == 0: continue
                Data[3][0] = hh.GetBinCenter(jj+1)
                Data[4][0] = hh.GetBinContent(ii+1)/hh.GetBinContent(jj+1)
                OutTree.Fill()

    OutTree.Write()
    OutFile.Close()
    return

# Plot occupancy
for ee in range(-29,30):
    if ee == 0:continue
    tc = rt.TCanvas('aa','bb',800,600)
    tc.SetMargin(.11,.05,.1,.1)
    YMax = 0.0
    for dd in range(1,8):
        if YMax < hNewOccup[f'{ee}_{dd}'].GetMaximum():
            YMax = hNewOccup[f'{ee}_{dd}'].GetMaximum()
    
    for dd in range(1,8):
        if hNewOccup[f'{ee}_{dd}'].GetEntries() == 0: continue
        hNewOccup[f'{ee}_{dd}'].SetMaximum(1.44*YMax)
        hNewOccup[f'{ee}_{dd}'].SetLineWidth(0)
        hNewOccup[f'{ee}_{dd}'].SetMarkerColor(dd)
        hNewOccup[f'{ee}_{dd}'].SetMarkerStyle(21)
        hNewOccup[f'{ee}_{dd}'].Draw('p same')
    tc.BuildLegend(.75,.7,.95,.9)
    # tc.SetGrid()
    DrawCMSHeading(3,LumiInfo['Full'])
    etaInfo = rt.TLatex()
    etaInfo.SetTextSize(0.04)
    etaInfo.DrawLatexNDC(0.14,0.85,f"i#eta {ee}")
    tc.SaveAs(OutFolder+f'NewOccup/IEta_{ee}.png')
    tc.SaveAs(OutFolder+f'NewOccup/IEta_{ee}.pdf')
    del tc

# Plot New energy scale
for ee in range(-29,30):
    if ee == 0:continue
    tc = rt.TCanvas('aa','bb',800,600)
    tc.SetMargin(.11,.05,.1,.1)
    YMax = 0.0
    for dd in range(1,8):
        if YMax < hNewScale[f'{ee}_{dd}'].GetMaximum():
            YMax = hNewScale[f'{ee}_{dd}'].GetMaximum()
    
    for dd in range(1,8):
        if hNewScale[f'{ee}_{dd}'].GetEntries() == 0: continue
        hNewScale[f'{ee}_{dd}'].SetMaximum(1.44*YMax)
        hNewScale[f'{ee}_{dd}'].SetLineWidth(0)
        hNewScale[f'{ee}_{dd}'].SetMarkerColor(dd)
        hNewScale[f'{ee}_{dd}'].SetMarkerStyle(21)
        hNewScale[f'{ee}_{dd}'].Draw('p same')
    tc.BuildLegend(.75,.7,.95,.9)
    # tc.SetGrid()
    DrawCMSHeading(3,LumiInfo['Full'])
    etaInfo = rt.TLatex()
    etaInfo.SetTextSize(0.04)
    etaInfo.DrawLatexNDC(0.14,0.85,f"i#eta {ee}")
    tc.SaveAs(OutFolder+f'NewScale/IEta_{ee}.png')
    tc.SaveAs(OutFolder+f'NewScale/IEta_{ee}.pdf')
    del tc

WriteRespCorr()
