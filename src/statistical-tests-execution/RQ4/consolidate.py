import sys

#patches = []
evaluatedpatches = []
#f = open("patches_gp_rq2.txt")
#for line in f:
#	patches.append(line.strip())

defect = {}
filepath = sys.argv[1]
technique = sys.argv[2]
f = open(filepath)
totaltests = 0.0
totalfailingtests = 0.0
prevproject = ""
prevbug = ""
prevpatch = ""
prevnegtestcount = ""
patchcount = 0
for line in f:
	record = line.split(",")
	if "Project" in record:
		continue
	project = record[0]
	bug = record[1]
	patch = record[2]
	negtestcount = patch.split("_")[1].strip()
	TSSeed = int(record[3].strip())
	NumberOfTests = float(record[4].strip())
	NumberOfFailingTests = float(record[5].strip())	
	if TSSeed == 1 and prevpatch != "":
		patchcount += 1
		if (prevproject,prevbug,prevpatch,prevnegtestcount) not in defect:
			defect[(prevproject,prevbug,prevpatch,prevnegtestcount)] = (totaltests, totalfailingtests, totaltests-totalfailingtests, float(totalfailingtests/totaltests)*100.0, float((totaltests-totalfailingtests)/totaltests)*100.0)
			evaluatedpatches.append(prevpatch)
		
		totaltests = NumberOfTests
		totalfailingtests = NumberOfFailingTests
	else:
		totaltests += NumberOfTests
		totalfailingtests += NumberOfFailingTests
	if TSSeed == 10:
		prevproject = project
		prevbug = bug
		prevpatch = patch
		prevnegtestcount = negtestcount

# the last patch entry needs to be added at the end of the loop
if (project,bug,prevpatch,negtestcount) not in defect:
	defect[(project,bug,prevpatch,negtestcount)] = (totaltests, totalfailingtests, totaltests-totalfailingtests, float(totalfailingtests/totaltests)*100.0, float((totaltests-totalfailingtests)/totaltests)*100.0)
	evaluatedpatches.append(prevpatch)

print "project,defect,patch,negtestcount,totaltests,failingtests,passingtests,failpercentage,passpercentage,technique" 
for i in sorted(defect.keys()):
	outstr = i[0] + "," + i[0] + i[1] + "," + i[2] + "," + i[3] + "," + str(defect[i][0]) + "," + str(defect[i][1]) + "," + str(defect[i][2]) + "," + str(defect[i][3]) + "," + str(defect[i][4]) + "," + technique
	print outstr
