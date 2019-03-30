#/bin/python

#The purpose of this script is to create the positive and negative files which describe which tests pass and fail 
#the indicated patches. These files are necessary to compute the behavior of the N version patch

#Preconditions:
#There should be a folder called generatedTestSuites in the defects4j folder where the test suites and their output will be stored.
#The variable D4J_HOME should be directed to the folder where defects4j is installed.
#The variable JAVA_HOME should be directed to the folder where java 7 is installed (It must be Java 7).

#Ooutput
#The output is a set of .pos and .neg files in the file described in <Param 1>

#Parameters:
# 1st param is the working directory to check out project versions
# 2nd param is the folder where the patches are located")
# 3rd param is the absolute path where the test suite is located")

#Example of usage:
#python evaluatePatchesIn10TS.py /home/mausoto/tsePaperScripts/NewRepo/JavaRepair-results/src/patch-quality-assessment/NVersionProgram/GP/ /home/mausoto/tsePaperScripts/NewRepo/JavaRepair-results/results/RQ1/patches/GenProg/ /home/mausoto/tsePaperScripts/NewRepo/JavaRepair-results/test_suites/Evosuite106Budget1800/

import os
import subprocess
import sys
import argparse
import xml.etree.ElementTree
import shutil
import time

d4jHome = os.environ['D4J_HOME']
defects4jCommand = d4jHome + "/framework/bin/defects4j"
posTests=[]
negTests=[]

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

		
	
def getBugsFromPatchNames(bugs,args):
	cmd = "ls -d *.patch"
	p = subprocess.Popen(cmd, shell=True, cwd=args.patches, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	for line in p.stdout:
		defect=line.split('_')[0]
		bug=int(filter(str.isdigit, defect))
		project=str(filter(str.isalpha, defect)).title()
		bug = BugInfo(project, int(bug), args.outputFolder, args.testDir)
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

def populatePosList(suitePath,bug):
    global posTests
    posTests=[]
	#When using Evosuite 6
    posTestsTmp = open(bug.getFixPath()+"/all_tests").readlines()
	#When using Evosuite 3
    #posTestsTmp = open(bug.getFixPath()+"/all-tests.txt").readlines()
	
    for p in posTestsTmp:
        testName = (p.split("(")[0]).strip()
        className = ((p.split("(")[1]).split(")")[0]).strip()
        transformedP = className+"::"+testName
        posTests.append(transformedP)
def populateNegList(suitePath,bug): 
	global negTests
	cmd = "defects4j  test -s "+ suitePath
	print cmd
	p = subprocess.Popen(cmd, shell=True, cwd=bug.getFixPath(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	negTests=[]
	for line in p.stdout:
		if not ("Failing" in line):
			negTests.append((line[4:]).strip())
			#negTests=line.split("Failing tests:")[-1].strip() 
	
def writeListsToFile(project,bugNum,args,tsSeed,patch):
    global posTests
    global negTests
    with open(args.outputFolder+"/"+project+str(bugNum)+"_Patch_"+patch+"_TSSeed_"+str(tsSeed)+".neg", "a+") as negFile:
        for n in negTests:
            #n=(n[2:]).strip()
            negFile.write(str(n).strip()+"\n")
    negFile.close()
    with open(args.outputFolder+"/"+project+str(bugNum)+"_Patch_"+patch+"_TSSeed_"+str(tsSeed)+".pos", "a+") as posFile:
        for p in posTests:
            #testName = (p.split("(")[0]).strip()
            #className = ((p.split("(")[1]).split(")")[0]).strip()
            #transformedP = className+"::"+testName
            if not (p in negTests):
                posFile.write(str(p).strip()+"\n")
    posFile.close()
			
def getOptions():
	parser = argparse.ArgumentParser(description="Example of usage: python evaluatePatchesIn10TS.py /home/mausoto/JavaRepair-results/defects4j-scripts/NVersionProgram/GenProg/  /home/mausoto/JavaRepair-results/patches/GenProg/RQ0/  /home/mausoto/JavaRepair-results/generatedTestSuites/Evosuite103Budget1800/")
	parser.add_argument("outputFolder", help="working directory to check out project versions")
	parser.add_argument("patches", help="the folder where the patches are located")
	parser.add_argument("testDir", help="the absolute path where the test suite is located")
	
	return parser.parse_args()
			
def main():
	args=getOptions()
	#first line to output file
	outputFolder= str(args.outputFolder) + "/"
	id=args.patches.split("/")[-3]+args.patches.split("/")[-2]
	#print str(id)
	outputFile=outputFolder + "/QualityAssessmentForGeneratedTS"+ str(id) +".csv"
	if(os.path.isfile(outputFile)):
		os.remove(outputFile)
	#fill bug list
	bugs = []	
	getBugsFromPatchNames(bugs,args)
	for bug in bugs:
		#if "Time" not in  bug.project:
		#	continue
		#if  "19" not in str(bug.bugNum):
		#	continue
		#print "==>", bug.project, "Time" not in bug.project, "19" not in str(bug.bugNum)
		print "Defect: "+bug.project + " " + str(bug.bugNum)
		ensureVersionAreCheckedOut(bug)
		
		#patch the fixed version
		patchFixedFile(bug,args)
	
		cmd = defects4jCommand+" compile "
                print "COMPILING:", cmd, " from:", bug.getFixPath()
                p = subprocess.Popen(cmd, shell=True, cwd=bug.getFixPath(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, err = p.communicate()
                print out

	
		for seed in range(1,11):
			suitePath =  os.path.join(bug.getTestDir(), bug.getProject()+"-"+bug.getBugNum()+"f-evosuite-line."+str(seed)+".tar.bz2")
			#capture number of failing test cases
			#When using Evosuite 6 test suites
			p = subprocess.call("rm all_tests", shell=True, cwd=bug.getFixPath(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			#When using Evosuite 3 test suites
			#p = subprocess.call("rm all-tests.txt", shell=True, cwd=bug.getFixPath(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	
			populateNegList(suitePath,bug)
			populatePosList(suitePath,bug)
			writeListsToFile(bug.project,bug.bugNum,args,seed,bug.getPatch())
			#capture total number of test cases ran
			#numberOfTests=getNumberOfTC(suitePath,bug).strip() 
			
			#recordInOutputFile = "echo \"" + str(bug.getProject()) + ","+ str(bug.getBugNum()) + "," + str(bug.getPatch()) +"," +str(seed) + "," + str(numberOfTests) + ","+ str(failingTests) + "\" >> "+ outputFile
			#p = subprocess.call(recordInOutputFile, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	
#	print "Result in "+ outputFile

main()
