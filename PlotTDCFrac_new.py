# Syntax: python3 PlotTDCFrac_new.py <input root file> <output root file>
# Example: python3 PlotTDCFrac_new.py TestSkimmed.root TestHist.root
from sys import argv
from ROOT import RDataFrame, TFile, EnableImplicitMT
from ROOT.RDF import THnDModel

EnableImplicitMT()

InRoot = argv[1]
OutRoot = argv[2]
Det = "hb"
SOI = 4

# Histogram binning for TDC v tshift THnD
# Axes: depth  ieta   tshift  TDC
nBins = [4,    33,    51,     4]
bLow =  [0.5, -16.5, -25.5,   0]
bHigh = [4.5,  16.5,  25.5,   4]
model = THnDModel("hN_TDCvtshift",";depth;ieta;tshift;TDC",4,nBins,bLow,bHigh)

# Axes: depth  ieta   tshift  QFrac	QSum
QnBins = [4,    33,    51,   100,	10]
QbLow =  [0.5,   -16.5, -25.5,   0,	0]
QbHigh = [4.5,    16.5,  25.5,   1,	100000]

df = RDataFrame('Events',InRoot)

df = df.Define('MyShift',f"vector<Double_t>temp; for(auto cc: {Det}_tdc{SOI}) temp.push_back(tshift); return temp;")\
       .Define("QSum",f"{Det}_fc0+{Det}_fc1+{Det}_fc2+{Det}_fc3+{Det}_fc4+{Det}_fc5+{Det}_fc6+{Det}_fc7")

# hist = df.HistoND(model[0],[f"{Det}_depth",f"{Det}_ieta","MyShift",f"{Det}_tdc{SOI}"])

tf = TFile(OutRoot,"RECREATE")
df.HistoND(model,[f"{Det}_depth",f"{Det}_ieta","MyShift",f"{Det}_tdc{SOI}"]).Write()

# for ts in range(8):
#     df = df.Define(f"QFrac{ts}",f"{Det}_fc{ts}/QSum")
#     model_ = THnDModel(f"hN_Q{ts}vTShift",";depth;ieta;tshift;QFrac,QSum",5,QnBins,QbLow,QbHigh)
#     df.HistoND(model_,[f"{Det}_depth",f"{Det}_ieta","MyShift",f"QFrac{ts}",'QSum']).Write()

# hist.Write()
tf.Write()
tf.Close()
