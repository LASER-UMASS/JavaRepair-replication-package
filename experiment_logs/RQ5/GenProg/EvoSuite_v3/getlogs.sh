

for filename in /home/mmotwani/mywork1dir/Defects4Java7/defects4j/GP_RQ2_RERUNJune15/*Buggy*/log*.txt; do 
	defect=$(echo $filename | cut -d '/' -f 8)
	logfile=$(echo $filename | cut -d '/' -f 9)
	echo $filename "$defect-$logfile"
	cp $filename "$defect-$logfile"
done
