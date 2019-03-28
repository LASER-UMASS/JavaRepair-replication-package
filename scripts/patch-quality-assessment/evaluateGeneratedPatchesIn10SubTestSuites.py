#/bin/python

#The purpose of this script is to evaluate the quality of generated patches given a directory with held-out test suites

# DEPENDENCIES:
# 1. JAVA_HOME is set to Java 8
# 2. D4J_HOME is set to Defects4J (Java 8 support) 
# 3. The symbolic link "defects4j/framework/lib/test_generation/runtime/evosuite-rt.jar" points to evosuite-standalone-runtime-1.0.3.jar 
# 4. Python version 2.7 

#INPUT:
# 1st param is the directory to store the data (strating in D4J_HOME)
# 2nd param is the path to the directory containing patches
# 3th param is the path to directory containing generated tests

# CMD TO RUN: 
# e.g., python evaluateGeneratedPatchesIn10SubTestSuites.py GP_RQ2_QUALITY  ~/JavaRepair-results/patches/GenProg/RQ2/  ~/JavaRepair-results/generatedTestSuites/Evosuite103Budget1800/

# OUTPUT:
# File QualityAssessmentForGeneratedTSGenProgRQ2.csv is generated in the folder D4J_HOME/<dir to store the data inside D4J_HOME> 

import os
import subprocess
import sys
import argparse
import xml.etree.ElementTree
import shutil
import time

d4jHome = os.environ['D4J_HOME']
defects4jCommand = d4jHome + "/framework/bin/defects4j"

