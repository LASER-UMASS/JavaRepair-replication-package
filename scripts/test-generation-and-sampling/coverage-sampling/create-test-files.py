# The purpose of this script is to parse the output file generated using 
# ComputeSubsetsDefects4J.java and generate files that contain positive 
# and negative tests of a a defect which are used while running experiments.
#
# This script requires two arguments: (1) path to the output file generated 
# using ComputeSubsetsDefects4J.java and (2) path to the "triggering-tests.txt"
# file which is extracted from coverage_stats.csv and lists the triggering-tests
# for each defect 
# 
# The output of this script are the files that follow the naming convention:
# <defect>_<target-coverage>_<data-point>_pos.tests where target-coverage can 
# be 20, 40, 60, 80, 100 and data-point denotes the iteration in which we obtain
# a distinct sample for e.g. Math85Buggy_80_2_pos.tests denotes a sampled test-suite
# with two positive tests and the normalized coverage of the combined set of these 
# two positive tests and all the negative tests of Math 85 belongs to range 75%-85%. 

import sys

sampledoutput = open(sys.argv[1])    # path to output file generated using ComputeSubsetsDefects4J.java
triggeringtests = open(sys.argv[2])  # path to triggering-tests.txt

sample = sys.argv[1].split("_")[1].replace(".txt","").strip()
defect = ""
mincov = ""
maxcov = ""
numtrig = ""
numrel = ""
cov = 0

defectInfo = {}
defectTests = {}
defectCoverages = {}
defectdp = {}
defectTrigTests = {}
defect = ""
dp = 0

for line in triggeringtests:
	info = line.split(",")
	defect = info[0]
	trigtest = info[1]
	if defect not in defectTrigTests:
		defectTrigTests[defect] = [trigtest]
	else:
		tests = defectTrigTests[defect]
		tests.append(trigtest)
		defectTrigTests[defect] = tests

for line in sampledoutput:
	if "SAMPLING BEGINS FOR DEFECT:" in line or "******** DONE FOR ALL DEFECTS *****************" in line:
		if defect!="": 
			defectdp[defect] = dp
			dp = 0
		if "SAMPLING BEGINS FOR DEFECT:" in line:
			defect = line.split("SAMPLING BEGINS FOR DEFECT:")[1].strip()
		
	if "MINCOV:" in line:
		info = line.split(" ")
		mincov = info[0].strip()
		maxcov = info[1].strip()
		numtrig = info[2].strip()
		numrel = info[3].strip()
		defectInfo[defect] = (mincov, maxcov, numtrig, numrel)
	
	if "TARGET COVERAGE:20.0" in line:
		cov = 20
	if "TARGET COVERAGE:40.0" in line:
		cov = 40
	if "TARGET COVERAGE:60.0" in line:
		cov = 60
	if "TARGET COVERAGE:80.0" in line:
		cov = 80
	if "TARGET COVERAGE:100.0" in line:
		cov = 100
		
	if "normalized-cov:" in line:
		if cov < 100:
			dp += 1
		info = line.split(" ")
		nc = info[0].split("normalized-cov:")[1].strip()		
		ac = info[1].split("actual-cov:")[1].strip()
		numtests = info[2].split("sample-size:")[1].strip()
				
		if defect not in defectCoverages:	
			defectCoverages[defect] = [(cov,nc,ac,numtests)]
		else:
			existingEntries = defectCoverages[defect]
			existingEntries.append((cov,nc,ac,numtests))
			defectCoverages[defect] = existingEntries
	
	if "tests => " in line:
		tests = line.split("tests => ")[1]
		if defect not in defectTests:	
			defectTests[defect] = [(cov,tests)]
		else:
			existingEntries = defectTests[defect]
			existingEntries.append((cov,tests))
			defectTests[defect] = existingEntries

def getPosTests(defect, alltests, trigtests):
	posTests = []	
	for test in alltests:
		test = test.replace(defect + ":::", "").strip()
		if test not in trigtests:
			posTests.append(test)
	return posTests	

for defect in sorted(defectTests.keys()):
	info = defectTests[defect]
	if len(info)==5:
		negtestfilename = defect + "_neg.tests"
		negtestfile = open(negtestfilename, "w")
		trigtests = defectTrigTests[defect]
		for test in trigtests:
			test = test.replace("#", "::");
			negtestfile.write(test + "\n")
		negtestfile.close()

		for element in info:
			samplesize = len(trigtests)
			cov = element[0]
			alltests = element[1].replace("[","").replace("]","").strip().split(",")
			postests = getPosTests(defect, alltests, trigtests)		
			postestfilename = defect + "_" + str(cov) + "_" + sample + "_pos.tests"
			postestfile = open(postestfilename, "w") 
			samplesize += len(postests)
			for test in postests:
				test = test.replace("#", "::");
				postestfile.write(test + "\n")
			postestfile.close()
			
			print defect,";", cov, ";", samplesize
			
	else:
		print "COULDN'T SAMPLE FOR ALL DATAPOINTS FOR DEFECT: ", defect			

#for defect in sorted(defectInfo.keys()):
#	print defect, "###", defectdp[defect], "###", len(defectCoverages[defect]), "###",  defectInfo[defect] 
#	print defectInfo[defect] 
#	print defectCoverages[defect]
#	print defectTrigTests[defect]
#	print defectTests[defect]
#	print 
#	print 
