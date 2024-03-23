# Script to skim the nanoAOD files, calculate phase shifts, save the relevant branches.
# Syntax: python3 SkimNano.py <input root file> <output root file>

from sys import argv
from ROOT import RDataFrame, std, EnableImplicitMT
import ROOT as rt

EnableImplicitMT()

# # Copied from John's skim code. Ensures the hits really have high energy deposit (very far from the noise levels)
# cutHB = "(DigiHB_fc2 > 21.*DigiHB_pedestalfc2)||(DigiHB_fc3 > 21.*DigiHB_pedestalfc3)||(DigiHB_fc4 > 46.*DigiHB_pedestalfc4)"
# cutHE = "(DigiHE_fc2 > 21.*DigiHE_pedestalfc2)||(DigiHE_fc3 > 21.*DigiHE_pedestalfc3)||(DigiHE_fc4 > 46.*DigiHE_pedestalfc4)"

# cutHB = "DigiHB_fc3 > 0."
# cutHE = "DigiHE_fc3 > 0."

# Create a function to match rechit and digis
rt.gInterpreter.Declare('''
ROOT::VecOps::RVec<bool> Match(ROOT::VecOps::RVec<Double_t> Rec,ROOT::VecOps::RVec<Double_t> Dig){
  ROOT::VecOps::RVec<bool> result;
  result.clear();
  for(auto dd: Dig){
    bool temp_result = false;
    for(auto rr: Rec)
      if(rr == dd){
        temp_result = true;
        break;
      }
    result.push_back(temp_result);
  }
  return result;
}
''')

