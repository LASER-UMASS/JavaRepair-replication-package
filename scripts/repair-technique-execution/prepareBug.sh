#!/bin/bash

#The purpose of this script is to set up the environment to run Genprog of a particular defects4j bug.

#Preconditions:
#The variable D4J_HOME should be directed to the folder where defects4j is installed.
#The variable GP4J_HOME should be directed to the folder where genprog4java is installed.

#Output
#The output is a txt file with the output of running the coverage analysis of the test suite on each of the folders indicated. 

# 1st param: project name, sentence case (ex: Lang, Chart, Closure, Math, Time)
# 2nd param: bug number (ex: 1,2,3,4,...)
# 3th param: testing option (ex: humanMade, generated)
# 4th param: test suite sample size (ex: 1, 100)
# 5th param is the folder where the bug files will be cloned to. Starting from $D4J_HOME (Ex: ExamplesCheckedOut)
# 6th param is the folder where the java 7 instalation is located
# 7th param is the folder where the java 8 instalation is located

# Example usage, VM:
#./prepareBug.sh Math 2 allHuman 100 ExamplesCheckedOut /usr/lib/jvm/java-7-oracle/ /usr/lib/jvm/java-8-oracle/ true <path to neg.test> true <path to pos.test>

if [ "$#" -ne 11 ]; then
    echo "This script should be run with 11 parameters:"
	echo "1st param: project name, sentence case (ex: Lang, Chart, Closure, Math, Time)"
	echo "2nd param: bug number (ex: 1,2,3,4,...)"
	echo "3th param: testing option (ex: humanMade, generated)"
	echo "4th param: test suite sample size (ex: 1, 100)"
	echo "5th param is the folder where the bug files will be cloned to. Starting from $D4J_HOME"
	echo "6th param is the folder where the java 7 instalation is located"
	echo "7th param is the folder where the java 8 instalation is located"
	echo "8th param is set to \"true\" if negative tests are to be specified using sampled tests else set this to \"false\""
	echo "9th param is the path to file containing sampled negative tests"
	echo "10th param is set to \"true\" if positive tests are to be specified using sampled tests else set this to \"false\""
	echo "11th param is the path to file containing sampled positive tests"
    exit 0
fi

PROJECT="$1"
BUGNUMBER="$2"
OPTION="$3"
TESTSUITESAMPLE="$4"
BUGSFOLDER="$5"
DIROFJAVA7="$6"
DIROFJAVA8="$7"
SAMPLENEGTESTS="$8"
NEGTESTPATH="$9"
SAMPLEPOSTESTS="${10}"
POSTESTPATH="${11}"

#Add the path of defects4j so the defects4j's commands run 
export PATH=$PATH:"$D4J_HOME"/framework/bin/
export PATH=$PATH:"$D4J_HOME"/framework/util/
export PATH=$PATH:"$D4J_HOME"/major/bin/

#copy these files to the source control

mkdir -p $D4J_HOME/$BUGSFOLDER

LOWERCASEPACKAGE=`echo $PROJECT | tr '[:upper:]' '[:lower:]'`

# directory with the checked out buggy project
BUGWD=$D4J_HOME/$BUGSFOLDER"/"$LOWERCASEPACKAGE"$BUGNUMBER"Buggy

#Checkout the buggy and fixed versions of the code (latter to make second testsuite
defects4j checkout -p $1 -v "$BUGNUMBER"b -w $BUGWD

##defects4j checkout -p $1 -v "$BUGNUMBER"f -w $D4J_HOME/$BUGSFOLDER/$LOWERCASEPACKAGE"$2"Fixed

#Compile the both buggy and fixed code
for dir in Buggy
do
    pushd $D4J_HOME/$BUGSFOLDER"/"$LOWERCASEPACKAGE$BUGNUMBER$dir
    defects4j compile
    popd
done
# Common genprog libs: junit test runner and the like
CONFIGLIBS=$GP4J_HOME"/lib/junittestrunner.jar"
#:"$GP4J_HOME"/lib/commons-io-1.4.jar:"$GP4J_HOME"/lib/junit-4.12.jar:"$GP4J_HOME"/lib/hamcrest-core-1.3.jar"

cd $D4J_HOME/$BUGSFOLDER/$LOWERCASEPACKAGE$2Buggy/
TESTWD=`defects4j export -p dir.src.tests`
SRCFOLDER=`defects4j export -p dir.bin.classes`
COMPILECP=`defects4j export -p cp.compile`
TESTCP=`defects4j export -p cp.test`
WD=`defects4j export -p dir.src.classes`
cd $BUGWD/$WD

#Create file to run defects4j compile

FILE=$D4J_HOME/$BUGSFOLDER/$LOWERCASEPACKAGE$2Buggy/runCompile.sh
/bin/cat <<EOM >$FILE
#!/bin/bash
export JAVA_HOME=$DIROFJAVA7
export PATH=$DIROFJAVA7/bin/:$PATH
#sudo update-java-alternatives -s java-7-oracle
cd $D4J_HOME/$BUGSFOLDER/$LOWERCASEPACKAGE$2Buggy/
$D4J_HOME/framework/bin/defects4j compile
if [[ \$? -ne 0 ]]; then
      echo "error compiling defect"
      exit 1
fi
export JAVA_HOME=$DIROFJAVA8
export PATH=$DIROFJAVA8/bin/:$PATH
#sudo update-java-alternatives -s java-8-oracle
EOM

