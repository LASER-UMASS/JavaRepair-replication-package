# This script is similar to consolidate.py script, this is used to combine 
# patch quality scores of defective programs on held-out test suites 

import sys

defect = {}
filepath = sys.argv[1]
f = open(filepath)
totaltests = 0.0
totalfailingtests = 0.0
prevproject = ""
prevbug = ""
for line in f:
	record = line.split(",")
	if "Project" in record:
		continue
	project = record[0]
	bug = record[1]
	TSSeed = int(record[2].strip())
	NumberOfTests = float(record[3].strip())
	NumberOfFailingTests = float(record[4].strip())	
	if TSSeed == 1 and prevbug != "":
		if (prevproject,prevbug) not in defect:
			defect[(prevproject,prevbug)] = (totaltests, totalfailingtests, totaltests-totalfailingtests, float(totalfailingtests/totaltests)*100.0, float((totaltests-totalfailingtests)/totaltests)*100.0)
		totaltests = NumberOfTests
		totalfailingtests = NumberOfFailingTests
	else:
		totaltests += NumberOfTests
		totalfailingtests += NumberOfFailingTests
	if TSSeed == 10:
		prevproject = project
		prevbug = bug

# the last patch entry needs to be added at the end of the loop
if (project,bug) not in defect:
	defect[(project,bug)] = (totaltests, totalfailingtests, totaltests-totalfailingtests, float(totalfailingtests/totaltests)*100.0, float((totaltests-totalfailingtests)/totaltests)*100.0)

print("project,defect,totaltests,failingtests,passingtests,failpercentage,passpercentage")
for i in sorted(defect.keys()):
	outstr = i[0].title() + "," + i[1].title() + "," + str(defect[i][0]) + "," + str(defect[i][1]) + "," + str(defect[i][2]) + "," + str(defect[i][3]) + "," + str(defect[i][4])
	print(outstr)
