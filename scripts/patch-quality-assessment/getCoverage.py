#/bin/python

#The purpose of this script is to collect branch and line coverage data of a test suite of the class and modified methods in the selected bugs

# DEPENDENCIES:
# 1. JAVA_HOME is set to Java 8
# 2. D4J_HOME is set to Defects4J (Java 8 support) 
# 3. The symbolic link "defects4j/framework/lib/test_generation/runtime/evosuite-rt.jar" points to evosuite-standalone-runtime-1.0.3.jar 
# 4. Python version 2.7 

#INPUT:	
# 1st param is the working directory to check out project versions, starting from the the D4J_HOME folder
# 2nd param is the absolute path where the test suite is located (Example: /home/mausoto/defects4j/generatedTestSuites)
# 3rd param is the a descriptive name for the outputFile
# --project is the project in upper case (ex: Lang, Chart, Closure, Math, Time)
# --bug is the bug number (ex: 1,2,3,4,...)
# --many is Absolute path, the file listing bugs to process: project,bugNum (one per line). Lines starting with # are skipped
# --patches is the folder where the patches are located, starting from the the D4J_HOME folder
# --tool is the generation tool (Randoop or Evosuite)
# --seed is the seed the test suite was created with
# --coverage is a coverage file

# CMD TO RUN: 
# e.g., python getCoverage.py ExamplesCheckedOut1 /home/mausoto/defects4jJava8/defects4j/generatedTestSuites/allTestSuites/ 20180215 --project Closure --bug 83 --seed 1

# OUTPUT:
# The output file is generated in <d4jHome>/<1st param>/<3rd param>

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
		self.patch=patch #this is the path from d4jHome + where it is + the patch name

	def getPatch(self):
		return str(os.path.join(d4jHome,"/"+self.patch))

		
def getNumberOfLinesCovered(changedLinesInXML):
	#get number of lines covered
	linesCovered=0
	methodsChanged=[]
	for changedLineInXML in changedLinesInXML:
		# check if covered
		if(int(changedLineInXML.attrib['hits']) != 0):
			linesCovered += 1
	return linesCovered
	
def getCoveragesOfMethodsChanged(methodsChanged, coverageFile):
	e = xml.etree.ElementTree.parse(coverageFile).getroot()
	ret = ""	
	for m in methodsChanged:
		#print  str(m)
		methodFound=False
		for mxml in e.findall(".//method"):
			#print "line 71: "+ m +" "+str(mxml.attrib['name'])+str(mxml.attrib['signature'])
			if (m == str(mxml.attrib['name'])+str(mxml.attrib['signature'])):
				methodFound=True
				methodLineCov= round(float(mxml.attrib['line-rate'])*100,2)
				methodBranchCov=round(float(mxml.attrib['branch-rate'])*100,2)
				ret +=","+str(mxml.attrib['name'])+","+str(methodLineCov)+","+str(methodBranchCov)
				#print "Added " + str(mxml.attrib['name'])
				break
		if methodFound == True:
			methodFound == False
		else:
			ret +=","+str(m.split("(")[0])+",Method not found in fixed version,Method not found in fixed version"
	#print "ret "+ret
	return ret
	
def getInitialCoverageMetrics(coverageFile):
	#Class coverage
	e = xml.etree.ElementTree.parse(coverageFile).getroot()
	classLineCoverage=round(float(e.attrib['line-rate'])*100,2)
	classConditionCoverage=round(float(e.attrib['branch-rate'])*100,2)
	ret = str(classLineCoverage) + "," + str(classConditionCoverage)
	return ret
	
def getChangedLinesInXML(listOfChangedLines,coverageFile):
	e = xml.etree.ElementTree.parse(coverageFile).getroot()
	lines = e.findall(".//line")
	changedLinesInXML = []
	lineNumbersCoveredAlready = []
	for line in lines:
		if(line.attrib['number'] in listOfChangedLines):
			if(not (line.attrib['number'] in lineNumbersCoveredAlready)):
				changedLinesInXML.append(line)
				lineNumbersCoveredAlready.append(line.attrib['number'])
	return list(set(changedLinesInXML))
	
