#!/bin/bash
# Set up CMSSW env
source /cvmfs/cms.cern.ch/cmsset_default.sh
scram p CMSSW_14_1_0_pre0
cd CMSSW_14_1_0_pre0/src
cmsenv
cd -

time cmsDriver.py step2  -s RAW2DIGI,RECO,USER:DPGAnalysis/HcalNanoAOD/hcalNano_cff.hcalNanoTask --conditions auto:run3_data_prompt \
     --era Run3 --geometry DB:Extended --datatier NANOAOD --eventcontent NANOAOD \
     --customise_commands="process.load('DPGAnalysis.HcalNanoAOD.hcalUMNioTable_cff')\nprocess.hcalNanoTask.add(process.uMNioTable)\nprocess.hcalNanoDigiTask.add(process.uMNioTable)" \
     -n -1 --filein $1 --fileout file:TempOut.root

ls -alht
mv TempOut.root $2
ls -alht
rm -rf step2_RAW2DIGI_RECO_USER.py CMSSW_14_1_0_pre0  TempOut.root
exit
