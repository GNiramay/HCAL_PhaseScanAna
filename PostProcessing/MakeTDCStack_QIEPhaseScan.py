# Program to plot stack plots for skimmed 2023 QIE Phase scan hcalnanos
# Syntax: python3 MakeTDCStack_new.py <input root> <Parity (odd/even)> <output root>
# Example: time python3 MakeTDCStack_QIEPhaseScan.py ../OutRoot/FullQIEPhaseScan2023.root even FullQIEPhaseScan2023_even.root

from sys import argv
from sys import exit as et
from ROOT import TFile, TCanvas
import ROOT as rt

rt.gROOT.SetBatch(True)
TDCInfo = ["Prompt","Slight delay","Delayed","No TDC"]
axName = ["depth","ieta","tshift","TDC"]

if len(argv) !=4:
    print("Arguments not right. Pleas provide <input root> <Parity (odd/even)> <output root>")
    et(1)

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
hN = tf_in.Get(f"hN_TDCvtshift_{argv[2]}")
SOI = 3                         # Sample of Intrest
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
        hs.GetXaxis().SetRangeUser(-10,20)
        tc.BuildLegend(.7,.7,.9,.9)
        tc.SetGrid()
        tc.SaveAs(f'../PNG/QIEPhaseScan_TDCSvTShift_ieta{ee}_depth{dd}_{argv[2]}.png')

tf_out = TFile(argv[3],'RECREATE')

for ss in StackList:
    ss.Write()
tf_out.Write()

tf_out.Close()
tf_in.Close()
