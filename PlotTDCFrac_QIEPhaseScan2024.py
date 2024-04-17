# Program to analyze skimmed 2023 QIE phase scan data
# Original code copied from PlotTDCFrac_QIEPhaseScan.py
# Syntax: python3 PlotTDCFrac_QIEPhaseScan2024.py <output root file> <input root file> 
# Example: python3 PlotTDCFrac_QIEPhaseScan2024.py TestHist.root TestSkimmed.root 
from sys import argv
from ROOT import RDataFrame, TFile, EnableImplicitMT, gInterpreter, GetThreadPoolSize
from ROOT.RDF import THnDModel

EnableImplicitMT()

InRoot = [argv[2]]
for aa in range(3,len(argv)):
    InRoot.append(argv[aa])

OutRoot = argv[1]
Det = "HB"
SOI = 3
df = RDataFrame('Events',InRoot)
tf = TFile(OutRoot,"RECREATE")
print("Number of threads used: ",GetThreadPoolSize())

df.Define("T1",f"({Det}_tdc{SOI-1} <3) && ({Det}_tdc{SOI} == 3) && ({Det}_tdc{SOI+1} == 3)")\
  .Define("T2",f"({Det}_tdc{SOI-1} == 3) && ({Det}_tdc{SOI} <3) && ({Det}_tdc{SOI+1} == 3)")\
  .Define("T3",f"({Det}_tdc{SOI-1} == 3) && ({Det}_tdc{SOI} == 3) && ({Det}_tdc{SOI+1} <3)")\
  .Define("GoodChan",f"({Det}_QSum > 5000) && (T1 || T2 || T3)")\
  .Define("TShift",f"tshift+0*{Det}_tdc0[GoodChan]")\
  .Define("CWTCorr",f"25*({Det}_fc1[GoodChan]+2*{Det}_fc2[GoodChan]+3*{Det}_fc3[GoodChan]+4*{Det}_fc4[GoodChan]+5*{Det}_fc5[GoodChan]+6*{Det}_fc6[GoodChan]+7*{Det}_fc7[GoodChan])/{Det}_QSum[GoodChan]-TShift")\
  .Define("Depth",f"{Det}_depth[GoodChan]")\
  .Define("IEta",f"{Det}_ieta[GoodChan]")\
  .Define("TDCLoc",f"({Det}_tdc2[GoodChan])*({Det}_tdc2[GoodChan]<3)+(3+{Det}_tdc3[GoodChan])*({Det}_tdc3[GoodChan]<3)+(6+{Det}_tdc4[GoodChan])*({Det}_tdc4[GoodChan]<3)")\
  .Define("TDC",f"{Det}_tdc{SOI}[GoodChan]")\
  .HistoND(
      THnDModel("hN_TDCvtshift","QSum > 5k | Exactly 1 good TDC in ts 2,3,4;depth;ieta;tshift;TDC;CWTCorr;TDCLoc",6
                ,[4,    33,    11,    4,  180,	9]
                ,[0.5, -16.5, -6.5,   0,  0,	-0.5]
                ,[4.5,  16.5,  4.5,   4,  180,	8.5])
      ,["Depth",f"IEta","TShift","TDC","CWTCorr","TDCLoc"]).Write()

tf.Write()
tf.Close()
