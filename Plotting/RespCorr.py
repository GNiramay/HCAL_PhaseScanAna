# Calculating compensating response correection
import ROOT as rt
from sys import argv
from array import array as ar
rt.gROOT.SetBatch(True)
rt.gStyle.SetOptStat(0)
tf = rt.TFile(argv[1],'READ')
hAll = tf.Get('hRespCorrData')

LumiInfo = {"379349":46.48,
            "379350":38.75,
            "Full"  :85.23}

# Get hits over 4GeV
hAll.GetAxis(3).SetRange(hAll.GetAxis(3).GetNbins(),hAll.GetAxis(3).GetNbins()+1)
hGood = hAll.Projection(3,ar('i',[0,1,2]))
hAll.GetAxis(3).SetRange(0,hAll.GetAxis(3).GetNbins()+1)

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

    for hh in hlist:
        hh.Draw("p same")
        hh.GetXaxis().SetRangeUser(-6,4)
        hh.SetMinimum(0)
        hh.SetMaximum(0.01)
    tc.BuildLegend(.75,.7,.95,.9)
    DrawCMSHeading(3,LumiInfo['Full'])
    etaInfo = rt.TLatex()
    etaInfo.SetTextSize(0.04)
    etaInfo.DrawLatexNDC(0.14,0.85,f"i#eta {IEta}")
    hlist[0].SetTitle('')
    tc.SaveAs(OutName)
    del tc
    return

IEtaSlice(hAll,hGood,15,'/eos/home-n/ngogate/www/HCAL_PFG_Dump/PhaseScan_2024/IEta_15.png')
for ii in range(3):
    for hh in [hAll,hGood]:
        hh.GetAxis(ii).SetRange(0,hh.GetAxis(ii).GetNbins()+1)

# # Loop over depths
# for dd in range(1,8):
#     hAll.GetAxis(0).SetRangeUser(dd-0.1,dd+0.1)
#     hAll_ = hAll.Projection(2,1)
#     hGood.GetAxis(0).SetRangeUser(dd-0.1,dd+0.1)
#     hGood_ = hGood.Projection(2,1)
#     hFinal = rt.TH2F(f'hFinal_depth{dd}',f'depth {dd};i#eta;tshift [ns];Fraction of rechits > 4GeV',61,-30.5,30.5,11,-6.5,4.5)
#     gMax = rt.TGraph()
#     gMaxVal = rt.TGraph()
#     for bX in range(1,62):
#         MaxVal = -1
#         MaxLoc = -1
#         for bY in range(1,22):
#             if hAll_.GetBinContent(bX,bY) >0:
#                 hFinal.Fill(bX-31,bY-11,hGood_.GetBinContent(bX,bY)/hAll_.GetBinContent(bX,bY))
#                 if MaxVal < hGood_.GetBinContent(bX,bY)/hAll_.GetBinContent(bX,bY):
#                     MaxVal = hGood_.GetBinContent(bX,bY)/hAll_.GetBinContent(bX,bY)
#                     MaxLoc = bY-11
#         if MaxVal > -1:
#             gMax.AddPoint(bX-31,MaxLoc)
#             gMaxVal.AddPoint(bX-31,MaxVal)
            
#     tc = rt.TCanvas('aa','bb',800,600)
#     hFinal.Draw('colz')
#     hFinal.GetZaxis().SetTitleOffset(1.3)
#     tc.SetRightMargin(.2)
#     tc.SaveAs(f'/eos/home-n/ngogate/www/HCAL_PFG_Dump/PhaseScan_2024/Depth_{dd}.png')

#     gMax.Draw('apl')
#     tc.SetGrid()
#     gMax.SetMarkerStyle(21)
#     tc.SetRightMargin(.1)
#     gMax.SetTitle(f'Depth {dd};i#eta;Time shift with max fraction [ns]')
#     tc.SaveAs(f'/eos/home-n/ngogate/www/HCAL_PFG_Dump/PhaseScan_2024/Depth_{dd}_MaxLoc.png')

#     gMaxVal.Draw('apl')
#     tc.SetGrid()
#     gMaxVal.SetMarkerStyle(21)
#     tc.SetRightMargin(.1)
#     gMaxVal.SetTitle(f'Depth {dd};i#eta;max. fraction of 4GeV rechits achieeved')
#     tc.SaveAs(f'/eos/home-n/ngogate/www/HCAL_PFG_Dump/PhaseScan_2024/Depth_{dd}_MaxVal.png')
    
#     del tc
#     hFinal.Delete()
#     hGood_.Delete()
#     hAll_.Delete()
#     gMax.Delete()
#     gMaxVal.Delete()
tf.Close()
