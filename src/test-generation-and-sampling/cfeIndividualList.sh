#!/bin/bash

#The purpose of this script is to run the cfeIndividual.sh script on a list of bugs

#Preconditions:
#There should be a folder called generatedTestSuites in the defects4j folder where the test suites and their output will be stored.
#The variable D4J_HOME should be directed to the folder where defects4j is installed.
#The variable JAVA_HOME should be directed to the folder where java 7 is installed (It must be Java 7).
#You should manually modify the list of bugs to be ran in the array called "bugs"

#Output
#The output is a txt file with the output of testing the test suite on the folder indicated. The name of the txt file is: EvaluatingTestSuite"$PROJECT"-"$BUGNUMBER"f-evosuite-branch."$SEED".tar.bz2On"$LOWERCASEPACKAGE""$BUGNUMBER"BuggyOutput.txt and it is located in $D4J_HOME/generatedTestSuites/$IDENTIFIER/"$PROJECT"/evosuite-branch/"$SEED"/ for each of the d4j bugs

#Input:
# 1th param is the generation tool (Randoop or Evosuite)
# 2th param is the budget of time in seconds the tool has to generate the test suite
# 3th param is weather you want to run only sections of the script: C=create, F=fix. You can run: CF, C, F
# 4th param is the name of the folder the test suite will be stored in. This is located in $D4J_HOME/generatedTestSuites/ . Example: September21
# 5th param is the seed: 1
# 6th param is an optional patch file Example: /path/to/patch.txt
	
#Example of usage:
#./cfeIndividualList.sh Evosuite 1800 CF GeneratedTestSuitesForNotPatchedBugs 5


RANDOOPOREVOSUITE="$1"
BUDGET="$2"
CFE="$3"
IDENTIFIER="$4"
SEED="$5"
PATCHFILE="$6"

if [ "$#" -lt 5 ]; then
    echo "This script should be run with at least 4 parameters: "
	echo "1th param is the generation tool (Randoop or Evosuite)"
	echo "2th param is the budget of time in seconds the tool has to generate the test suite"
	echo "3th param is weather you want to run only sections of the script: C=create, F=fix. You can run: CF, C, F"
	echo "4th param is the name of the folder the test suite will be stored in. This is located in $D4J_HOME/generatedTestSuites/. Example: September21"
	echo "5th param is the seed: 1"
	echo "6th param is an optional patch file Example: /path/to/patch.txt"
    exit 0
fi

LOWERCASERANDOOPOREVOSUITE=`echo $RANDOOPOREVOSUITE | tr '[:upper:]' '[:lower:]'`

mkdir $D4J_HOME/generatedTestSuites/$IDENTIFIER
rm -f $D4J_HOME/generatedTestSuites/$IDENTIFIER/resultsEvaluatingSeveralTestSuites.txt
touch $D4J_HOME/generatedTestSuites/$IDENTIFIER/resultsEvaluatingSeveralTestSuites.txt

#Change this list to the Bugs you want to evaluate
#Allbugs with a fix found (GenProg) Remaining from the list above:
#GENPROG
#declare -a bugs=("Math 40" "Math 49" "Math 50" "Math 53" "Math 73" "Math 80" "Math 81" "Math 82" "Math 84" "Math 85" "Math 95" "Time 19")
#PAR and TRP
#declare -a bugs=("Chart 7" "Closure 11" "Closure 31" "Closure 38" "Closure 62" "Closure 63" "Closure 64" "Lang 33" "Lang 44" "Lang 51" "Lang 58" "Math 2" "Math 5" "Math 62" "Math 75" "Math 78" "Time 7" "Chart 21" "Closure 86" "Lang 45")
#PAR and TRP
#declare -a bugs=("Lang 45" "Closure 86" "Chart 21" "Time 7" "Math 78" "Math 75" "Math 62" "Math 5" "Math 2" "Lang 58" "Lang 51" "Lang 44" "Lang 33" "Closure 64" "Closure 63" "Closure 62" "Closure 38" "Closure 31" "Closure 11" "Chart 7")
#All bugs we did NOT find a patch for
declare -a bugs=("Closure 106" "Closure 108" "Closure 109" "Closure 110" "Closure 111" "Closure 112" "Closure 113" "Closure 114" "Closure 116" "Closure 117" "Closure 118" "Closure 119" "Closure 120" "Closure 121" "Closure 122" "Closure 123" "Closure 124" "Closure 127" "Closure 128" "Closure 129" "Closure 130" "Closure 131" "Closure 132" "Closure 133" "Lang 1" "Lang 2" "Lang 3" "Lang 4" "Lang 5" "Lang 6" "Lang 8" "Lang 9" "Lang 11" "Lang 12" "Lang 13" "Lang 14" "Lang 15" "Lang 16" "Lang 17" "Lang 18" "Lang 19" "Lang 20" "Lang 21" "Lang 23" "Lang 25" "Lang 26" "Lang 27" "Lang 28" "Lang 29" "Lang 30" "Lang 31" "Lang 32" "Lang 34" "Lang 35" "Lang 36" "Lang 37" "Lang 38" "Lang 40" "Lang 41" "Lang 42" "Lang 46" "Lang 47" "Lang 48" "Lang 49" "Lang 50" "Lang 52" "Lang 53" "Lang 54" "Lang 55" "Lang 56" "Lang 57" "Lang 60" "Lang 61" "Lang 62" "Lang 64" "Lang 65" "Math 1" "Math 3" "Math 4" "Math 6" "Math 9" "Math 10" "Math 11" "Math 12" "Math 13" "Math 14" "Math 15" "Math 16" "Math 17" "Math 19" "Math 21" "Math 22" "Math 23" "Math 25" "Math 26" "Math 27" "Math 30" "Math 31" "Math 32" "Math 33" "Math 34" "Math 35" "Math 36" "Math 37" "Math 38" "Math 39" "Math 41" "Math 42" "Math 43" "Math 44" "Math 45" "Math 46" "Math 47" "Math 48" "Math 51" "Math 52" "Math 54" "Math 55" "Math 56" "Math 57" "Math 58" "Math 59" "Math 60" "Math 61" "Math 63" "Math 64" "Math 65" "Math 66" "Math 67" "Math 68" "Math 69" "Math 70" "Math 71" "Math 72" "Math 74" "Math 76" "Math 77" "Math 79" "Math 83" "Math 86" "Math 87" "Math 88" "Math 89" "Math 90" "Math 91" "Math 92" "Math 93" "Math 94" "Math 96" "Math 97" "Math 98" "Math 99" "Math 100" "Math 101" "Math 102" "Math 103" "Math 104" "Math 105" "Math 106" "Time 1" "Time 2" "Time 3" "Time 4" "Time 5" "Time 6" "Time 8" "Time 9" "Time 10" "Time 11" "Time 12" "Time 13" "Time 14" "Time 15" "Time 16" "Time 17" "Time 18" "Time 20" "Time 21" "Time 22" "Time 23" "Time 24" "Time 25" "Time 26" "Time 27")
#Random ones
#declare -a bugs=("Math 28" "Math 84" "Closure 45" "Closure 115" "Closure 46" "Closure 25")

## now loop through the above array
for i in "${bugs[@]}"
do
  echo "Si:"
  echo ""

  COM="./cfeIndividual.sh "$i" $1 $2 $3 $4 $5 $6" 
  echo "$COM"
  eval $COM
  echo ""
done
