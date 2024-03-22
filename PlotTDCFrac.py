# Syntax: python3 PlotTDCFrac.py <input root file> <output root file> <detector> <ieta> <depth>
# Example: python3 PlotTDCFrac.py TestSkimmed.root TestHist.root hb 15 2

from sys import argv
from ROOT import RDataFrame, TFile, EnableImplicitMT

EnableImplicitMT()

InRoot = argv[1]
OutRoot = argv[2]
Det_ = argv[3]
eta_ = argv[4]
depth_ = argv[5]
SOI = 3                         # Sample of interest

df = RDataFrame('Events',InRoot)
# TShift = df.Max('tshift').GetValue()

df = df.Define('MyChannel',f"{Det_}_ieta == {eta_} && {Det_}_depth == {depth_}")\
       .Define('MyTDC',f"{Det_}_tdc{SOI}[MyChannel]")\
       .Define('MyShift',f"vector<Double_t>temp; for(auto cc: MyTDC) temp.push_back(tshift); return temp;")

hist = df.Histo2D(("h2TDCvTShift",f"{Det_} i#eta {eta_} | depth {depth_} | ts {SOI};phase shift [ns];TDC",32,-10.5,21.5,4,-0.5,3.5),'MyShift','MyTDC')
hist2 = df.Histo1D(("hMyShift",";phase shift according to MyShift",34,-12,22),"MyShift")
hist3 = df.Histo1D(("htshift",";phase shift according to tshift",34,-12,22),"tshift")
hist4 = df.Histo1D(("hMyTDC",f"{Det_} i#eta {eta_} | depth {depth_} | ts {SOI};TDC",4,-0.5,3.5),"MyTDC")

tf = TFile(OutRoot,"RECREATE")
hist.Write()
hist2.Write()
hist3.Write()
hist4.Write()
tf.Write()
tf.Close()
# .Define('MyShift',f"{TShift} + 0*MyTDC")\
