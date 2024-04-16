# Script to skim the nanoAOD files, calculate phase shifts, save the relevant branches.
# Syntax: python3 SkimNano.py <input root file> <output root file>

from sys import argv
from ROOT import RDataFrame, std, EnableImplicitMT, TFile
import ROOT as rt
from ROOT.RDF import THnDModel

EnableImplicitMT()
columns = std.vector("string")()

df = RDataFrame("Events",argv[1])\
    .Define("tshift","(uMNio_UserWord1*(uMNio_UserWord1<2147483648))+(uMNio_UserWord1-4294967296)*(uMNio_UserWord1>2147483648)"
    ).Filter("tshift != 111 && tshift != 999 && tshift != 888")


for c in ["run", "luminosityBlock", "tshift", 
          "HB_ieta",   "HB_iphi",   "HB_depth", "HB_QSum", "HB_CWTCorr",
          "HE_ieta",   "HE_iphi",   "HE_depth", "HE_QSum", "HE_CWTCorr",
          "RecHitHBHE_ieta","RecHitHBHE_iphi","RecHitHBHE_depth","RecHitHBHE_energy","RecHitHBHE_time"
]:
    columns.push_back(c)

for Det_ in ['HB','HE']:
    # Create a strim for total sum charge.
    s_QSum = "0"
    for tt in range(8):
        s_QSum = f"{s_QSum}+Digi{Det_}_fc{tt}-Digi{Det_}_pedestalfc{tt}"

    df = df.Define(f"temp{Det_}_QSum", s_QSum)\
           .Define(f"{Det_}GoodChan",  f"temp{Det_}_QSum > 0")\
           .Define(f"{Det_}_QSum",     f"temp{Det_}_QSum[{Det_}GoodChan]")\
           .Define(f"{Det_}_ieta",     f"Digi{Det_}_ieta[{Det_}GoodChan]")\
           .Define(f"{Det_}_iphi",     f"Digi{Det_}_iphi[{Det_}GoodChan]")\
           .Define(f"{Det_}_depth",    f"Digi{Det_}_depth[{Det_}GoodChan]")
    for ts in range(8):
        df = df.Define(f"{Det_}_tdc{ts}",     f"Digi{Det_}_tdc{ts}[{Det_}GoodChan]")\
               .Define(f"{Det_}_fc{ts}",      f"Digi{Det_}_fc{ts}[{Det_}GoodChan]-Digi{Det_}_pedestalfc{ts}[{Det_}GoodChan]")
        columns.push_back(f"{Det_}_tdc{ts}")
        columns.push_back(f"{Det_}_fc{ts}")
    df = df.Define(f"{Det_}_CWTCorr",f"25*({Det_}_fc1+2*{Det_}_fc2+3*{Det_}_fc3+4*{Det_}_fc4+5*{Det_}_fc5+6*{Det_}_fc6+7*{Det_}_fc7)/{Det_}_QSum-tshift")
    # df = df.Define(f"{Det_}_QSum",f"{Det_}_fc0+{Det_}_fc1+{Det_}_fc2+{Det_}_fc3+{Det_}_fc4+{Det_}_fc5+{Det_}_fc6+{Det_}_fc7")\
    #        .Define(f"{Det_}_CWTCorr",f"25*({Det_}_fc1+2*{Det_}_fc2+3*{Det_}_fc3+4*{Det_}_fc4+5*{Det_}_fc5+6*{Det_}_fc6+7*{Det_}_fc7)/{Det_}_QSum-tshift")

df.Snapshot("Events",argv[2],columns)
tf = TFile(argv[2],"UPDATE")
# tf = TFile(argv[2],"RECREATE")

# Histogram binning for TDC v tshift THnD
# Axes: depth  ieta   tshift  TDC  CWT-corrected
nBins = [4,    33,    31,     4,   180]
bLow =  [0.5, -16.5, -10.5,   0,   0]
bHigh = [4.5,  16.5,  20.5,   4,   180]

SOI = 3

model = THnDModel("hN_TDCvtshift",";depth;ieta;tshift;TDC",5,nBins,bLow,bHigh)
df.Define("GoodChan",f"(HB_tdc{SOI-1} <3) || (HB_tdc{SOI}<3) || (HB_tdc{SOI+1}<3)")\
  .Define("Depth","HB_depth[GoodChan]")\
  .Define("IEta","HB_ieta[GoodChan]")\
  .Define("TShift","tshift+0*HB_tdc0[GoodChan]")\
  .Define("TDC",f"HB_tdc{SOI}[GoodChan]")\
  .Define("CWTCorr","HB_CWTCorr[GoodChan]")\
  .HistoND(model,["Depth","IEta","TShift","TDC","CWTCorr"])\
  .Write()

tf.Write()
tf.Close()
