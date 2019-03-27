import sys

resultfile = sys.argv[1]

if "gp" in resultfile:
	technique = "GenProg"
elif "par" in resultfile:
	technique = "Par"
elif "trp" in resultfile:
	technique = "TRPAutoRepair"


f = open("triggering_test_results.csv", "w")
f.write("project,defect,patch,totaltests,failingtests,passingtests,failpercentage,passpercentage,negtestcount,normalizednegtestcount,technique\n")


for line in open(resultfile):
	if "project" in line:
		continue
	line1 = line.split(",")
	patch = line1[2]
	failingtestcount = int(patch.split("_")[1].strip())
	normalisedfailingtests = -1
	if ("Closure" in line and failingtestcount==1) or ("Chart" in line and failingtestcount== 4):
		normalisedfailingtests = 0.2
	elif ("Closure" in line and failingtestcount==2) or ("Chart" in line and failingtestcount== 8):
		normalisedfailingtests = 0.4
	elif ("Closure" in line and failingtestcount==4) or ("Chart" in line and failingtestcount== 13):
		normalisedfailingtests = 0.6
	elif ("Closure" in line and failingtestcount==5) or ("Chart" in line and failingtestcount== 17):
		normalisedfailingtests = 0.8
	elif ("Closure" in line and failingtestcount==7) or ("Chart" in line and failingtestcount== 22):
		normalisedfailingtests = 1.0
	f.write(line.strip() + "," + str(failingtestcount) + "," + str(normalisedfailingtests) + "," + technique + "\n")	

f.close()
