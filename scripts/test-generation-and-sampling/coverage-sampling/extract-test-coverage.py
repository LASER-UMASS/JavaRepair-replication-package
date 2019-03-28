############################
# This script is used to extract the test suite coverage of the Defects4J defects 
# along with identifying the failing tests of the defects.
# The input to this script is a directory that contains the 68 defects checkedout 
# using the defects4j framework and a file "relevant-test-methods.txt" is generated 
# by running defects4j command: defects4j test -r; mv all-tests.txt relevant-test-methods.txt
############################  

import os
import subprocess
import xml.etree.ElementTree as ET
import sys

defectDir = sys.argv[1]

defectCoverageMatrix={}
defectCoverageStats={}

def executeCommand(command):	
	status=0
	output=""
	try:
		output = subprocess.check_output(command, shell=True)                       
	except subprocess.CalledProcessError as grepexc:              
		print "ERROR EXECUTING COMMAND: %s"%(command)
		status = grepexc.returncode                  
		print "ERROR CODE: %s" %(status)                                                                   
	return status, output

path = '.' # path to directory containing defect folders containing relevant-test-methods.txt file that lists the relevant test methods for that defect
defectDirs = [ name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]

#for defectDir in defectDirs:
outputfile1 = open("coverage_matrix_%s.csv"%(defectDir), 'w')			
outputfile1.write("Defect" + "\t" + "RelevantTestMethod" + "\t" + "MethodCovered" + "\t" + "LinesCovered\n")

outputfile2 = open("coverage_stats_%s.csv"%(defectDir), 'w')			
outputfile2.write("Defect" + "\t" + "RelevantTestMethod" + "\t" + "LinesTotal#LinesCovered#LineCoverage" + "\t" + "TestType\n")
print defectDir
coverageMatrix={}
coverageStats={}
reltest_file = defectDir + "/relevant-test-methods.txt"

if os.path.isfile(reltest_file):
	os.chdir(defectDir)
	f = open("relevant-test-methods.txt")
	tritestdata = ""
	with open('triggering-tests.txt', 'r') as myfile:
		trigtestdata = myfile.read().replace('\n', ':::')
	print trigtestdata
	c=0
	for reltestmethod in f.readlines():
		c=c+1
		reltestmethod = reltestmethod.strip()
		print c
		print reltestmethod 
		command = "defects4j coverage -t %s" %(reltestmethod.replace("#","::")) 
		status, output = executeCommand(command)
		output = output.split('\n')
		print output
		linestotal = output[0].split(":")[1].strip()
		linescovered = output[1].split(":")[1].strip()
		coverage = output[4].split(":")[1].strip()
		print linestotal, linescovered, coverage
		tree = ET.parse('coverage.xml')
		root = tree.getroot()
		methodsexecuted = {}
		for classes in root.iter('class'):
			methods = classes.find('methods')
			for method in methods.findall('method'):
             			methodname=method.get('name')
				methodsign=method.get('signature')
				lines = method.find('lines')
				linesexecuted = []	
       				exeflag=False
				for line in lines.findall('line'):
					if int(line.get('hits')) > 0:	
						lineno=line.get('number')
						linesexecuted.append(lineno)
						exeflag=True
				if exeflag==True:			
					methodkey = methodname + "#" + methodsign
					methodsexecuted[methodkey] = linesexecuted	
					exeflag=False
		coverageMatrix[reltestmethod] = methodsexecuted
		coverageStats[reltestmethod] = linestotal + "#" + linescovered + "#" + coverage
	defectCoverageMatrix[defectDir] = coverageMatrix
	defectCoverageStats[defectDir] = coverageStats
        print "writing coverage matrix"	
	for reltestmethod in sorted(defectCoverageMatrix[defectDir].keys()):
		for methodcovered in sorted(defectCoverageMatrix[defectDir][reltestmethod].keys()):
			outstr = defectDir + "\t" + reltestmethod + "\t" + methodcovered + "\t" + ' '.join(defectCoverageMatrix[defectDir][reltestmethod][methodcovered]) + "\n"
			outputfile1.write(outstr)
	
        print "writing coverage stats"	
	for reltestmethod in sorted(defectCoverageStats[defectDir].keys()):
		if reltestmethod.replace("#","::") == trigtestdata:
			outstr = defectDir + "\t" + reltestmethod + "\t" + defectCoverageStats[defectDir][reltestmethod] + "\t triggering\n"
		else:
			outstr = defectDir + "\t" + reltestmethod + "\t" + defectCoverageStats[defectDir][reltestmethod] + "\t relevant\n"
		outputfile2.write(outstr)

	os.chdir("..")
else:
	print "RELEVANT TEST METHODS FILE NOT FOUND"
	print

outputfile1.close()
outputfile2.close()
