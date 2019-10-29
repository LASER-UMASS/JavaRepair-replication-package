#/bin/python

import argparse
import os
import xml.etree.ElementTree
import subprocess
import sys
import shutil
import time

WD="/home/mausoto/tsePaperScripts/NewRepo/JavaRepair-results/test_suites/TS103SimFix/"

def getProjPath(project,version,tsName): 
    cmd = "defects4j checkout -p "+project + " -v "+version+ " -w toRemove" 
    p = subprocess.call(cmd, shell=True, cwd=str(WD)+"/TSForRQ4/", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    p = subprocess.Popen("tar -vxjf "+ tsName+" -C TSForRQ4/", shell=True, cwd=str(WD), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    cmd = "defects4j export -p classes.modified"
    p = subprocess.Popen(cmd, shell=True, cwd=str(WD)+"/TSForRQ4/toRemove/", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    projectPath=""
    for line in p.stdout:
        #print line
        projectPath=(line.strip().replace(".","/")[:line.strip().replace(".","/").rfind("/")+1])
        className=(line.strip().split(".")[-1])
        renameClass(projectPath,className,tsName)
        renameScaffolding(projectPath,className,tsName)
	
    cmd="tar -cvjSf "+ tsName+" "+projectPath.split("/")[0]
    p = subprocess.call(cmd , shell=True, cwd=str(WD)+"/TSForRQ4/", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p = subprocess.call("rm -rf "+projectPath.split("/")[0], shell=True, cwd=str(WD)+"/TSForRQ4/", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p = subprocess.call("rm -rf toRemove/", shell=True, cwd=str(WD)+"/TSForRQ4/", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	
def renameClass(projectPath,className,tsName):
    seedNum=tsName.split(".")[1]
    iName=str(str(WD)+"/TSForRQ4/"+projectPath+className+"_ESTest.java")
    oName=str(str(WD)+"/TSForRQ4/"+projectPath+className+str(seedNum)+"_ESTest.java")
    if os.path.isfile(iName):
        with open(iName) as i:
            with open(str(oName), "w") as o:
                for line in i:
                    if "_ESTest" in line:
                        line=line.replace(className+"_ESTest", className+str(seedNum)+"_ESTest")
						#line=line.replace(className+"_ESTest_scaffolding", className+str(seedNum)+"_ESTest_scaffolding")
                    if "separateClassLoader = true" in line:
                        line = line.replace("separateClassLoader = true", "separateClassLoader = false")
                    o.write(line) 
        p = subprocess.Popen("rm "+iName, shell=True, cwd=str(WD)+"/TSForRQ4/", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        subprocess.call("echo \""+tsName +":"+projectPath+className+"\" >> NonSuccessful.txt", shell=True, cwd=str(WD)+"/TSForRQ4/", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	
def renameScaffolding(projectPath,className,tsName):
    seedNum=tsName.split(".")[1]
    iName=str(str(WD)+"/TSForRQ4/"+projectPath+className+"_ESTest_scaffolding.java")
    oName=str(str(WD)+"/TSForRQ4/"+projectPath+className+str(seedNum)+"_ESTest_scaffolding.java")
    if os.path.isfile(iName):
        with open(iName) as i:
            with open(str(oName), "w") as o:
                for line in i:
                    if "_ESTest" in line:
                        line=line.replace(className+"_ESTest_scaffolding", className+str(seedNum)+"_ESTest_scaffolding")
                    o.write(line) 
        p = subprocess.Popen("rm "+iName, shell=True, cwd=str(WD)+"/TSForRQ4/", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        subprocess.call("echo "+tsName +": "+projectPath+className+" >> NonSuccessful.txt", shell=True, cwd=str(WD)+"/TSForRQ4/", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	
def main():
    #subprocess.call("rm -f NonSuccessful.txt", shell=True, cwd=str(WD)+"/TSForRQ4/", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p = subprocess.Popen("mkdir TSForRQ4", shell=True, cwd=str(WD)+"/", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    cmd = "ls -d *.tar.bz2"
    p = subprocess.Popen(cmd, shell=True, cwd=str(WD)+"/", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for tsName in p.stdout:
        tsName =tsName.strip()
        print tsName
        project=tsName.split('-')[0]
        version=tsName.split('-')[1]
        getProjPath(project,version,tsName)
		
main()