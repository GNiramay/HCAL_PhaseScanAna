#!/bin/bash
CMSSWVer=CMSSW_14_2_2
source /cvmfs/cms.cern.ch/cmsset_default.sh
scram p $CMSSWVer
cd $CMSSWVer/src;cmsenv;cd -
ls -alht

echo Input arguments: $*
AnaScript=$1
InRoot=$2
AnaTag=$(echo $AnaScript | sed 's/.py//')
OutRoot=${AnaTag}_$(basename $InRoot)

time python3 $AnaScript $InRoot $OutRoot
ls -alht

