import sys

f = open(sys.argv[1])
c = 0
r1 = ""
r2 = ""
out = open("results.txt", "w")
out.write("project,defect,patch,totaltests,failingtests,passingtests,failpercentage,passpercentage\n")

#project,defect,patch,negtestcount,totaltests,failingtests,passingtests,failpercentage,passpercentage,technique

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
		totaltests1 = float(r1[4].strip())
		failingtests1 = float(r1[5].strip())
		passingtests1 = float(r1[6].strip())
	elif c%2 == 0:
		r2 = line.split(",")
		project2 = r2[0]
		defect2 = r2[1]
		patch2 = r2[2]
		totaltests2 = float(r2[4].strip())
		failingtests2 = float(r2[5].strip())
		passingtests2 = float(r2[6].strip())
	
		if project1 == project2 and defect1 == defect2 and patch1 == patch2:
			totaltests = totaltests1 + totaltests2
			failingtests = failingtests1 + failingtests2
			passingtests = passingtests1 + passingtests2
			failpercentage = (failingtests / totaltests) * 100.0
			passpercentage = (passingtests / totaltests) * 100.0
#			print("PASS:", passingtests, totaltests, passpercentage)
#			print("FAIL:", failingtests, totaltests, failpercentage)
			out.write(project2 + "," + defect2 + "," + patch2 + "," + str(totaltests) + "," + str(failingtests) + "," + str(passingtests) + "," + str(failpercentage) + "," + str(passpercentage) + "\n")
		else:	
			print "Consecutive duplicates not found!"
			print project1, project2, defect1, defect2, patch1, patch2
			break
		
