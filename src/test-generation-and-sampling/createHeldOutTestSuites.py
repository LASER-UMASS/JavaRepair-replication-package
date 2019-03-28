#/bin/python

#The purpose of this script is to create held out test suites when the Evosuite version used is different from the one in defects4j.

#Preconditions:
#There should be a folder called generatedTestSuites in the defects4j folder where the test suites and their output will be stored.
#The variable D4J_HOME should be directed to the folder where defects4j is installed.
#The variable JAVA_HOME should be directed to the folder where java 7 is installed (It must be Java 7).
#You should manually modify the list of bugs to be ran in the array called "bugs"

#Output
#The output is the set of generated test suites

#Input:
#1st param is the absolute path, the file listing bugs to process: project,bugNum (one per line). Lines starting with # are skipped
#2nd param is the absolute path, the path where evosuite is located
#3rd param is a descriptive name for the outputFile 
	
#Example of usage:
#python createHeldOutTestSuites.py /home/mausoto/QualityEvaluationDefects4jGenProg/AllBugsFixedByAllApproaches.csv /home/mausoto/defects4jJava8/defects4j/framework/lib/test_generation/generation/evosuite-1.0.6.jar /home/mausoto/output/

import argparse
import os
import xml.etree.ElementTree
import subprocess
import sys
import shutil
import time

d4jHome = os.environ['D4J_HOME']
defects4jCommand = d4jHome + "/framework/bin/defects4j"

class BugInfo(object):
	def __init__(self, project, bugNum):
		self.project = project
		self.bugNum = bugNum
		
def getAllBugs(bugs,args):
	if(not os.path.isfile(args.bugsFile)):
		sys.exit("The file " + str(args.bugsFile) + " does not exist")
	else:
		with open(args.bugsFile) as f:
			pairs = [x.strip().split(',') for x in f.readlines() if x[0] != '#' and str(x.strip())]
			if pairs is None:
				sys.exit("There has been a problem reading the file with the bugs")
			for pair in pairs:
				bug = BugInfo(pair[0], int(pair[1]))
				bugs.append(bug)
				
def ensureVersionAreCheckedOut(bug,fixedFolder):
	if(not(os.path.exists(fixedFolder))):
		checkout(fixedFolder, bug.project, bug.bugNum, "f")
	
def checkout(folderToCheckout, project, bugNum, vers):
	cmd = defects4jCommand + " checkout -p " + str(project) + " -v " + str(bugNum) + str(vers) + " -w " + str(folderToCheckout)
	print cmd
	p = subprocess.call(cmd, shell=True)
	
def runD4jCommand(fixedFolder, d4jCommand):
	cmd = defects4jCommand + d4jCommand
	p = subprocess.Popen(cmd, shell=True, cwd=fixedFolder, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	return [ line.split("2>&1")[-1].strip() for line in p.stdout ]
	
def getCoverage(outputFolder,fixedFolder,testSuiteName):
	cmd = "defects4j test -s "+str(testSuiteName)
	print(cmd)
	p = subprocess.call(cmd, shell=True, cwd=str(fixedFolder)+"/evosuite-tests/")
	
	cmd="defects4j coverage -s evosuite-tests/"+str(testSuiteName)
	print(cmd)
	p = subprocess.Popen(cmd, shell=True, cwd=str(fixedFolder), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	toPrint=str(testSuiteName)
	for l in p.stdout:
		if "Line coverage" in l or "Condition coverage" in l: 
			toPrint+= ","+str((l.split(":")[-1]).strip().split("%")[0])
	writeToOutputFile(outputFolder,toPrint)
	
	
def writeToOutputFile(outputFolder,toPrint):
	cmd="echo \""+str(toPrint).strip()+"\" >> "+str(outputFolder)+"/evosuite106coverageInfo.txt"
	print(cmd)
	#first one is line coverage, second is condition coverage
	p = subprocess.call(cmd, shell=True)
	
def fixTS(fixedFolder, testSuiteName, bug):
	cmd="perl fix_test_suite.pl -p "+str(bug.project)+" -d "+str(fixedFolder)+"/evosuite-tests/ -v "+str(bug.bugNum)+"f"
	print(cmd)
	p = subprocess.call(cmd, shell=True)
			
def copyTS(outputFolder,fixedFolder,testSuiteName):
	cmd="cp "+str(fixedFolder)+"/evosuite-tests/"+str(testSuiteName)+" "+str(outputFolder)
	print(cmd)
	p = subprocess.call(cmd, shell=True)
	

def getOptions():
	parser = argparse.ArgumentParser(description="This script creates test suites for all the bugs listed in a file. Example of usage: python createHeldOutTestSuites.py /home/mausoto/QualityEvaluationDefects4jGenProg/AllBugsFixedByAllApproaches.csv /home/mausoto/defects4jJava8/defects4j/framework/lib/test_generation/generation/evosuite-1.0.6.jar /home/mausoto/pleaseRemove/")
	parser.add_argument("bugsFile", help="Absolute path, the file listing bugs to process: project,bugNum (one per line). Lines starting with # are skipped")
	parser.add_argument("evosuitePath", help="Absolute path, the path where evosuite is located")
	parser.add_argument("outputFolder", help="a descriptive name for the outputFile (Example: human)")
	
	return parser.parse_args()
	
def main():
	args=getOptions()
	outputFolder= str(args.outputFolder) + "/" 
	p = subprocess.call("rm "+str(outputFolder)+"/evosuite106coverageInfo.txt", shell=True)			
	#creates new folder to output all the useful outputs
	if(not(os.path.isfile(outputFolder))):
		p = subprocess.call("mkdir " + str(outputFolder), shell=True)
				
	#fill bug list
	bugs = []
	getAllBugs(bugs, args)
	for bug in bugs:
		for tsSeed in range(1,11):
			try:
				print "\nDefect: "+bug.project + " " + str(bug.bugNum)
				fixedFolder=str(outputFolder)+"/"+str(bug.project)+str(bug.bugNum)+"fixed/"
				testSuiteName = str(bug.project)+"-"+str(bug.bugNum)+"f-evosuite-line."+str(tsSeed)+".tar.bz2"
				ensureVersionAreCheckedOut(bug,fixedFolder)
				p = subprocess.call("defects4j compile", shell=True, cwd=fixedFolder)
				targetClass = runD4jCommand(fixedFolder, " export -p classes.modified")[0]
				pathToBinary = runD4jCommand(fixedFolder, " export -p cp.compile")[0]
				if '.' not in pathToBinary.split("/")[-1]: pathToBinary+='/'
				cmd = "java -jar "+str(args.evosuitePath)+" -class "+str(targetClass)+" -projectCP "+str(pathToBinary)+" -criterion line -seed "+str(tsSeed)+" -Dsearch_budget=1800"
				print(cmd)
				p = subprocess.call(cmd, shell=True, cwd=fixedFolder)
				#for l in p.stdout:
				#	print("stdout:"+str(l))
				#for l in p.stderr:
				#	print("stderr:"+str(l))
				#p.communicate()
					
				cmd = "tar -cvjSf "+str(testSuiteName)+" "+str(targetClass).split('.')[0]+"/"
				print(cmd)
				p = subprocess.call(cmd, shell=True, cwd=str(fixedFolder)+"/evosuite-tests/")
				fixTS(fixedFolder, testSuiteName, bug)
				getCoverage(outputFolder,fixedFolder,testSuiteName)
				copyTS(outputFolder,fixedFolder,testSuiteName)
			except:
				writeToOutputFile(outputFolder,str(testSuiteName)+",Error")
main()
