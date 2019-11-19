import sys

#patches = []
evaluatedpatches = []
#f = open("patches_gp_rq2.txt")
#for line in f:
#	patches.append(line.strip())

defect = {}
filepath = sys.argv[1]		# file generated using Mau's script to evaluate quality on each sub suite
technique = int(sys.argv[2]) 	# input 1 GenProg, 2 PAR, 3 TrpAutoRepair, 4 SimFix
techname = ""
if technique == 1:
	techname = "GenProg"
elif technique == 2:
	techname = "PAR"
elif technique == 3:
	techname = "TrpAutoRepair"
elif technique == 4:
	techname = "SimFix"

f = open(filepath)
totaltests = 0.0
totalfailingtests = 0.0
prevproject = ""
prevbug = ""
prevpatch = ""
prevtargetcov = ""
prevrealcov = ""
patchcount = 0
prevdatapoint= ""

#Project,Bug,Patch,TSSeed,NumberOfTests,NumberOfFailingTests,TargetCoverage,RealCoverage,SampleSize
for line in f:
	record = line.split(",")
	if "Project" in record:
		continue
	project = record[0]
	bug = record[1]
	datapoint = ""
	if "seed" in line:
		datapoint = record[2].split("_seed")[0]
	else:
                datapoint = '_'.join(record[2].split(".")[0].split("_")[:-1])
	patch = record[2]
	TSSeed = int(record[3].strip())
	NumberOfTests = float(record[4].strip())
	NumberOfFailingTests = float(record[5].strip())	
	targetCov = record[6].strip()
	realCov = record[7].strip()
	size = record[8].strip()
	if TSSeed == 1 and prevpatch != "":
		patchcount += 1
		if (prevproject,prevbug,prevdatapoint,prevpatch,prevtargetcov, prevrealcov, prevsize) not in defect:
			defect[(prevproject,prevbug,prevdatapoint,prevpatch,prevtargetcov,prevrealcov,prevsize)] = (totaltests, totalfailingtests, totaltests-totalfailingtests, float(totalfailingtests/totaltests)*100.0, float((totaltests-totalfailingtests)/totaltests)*100.0)
			evaluatedpatches.append(prevpatch)
		totaltests = NumberOfTests
		totalfailingtests = NumberOfFailingTests
	else:
		totaltests += NumberOfTests
		totalfailingtests += NumberOfFailingTests
	if TSSeed == 10:
		prevpatch = patch
		prevproject = project
		prevbug = bug
		prevtargetcov = targetCov
		prevrealcov = realCov
		prevdatapoint = datapoint
		prevsize = size

# the last patch entry needs to be added at the end of the loop
if (project,bug,datapoint,patch,targetCov,realCov,size) not in defect:
	defect[(project,bug,datapoint,patch,targetCov,realCov,size)] = (totaltests, totalfailingtests, totaltests-totalfailingtests, float(totalfailingtests/totaltests)*100.0, float((totaltests-totalfailingtests)/totaltests)*100.0)
	evaluatedpatches.append(prevpatch)

print "project,defect,patch,targetcov,realcov,samplesize,totaltests,failingtests,passingtests,failpercentage,passpercentage,technique" 
for i in sorted(defect.keys()):
	outstr = i[0] + "," + i[0] + i[1] + "," + i[3] + "," + i[4] + "," + i[5] + ","  + i[6] + "," + str(defect[i][0]) + "," + str(defect[i][1]) + "," + str(defect[i][2]) + "," + str(defect[i][3]) + "," + str(defect[i][4]) + "," + techname
	print outstr
