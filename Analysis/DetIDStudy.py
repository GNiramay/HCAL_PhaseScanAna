import ROOT as rt
from sys import argv
rt.EnableImplicitMT()

# Make sure to define HBidx,HEidx as the columns returned after matching.
# Eg,
# auto HBidx = HB_QSum;
# auto HEidx = HE_QSum;
s_match = '''
ROOT::VecOps::RVec<Int_t> result;
for(auto R:RecHitHBHE_detId)
  if(R < 1.14e9)
    result.push_back(HBidx[DigiHB_rawId == R][0]);
  else
    result.push_back(HEidx[DigiHE_rawId == R][0]);
return result;
'''

def Analyze(InRoot,OutRoot):
    df = rt.RDataFrame('Events',InRoot)\
           .Define('RechitID','RecHitHBHE_detId*1e-6-1123')\
           .Define('DigiHBID','DigiHB_rawId[DigiHB_rawId>0]*1e-6-1123')\
           .Define('DigiHEID','DigiHE_rawId[DigiHE_rawId>0]*1e-6-1123')\
           .Define('MatchedDepth','auto HBidx = DigiHB_depth;auto HEidx = DigiHE_depth;'+s_match)\
           .Define('MatchedIeta','auto HBidx = DigiHB_ieta;auto HEidx = DigiHE_ieta;'+s_match)\
           .Define('MatchedIphi','auto HBidx = DigiHB_iphi;auto HEidx = DigiHE_iphi;'+s_match)
    
    # Compare rechit prop with matched prop
    df = df.Define('dDepth','MatchedDepth-RecHitHBHE_depth')\
           .Define('dIeta','MatchedIeta-RecHitHBHE_ieta')\
           .Define('dIphi','MatchedIphi-RecHitHBHE_iphi')
    
    hlist = [
        df.Histo1D(('hdDepth',';RecHit depth - matched digi depth',15,-7.5,7.5),'dDepth'),
        df.Histo1D(('hdIeta',';RecHit ieta - matched digi ieta',41,-20.5,20.5),'dIeta'),
        df.Histo1D(('hdIphi',';RecHit iphi - matched digi iphi',41,-20.5,20.5),'dIphi'),
    ]
    
    tf = rt.TFile(OutRoot,'RECREATE')
    for hh in hlist: hh.Write()
    tf.Close()
    print(df.GetNRuns())
    return
Analyze('/eos/cms/store/group/dpg_hcal/comm_hcal/QIEPhaseScan2024/hcalnano/r379350/QIEPhaseScan2024_r379350_NanoProd_job0.root','Out.root')
