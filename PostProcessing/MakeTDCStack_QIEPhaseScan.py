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

tf_in = TFile(argv[1])
hN_ = tf_in.Get(f"hN_TDCvtshift_{argv[2]}")
SOI = 3                         # Sample of Intrest
StackList = []
txtOut = open(f"QIEPhaseScan_PromptPeak_{argv[2]}.txt", "w")
txtOut.write("{}\t{}\t{}\t{}\t{}\n".format("ieta","depth","Mean","StdDev","Chi2"))

# Function that considers cut on CWT as well
# Requires a THnD object with the axes:
# depth  ieta   tshift  TDC  CWT-corrected
def PlotWIthCWTCut(hN):
    hPromptPeak = rt.TH2D("hPromptPeak","mean prompt pulse time;i#eta;depth",33,-16.5,16.5,4,0.5,4.5)
    for dd in range(1,5):
        hN.GetAxis(0).SetRangeUser(dd-.1,dd+.1)
        for ee in range(-16,17):
            if ee == 0:
                continue
            hN.GetAxis(1).SetRangeUser(ee-.1,ee+.1)
            hTDC = [rt.TH1F(f"hTDC0_{dd}_{ee}",f"TDC 0 ({TDCInfo[0]});time shift [ns]",31,-10.5,20.5),
                    rt.TH1F(f"hTDC1_{dd}_{ee}",f"TDC 1 ({TDCInfo[1]});time shift [ns]",31,-10.5,20.5),
                    rt.TH1F(f"hTDC2_{dd}_{ee}",f"TDC 2 ({TDCInfo[2]});time shift [ns]",31,-10.5,20.5),
                    rt.TH1F(f"hTDC3_{dd}_{ee}",f"TDC 3 ({TDCInfo[3]});time shift [ns]",31,-10.5,20.5)]
            hCWTvTShift = rt.TH2F(f"hCWTvTShift_{dd}_{ee}",f'i#eta {ee} | depth {dd};time shift [ns];CWT-tshift (After cut)',31,-10.5,20.5,180,0,180)

            # Taking care of the out-of-time pulses, by placing a cut on CWT-tshift
            for tt in range(-10,21):
                hN.GetAxis(2).SetRangeUser(tt-.1,tt+.1)
                hCWT = hN.Projection(4)
                hCWT.SetName(f"hCWT_{dd}_{ee}_{tt}")
                # hCWT.GetXaxis().SetRangeUser(75,100)
                ModeCWT = hCWT.GetBinCenter(hCWT.GetMaximumBin())
                # if ModeCWT > 100:
                #     ModeCWT -= 25
                # if ModeCWT < 75:
                #     ModeCWT += 25
                ModeCWT = ModeCWT+25.*int(4.-ModeCWT/25.)
                hN.GetAxis(4).SetRangeUser(ModeCWT-5,ModeCWT+5)
                hMyTDC = hN.Projection(3)
                hMyTDC.SetName(f"hMyTDC_{dd}_{ee}_{tt}")
                # htemp = hN.Projection(4,2)
                htemp = hN.Projection(4)
                htemp.SetName(f"hCWTvTShiftData_{dd}_{ee}_{tt}")
                for bb in range(htemp.GetNbinsX()):
                    hCWTvTShift.Fill(tt,htemp.GetBinCenter(bb),htemp.GetBinContent(bb))

                if hMyTDC.GetEntries() > 0:
                    for td in range(4):
                        hTDC[td].SetBinContent(tt+11,hMyTDC.GetBinContent(td+1)/hMyTDC.GetEntries())
                    # hTDC[td].Fill(tt,hMyTDC.GetBinContent(td+1)/hMyTDC.GetEntries())
            hs = rt.THStack()
            for by in range(4):
                hTDC[by].SetFillColor(by+2)
                hTDC[by].SetLineColor(1)
                hs.Add(hTDC[by])

            hs.SetTitle(f'HB i#eta {ee} | depth {dd} | TS {SOI};time shift [ns];TDC fraction')
            hs.SetName(f'hTDCStack_ieta{ee}_depth{dd}')
            StackList.append(hs)
            StackList.append(hCWTvTShift)

            # Plot the graphs.
            tc = rt.TCanvas(f'ieta{ee}_depth{dd}','bb',800,600)
            hs.Draw("hist")
            hs.GetYaxis().SetRangeUser(0,1)
            hs.SetMaximum(1.)
            tc.BuildLegend(.7,.7,.9,.9)
            tc.SetGrid()
            # tc.SaveAs('temp.png')
            # return
            tc.SaveAs(f'../PNG/QIEPhaseScan_TDCSvTShift_ieta{ee}_depth{dd}_{argv[2]}.png')

            # Add the prompt peak mean to hPromptPeak, also print it
            if hTDC[0].GetEntries() == 0:
                continue
            result = hTDC[0].Fit("gaus","NQS")
            if result.Parameter(1) !=0:
                hPromptPeak.Fill(ee,dd,int(10*result.Parameter(1))/10)
            txtOut.write("{}\t{}\t{:.2}\t{:.2}\t{:.2}\n".format(ee,dd,result.Parameter(1),result.Parameter(2),result.Chi2()))
    StackList.append(hPromptPeak)
    # Plot the graphs.
    tc = rt.TCanvas('PromptPeak','bb',1200,600)
    rt.gStyle.SetOptStat(0)
    hPromptPeak.Draw("colz text")
    tc.SaveAs(f'../PNG/QIEPhaseScan_PromptPeak_{argv[2]}.png')

