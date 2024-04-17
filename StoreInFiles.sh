mkdir -p /uscmst1b_scratch/lpc1/3DayLifetime/ngogate
cp /eos/uscms/store/user/ngogate/HCAL_DPG/QIEPhaseScan2024_skimmed/QIEPhaseScan2024_*.root /uscmst1b_scratch/lpc1/3DayLifetime/ngogate/
# xrdcp -r --parallel 8 root://eoscms.cern.ch//store/group/dpg_hcal/comm_hcal/QIEPhaseScan2024/ /uscmst1b_scratch/lpc1/3DayLifetime/ngogate
