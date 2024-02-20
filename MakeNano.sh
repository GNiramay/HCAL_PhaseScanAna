#!/bin/bash
# Script to convert RAW to Nano.
# Syntax: . MakeNano.sh <input RAW root file> <output Nano root file>
# Example: . MakeNano.sh root://cmsxrootd.fnal.gov//store/group/dpg_hcal/comm_hcal/QIEPhaseScan2023/raw/366874/b176677f-5370-4468-b542-16519e7c935d.root TestOut.root

# time cmsDriver.py step2  -s RAW2DIGI,RECO,USER:DPGAnalysis/HcalNanoAOD/hcalNano_cff.hcalNanoTask --conditions auto:run3_data_prompt -n 10 --era Run3 --geometry DB:Extended --datatier NANOAOD --eventcontent NANOAOD --filein $1 --fileout file:$2

# John's solution
time cmsDriver.py step2  -s RAW2DIGI,RECO,USER:DPGAnalysis/HcalNanoAOD/hcalNano_cff.hcalNanoTask --conditions auto:run3_data_prompt -n 10 --era Run3 --geometry DB:Extended --datatier NANOAOD --eventcontent NANOAOD --customise_commands="process.load('DPGAnalysis.HcalNanoAOD.hcalUMNioTable_cff')\nprocess.hcalNanoTask.add(process.uMNioTable)\nprocess.hcalNanoDigiTask.add(process.uMNioTable)" --filein $1 --fileout file:$2