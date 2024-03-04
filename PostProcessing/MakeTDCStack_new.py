# Program to plot 1D histograms.
# Syntax: python3 MakeTDCStack_new.py <input root> <output root>
# Example: python3 MakeTDCStack_new.py CondorSubmissions/LEDPhaseScan2024_r377041_TDCFrac_new.root OutRoot/LEDPhaseScan2024_r377041_TDCFrac_new.root
from sys import argv
from ROOT import TFile, TCanvas
import ROOT as rt

rt.gROOT.SetBatch(True)
TDCInfo = ["Prompt","Slight delay","Delayed","No TDC"]
axName = ["depth","ieta","tshift","TDC"]

# Function to make the stackplot.
# ULabel: some unique lable, to ensure 1D histograms don't get overwritten
def GetStack(hist_,ULabel):
    hs_ = rt.THStack()
    hTotEvt = hist_.ProjectionX()
    nxbins = hist_.GetNbinsX()
    nybins = hist_.GetNbinsY()

    hTDC = [rt.TH1F(f"hTDC0_{ULabel}","",nxbins,hTotEvt.GetBinLowEdge(0),hTotEvt.GetBinLowEdge(nxbins)),
            rt.TH1F(f"hTDC1_{ULabel}","",nxbins,hTotEvt.GetBinLowEdge(0),hTotEvt.GetBinLowEdge(nxbins)),
            rt.TH1F(f"hTDC2_{ULabel}","",nxbins,hTotEvt.GetBinLowEdge(0),hTotEvt.GetBinLowEdge(nxbins)),
            rt.TH1F(f"hTDC3_{ULabel}","",nxbins,hTotEvt.GetBinLowEdge(0),hTotEvt.GetBinLowEdge(nxbins))]

    for by in range(nybins):
        hTDC[by].SetTitle(f"TDC {by} ({TDCInfo[by]});time shift [ns]")
        hTDC[by].SetFillColor(by+2)
        hTDC[by].SetLineColor(1)

        for bx in range(nxbins):
            if hTotEvt.GetBinContent(bx+1) > 0:
                hTDC[by].SetBinContent(bx,hist_.GetBinContent(hist_.GetBin(bx+1,by+1))/hTotEvt.GetBinContent(bx+1))

        hs_.Add(hTDC[by])

    return hs_

tf_in = TFile(argv[1])
hN = tf_in.Get("hN_TDCvtshift")
SOI = 4                         # Sample of Intrest
StackList = []

# Loop over depth
for dd in range(1,5):
    hN.GetAxis(0).SetRangeUser(dd-.5,dd+.5)
    # Loop over ieta
    for ee in range(-16,17):
        hN.GetAxis(1).SetRangeUser(ee-.5,ee+.5)
        hh = hN.Projection(3,2)
        hs = GetStack(hh,f'{dd}_{ee}')
        hs.SetTitle(f'HB i#eta {ee} | depth {dd} | TS {SOI};time shift [ns];TDC fraction')
        hs.SetName(f'hTDCStack_ieta{ee}_depth{dd}')
        StackList.append(hs)

        # Plot the graphs.
        tc = rt.TCanvas(f'ieta{ee}_depth{dd}','bb',800,600)
        hs.Draw()
        hs.GetYaxis().SetRangeUser(0,1)
        hs.SetMaximum(1.)
        hs.GetXaxis().SetRangeUser(-12,18)
        tc.BuildLegend(.7,.7,.9,.9)
        tc.SetGrid()
        tc.SaveAs(f'../PNG/TDCSvTShift_ieta{ee}_depth{dd}.png')

tf_out = TFile(argv[2],'RECREATE')

for ss in StackList:
    ss.Write()
tf_out.Write()

tf_out.Close()
tf_in.Close()
