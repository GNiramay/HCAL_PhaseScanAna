# 1. Read one of the root files created by RespCorr_EnergyScale.py
# 2. Deliver the compensating response correction for given ieta ring and phases
from ROOT import RDataFrame as rd
from sys import argv
InRoot,ieta,depth,InitialPhase,FinalPhase = argv[1:]
print(rd('RespCorrData',InRoot)
      .Filter(f'ieta == {ieta} && depth == {depth} && InitialPhase == {InitialPhase} && FinalPhase == {FinalPhase}')
      .Mean('RespCorr')
      .GetValue())
