from os import system as ss
# Arguments to deliver:
# 1. input histogram file
# 2. histogram name to for calculations
# 3. text file to write the occupancies
# 4. output path to save images

# # To plot hit occupancy
# OutPath = '/eos/home-n/ngogate/www/HCAL_DPG/GlobalQIEPhaseScan2023_hcalnano/RespCorr/'
# for dd in ['HB','HE']:
#     ss(f'python3 RespCorr_Occup_v_ieta.py ../Hadded/QIEPhaseScan2023_Full.root hRespCorrData_{dd} RefVal_QIE2023_{dd}.txt {OutPath}{dd}_NoCut/')
#     ss(f'python3 RespCorr_Occup_v_ieta.py ../Hadded/QIEPhaseScan2023_Full.root hRespCorrData_{dd}_TDCCut RefVal_QIE2023_{dd}_TDCCut.txt {OutPath}{dd}_TDCCut/')

# To plot energy scale, new occupancy
OutPath = '/eos/home-n/ngogate/www/HCAL_DPG/GlobalQIEPhaseScan2023_hcalnano/RespCorr/'
for dd in ['HB','HE']:
    ss(f'python3 RespCorr_EnergyScale.py ../Hadded/QIEPhaseScan2023_Full.root hRespCorrData_{dd} RefVal_QIE2023_{dd}.txt {OutPath}{dd}_NoCut/')
    ss(f'python3 RespCorr_EnergyScale.py ../Hadded/QIEPhaseScan2023_Full.root hRespCorrData_{dd}_TDCCut RefVal_QIE2023_{dd}_TDCCut.txt {OutPath}{dd}_TDCCut/')
    ss(f'python3 RespCorr_calc.py RefVal_QIE2023_{dd}.root 15 2 1 4')
    ss(f'python3 RespCorr_calc.py RefVal_QIE2023_{dd}_TDCCut.root 15 2 1 4')
    break
