# HCAL_PhaseScanAna

This repository holds the codes for the following actions.

1. Search for RAW files created during phase scans (LED, QIE)
2. Create hcalnano's from RAW
3. Skim the hcalnano's
4. Make TDC Stack plot
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
## Skim the hcalnano's
`SkimNano.py` script skims the hcalnanos in the following way.
1. Events with `uMNio_UserWord1` value of `111,888,999` are ignored
2. `uMNio_UserWord1` is used to calculate the relative shift in the QIE timing.
3. For each event, channels with charges in SOI and SOI close to the pdestal levels are ignored. (To ensure the genuine current pulses formed the hits)
4. Only the relevant branches are kept
5. A new root file containing these branches is formed

The syntax is given in the file itself. 

## Make TDC Stack plot
This is done in two steps.
1. For a given `iphi` slice, create a 2D histogram of TDC in `ts 3` vs `time shift`. This is done by `PlotTDCFrac.py`
2. From the 2D histogram, get projection along x-axis, for each TDC value (y bins). Stack these projections, and scale them to 1. This is done by `MakeTDCStack.py`

The syntax for both is given in the respective files.
