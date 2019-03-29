#####################################
# PURPOSE:    This is a helper script used to combine the consolidated patch quality results 
#	      obtained using two version of EvoSuite. This script combines the results by
#	      adding the #failing tests and the total #tests and recomputing the patch quality score
# INPUT:      A csv file that contains patch quality results obtained using EvoSuite v3 and v6
# OUTPUT:     results.csv - a file that contains the combined patch quality results
# CMD TO RUN: python combineresults.py gp_rq1_es3_es6_consolidated_sorted.csv 
#####################################
import sys

f = open(sys.argv[1])
c = 0
r1 = ""
r2 = ""
out = open("results.csv", "w")
out.write("project,defect,patch,totaltests,failingtests,passingtests,failpercentage,passpercentage\n")

for line in f:
	if "project" in line:
		continue
	else:
		c += 1
	if c%2 != 0:
		r1 = line.split(",")
		project1 = r1[0]
		defect1 = r1[1]
		patch1 = r1[2]
		totaltests1 = float(r1[3].strip())
		failingtests1 = float(r1[4].strip())
		passingtests1 = float(r1[5].strip())
	elif c%2 == 0:
		r2 = line.split(",")
		project2 = r2[0]
		defect2 = r2[1]
		patch2 = r2[2]
		totaltests2 = float(r2[3].strip())
		failingtests2 = float(r2[4].strip())
		passingtests2 = float(r2[5].strip())
	
		if project1 == project2 and defect1 == defect2 and patch1 == patch2:
			totaltests = totaltests1 + totaltests2
			failingtests = failingtests1 + failingtests2
			passingtests = passingtests1 + passingtests2
			failpercentage = (failingtests / totaltests) * 100.0
			passpercentage = (passingtests / totaltests) * 100.0
			out.write(project2 + "," + defect2 + "," + patch2 + "," + str(totaltests) + "," + str(failingtests) + "," + str(passingtests) + "," + str(failpercentage) + "," + str(passpercentage) + "\n")
		else:	
			print("Consecutive duplicates not found!")
			print(project1, project2, defect1, defect2, patch1, patch2)
			break
		
