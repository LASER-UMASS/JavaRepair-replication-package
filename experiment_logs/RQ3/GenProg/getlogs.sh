

for filename in ../../../../Defects4Java7/defects4j/RQ2_GP/*Buggy*/log*.txt; do 
	defect=$(echo $filename | cut -d '/' -f 8)
	logfile=$(echo $filename | cut -d '/' -f 9)
	echo $filename "$defect-$logfile"
	cp $filename "$defect-$logfile"
done
