## Script to make stack plot of the TDC code, from a 2D histogram of TDC vs shift.
# Syntax: python3 MakeTDCStack.py <input root file> <output png/pdf>
# Example: python3 MakeTDCStack.py ieta6_depth2.root TestPlot.png

import ROOT as rt
from sys import argv

TDCInfo = ["Prompt","Slight delay","Delayed","No TDC"]

def GetStack(hist_):
    hs_ = rt.THStack()
    hTotEvt = hist_.ProjectionX()
    nxbins = hist_.GetNbinsX()
    nybins = hist_.GetNbinsY()

    hTDC = [rt.TH1F("hTDC0","",nxbins,hTotEvt.GetBinLowEdge(0),hTotEvt.GetBinLowEdge(nxbins)),
            rt.TH1F("hTDC1","",nxbins,hTotEvt.GetBinLowEdge(0),hTotEvt.GetBinLowEdge(nxbins)),
            rt.TH1F("hTDC2","",nxbins,hTotEvt.GetBinLowEdge(0),hTotEvt.GetBinLowEdge(nxbins)),
            rt.TH1F("hTDC3","",nxbins,hTotEvt.GetBinLowEdge(0),hTotEvt.GetBinLowEdge(nxbins))]  

    for by in range(1,nybins+1):
        hTDC[by-1].SetTitle(f"TDC {by-1} ({TDCInfo[by-1]});time shift [ns]")
        hTDC[by-1].SetFillColor(by+1)
        hTDC[by-1].SetLineColor(1)

        for bx in range(nxbins):
            if hTotEvt.GetBinContent(bx+1) > 0:
                hTDC[by-1].SetBinContent(bx,hist_.GetBinContent(hist_.GetBin(bx+1,by))/hTotEvt.GetBinContent(bx+1))

        hs_.Add(hTDC[by-1])

    return hs_


# Load the 2D histogram
tf = rt.TFile(argv[1],"READ")
hist = tf.Get("h2TDCvTShift")

# Get the stackplot
hs = GetStack(hist)

tc = rt.TCanvas("aa","bb",800,600)
hs.Draw("hist")
## Some formatting
hs.SetTitle(f"{hist.GetTitle()};time shift [ns];fraction of events")
tc.BuildLegend(.7,.7,.9,.9)
hs.SetMaximum(1)

## Save png
tc.SaveAs(argv[2])
tf.Close()
