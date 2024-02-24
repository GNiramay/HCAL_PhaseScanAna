# Script to skim the nanoAOD files, calculate phase shifts, save the relevant branches.
# Syntax: python3 SkimNano.py <input root file> <output root file>

from sys import argv
from ROOT import RDataFrame, std

# Copied from John's skim code. Ensures the hits really have high energy deposit (very far from the noise levels)
cutHB = "(DigiHB_fc2 > 21.*DigiHB_pedestalfc2)||(DigiHB_fc3 > 21.*DigiHB_pedestalfc3)||(DigiHB_fc4 > 46.*DigiHB_pedestalfc4)"
cutHE = "(DigiHE_fc2 > 21.*DigiHE_pedestalfc2)||(DigiHE_fc3 > 21.*DigiHE_pedestalfc3)||(DigiHE_fc4 > 46.*DigiHE_pedestalfc4)"

df = RDataFrame("Events",argv[1])\
    .Define("tshift","(uMNio_UserWord1*(uMNio_UserWord1<2147483648))+(uMNio_UserWord1-4294967296)*(uMNio_UserWord1>2147483648)"
    ).Filter("tshift != 111 && tshift != 999 && tshift != 888"
    ).Define("hb_ieta",     f"DigiHB_ieta[{cutHB}]"
    ).Define("hb_iphi",     f"DigiHB_iphi[{cutHB}]"
    ).Define("hb_depth",    f"DigiHB_depth[{cutHB}]"
    ).Define("hb_subdet",   f"DigiHB_subdet[{cutHB}]"
    ).Define("hb_tdc0",     f"DigiHB_tdc0[{cutHB}]"
    ).Define("hb_tdc1",     f"DigiHB_tdc1[{cutHB}]"
    ).Define("hb_tdc2",     f"DigiHB_tdc2[{cutHB}]"
    ).Define("hb_tdc3",     f"DigiHB_tdc3[{cutHB}]"
    ).Define("hb_tdc4",     f"DigiHB_tdc4[{cutHB}]"
    ).Define("hb_tdc5",     f"DigiHB_tdc5[{cutHB}]"
    ).Define("hb_tdc6",     f"DigiHB_tdc6[{cutHB}]"
    ).Define("hb_tdc7",     f"DigiHB_tdc7[{cutHB}]"
    ).Define("hb_fc0",      f"DigiHB_fc0[{cutHB}]-DigiHB_pedestalfc0[{cutHB}]"
    ).Define("hb_fc1",      f"DigiHB_fc1[{cutHB}]-DigiHB_pedestalfc1[{cutHB}]"
    ).Define("hb_fc2",      f"DigiHB_fc2[{cutHB}]-DigiHB_pedestalfc2[{cutHB}]"
    ).Define("hb_fc3",      f"DigiHB_fc3[{cutHB}]-DigiHB_pedestalfc3[{cutHB}]"
    ).Define("hb_fc4",      f"DigiHB_fc4[{cutHB}]-DigiHB_pedestalfc4[{cutHB}]"
    ).Define("hb_fc5",      f"DigiHB_fc5[{cutHB}]-DigiHB_pedestalfc5[{cutHB}]"
    ).Define("hb_fc6",      f"DigiHB_fc6[{cutHB}]-DigiHB_pedestalfc6[{cutHB}]"
    ).Define("hb_fc7",      f"DigiHB_fc7[{cutHB}]-DigiHB_pedestalfc7[{cutHB}]"
    ).Define("he_ieta",     f"DigiHE_ieta[{cutHE}]"
    ).Define("he_iphi",     f"DigiHE_iphi[{cutHE}]"
    ).Define("he_depth",    f"DigiHE_depth[{cutHE}]"
    ).Define("he_tdc0",     f"DigiHE_tdc0[{cutHE}]"
    ).Define("he_tdc1",     f"DigiHE_tdc1[{cutHE}]"
    ).Define("he_tdc2",     f"DigiHE_tdc2[{cutHE}]"
    ).Define("he_tdc3",     f"DigiHE_tdc3[{cutHE}]"
    ).Define("he_tdc4",     f"DigiHE_tdc4[{cutHE}]"
    ).Define("he_tdc5",     f"DigiHE_tdc5[{cutHE}]"
    ).Define("he_tdc6",     f"DigiHE_tdc6[{cutHE}]"
    ).Define("he_tdc7",     f"DigiHE_tdc7[{cutHE}]"
    ).Define("he_fc0",      f"DigiHE_fc0[{cutHE}]-DigiHE_pedestalfc0[{cutHE}]"
    ).Define("he_fc1",      f"DigiHE_fc1[{cutHE}]-DigiHE_pedestalfc1[{cutHE}]"
    ).Define("he_fc2",      f"DigiHE_fc2[{cutHE}]-DigiHE_pedestalfc2[{cutHE}]"
    ).Define("he_fc3",      f"DigiHE_fc3[{cutHE}]-DigiHE_pedestalfc3[{cutHE}]"
    ).Define("he_fc4",      f"DigiHE_fc4[{cutHE}]-DigiHE_pedestalfc4[{cutHE}]"
    ).Define("he_fc5",      f"DigiHE_fc5[{cutHE}]-DigiHE_pedestalfc5[{cutHE}]"
    ).Define("he_fc6",      f"DigiHE_fc6[{cutHE}]-DigiHE_pedestalfc6[{cutHE}]"
    ).Define("he_fc7",      f"DigiHE_fc7[{cutHE}]-DigiHE_pedestalfc7[{cutHE}]"
    )

columns = std.vector("string")()
for c in ["run", "luminosityBlock", "tshift", 
          "hb_ieta",   "hb_iphi",   "hb_depth",  "hb_subdet", 
          "hb_tdc0",   "hb_tdc1",   "hb_tdc2",   "hb_tdc3",   "hb_tdc4",   "hb_tdc5",   "hb_tdc6",   "hb_tdc7",   
          "hb_fc0",    "hb_fc1",    "hb_fc2",    "hb_fc3",    "hb_fc4",    "hb_fc5",    "hb_fc6",    "hb_fc7",    
          "he_ieta",   "he_iphi",   "he_depth",  
          "he_tdc0",   "he_tdc1",   "he_tdc2",   "he_tdc3",   "he_tdc4",   "he_tdc5",   "he_tdc6",   "he_tdc7",   
          "he_fc0",    "he_fc1",    "he_fc2",    "he_fc3",    "he_fc4",    "he_fc5",    "he_fc6",    "he_fc7"    
]:
    columns.push_back(c)

df.Snapshot("Events",argv[2],columns)
