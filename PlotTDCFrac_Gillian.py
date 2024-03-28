# Program to skim's Gilian's minituples.
# Original code copied from PlotTDCFrac_new.py
# Syntax: python3 PlotTDCFrac_new.py <input root file> <output root file>
# Example: python3 PlotTDCFrac_new.py TestSkimmed.root TestHist.root
from sys import argv
from ROOT import RDataFrame, TFile, EnableImplicitMT, gInterpreter
from ROOT.RDF import THnDModel

EnableImplicitMT()

InRoot = argv[1]
OutRoot = argv[2]
Det = "hb"
SOI = 3

# Histogram binning for TDC v tshift THnD
# Axes: depth  ieta   tshift  TDC
nBins = [4,    33,    51,     4]
bLow =  [0.5, -16.5, -25.5,   0]
bHigh = [4.5,  16.5,  25.5,   4]
model = [THnDModel("hN_TDCvtshift_even",";depth;ieta;tshift;TDC",4,nBins,bLow,bHigh),
         THnDModel("hN_TDCvtshift_odd",";depth;ieta;tshift;TDC",4,nBins,bLow,bHigh)]

# Axes: depth  ieta   tshift  QFrac	QSum
QnBins = [4,    33,    51,   100,	10]
QbLow =  [0.5,   -16.5, -25.5,   0,	0]
QbHigh = [4.5,    16.5,  25.5,   1,	100000]

df = RDataFrame('Channel_Hits4GeV',InRoot)

# # Divide events into even and odd
# df_new = [df.Filter("GetParity(event,0)"), # Even
#           df.Filter("GetParity(event,1)")] # Odd

# # For debugging
# print(df.Count().GetValue())
# for DD in df_new:
#     print(DD.Count().GetValue())

tf = TFile(OutRoot,"RECREATE")

# df_new[0].HistoND(model[0],["idepth","ieta","QIE_phase",f"TDC_code_s{SOI}"]).Write()
# df_new[1].HistoND(model[1],["idepth","ieta","QIE_phase",f"TDC_code_s{SOI}"]).Write()

df.Filter("(rdfentry_ % 2) == 0").HistoND(model[0],["idepth","ieta","QIE_phase",f"TDC_code_s{SOI}"]).Write()
df.Filter("(rdfentry_ % 2) == 1").HistoND(model[1],["idepth","ieta","QIE_phase",f"TDC_code_s{SOI}"]).Write()

tf.Write()
tf.Close()
