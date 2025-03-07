# Calculating compensating response correection
import ROOT as rt
from sys import argv
rt.EnableImplicitMT()

# Threshold rechit energy required to be considered a good rechit [in GeV]
Rechit_energy_thr = 4.0

def Analyze(df,OutRoot):

    # Exclude 0 rechit energy hits
    for prop in ['depth','ieta','iphi','energy']:
        df = df.Redefine(f'RecHitHBHE_{prop}',f'RecHitHBHE_{prop}[RecHitHBHE_energy > 0]')

    # QIE phase offset (tshift)
    if 'tshift' not in df.GetColumnNames():
        df = df.Define("tshift","(uMNio_UserWord1*(uMNio_UserWord1<2147483648))+(uMNio_UserWord1-4294967296)*(uMNio_UserWord1>2147483648)")
    df = df.Define('TShift1','tshift+0*RecHitHBHE_depth')

    # 	     Depth	ieta	tshift	Rechit energy
    nBins = [7, 	61,	21,	400]
    bLow =  [0.5,	-30.5,	-10.5,	0.]
    bHigh = [7.5,  	30.5,   10.5,	4*Rechit_energy_thr]

    tf = rt.TFile(OutRoot,'RECREATE')
    df.HistoND(rt.RDF.THnDModel("hRespCorrData",";depth;ieta;tshift",4,nBins,bLow,bHigh),
               ['RecHitHBHE_depth','RecHitHBHE_ieta','TShift1','RecHitHBHE_energy']).Write()
    tf.Close()
    return

Analyze(rt.RDataFrame('Events',argv[1]),argv[2])
