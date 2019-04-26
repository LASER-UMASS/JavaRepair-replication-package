#!/bin/bash

#The purpose of this script is to merge the coverages from different test suite seeds
#This script is meant to be ran after getCoverage.py with all seeds

# DEPENDENCIES:
# 1. JAVA_HOME is set to Java 8
# 2. D4J_HOME is set to Defects4J (Java 8 support) 
# 3. The symbolic link "defects4j/framework/lib/test_generation/runtime/evosuite-rt.jar" points to evosuite-standalone-runtime-1.0.3.jar  or evosuite-standalone-runtime-1.0.6.jar 
# 4. Python version 2.7 

#INPUT:
# 1st param is the option for merging generated patches or human patches (G or H)
# 2nd param is the folder where the patches are located (if generated) or a two column csv file <Project, BugNumber> (if human) (UFT-8 encoding) 
# 3rd param is an identifier for this execution which is used to create the output file (it has to be the same as the ID used in getCoverage.py)

# CMD TO RUN: 
#Example of usage:  ./mergeSeveralSeedsCovFiles.sh G /home/mausoto/defects4j/patchesGenerated/JavaRepair-results/PARPatches/ PAR
#Example of usage:  ./mergeSeveralSeedsCovFiles.sh H /home/mausoto/QualityEvaluationDefects4jGenProg/AllBugsFixedByAllApproaches.csv HUMAN

# OUTPUT:
# This script creates a file in D4J_HOME/MergedCoverages/ with files $BUG.xml that describe the coverage of all seeds
# This script copies all the folders with results, with xml and ser files to a central folder in D4J_HOME/MergedCoverages/


D4JLOCATION="$D4J_HOME"
HorG="$1"
BUGLISTSOURCE="$2"
ID="$3"
OUTPUTFOLDER=$D4JLOCATION"/MergedCoverages/"$ID"/"
FILESTOMERGE=""

moveFoldersToOutputFolder(){
	for (( TSSEED=1; TSSEED<=10; TSSEED++ ))
	do	
		com="ls -d "$D4JLOCATION"/ExamplesCheckedOut"$TSSEED"/"$ID"*TSSeed"$TSSEED"*/"
		FOLDERTOMOVE=$($com)
		#com="cp -r "$FOLDERTOMOVE" /home/mausoto/deletePlease/"
		#eval $com
		#rm -rf $OUTPUTFOLDER"/"$ID"TSSeed"$TSSEED
		com="cp -r "$FOLDERTOMOVE" "$OUTPUTFOLDER"/"$ID"TSSeed"$TSSEED
		echo $com
		#TO MOVE FOLDERS FROM EXAMPLESCHECKEDOUT TO MERGEDCOVERAGES UNDOCUMENT THIS
		eval $com
	done
}

gatherFiles(){
	PROJECTANDBUG="$1"
	PATCHSEED="$2"
	PROJECTANDBUG=$(echo ${PROJECTANDBUG^})
	FILESTOMERGE=""
	#echo $PROJECTANDBUG
	for (( TSSEED=1; TSSEED<=10; TSSEED++ ))
	do	
		com="ls -d "$OUTPUTFOLDER"/"$ID"TSSeed"$TSSEED"/"$PROJECTANDBUG
		if [ $HorG == "G" ]; then
			com+="Patch"$PATCHSEED
		fi
		com+=".ser"
		SERFILE=$($com)
		FILESTOMERGE="$FILESTOMERGE $SERFILE"
	done
	echo $FILESTOMERGE
}

merge(){
	PROJECTANDBUG="$1"
	PATCHSEED="$2"
	#merge all .ser files
	COM="bash ~/Cobertura/cobertura-2.1.1-bin/cobertura-2.1.1/cobertura-merge.sh --datafile "$OUTPUTFOLDER"/"$PROJECTANDBUG
	if [ $HorG == "G" ]; then
			COM+="Patch"$PATCHSEED
		fi
	COM+=".ser "$FILESTOMERGE
	echo $COM
	eval $COM 
	
	echo ""
	
	#turn .ser into .xml
	FILEDIR=$OUTPUTFOLDER"/"$PROJECTANDBUG
	if [ $HorG == "G" ]; then
		FILEDIR+="Patch"$PATCHSEED
	fi
	#creates folder in $FILEDIR with a file named coverage.xml
	COM="bash ~/Cobertura/cobertura-2.1.1-bin/cobertura-2.1.1/cobertura-report.sh --format xml --destination "$FILEDIR" --datafile "$FILEDIR".ser"
	
	#echo $COM
	eval $COM
	cp $FILEDIR"/coverage.xml" $FILEDIR".xml"
	#rm -r $FILEDIR
}

if [ "$#" -lt 3 ]; then
    echo "This script should be run with 3 parameters"
    exit 0
fi

export PATH=$PATH:$D4JLOCATION/framework/bin/
export PATH=$PATH:$D4JLOCATION/framework/util/
export PATH=$PATH:$D4JLOCATION/major/bin/

#rm -rf $OUTPUTFOLDER
mkdir $OUTPUTFOLDER
#mv "$D4JLOCATION/ExamplesCheckedOut$TSSEED/$ID*$TSSEED*/$PROJECTANDBUG"*.ser

moveFoldersToOutputFolder
if [ $HorG == "G" ]; then
	PATCHES=$BUGLISTSOURCE/*.diff
	for PATCH in $PATCHES
	do
		PATCHNAME=${PATCH##*/}
		PROJECTANDBUG=$(echo $PATCHNAME | cut -d'_' -f 1)
		PATCHSEED=$(echo $PATCHNAME | cut -d'_' -f 2)
		gatherFiles $PROJECTANDBUG $PATCHSEED
		merge $PROJECTANDBUG $PATCHSEED
		
	done

elif [ $HorG == "H" ]; then
	while read line; do
		PROJECTANDBUG=$(echo "${line//,}")
		#echo "$PROJECTANDBUG"
		gatherFiles $PROJECTANDBUG $PATCHSEED
		merge $PROJECTANDBUG $PATCHSEED
	done < $BUGLISTSOURCE
fi