df = RDataFrame("Events",argv[1])\
    .Define("tshift","(uMNio_UserWord1*(uMNio_UserWord1<2147483648))+(uMNio_UserWord1-4294967296)*(uMNio_UserWord1>2147483648)"
    ).Filter("tshift != 111 && tshift != 999 && tshift != 888"
    ).Define("GoodRechit","RecHitHBHE_energy > 4"
    ).Redefine("RecHitHBHE_ieta","RecHitHBHE_ieta[GoodRechit]"
    ).Redefine("RecHitHBHE_iphi","RecHitHBHE_iphi[GoodRechit]"
    ).Redefine("RecHitHBHE_depth","RecHitHBHE_depth[GoodRechit]"
    ).Redefine("RecHitHBHE_energy","RecHitHBHE_energy[GoodRechit]"
    ).Redefine("RecHitHBHE_time","RecHitHBHE_time[GoodRechit]"
    ).Define("GoodDigiHBEta","Match(RecHitHBHE_ieta,DigiHB_ieta)"
    ).Define("GoodDigiHBPhi","Match(RecHitHBHE_iphi,DigiHB_iphi)"
    ).Define("GoodDigiHBDepth","Match(RecHitHBHE_depth,DigiHB_depth)"
    ).Define("GoodHB","GoodDigiHBEta && GoodDigiHBPhi && GoodDigiHBDepth"
    ).Define("GoodDigiHEEta","Match(RecHitHBHE_ieta,DigiHE_ieta)"
    ).Define("GoodDigiHEPhi","Match(RecHitHBHE_iphi,DigiHE_iphi)"
    ).Define("GoodDigiHEDepth","Match(RecHitHBHE_depth,DigiHE_depth)"
    ).Define("GoodHE","GoodDigiHEEta && GoodDigiHEPhi && GoodDigiHEDepth"
    ).Define("hb_ieta",     "DigiHB_ieta[GoodHB]"
    ).Define("hb_iphi",     "DigiHB_iphi[GoodHB]"
    ).Define("hb_depth",    "DigiHB_depth[GoodHB]"
    ).Define("hb_subdet",   "DigiHB_subdet[GoodHB]"
    ).Define("hb_tdc0",     "DigiHB_tdc0[GoodHB]"
    ).Define("hb_tdc1",     "DigiHB_tdc1[GoodHB]"
    ).Define("hb_tdc2",     "DigiHB_tdc2[GoodHB]"
    ).Define("hb_tdc3",     "DigiHB_tdc3[GoodHB]"
    ).Define("hb_tdc4",     "DigiHB_tdc4[GoodHB]"
    ).Define("hb_tdc5",     "DigiHB_tdc5[GoodHB]"
    ).Define("hb_tdc6",     "DigiHB_tdc6[GoodHB]"
    ).Define("hb_tdc7",     "DigiHB_tdc7[GoodHB]"
    ).Define("hb_fc0",      "DigiHB_fc0[GoodHB]-DigiHB_pedestalfc0[GoodHB]"
    ).Define("hb_fc1",      "DigiHB_fc1[GoodHB]-DigiHB_pedestalfc1[GoodHB]"
    ).Define("hb_fc2",      "DigiHB_fc2[GoodHB]-DigiHB_pedestalfc2[GoodHB]"
    ).Define("hb_fc3",      "DigiHB_fc3[GoodHB]-DigiHB_pedestalfc3[GoodHB]"
    ).Define("hb_fc4",      "DigiHB_fc4[GoodHB]-DigiHB_pedestalfc4[GoodHB]"
    ).Define("hb_fc5",      "DigiHB_fc5[GoodHB]-DigiHB_pedestalfc5[GoodHB]"
    ).Define("hb_fc6",      "DigiHB_fc6[GoodHB]-DigiHB_pedestalfc6[GoodHB]"
    ).Define("hb_fc7",      "DigiHB_fc7[GoodHB]-DigiHB_pedestalfc7[GoodHB]"
    ).Define("he_ieta",     "DigiHE_ieta[GoodHE]"
    ).Define("he_iphi",     "DigiHE_iphi[GoodHE]"
    ).Define("he_depth",    "DigiHE_depth[GoodHE]"
    ).Define("he_tdc0",     "DigiHE_tdc0[GoodHE]"
    ).Define("he_tdc1",     "DigiHE_tdc1[GoodHE]"
    ).Define("he_tdc2",     "DigiHE_tdc2[GoodHE]"
    ).Define("he_tdc3",     "DigiHE_tdc3[GoodHE]"
    ).Define("he_tdc4",     "DigiHE_tdc4[GoodHE]"
    ).Define("he_tdc5",     "DigiHE_tdc5[GoodHE]"
    ).Define("he_tdc6",     "DigiHE_tdc6[GoodHE]"
    ).Define("he_tdc7",     "DigiHE_tdc7[GoodHE]"
    ).Define("he_fc0",      "DigiHE_fc0[GoodHE]-DigiHE_pedestalfc0[GoodHE]"
    ).Define("he_fc1",      "DigiHE_fc1[GoodHE]-DigiHE_pedestalfc1[GoodHE]"
    ).Define("he_fc2",      "DigiHE_fc2[GoodHE]-DigiHE_pedestalfc2[GoodHE]"
    ).Define("he_fc3",      "DigiHE_fc3[GoodHE]-DigiHE_pedestalfc3[GoodHE]"
    ).Define("he_fc4",      "DigiHE_fc4[GoodHE]-DigiHE_pedestalfc4[GoodHE]"
    ).Define("he_fc5",      "DigiHE_fc5[GoodHE]-DigiHE_pedestalfc5[GoodHE]"
    ).Define("he_fc6",      "DigiHE_fc6[GoodHE]-DigiHE_pedestalfc6[GoodHE]"
    ).Define("he_fc7",      "DigiHE_fc7[GoodHE]-DigiHE_pedestalfc7[GoodHE]"
    )

columns = std.vector("string")()
for c in ["run", "luminosityBlock", "tshift", 
          "hb_ieta",   "hb_iphi",   "hb_depth",  "hb_subdet", 
          "hb_tdc0",   "hb_tdc1",   "hb_tdc2",   "hb_tdc3",   "hb_tdc4",   "hb_tdc5",   "hb_tdc6",   "hb_tdc7",   
          "hb_fc0",    "hb_fc1",    "hb_fc2",    "hb_fc3",    "hb_fc4",    "hb_fc5",    "hb_fc6",    "hb_fc7",    
          "he_ieta",   "he_iphi",   "he_depth",  
          "he_tdc0",   "he_tdc1",   "he_tdc2",   "he_tdc3",   "he_tdc4",   "he_tdc5",   "he_tdc6",   "he_tdc7",   
          "he_fc0",    "he_fc1",    "he_fc2",    "he_fc3",    "he_fc4",    "he_fc5",    "he_fc6",    "he_fc7",
          "RecHitHBHE_ieta","RecHitHBHE_iphi","RecHitHBHE_depth","RecHitHBHE_energy","RecHitHBHE_time"
]:
    columns.push_back(c)

df.Snapshot("Events",argv[2],columns)
