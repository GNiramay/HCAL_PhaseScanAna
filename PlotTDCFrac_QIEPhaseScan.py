# Program to analyze skimmed 2023 QIE phase scan data
# Original code copied from PlotTDCFrac_QIEPhaseScan.py
# Syntax: python3 PlotTDCFrac_QIEPhaseScan.py <input root file> <output root file>
# Example: python3 PlotTDCFrac_QIEPhaseScan.py TestSkimmed.root TestHist.root
from sys import argv
from ROOT import RDataFrame, TFile, EnableImplicitMT, gInterpreter, GetThreadPoolSize
from ROOT.RDF import THnDModel

EnableImplicitMT()

InRoot = argv[1]
OutRoot = argv[2]
Det = "hb"
SOI = 3
df = RDataFrame('Events',InRoot)
tf = TFile(OutRoot,"RECREATE")
print("Number of threads used: ",GetThreadPoolSize())

# Reject some lumo block.
# Following https://gitlab.cern.ch/kikenned/L1LLPJetStudies/-/blob/main/TDCAnalyzer/TDCAnalyzer/src/Loop.cxx?ref_type=heads#L19-34
L1 = "run == 366873 && (luminosityBlock < 147)"
L2 = "run == 366874 && ((luminosityBlock > 13 && luminosityBlock < 56) || (luminosityBlock > 125 && luminosityBlock < 157))"
L3 = "run == 366876 && (luminosityBlock > 210 && luminosityBlock < 252 )"
L4 = "run == 366891 && (luminosityBlock < 55)"
L5 = "run == 366895 && ((luminosityBlock < 44 || luminosityBlock > 1492) || (luminosityBlock == 81 || luminosityBlock == 611 || luminosityBlock == 612 || luminosityBlock == 613))"

df = df.Define("BadEvents",f"{L1} || {L2} || {L3} || {L4} || {L5}")\
       .Filter("!(BadEvents)")

# Histogram binning for TDC v tshift THnD
# Axes: depth  ieta   tshift  TDC  CWT-corrected
nBins = [4,    33,    31,     4,   180]
bLow =  [0.5, -16.5, -10.5,   0,   0]
bHigh = [4.5,  16.5,  20.5,   4,   180]

# Divide events into odd and even
pInfo = ['even','odd']
for EvtPar in range(2):
    df_new = df.Filter(f"(rdfentry_ % 2) == {EvtPar}")
    model = THnDModel(f"hN_TDCvtshift_{pInfo[EvtPar]}",";depth;ieta;tshift;TDC",5,nBins,bLow,bHigh)
    df_new.Define("GoodChan",f"({Det}_tdc{SOI-1} <3) || ({Det}_tdc{SOI}<3) || ({Det}_tdc{SOI+1}<3)")\
          .Define("Depth",f"{Det}_depth[GoodChan]")\
          .Define("IEta",f"{Det}_ieta[GoodChan]")\
          .Define("TShift",f"tshift+0*{Det}_tdc0[GoodChan]")\
          .Define("TDC",f"{Det}_tdc{SOI}[GoodChan]")\
          .Define("QSum",f"{Det}_fc0[GoodChan]+{Det}_fc1[GoodChan]+{Det}_fc2[GoodChan]+{Det}_fc3[GoodChan]+{Det}_fc4[GoodChan]+{Det}_fc5[GoodChan]+{Det}_fc6[GoodChan]+{Det}_fc7[GoodChan]")\
          .Define("CWTCorr",f"25*({Det}_fc1[GoodChan]+2*{Det}_fc2[GoodChan]+3*{Det}_fc3[GoodChan]+4*{Det}_fc4[GoodChan]+5*{Det}_fc5[GoodChan]+6*{Det}_fc6[GoodChan]+7*{Det}_fc7[GoodChan])/QSum-TShift")\
          .HistoND(model,["Depth","IEta","TShift","TDC","CWTCorr"])\
          .Write()

tf.Write()
tf.Close()
