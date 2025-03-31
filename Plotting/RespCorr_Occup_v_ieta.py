# Calculating compensating response correection
import ROOT as rt
from sys import argv
from array import array as ar
rt.gROOT.SetBatch(True)
rt.gStyle.SetOptStat(0)

# 2024 phase scan lumi info
LumiInfo = {"379349":46.48,
            "379350":38.75,
            "Full"  :85.23}


tf = rt.TFile(argv[1],'READ')
hAll = tf.Get(argv[2])
# hAll = tf.Get('hRespCorrData')

# Write the occupancy reference values to a text file
# There is a freedom to choose the reference value, but for convenience, we will stick to values at 4ns (for 2024 phase scan)
# In general, select a value which is less that what appears at 0 ns
refPhase = 20
# refPhase = 4
fRefVal = open(argv[3],'w')
# fRefVal = open('RefVal_NonzeroRechits.txt','w')

OutFolder = argv[4]
# OutFolder = '/eos/home-n/ngogate/www/HCAL_DPG/PhaseScan_2024/Occup_v_IEta_NonzeroRechits/'

# Get total no. of bins along all axes
nTotalBins = [hAll.GetAxis(ii).GetNbins() for ii in range(hAll.GetNdimensions())]

# Get hits over 4GeV
Rechit_energy_thr = 4.0

hAll.GetAxis(3).SetRange(hAll.GetAxis(3).FindBin(Rechit_energy_thr),nTotalBins[3]+1)
hGood = hAll.Projection(3,ar('i',[0,1,2]))
hAll.GetAxis(3).SetRange(1,nTotalBins[3]+1)

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

# Plot fraction of hits with energy > 4GeV for single ieta ring
def IEtaSlice(hall,hgood,IEta,OutName):
    hall.GetAxis(1).SetRangeUser(IEta-.1,IEta+.1)
    hgood.GetAxis(1).SetRangeUser(IEta-.1,IEta+.1)
    tc = rt.TCanvas('aa','bb',800,600)
    tc.SetMargin(.11,.05,.1,.1)
    hlist = []
    YMax = 0.

    for dd in range(1,8):
        hall.GetAxis(0).SetRangeUser(dd-0.1,dd+0.1)        
        hgood.GetAxis(0).SetRangeUser(dd-0.1,dd+0.1)
        h1 = hall.Projection(2)
        h2 = hgood.Projection(2)
        h1.SetName(f'h1_{dd}')
        h2.SetName(f'h2_{dd}')
        if h1.Integral() == 0: continue
        hRatio = h2.Clone()
        hRatio.SetName(f'hRatio_{dd}')
        hRatio.Divide(h1)

        hRatio.SetLineWidth(0)
        hRatio.SetMarkerStyle(21)
        hRatio.SetMarkerColor(dd)
        hRatio.SetTitle(f'depth {dd};QIE Phase Offset [ns];Fraction of hits over 4 GeV')
        hlist.append(hRatio)
        fRefVal.write(f'{IEta}\t{dd}\t{hRatio.GetBinContent(hRatio.FindBin(refPhase))}\n')

        if YMax < hRatio.GetMaximum():
            YMax = hRatio.GetMaximum()

    # Don't save, if no histogram was made
    if hlist == []:return

    for hh in hlist:
        hh.Draw("p same")
        # hh.GetXaxis().SetRangeUser(-6,4)
        hh.SetMinimum(0)
        hh.SetMaximum(1.2*YMax)
    tc.BuildLegend(.75,.7,.95,.9)
    DrawCMSHeading(3,LumiInfo['Full'])
    etaInfo = rt.TLatex()
    etaInfo.SetTextSize(0.04)
    etaInfo.DrawLatexNDC(0.14,0.85,f"i#eta {IEta}")
    hlist[0].SetTitle('')

    tc.SaveAs(OutName+'.png')
    tc.SaveAs(OutName+'.pdf')
    del tc

    return

# plot each ieta
for ee in range(-29,30):
    IEtaSlice(hAll,hGood,ee,OutFolder+f'IEta_{ee}')
fRefVal.close()

# IEtaSlice(hAll,hGood,15,OutFolder+f'IEta_15')
