#/bin/python

#The purpose of this script is to determine the behavior of the N version patches
#This script is meant to be ran after evaluatePatchesIn10TS.py

#Preconditions:
#There should be a folder called generatedTestSuites in the defects4j folder where the test suites and their output will be stored.
#The variable D4J_HOME should be directed to the folder where defects4j is installed.
#The variable JAVA_HOME should be directed to the folder where java 7 is installed (It must be Java 7).

#Ooutput
#The output is a file in <1st param>/ResultsNVersion.csv

#Parameters:
# 1st param is the folder where the pos and neg files are located

#Example of usage:
#python analyzeLogs.py /home/mausoto/JavaRepair-results/defects4j-scripts/NVersionProgram/GP/

import os
import subprocess
import sys
import argparse
import xml.etree.ElementTree
import shutil
import time
import string

bug=""
patch=""
failingTests = {}
patchCounter = 0
totalNumOfTests = 0
testsFailedByNVersion=0

def getNumberOfTC(line,args):
	#neg
	cmd="wc -l < "+line
	p = subprocess.Popen(cmd, shell=True, cwd=args.posAndNegFolder, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err = p.communicate()
	total = int(out.strip())
	
	#pos
	cmd="wc -l < "+string.replace(line,'.neg','.pos')
	p = subprocess.Popen(cmd, shell=True, cwd=args.posAndNegFolder, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err = p.communicate()
	total += int(out.strip())
	
	#print "total:"+str(total)
	return total
	
def appendToResultsFile(bug,totalNumOfTests,testsFailedByNVersion,args):
	cmd="echo "+ str(bug)+","+str(totalNumOfTests)+","+str(testsFailedByNVersion)+" >> ResultsNVersion.csv"
	#print cmd
	p = subprocess.Popen(cmd, shell=True, cwd=args.posAndNegFolder, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	
def appendToListOfFailedTestsFile(t,args):
	cmd="echo "+str(t)+" >> FailedTestsByNVersion.csv"
	#print cmd
	p = subprocess.Popen(cmd, shell=True, cwd=args.posAndNegFolder, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def wrapUp(args):
	global bug
	global failingTests
	global patchCounter 
	global totalNumOfTests 
	global testsFailedByNVersion
	
	#print "\n"+str(bug)
	#print patchCounter
	#print failingTests
	for test in failingTests.keys():
		if failingTests[test] >= (patchCounter/2) and patchCounter > 2:
			#print "bug:"+str(bug)
			#print "patchCounter:"+str(patchCounter)
			#print "test:"+str(test)
			#print "failingtests[test]"+str(failingTests[test])
			#this patch failed in over half of the patches
			appendToListOfFailedTestsFile(bug+"::"+test,args)
			testsFailedByNVersion += 1
	if patchCounter > 2:
		appendToResultsFile(bug,totalNumOfTests,testsFailedByNVersion,args)
	failingTests = {}
	patchCounter = 0
	testsFailedByNVersion = 0
			
def getOptions():
	parser = argparse.ArgumentParser(description="Example of usage: python analyzeLogs.py /home/mausoto/JavaRepair-results/defects4j-scripts/NVersionProgram/GP/")
	parser.add_argument("posAndNegFolder", help="the folder where the pos and neg files are located")
	return parser.parse_args()
	
def main():
	global bug
	global patch
	global failingTests
	global patchCounter 
	global totalNumOfTests 
	global testsFailedByNVersion
	args=getOptions()
	subprocess.Popen("rm ResultsNVersion.csv", shell=True, cwd=args.posAndNegFolder, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	subprocess.Popen("rm FailedTestsByNVersion.csv", shell=True, cwd=args.posAndNegFolder, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	appendToResultsFile("Bug","TotalTestCases","FailedTestCases",args)
	cmd = "ls -d *.neg"
	p = subprocess.Popen(cmd, shell=True, cwd=args.posAndNegFolder, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	
	for line in p.stdout:
		line=line.strip()
		if bug != "" and line.split('_')[0] != bug:
			#wrap up previous bug
			wrapUp(args)
		
		if line.split('.patch')[0] != patch:
			patchCounter += 1
			totalNumOfTests = 0
				
		tsSeed=(line.split('TSSeed_')[-1]).split('.neg')[0]
		ftInThisFile = open(args.posAndNegFolder+line).readlines()
		for ft in ftInThisFile:
			ft=ft.strip()
			testName = "SubTS"+str(tsSeed)+str(ft)
			if testName in failingTests:
				failingTests[testName] += 1
			else:
				failingTests[testName] = 1
		
		totalNumOfTests += int(getNumberOfTC(line,args))
		patch=line.split('.patch')[0]
		bug=line.split('_')[0]
	
	#last bug
	wrapUp(args)
	
main()
