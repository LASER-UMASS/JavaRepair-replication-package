# This script is similar to combineresults.py script. This is used to combine 
# the patch quality scores obtained using EvoSuite v3 and EvoSuite v6 for 
# the defective programs 

import sys

f = open(sys.argv[1])
r1 = ""
r2 = ""
defect_result = {}
out = open("results.csv", "w")
out.write("project,defect,totaltests,failingtests,passingtests,failpercentage,passpercentage\n")

for line in f:
	if "project" in line:
		continue	
	defect = line.split(",")[1].strip()
	
	if defect not in defect_result:
		defect_result[defect] = line.strip()
	else:
		r1 = defect_result[defect].split(",")
		project1 = r1[0]
		defect1 = r1[1]
		totaltests1 = float(r1[2].strip())
		failingtests1 = float(r1[3].strip())
		passingtests1 = float(r1[4].strip())

		r2 = line.split(",")
		project2 = r2[0]
		defect2 = r2[1]
		totaltests2 = float(r2[2].strip())
		failingtests2 = float(r2[3].strip())
		passingtests2 = float(r2[4].strip())
	
		if project1 == project2 and defect1 == defect2:
			totaltests = totaltests1 + totaltests2
			failingtests = failingtests1 + failingtests2
			passingtests = passingtests1 + passingtests2
			failpercentage = (failingtests / totaltests) * 100.0
			passpercentage = (passingtests / totaltests) * 100.0
			out.write(project2 + "," + defect2 + "," + str(totaltests) + "," + str(failingtests) + "," + str(passingtests) + "," + str(failpercentage) + "," + str(passpercentage) + "\n")
	