PlotWIthCWTCut(hN_)
txtOut.close()

# # Function to make the stackplot.
# # ULabel: some unique lable, to ensure 1D histograms don't get overwritten
# def GetStack(hist_,ULabel):
#     hs_ = rt.THStack()
#     hTotEvt = hist_.ProjectionX()
#     nxbins = hist_.GetNbinsX()
#     nybins = hist_.GetNbinsY()

#     hTDC = [rt.TH1F(f"hTDC0_{ULabel}","",nxbins,hTotEvt.GetBinLowEdge(0),hTotEvt.GetBinLowEdge(nxbins)),
#             rt.TH1F(f"hTDC1_{ULabel}","",nxbins,hTotEvt.GetBinLowEdge(0),hTotEvt.GetBinLowEdge(nxbins)),
#             rt.TH1F(f"hTDC2_{ULabel}","",nxbins,hTotEvt.GetBinLowEdge(0),hTotEvt.GetBinLowEdge(nxbins)),
#             rt.TH1F(f"hTDC3_{ULabel}","",nxbins,hTotEvt.GetBinLowEdge(0),hTotEvt.GetBinLowEdge(nxbins))]

#     for by in range(nybins):
#         hTDC[by].SetTitle(f"TDC {by} ({TDCInfo[by]});time shift [ns]")
#         hTDC[by].SetFillColor(by+2)
#         hTDC[by].SetLineColor(1)

#         for bx in range(nxbins):
#             if hTotEvt.GetBinContent(bx+1) > 0:
#                 hTDC[by].SetBinContent(bx,hist_.GetBinContent(hist_.GetBin(bx+1,by+1))/hTotEvt.GetBinContent(bx+1))

#         hs_.Add(hTDC[by])

#     return hs_

# # Loop over depth
# for dd in range(1,5):
#     hN.GetAxis(0).SetRangeUser(dd-.5,dd+.5)
#     # Loop over ieta
#     for ee in range(-16,17):
#         hN.GetAxis(1).SetRangeUser(ee-.5,ee+.5)
#         hh = hN.Projection(3,2)
#         hs = GetStack(hh,f'{dd}_{ee}')
#         hs.SetTitle(f'HB i#eta {ee} | depth {dd} | TS {SOI};time shift [ns];TDC fraction')
#         hs.SetName(f'hTDCStack_ieta{ee}_depth{dd}')
#         StackList.append(hs)

#         # Plot the graphs.
#         tc = rt.TCanvas(f'ieta{ee}_depth{dd}','bb',800,600)
#         hs.Draw()
#         hs.GetYaxis().SetRangeUser(0,1)
#         hs.SetMaximum(1.)
#         hs.GetXaxis().SetRangeUser(-10,20)
#         tc.BuildLegend(.7,.7,.9,.9)
#         tc.SetGrid()
#         tc.SaveAs(f'../PNG/QIEPhaseScan_TDCSvTShift_ieta{ee}_depth{dd}_{argv[2]}.png')

tf_out = TFile(argv[3],'RECREATE')

for ss in StackList:
    ss.Write()
tf_out.Write()

tf_out.Close()
tf_in.Close()
