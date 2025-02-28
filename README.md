# HCAL_PhaseScanAna

This branch stores code for analyzing QIE 2024 phase scan data along [HCAL timing paper](https://cds.cern.ch/record/2891496) sec. 5

## Installation
* Clone the repo. `git clone git@github.com:GNiramay/HCAL_PhaseScanAna.git`
* Check out the correct branch. `git checkout PhaseScan2024`
* Write the desired CMSSW version on the first line of [INSTALL](INSTALL) and second line of [Exec/GeneralAna.sh](Exec/GeneralAna.sh)
* Install the package. `. INSTALL`

## General analysis workflow.
1. Write the hcalnano file paths to a text file and save it under `FilePaths/`.
2. Write an analysis script in python under `Analysis/`. For simplicity, make sure the script takes exactly two arguments:
   - Full path to the hcalnano file
   - Root file name to write the histograms to.
4. Write a condor config file under `ConfFiles/` For simplicity, use `Exec/GeneralAna.sh` as the executable
5. Submit condor jobs. `condor_submit ConfFile/<name of the condor config file>`
6. Once all the jobs are done, new histogram files appear. Use `hadd Hadded/<final output file> <all the histogram files>` to combine the histograms.
7. Delete the condor-related files. `. CleanIn.sh`
8. Delete the histogram files of each job. `rm -f *.root`

## General plotting workflow
The plotting goals change all the time. There is a lot of freedom. Following are the general guidelines
1. Write the plotting script under `Plotting/`.
2. This is work on the new files created under `Hadded/` in the previous workflow.
3. Save the canvases as pmg (and pdf if needed) at some location that can be viewed on CERN webpages.

## Example
1. 2024 phase scan hcalnano file paths are written at `FilePaths/hcalnano*`
2. Script for making 4 dimensional histogram of rechit ieta,depth,timeshift, energy is written at [Analysis/RespCorr.py](Analysis/RespCorr.py)
3. Condor config file is written at [ConfFiles/RespCorr_NoSkim.jdl](ConfFiles/RespCorr_NoSkim.jdl)
4. Submit condor jobs.
```
condor_submit ConfFiles/RespCorr_NoSkim.jdl
```
5. Once the jobs finish,
```
hadd Hadded/hcalnano_r379349.root  QIE*_r379349*
hadd Hadded/hcalnano_r379350.root  QIE*_r379350*
hadd Hadded/Full.root Hadded/hcalnano*
rm -f *.root
. CleanIn.sh
```
6. Plotting script is written at [Plotting/RespCorr.py](Plotting/RespCorr.py)
7. Following command saves the plots to [Niramay's webpage](https://ngogate.web.cern.ch/ngogate/HCAL_PFG_Dump/PhaseScan_2024/)
```
cd Plotting/
python3 RespCorr.py ../Hadded/Full.root
```

## Script description:
|File name|Goal|
|:--------|:--:|
|[RespCorr_Occup_v_ieta.py](Plotting/RespCorr_Occup_v_ieta.py)|Overlays occupancy vs ieta for all depths|
|[RespCorr_EnergyScale.py](Plotting/RespCorr_EnergyScale.py)|Reads a text file that stores the occupancy reference values, calculates energy scale and plots energy scale, scaled occupancy|