chmod 777 $D4J_HOME/$BUGSFOLDER/$LOWERCASEPACKAGE$2Buggy/runCompile.sh


cd $BUGWD

#Create config file 
FILE=$D4J_HOME/$BUGSFOLDER/$LOWERCASEPACKAGE$2Buggy/defects4j.config
/bin/cat <<EOM >$FILE
seed = 0
sanity = yes
popsize = 40
javaVM = $DIROFJAVA7/jre/bin/java
workingDir = $D4J_HOME/$BUGSFOLDER/$LOWERCASEPACKAGE$2Buggy/
outputDir = $D4J_HOME/$BUGSFOLDER/$LOWERCASEPACKAGE$2Buggy/tmp
classSourceFolder = $D4J_HOME/$BUGSFOLDER/$LOWERCASEPACKAGE$2Buggy/$SRCFOLDER
libs = $CONFIGLIBS
sourceDir = $WD
positiveTests = $D4J_HOME/$BUGSFOLDER/$LOWERCASEPACKAGE$2Buggy/pos.tests
negativeTests = $D4J_HOME/$BUGSFOLDER/$LOWERCASEPACKAGE$2Buggy/neg.tests
jacocoPath = $GP4J_HOME/lib/jacocoagent.jar
testClassPath=$TESTCP
srcClassPath=$COMPILECP
compileCommand = $D4J_HOME/$BUGSFOLDER/$LOWERCASEPACKAGE$2Buggy/runCompile.sh
targetClassName = $BUGWD/bugfiles.txt
testGranularity=method

# 0.1 for GenProg and 1.0 for TrpAutoRepair and PAR
sample=1.0  

# edits for PAR, GenProg, TrpAutoRepair
#edits=append;replace;delete;FUNREP;PARREP;PARADD;PARREM;EXPREP;EXPADD;EXPREM;NULLCHECK;OBJINIT;RANGECHECK;SIZECHECK;CASTCHECK;LBOUNDSET;UBOUNDSET;OFFBYONE;SEQEXCH;CASTERMUT;CASTEEMUT
edits=append;replace;delete
#edits=FUNREP;PARREP;PARADD;PARREM;EXPREP;EXPADD;EXPREM;NULLCHECK;OBJINIT;RANGECHECK;SIZECHECK;CASTCHECK

# don't know whats this used for. Ask Mau.
#model=probabilistic
#modelPath=/home/mausoto/probGenProg/genprog4java/overallModel.txt

# use 1.0,0.1 for TrpAutoRepair and PAR. Use 0.65 and 0.35 for GenProg
negativePathWeight=1.0
positivePathWeight=0.1

# trp for TrpAutoRepair, gp for GenProg and PAR 
search=trp

# used only for TrpAutoRepair. value=400
maxVariants=400


EOM

#  get passing and failing tests as well as files
#info about the bug

if [ "$SAMPLENEGTESTS" = "true" ]; then
        if [ "$NEGTESTPATH" = "" ]; then
                echo "please enter path to file containing negative test cases"
                exit 1
        fi
        cp $NEGTESTPATH $BUGWD/neg.tests
else	
	defects4j export -p tests.trigger > $BUGWD/neg.tests
fi

currentpid="$currentpid $!"
wait $currentpid

case "$OPTION" in
"humanMade" ) 
	if [ "$SAMPLEPOSTESTS" = "true" ]; then
        	if [ "$POSTESTPATH" = "" ]; then
                	echo "please enter path to file containing positive test cases"
  	   		exit 1
        	fi
	        cp $POSTESTPATH $BUGWD/pos.tests
	else
	     	defects4j export -p tests.all > $BUGWD/pos.tests
	fi
;;
"allHuman" ) 
	if [ "$SAMPLEPOSTESTS" = "true" ]; then
        	if [ "$POSTESTPATH" = "" ]; then
                	echo "please enter path to file containing positive test cases"
  	   		exit 1
        	fi
	        cp $POSTESTPATH  $BUGWD/pos.tests
	else
		defects4j export -p tests.all > $BUGWD/pos.tests
	fi
;;
"onlyRelevant" ) 
	if [ "$SAMPLEPOSTESTS" = "true" ]; then
        	if [ "$POSTESTPATH" = "" ]; then
                	echo "please enter path to file containing positive test cases"
  	   		exit 1
        	fi
	        cp $POSTESTPATH  $BUGWD/pos.tests
	else
		defects4j export -p tests.relevant > $BUGWD/pos.tests
        fi
;;
esac

currentpid="$currentpid $!"
wait $currentpid

#Remove a percentage of the positive tests in the test suite
cd $D4J_HOME/$BUGSFOLDER/$LOWERCASEPACKAGE$2Buggy/

if [[ $TESTSUITESAMPLE -ne 100 ]]
then
    PERCENTAGETOREMOVE=$(echo "$TESTSUITESAMPLE * 0.01" | bc -l )
    echo "sample = $PERCENTAGETOREMOVE" >> $D4J_HOME/$BUGSFOLDER/$LOWERCASEPACKAGE$2Buggy/defects4j.config
fi

# get the class names to be repaired

defects4j export -p classes.modified > $BUGWD/bugfiles.txt

echo "This is the working directory: "
echo $D4J_HOME/$BUGSFOLDER/$LOWERCASEPACKAGE$2Buggy/$WD
