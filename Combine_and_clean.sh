Runs=(379349 379350)
FKey=$(find -name '*r'${Runs[0]}'_*_job0*' | sed 's/_job0.root//g' | sed 's/\.\///g' | sed 's/_r'${Runs[0]}'//g')
DateStamp=$(date +"%b%d" -r Hadded/${FKey}_Full.root)

for rr in ${Runs[*]};do
    mv Hadded/${FKey}_r${rr}.root Hadded/Old_${FKey}_r${rr}_${DateStamp}.root
    hadd Hadded/${FKey}_r${rr}.root *_r${rr}_*.root
done
mv Hadded/${FKey}_Full.root Hadded/Old_${FKey}_Full_${DateStamp}.root
hadd Hadded/${FKey}_Full.root Hadded/${FKey}_r${Runs[0]}.root Hadded/${FKey}_r${Runs[1]}.root
. CleanIn.sh
