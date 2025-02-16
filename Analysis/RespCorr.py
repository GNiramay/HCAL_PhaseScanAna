# Calculating compensating response correection
import ROOT as rt
from sys import argv
rt.EnableImplicitMT()

# Threshold rechit energy required to be considered a good rechit [in GeV]
Rechit_energy_thr = 4.0

def Analyze(df,OutRoot):
    df = df.Define('IEta','RecHitHBHE_ieta[RecHitHBHE_energy>4]')\
           .Define('Depth','RecHitHBHE_depth[RecHitHBHE_energy>4]')
    if 'tshift' not in df.GetColumnNames():
        df = df.Define("tshift","(uMNio_UserWord1*(uMNio_UserWord1<2147483648))+(uMNio_UserWord1-4294967296)*(uMNio_UserWord1>2147483648)")

    df = df.Define('TShift1','tshift+0*RecHitHBHE_depth')

    # 	     Depth	ieta	tshift	Rechit energy
    nBins = [7, 	61,	21,	100]
    bLow =  [0.5,	-30.5,	-10.5,	0.]
    bHigh = [7.5,  	30.5,   10.5,	Rechit_energy_thr]

    tf = rt.TFile(OutRoot,'RECREATE')
    df.HistoND(rt.RDF.THnDModel("hRespCorrData",";depth;ieta;tshift",4,nBins,bLow,bHigh),
               ['RecHitHBHE_depth','RecHitHBHE_ieta','TShift1','RecHitHBHE_energy']).Write()
    tf.Close()
    return

Analyze(rt.RDataFrame('Events',argv[1]),argv[2])
