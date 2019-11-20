import sys

resultfile = sys.argv[1]
technique = ""
if "gp" in resultfile:
	technique = "GenProg"
elif "par" in resultfile:
	technique = "Par"
elif "trp" in resultfile:
	technique = "TrpAutoRepair"
elif "sim" in resultfile:
	technique = "SimFix"


f = open("triggering_test_results.csv", "w")
f.write("project,defect,patch,totaltests,failingtests,passingtests,failpercentage,passpercentage,negtestcount,normalizednegtestcount,technique\n")

defect_failingtests = {}
defect_failingtests["chart22"] = [1,2,3,4,6]
defect_failingtests["chart26"] = [4,8,13,17,22]
defect_failingtests["closure26"] = [1,2,4,5,7]
defect_failingtests["closure86"] = [1,2,4,5,7]
defect_failingtests["time3"] = [1,2,3,4,5]

for line in open(resultfile):
	if "project" in line:
		continue
	line1 = line.split(",")
	patch = line1[2]
	bug = patch.split("_")[0].strip()
	failingtestcount = int(patch.split("_")[1].strip())
	normalisedfailingtests = float(defect_failingtests[bug].index(failingtestcount) + 1)/5.0
	f.write(line.strip() + "," + str(failingtestcount) + "," + str(normalisedfailingtests) + "," + technique + "\n")	
f.close()
