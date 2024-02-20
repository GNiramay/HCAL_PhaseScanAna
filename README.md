# HCAL_PhaseScanAna

This repository holds the codes for the following actions.

1. Search for RAW files created during phase scans (LED, QIE)
2. Create nanoAODs from RAW using hcalnano
3. Skim them to keep only the relevant branches, use `uMNio_UserWord` to determine the phase delay
4. Script to make important histograms
5. Batch processing using condor

## Create nanoAODs from RAW using hcalnano
### 1. `step2_RAW2DIGI_RECO_USER.py`
This converts a RAW file to HcalNano file. This script was obtained by running the following command under the latest CMSSW env. (I used `CMSSW_13_3_0_pre3`).
```
runTheMatrix.py -l 1060.1 --dryRun
```
One can use it directly, but I recommend using `MakeNano.sh`.
### 2. MakeNano.sh
The basic command was taken from the `cmdLog` file that was created after running the above `runTheMatrix.py` command. The basic command produces a root file, but doesn't have the crucial `uMNio_UserWord1` branch. John Hakala suggested including the following line in the `cmsDriver.py` command to fix it.
```
--customise_commands="process.load('DPGAnalysis.HcalNanoAOD.hcalUMNioTable_cff')\nprocess.hcalNanoTask.add(process.uMNioTable)\nprocess.hcalNanoDigiTask.add(process.uMNioTable)"
```
This works. So, in the end, a RAW file can be converted to `hcalnano` using the following syntax. An example usage is given in the file itself.
```
. MakeNano.sh <input RAW root file> <output Nano root file>
```