class BugInfo(object):
	def __init__(self, project, bugNum, wd, testDir):
		self.project = project
		self.bugNum = bugNum
		self.buggyFolder = wd + "/" + project.lower() + str(bugNum) + "Buggy"
		self.fixedFolder = wd + "/" + project.lower() + str(bugNum) + "Fixed"
		self.testDir = testDir
		self.srcPath=""
		self.patch=""

	def getProject(self):
		return str(self.project)

	def getBugNum(self):
		return str(self.bugNum)

	def getFixPath(self):
		return str(os.path.join(d4jHome, self.fixedFolder))

	def getBugPath(self):
		return str(os.path.join(d4jHome, self.buggyFolder))

	def getTestDir(self):
		return str(self.testDir)

	def getSrcPath(self):
		return str(self.srcPath)

	#this needs to be called after the buggy folder has been checked out
	def setScrPath(self):
		cmd = defects4jCommand + " export -p dir.src.classes"
		p = subprocess.Popen(cmd, shell=True, cwd=self.getBugPath(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		for i in p.stdout:
			self.srcPath = str(i).split("2>&1")[-1].strip()

	def setPatch(self,patch):
		self.patch=patch

	def getPatch(self):
		return str(self.patch)

		
def getOptions():
	parser = argparse.ArgumentParser(description="Example of usage: python evaluateGeneratedPatchesIn10SubTestSuites.py ExamplesCheckedOut  /home/mausoto/JavaRepair-results/patches/GenProg/RQ0/  /home/mausoto/JavaRepair-results/generatedTestSuites/Evosuite103Budget1800/")
	parser.add_argument("wd", help="working directory to check out project versions, starting from the the D4J_HOME folder")
	parser.add_argument("patches", help="the folder where the patches are located")
	parser.add_argument("testDir", help="the absolute path where the test suite is located")
	
	return parser.parse_args()
	
def getBugsFromPatchNames(bugs,args):
	cmd = "ls -d *.patch"
	p = subprocess.Popen(cmd, shell=True, cwd=args.patches, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	for line in p.stdout:
		defect=line.split('_')[0]
		bug=int(filter(str.isdigit, defect))
		project=str(filter(str.isalpha, defect)).title()
		bug = BugInfo(project, int(bug), args.wd, args.testDir)
		bug.setPatch(str(line).strip())
		bugs.append(bug)
		
def ensureVersionAreCheckedOut(bug):
	#Remove and re clone versions
	if(os.path.exists(bug.getBugPath())):
		shutil.rmtree(bug.getBugPath())
	checkout(bug.getBugPath(), bug.getProject(), bug.getBugNum(), "b")
	bug.setScrPath()
	shutil.rmtree(bug.getBugPath())
	
	#if(os.path.exists(bug.getFixPath())):
	#	shutil.rmtree(bug.getFixPath())
	#checkout(bug.getFixPath(), bug.getProject(), bug.getBugNum(), "f")
	

def checkout(folderToCheckout, project, bugNum, vers):
	cmd = defects4jCommand + " checkout -p " + str(project) + " -v " + str(bugNum) + str(vers) + " -w " + str(folderToCheckout)
	print cmd
	p = subprocess.call(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	
def patchFixedFile(bug,args):
	pathToSource=bug.getSrcPath()

	#Removing the fixed file
	if os.path.exists(bug.getFixPath()):
		shutil.rmtree(bug.getFixPath())
	checkout(bug.getFixPath(),bug.getProject(), bug.getBugNum(), "b")
		
	#Patching the fixed file
	whereToCallPatch=str(bug.getFixPath())+"/"+str(pathToSource)
	cmd ="patch -p2 -i "+args.patches+"/"+bug.getPatch() 
	print cmd +" called in "+ whereToCallPatch
	p = subprocess.Popen(cmd, shell=True, cwd=whereToCallPatch, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err = p.communicate()
	print out
	#for line in out:
	#	print line.strip()
		
def getNumberOfTC(testSuite,bug):
	whereToCall=bug.getFixPath()
	cmd="wc -l < all-tests.txt"
	p = subprocess.Popen(cmd, shell=True, cwd=whereToCall, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err = p.communicate()
	#print out
	return out

def main():
	args=getOptions()
	#first line to output file
	outputFolder= str(d4jHome) + "/" + str(args.wd) + "/"
	id=args.patches.split("/")[-3]+args.patches.split("/")[-2]
	#print str(id)
	outputFile=outputFolder + "/QualityAssessmentForGeneratedTS"+ str(id) +".csv"
	if(os.path.isfile(outputFile)):
		os.remove(outputFile)
	cmd = "echo \"Project,Bug,Patch,TSSeed,NumberOfTests,NumberOfFailingTests\" >> "+ outputFile
	p = subprocess.call(cmd, shell=True)
	#fill bug list
	bugs = []	
	getBugsFromPatchNames(bugs,args)
	for bug in bugs:
		print "Defect: "+bug.project + " " + str(bug.bugNum)
		ensureVersionAreCheckedOut(bug)
		
		#patch the fixed version
		patchFixedFile(bug,args)
		
		for seed in range(1,11):
			suitePath =  os.path.join(bug.getTestDir(), bug.getProject()+"-"+bug.getBugNum()+"f-evosuite-branch."+str(seed)+".tar.bz2")
			#capture number of failing test cases
			p = subprocess.call("rm all-tests.txt", shell=True, cwd=bug.getFixPath(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	
			cmd = defects4jCommand+" test -s "+ suitePath
			print cmd
			p = subprocess.Popen(cmd, shell=True, cwd=bug.getFixPath(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			failingTests=""
			for line in p.stdout:
				if "Failing tests:" in line: 
					print line
					failingTests=line.split("Failing tests:")[-1].strip() 
			#capture total number of test cases ran
			numberOfTests=getNumberOfTC(suitePath,bug).strip() 
			
			recordInOutputFile = "echo \"" + str(bug.getProject()) + ","+ str(bug.getBugNum()) + "," + str(bug.getPatch()) +"," +str(seed) + "," + str(numberOfTests) + ","+ str(failingTests) + "\" >> "+ outputFile
			print recordInOutputFile
			p = subprocess.call(recordInOutputFile, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	
	print "Result in "+ outputFile

main()
