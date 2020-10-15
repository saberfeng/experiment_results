
for i in {100..300}
do
    grep -o 'open' FRVM/nmap_Time300_ScansS_Portdiscovered_$i.xml | wc -l
done

for i in {778..797}
do
    grep -o 'open' nmap_Time300_ScansS_Portdiscovered_$i.xml | wc -l
done