import sys

f = open(sys.argv[1])
c = 0
r1 = ""
r2 = ""
out = open("results.csv", "w")
out.write("project,defect,patch,targetcov,realcov,samplesize,totaltests,failingtests,passingtests,failpercentage,passpercentage,technique\n")

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
		targetcov1 = r1[3]
		realcov1 = r1[4]
		samplesize1 = r1[5]
		totaltests1 = float(r1[6].strip())
		failingtests1 = float(r1[7].strip())
		passingtests1 = float(r1[8].strip())
		technique1 = r1[11].strip()
	elif c%2 == 0:
		r2 = line.split(",")
		project2 = r2[0]
		defect2 = r2[1]
		patch2 = r2[2]
		targetcov2 = r2[3]
		realcov2 = r2[4]
		samplesize2 = r2[5]
		totaltests2 = float(r2[6].strip())
		failingtests2 = float(r2[7].strip())
		passingtests2 = float(r2[8].strip())
		technique2 = r2[11].strip()
		if project1 == project2 and defect1 == defect2 and patch1 == patch2:
			totaltests = totaltests1 + totaltests2
			failingtests = failingtests1 + failingtests2
			passingtests = passingtests1 + passingtests2
			failpercentage = (failingtests / totaltests) * 100.0
			passpercentage = (passingtests / totaltests) * 100.0
			out.write(project2 + "," + defect2 + "," + patch2 + "," + targetcov2 + "," + realcov2 + "," + samplesize2 + "," + str(totaltests) + "," + str(failingtests) + "," + str(passingtests) + "," + str(failpercentage) + "," + str(passpercentage) + "," + technique2 + "\n")
		else:	
			print "Consecutive duplicates not found!"
			print project1, project2, defect1, defect2, patch1, patch2
			break
		
