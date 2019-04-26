#!/bin/bash

#The purpose of this script is to merge the coverage of the ser files from SE3 and SE6

# DEPENDENCIES:
# 1. JAVA_HOME is set to Java 8
# 2. D4J_HOME is set to Defects4J (Java 8 support) 
# 4. Python version 2.7 

#INPUT:	
# 1st param is the csv file with the list of defects
# 2nd param is the folder where the SE3 ser files are located
# 3rd param is the folder where the SE6 ser files are located
# 4th param is the output folder

# CMD TO RUN: 
# e.g., ./mergeSE3andSE6CovFiles.sh AllBugsFixedByAllApproaches.csv /home/mausoto/defects4jJava8/defects4j/MergedCoverages/TestingReplicationPackageES3/ /home/mausoto/defects4jJava8/defects4j/MergedCoverages/TestingReplicationPackageES6/ ./MergedES3ES6/

# OUTPUT:
# The output files are generated in the 4th param, which are a set of files describing the merged coverage


#Example of usage: 

D4JLOCATION="$D4J_HOME"
BUGLISTSOURCE="$1"
FOLDERSE3="$2"
FOLDERSE6="$3"
OUTPUT="$4"
FILESTOMERGE=""

merge(){
	PROJECTANDBUG="$1"
	#merge all .ser files
	COM="bash ~/Cobertura/cobertura-2.1.1-bin/cobertura-2.1.1/cobertura-merge.sh --datafile $OUTPUT/"$PROJECTANDBUG
	COM+=".ser "$FILESTOMERGE
	echo $COM
	eval $COM 
	
	echo ""
	
	#turn .ser into .xml
	#creates folder in $FILEDIR with a file named coverage.xml
	COM="bash ~/Cobertura/cobertura-2.1.1-bin/cobertura-2.1.1/cobertura-report.sh --format xml --destination $OUTPUT/ --datafile $OUTPUT/"$PROJECTANDBUG".ser"
	
	#echo $COM
	eval $COM
	cp "$OUTPUT/coverage.xml" $OUTPUT/$PROJECTANDBUG".xml"
	#rm -r $FILEDIR
}

export PATH=$PATH:$D4JLOCATION/framework/bin/
export PATH=$PATH:$D4JLOCATION/framework/util/
export PATH=$PATH:$D4JLOCATION/major/bin/

mkdir $OUTPUT
while read line; do
	PROJECTANDBUG=$(echo "${line//,}")
	FILESTOMERGE=" $FOLDERSE3/"$PROJECTANDBUG".ser $FOLDERSE6/"$PROJECTANDBUG".ser "
	merge $PROJECTANDBUG
done < $BUGLISTSOURCE