def methodsAssociatedWithLines(listOfChangedLines, coverageFile):
	#print "got into methodsAssociatedWithLines"
	#get methods associated with the changed lines
	e = xml.etree.ElementTree.parse(coverageFile).getroot()
	methodsForThisLine=[]
	for changedLine in listOfChangedLines:
		for m in printMethodCorrespondingToLine(changedLine, e):
			methodsForThisLine.append(m)
	methodsChanged= list(set(methodsForThisLine))
	return list(set(methodsChanged))
	
def getChangedMethods(listOfChangedLines, coverageFile):		
	#print "got into getChangedMethods"
	#changedLinesInXML=getChangedLinesInXML(listOfChangedLines,coverageFile)
	#numberOfLinesCovered=getNumberOfLinesCovered(changedLinesInXML)
	methodsChanged=methodsAssociatedWithLines(listOfChangedLines,coverageFile)
	#print "Methods changed: "+ str(methodsChanged)
	#linesChanged=len(listOfChangedLines)
	#percentageLinesCovered=round(numberOfLinesCovered*100/linesChanged,2)
	
	#ret=","+str(linesChanged)
	#ret+=","+str(percentageLinesCovered)
	#ret+=","+str(len(methodsChanged))
	
	methods = []
	for m in methodsChanged:
		#methodLineCov= round(float(m.attrib['line-rate'])*100,2)
		#methodBranchCov=round(float(m.attrib['branch-rate'])*100,2)
		#mi = MethodInfo(str(m.attrib['name']),str(methodLineCov),str(methodBranchCov), m)
		#methods.append(mi)
		
		id=str(m.attrib['name'])+str(m.attrib['signature'])
		#print id
		methods.append(id)
	#return [ret,methods]
	return list(set(methods))

def printMethodCorrespondingToLine(lineNumber, tree):
	#print "Looking for method from line "+ lineNum
	lineNum=int(lineNumber)
	methodsChanged=[]
	
	#sometimes the modified line is the middle of a stmt, so we look for the line in the beggining of the stmt
	existsLineNum=False
	#In case the Infix Expression takes more than one line
	lowerBound=lineNum-2
	while not existsLineNum and lineNum>lowerBound:
		for l in tree.findall(".//line"):
			#print "Comparing "+str(l.attrib['number'])+" to "+ str(lineNum)
			if str(l.attrib['number']) == str(lineNum):
				existsLineNum=True
				#print "Found line "+ str(lineNum)
				break
		if existsLineNum==False:
			#print "Didnt find line "+ str(lineNum)+ " Trying next one"
			lineNum-=1
	
	for method in tree.findall(".//method"):
		lines = method.find("lines")
		if int(len(lines)) > 0:
			for line in lines:
				#print "Comparing "+str(line.attrib['number']) +" to "+ str(lineNum)
				if(str(line.attrib['number']) == str(lineNum) and not method in methodsChanged):
					#print "Added "+ str(method.attrib['name'])
					methodsChanged.append(method)

#			firstLineOfMethod = lines[0]
#			highestLineNum=0
#			for l in lines:
#				if int(l.attrib['number']) > highestLineNum:
#					highestLineNum= int(l.attrib['number'])
#			if int(lineNum) >= int(firstLineOfMethod.attrib['number']) and int(lineNum) <= highestLineNum:
#				methodsChanged.append(method)
					
	return list(set(methodsChanged))

