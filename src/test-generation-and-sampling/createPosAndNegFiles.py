#/bin/python

#The purpose of this script is to create files with positive and negative test cases to run the provenance experiment

#Preconditions:
#There should be a folder called generatedTestSuites in the defects4j folder where the test suites and their output will be stored.
#The variable D4J_HOME should be directed to the folder where defects4j is installed.
#The variable JAVA_HOME should be directed to the folder where java 7 is installed (It must be Java 7).
#You should manually modify the list of bugs to be ran in the array called "bugs"

#Output
#The output is a set of files with lists of positive and negative tests.

#Input:
#1st param is the absolute path where the test suites are located
#2nd param is where to place the pos and neg files

#Example of usage:
#python createPosAndNegFiles.py /home/mausoto/JavaRepair-results/generatedTestSuites/Evosuite103Budget1800/TSForRQ4/ /home/mausoto/JavaRepair-results/generatedTestSuites/Evosuite103Budget1800/TSForRQ4/PosAndNeg/

import argparse
import os
import xml.etree.ElementTree
import subprocess
import sys
import shutil
import time

posBuggyList=[]
posFixedList=[]
negBuggyList=[]
negFixedList=[]
buggyFolder="buggyFolder/"
fixedFolder="fixedFolder/"

def populateNegBuggyList(project,version,tsName,args): 
    global negBuggyList	
    cmd = "defects4j test -s "+args.testDir+ tsName 
    print cmd
    p = subprocess.Popen(cmd, shell=True, cwd=args.testDir+buggyFolder, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for line in p.stdout:
        line=line.strip()
        print line
        if not ("Failing" in line):
            #cmd = "echo \""+ line[2:] + "\" >> /home/mausoto/JavaRepair-results/generatedTestSuites/Evosuite103Budget1800/TSForRQ4/PosAndNeg/"+project+version.replace("f","")+".neg"
            #p = subprocess.Popen(cmd, shell=True, cwd="/home/mausoto/JavaRepair-results/generatedTestSuites/Evosuite103Budget1800/TSForRQ4/", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            negBuggyList.append(line[2:])
			
def populateNegFixedList(project,version,tsName,args): 
    global negFixedList
    cmd = "defects4j test -s "+args.testDir+ tsName 
    print cmd
    p = subprocess.Popen(cmd, shell=True, cwd=args.testDir+fixedFolder, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for line in p.stdout:
        line=line.strip()
        print line
        if not ("Failing" in line):
            #cmd = "echo \""+ line[2:] + "\" >> /home/mausoto/JavaRepair-results/generatedTestSuites/Evosuite103Budget1800/TSForRQ4/PosAndNeg/"+project+version.replace("f","")+".neg"
            #p = subprocess.Popen(cmd, shell=True, cwd="/home/mausoto/JavaRepair-results/generatedTestSuites/Evosuite103Budget1800/TSForRQ4/", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            negFixedList.append(line[2:])
    
def checkout(project,version,args):  
    global posBuggyList
    global posFixedList
    global negBuggyList
    global negFixedList
    p = subprocess.call("rm -rf "+fixedFolder, shell=True, cwd=args.testDir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    cmd = "defects4j checkout -p "+project + " -v "+version+ " -w "+fixedFolder 
    p = subprocess.call(cmd, shell=True, cwd=args.testDir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print "\n"+str(cmd)
    p = subprocess.call("rm -rf "+buggyFolder, shell=True, cwd=args.testDir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    cmd = "defects4j checkout -p "+project + " -v "+version.replace("f","b")+ " -w "+buggyFolder
    p = subprocess.call(cmd, shell=True, cwd=args.testDir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print "\n"+str(cmd)
    posBuggyList=[]
    posFixedList=[]
    negBuggyList=[]
    negFixedList=[]
   
def populatePosBuggyList(args):
    global negBuggyList
    global posBuggyList
    with open(args.testDir+"/"+buggyFolder+"/all_tests",'r') as source:
        allTests = source.readlines()
    for t in allTests:
        t=t[:-1].strip()
        tInFormat = (t.split("(")[1])[:-1]+"::"+t.split("(")[0]
        if tInFormat not in negBuggyList:
            posBuggyList.append(tInFormat)
            
def populatePosFixedList(args):
    global negFixedList
    global posFixedList
    with open(args.testDir+"/"+fixedFolder+"/all_tests",'r') as source:
        allTests = source.readlines()
    for t in allTests:
        t=t[:-1].strip()
        tInFormat = (t.split("(")[1])[:-1]+"::"+t.split("(")[0]
        if tInFormat not in negFixedList:
            posFixedList.append(tInFormat)
            
def writeListsToFile(project,version,args):
    global posBuggyList
    global posFixedList
    global negBuggyList
    global negFixedList
    with open(args.output+"/"+project+version.replace("f","")+".neg", "w") as negFile:
        for n in negBuggyList:
            if n in posFixedList:
                negFile.write(str(n)+"\n")
    negFile.close()
    with open(args.output+"/"+project+version.replace("f","")+".pos", "w") as posFile:
        for p in posBuggyList:
            if p in posFixedList:
                posFile.write(str(p)+"\n")
    posFile.close()
    #discarded	
    with open(args.output+"/discarted.list", "a+") as disFile:
        disFile.write(project+version.replace("f","")+":\n")
        for p in negFixedList:
            disFile.write(str(p)+"\n")
    disFile.close()
	
	
def getOptions():
	parser = argparse.ArgumentParser(description="Example of usage: python createPosAndNegFiles.py /home/mausoto/JavaRepair-results/generatedTestSuites/Evosuite103Budget1800/TSForRQ4/ /home/mausoto/JavaRepair-results/generatedTestSuites/Evosuite103Budget1800/TSForRQ4/PosAndNeg/")
	parser.add_argument("testDir", help="the absolute path where the test suites are located")
	parser.add_argument("output", help="where to place the pos and neg files")
	return parser.parse_args()
   
def main():
    args=getOptions()
    if os.path.isdir(args.output):
        subprocess.call("rm -fr "+args.output, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p = subprocess.Popen("mkdir "+args.output, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    cmd = "ls -d *.tar.bz2"
    p = subprocess.Popen(cmd, shell=True, cwd=args.testDir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    tsNameToCompare=""
    for tsName in p.stdout:
        tsName =tsName.strip()
        print tsName
        project=tsName.split('-')[0]
        version=tsName.split('-')[1]
        if tsName.split(".")[0] != tsNameToCompare:
            checkout(project,version,args)
            tsNameToCompare=tsName.split(".")[0]
        populateNegBuggyList(project,version,tsName,args)
        populateNegFixedList(project,version,tsName,args)
        if tsName.split(".")[1]=="9": 
            populatePosBuggyList(args)
            populatePosFixedList(args)
            writeListsToFile(project,version,args)
    
    p = subprocess.call("rm -rf "+buggyFolder, shell=True, cwd=args.testDir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p = subprocess.call("rm -rf "+fixedFolder, shell=True, cwd=args.testDir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
main()