def generateCovXML(bug, tool, tsseed):
	if(tool.lower() == "evosuite"):
		#This can be evosuite-line or evosuite-branch
		testSuiteName="evosuite-line"
	elif(tool.lower() == "randoop"):
		testSuiteName="randoop"
	suitePath =  os.path.join(bug.getTestDir(), bug.getProject()+"-"+bug.getBugNum()+"f-"+testSuiteName+"."+str(tsseed)+".tar.bz2")
	if(os.path.isfile(suitePath)):
		cmd = defects4jCommand + " compile -w " + bug.getFixPath()
		subprocess.call(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
		#print cmd
		
		cmd = defects4jCommand + " coverage -w " + bug.getFixPath() + " -s " + str(suitePath)
		subprocess.call(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
		print "ran coverage on fixed folder: " + cmd
		
		cmd = defects4jCommand + " compile -w " + bug.getBugPath()
		subprocess.call(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
		print cmd
		
		cmd = defects4jCommand + " coverage -w " + bug.getBugPath() + " -s " + str(suitePath)
		subprocess.call(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
		print "ran coverage on buggy folder: " + cmd
	else:
		print "The script did not find a test suite: " + str(suitePath)
		
def getEditedFiles(bug):
	cmd = defects4jCommand + " export -p classes.modified"
	p = subprocess.Popen(cmd, shell=True, cwd=bug.getBugPath(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	return [ line.split("2>&1")[-1].strip().replace(".", "/") + ".java" for line in p.stdout ]


def getADiff(pathToFile, bug, new):
	pathToSource=bug.getSrcPath()
	
	cmd = "diff -w --unchanged-line-format=\"\"  "
	if new:
		cmd+="--old-line-format=\"\" --new-line-format=\"%dn \" " 
	else:
		cmd+="--old-line-format=\"%dn \" --new-line-format=\"\" " 
	cmd+=bug.getBugPath()+"/"+pathToSource+"/"+pathToFile +" " + bug.getFixPath()+"/"+pathToSource+"/"+pathToFile
	print cmd
	p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	diffLines=""
	for line in p.stdout:
		diffLines = line
	diffLines=diffLines.strip().split(" ")
	#remove empty strings
	diffLines=list(filter(None, diffLines))
	
	#ignore lines where there is a single bracket because it won't be covered by cobertura
	ret=[]
	for changedLine in diffLines:
		cmd="sed \'"+ str(changedLine)+"q;d\' "
		if new:
			cmd+= bug.getFixPath()
		else:
			cmd+= bug.getBugPath()
		cmd+="/"+pathToSource+"/"+pathToFile 
		p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		for line in p.stdout:
			if line.strip() != "}" and line.strip() != "{" and not line.strip() is None:
				#print "Appending to ret: \'" + str(changedLine) + "\'"
				ret.append(changedLine)
	return ret

#args.many is assumed to be not None
def getAllBugs(bugs,args):
	if(not os.path.isfile(args.many)):
		sys.exit("The file " + str(args.many) + " does not exist")
	else:
		with open(args.many) as f:
			pairs = [x.strip().split(',') for x in f.readlines() if x[0] != '#']
			if pairs is None:
				sys.exit("There has been a problem reading the file with the bugs")
			for pair in pairs:
				bug = BugInfo(pair[0], int(pair[1]), args.wd, args.testDir)
				bugs.append(bug)

def getBugsFromPatchNames(bugs,args):
	cmd = "ls -d *.diff"
	p = subprocess.Popen(cmd, shell=True, cwd=d4jHome+args.patches, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	for line in p.stdout:
		defect=line.split('_')[0]
		bug=int(filter(str.isdigit, defect))
		project=str(filter(str.isalpha, defect)).title()
		bug = BugInfo(project, int(bug), args.wd, args.testDir)
		bug.setPatch(args.patches+"/"+line)
		bugs.append(bug)

def patchFixedFile(bug):
	pathToSource=bug.getSrcPath()

	#Removing the fixed file
	shutil.rmtree(bug.getFixPath())
	checkout(bug.getFixPath(),bug.getProject(), bug.getBugNum(), "b")
		
	#Patching the fixed file
	whereToCallPatch=str(bug.getFixPath())+"/"+str(pathToSource)
	cmd ="patch -p10 -i "+d4jHome+"/"+bug.getPatch()
	#print whereToCallPatch
	p = subprocess.Popen(cmd, shell=True, cwd=whereToCallPatch, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def ensureVersionAreCheckedOut(bug):
	#Remove and re clone versions
	if(os.path.exists(bug.getBugPath())):
		shutil.rmtree(bug.getBugPath())
	checkout(bug.getBugPath(), bug.getProject(), bug.getBugNum(), "b")
	if(os.path.exists(bug.getFixPath())):
		shutil.rmtree(bug.getFixPath())
	checkout(bug.getFixPath(), bug.getProject(), bug.getBugNum(), "f")

def checkout(folderToCheckout, project, bugNum, vers):
	cmd = defects4jCommand + " checkout -p " + str(project) + " -v " + str(bugNum) + str(vers) + " -w " + str(folderToCheckout)
	print cmd
	p = subprocess.call(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def getOptions():
	parser = argparse.ArgumentParser(description="This script checks if a test suite is covering the human changes. Example of usage: python getCoverage.py ExamplesCheckedOut1 /home/mausoto/defects4jJava8/defects4j/generatedTestSuites/allTestSuites/ testingError --project Closure --bug 83 --seed 1")
	parser.add_argument("wd", help="working directory to check out project versions, starting from the the D4J_HOME folder")
	parser.add_argument("testDir", help="the absolute path where the test suite is located (Example: /home/mausoto/defects4j/generatedTestSuites)")
	parser.add_argument("outputName", help="a descriptive name for the outputFile (Example: human)")
	parser.add_argument("--project", help="the project in upper case (ex: Lang, Chart, Closure, Math, Time)")
	parser.add_argument("--bug", help="the bug number (ex: 1,2,3,4,...)")
	parser.add_argument("--many", help="Absolute path, the file listing bugs to process: project,bugNum (one per line). Lines starting with # are skipped")
	parser.add_argument("--patches", help="the folder where the patches are located, starting from the the D4J_HOME folder")
	parser.add_argument("--tool", help="the generation tool (Randoop or Evosuite)", default="Evosuite")
	parser.add_argument("--seed", help="the seed the test suite was created with", default="1")
	parser.add_argument("--coverage", help="a coverage file")
	return parser.parse_args()

def errorHandling(args):
	if os.environ['D4J_HOME'] is None:
		sys.exit("Environment variable D4J_HOME is not set")
	if not os.path.isdir(os.path.join(d4jHome, args.wd)):
		sys.exit("The folder " + str(os.path.join(d4jHome, args.wd)) + " does not exist")
	if not os.path.isdir(args.testDir):
		sys.exit("The folder " + str(args.testDir) + " does not exist")
	if not(args.many is None) and not os.path.exists(args.many):
		sys.exit("The file " + str(args.many) + " does not exist")
	if not(args.many is None) and (not(args.project is None) or not(args.bug is None) or not(args.patches is None)):
		sys.exit("There should be just one of these three options: 1) A file with a list of bugs should be provided with the --many parameter, 2) a particular bug with the --project and --bug parameters, 3) A location with patches with the --patches parameter")
	if not(args.patches is None) and (not(args.project is None) or not(args.bug is None) or not(args.many is None)):
		sys.exit("There should be just one of these three options: 1) A file with a list of bugs should be provided with the --many parameter, 2) a particular bug with the --project and --bug parameters, 3) A location with patches with the --patches parameter")
	if (not(args.project is None) and not(args.bug is None)) and (not(args.patches is None)  or not(args.many is None)):
		sys.exit("There should be just one of these three options: 1) A file with a list of bugs should be provided with the --many parameter, 2) a particular bug with the --project and --bug parameters, 3) A location with patches with the --patches parameter")
	if args.project is None and args.bug is None and args.patches is None and args.many is None:
		sys.exit("There should be one of these three options: 1) A file with a list of bugs should be provided with the --many parameter, 2) a particular bug with the --project and --bug parameters, 3) A location with patches with the --patches parameter")
	if not(args.tool is None):
		if args.tool != "Randoop" and args.tool != "Evosuite":	
			sys.exit("tool should be Randoop or Evosuite")
	if not(args.seed is None) and (not (args.seed.isdigit())):
		sys.exit("Seed should be an integer")
	if not(args.patches is None) and (not os.path.isdir(os.path.join(d4jHome, args.patches))):
		sys.exit("The folder " + str(os.path.join(d4jHome, args.patches)) + " does not exist")
	if not(args.coverage is None) and (not os.path.isfile(args.coverage)):
		sys.exit("The file " + str(args.coverage) + " does not exist")


def main():
	args=getOptions()
	errorHandling(args)

	date=time.strftime("%d%H%M%S")
	
	
	if not(args.patches is None):
		outputFolder= str(d4jHome)+ str(args.wd) + "/" + str(args.outputName) + "Date"+date+ "TSSeed"+ str(args.seed) + "Generated/"
		outputFile=outputFolder + str(args.outputName) + "Date"+date+ "TSSeed"+ str(args.seed) + "Generated.csv"
		cmd = "echo \"Project,Bug,PatchSeed,Edits,Class line cov,Class condition cov, Method changed,Method line coverage,Method Branch coverage\" >> "+ outputFile
	elif not(args.many is None) or not(args.bug is None):
		outputFolder= str(d4jHome)+ str(args.wd) + "/" + str(args.outputName) + "Date"+date+ "TSSeed"+ str(args.seed) + "Human/"
		outputFile=outputFolder + str(args.outputName) + "Date"+date+ "TSSeed"+ str(args.seed) + "Human.csv"
		cmd = "echo \"Project,Bug,Class line cov,Class condition cov,Method changed ,Method line coverage,Method Branch coverage\" >> "+ outputFile
	#removes outputfolder if exists
	if(os.path.isfile(outputFolder)):
		os.remove(outputFolder)
	#creates new folder to output all the useful outputs
	p = subprocess.call("mkdir " + str(outputFolder), shell=True)
	p = subprocess.call(cmd, shell=True)#, cwd=bug.getBugPath(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				
	#fill bug list
	bugs = []
	if(not(args.project is None)):
		bugs.append(BugInfo(args.project, args.bug, args.wd, args.testDir))
	elif(not(args.many is None)):
		getAllBugs(bugs, args)
	elif(not(args.patches is None)):
		getBugsFromPatchNames(bugs,args)

	for bug in bugs:
		print "Defect: "+bug.project + " " + str(bug.bugNum)
		ensureVersionAreCheckedOut(bug)
		bug.setScrPath()

		#if we are doing the patches flag, patch the fixed version
		if not args.patches is None:
			patchFixedFile(bug)

		#creating xml file
		if(args.coverage != None) or (not os.path.exists(bug.getFixPath()+"/coverage.xml")) or (not os.path.exists(bug.getBugPath()+"/coverage.xml")):
			generateCovXML(bug,args.tool, args.seed)
		if os.path.exists(bug.getFixPath()+"/coverage.xml"):
			allCoverageMetrics=""
			for f in getEditedFiles(bug):
				#print "Working on file "+f
				listOfAddedLines = getADiff(f, bug, True)
				##print "Added lines: "+ str(listOfAddedLines)
				listOfDeletedLines = getADiff(f, bug, False)
				##print "Deleted lines: "+ str(listOfDeletedLines) + " Length: " + str(len(listOfDeletedLines))
				allCoverageMetrics=getInitialCoverageMetrics(bug.getFixPath()+"/coverage.xml")
				
				listOfMethodsDel=[]
				if len(listOfDeletedLines) > 0:
					listOfMethodsDel = getChangedMethods(listOfDeletedLines, bug.getBugPath()+"/coverage.xml")
				#	[covInfoBuggy,listOfMethodsDel] = computeCoverage(listOfDeletedLines, bug.getBugPath()+"/coverage.xml")
					print "MethodsDel "+ str(listOfMethodsDel)
				#	allCoverageMetrics+=covInfoBuggy #index 0 has lines deleted, coverage of lines deleted and methods changed by lines deleted. Index 1 has a list methods changed
				#else:
				#	#print "Nothing deleted"
				#	allCoverageMetrics+=",0,-,0"
				#	listOfMethodsDel=[]
				
				listOfMethodsAdd=[]
				if len(listOfAddedLines) > 0:
					listOfMethodsAdd = getChangedMethods(listOfAddedLines, bug.getFixPath()+"/coverage.xml")
				#	[covInfoPatched,listOfMethodsAdd] = computeCoverage(listOfAddedLines, bug.getFixPath()+"/coverage.xml")
				#	#print listOfMethodsAdd
				#	allCoverageMetrics+=covInfoPatched
				#else:
				#	#print "Nothing added"
				#	allCoverageMetrics+=",0,-,0"
				#	listOfMethodsAdd=[]
					
				methodsChanged = list(set(listOfMethodsAdd))
				#print "Methods changed"
				#print [m for m in methodsChanged]
				for b in listOfMethodsDel:	
					#print "Checking if this is in the list above: "+ b 
					if not (b in methodsChanged):
						#print "It wasnt! " + str(b)
						methodsChanged.append(b)
			
				
				#print "Methods changed after adding the others"
				#print [m for m in methodsChanged]
				#Get coverages of changed methods in coverage.xml from the patched version
				allCoverageMetrics+=getCoveragesOfMethodsChanged(methodsChanged, bug.getFixPath()+"/coverage.xml")
				#pipes the result to a csv file
				patchSeed = ""
				#Generated patch
				if not args.patches is None:
					#patchName=str(bug.getPatch().split('/')[-1].strip())
					diffName=str(bug.getPatch().split('/')[-1].strip())
					defect=diffName.split('_')[0]
					bugN=int(filter(str.isdigit, defect))
					project=str(filter(str.isalpha, defect)).title()
					patchSeed=int(filter(str.isdigit, diffName.split('_')[1]))
					edits=diffName.split('_')[2:-1]
					edits=str(edits).replace("['","").replace("']",")").replace("r', '","r(").replace("d', '","d(").replace("a', '","a(").replace("e', '","e(").replace("', '","_").replace("zer)","zer")
					#print "diffName: "+diffName
					#variant=int(filter(str.isdigit, diffName.split('_')[-1]))
					#variant=""
					allCoverageMetrics=str(project)+","+str(bugN)+","+str(patchSeed)+","+str(edits)+","+str(allCoverageMetrics)
					#allCoverageMetrics=str(project)+","+str(bugN)+","+str(patchSeed)+","+str(edits)+","+str(variant)+","+str(allCoverageMetrics)
				#Human made patch
				if not args.many is None or not args.project is None:
					patchName=str(bug.getProject() +","+ bug.getBugNum())
					allCoverageMetrics=patchName+","+allCoverageMetrics
				print allCoverageMetrics
				cmd = "echo \""+str(allCoverageMetrics)+ "\" >> "+ outputFile
				p = subprocess.call(cmd, shell=True)#, cwd=bug.getBugPath(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				print ""
				
				#Move and rename coverage file
				xmlFileName=str(outputFolder) + str(bug.getProject()) + str(bug.getBugNum()) 
				if not patchSeed == "":
					xmlFileName += "PatchSeed"+str(patchSeed)
				cmd = "mv " + str(bug.getFixPath()) +"/coverage.xml " + xmlFileName + ".xml"
				p = subprocess.call(cmd, shell=True)#, cwd=bug.getBugPath(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				cmd = "mv " + str(bug.getFixPath()) +"/cobertura.ser " + xmlFileName+ ".ser"
				p = subprocess.call(cmd, shell=True)#, cwd=bug.getBugPath(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				
		else: 
			print "There is no coverage file in "+bug.getFixPath()+"/coverage.xml"
			allCoverageMetrics=str(bug.getProject()) + str(bug.getBugNum())
			cmd = "echo \""+str(allCoverageMetrics)+ "\" >> "+ outputFile
			p = subprocess.call(cmd, shell=True)#, cwd=bug.getBugPath(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		
	print "Results in "+outputFile
main()
