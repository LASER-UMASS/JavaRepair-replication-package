import sys


allpatchresults = open(sys.argv[1])
nversionresults = open(sys.argv[2])

technique = ""

if "gp" in sys.argv[1]:
	technique = "GenProg"
elif "par" in sys.argv[1]:
	technique = "Par"
elif "trp" in sys.argv[1]:
	technique = "TRPAutoRepair"

print "project,defect,patch,totaltests,failingtests,passingtests,failpercentage,passpercentage,approach"

defects = set()

for line in nversionresults:
	# Bug,TotalTestCases,FailedTestCases,GenProg(n-version)
	if "Bug" in line:
		continue		
	defect = line.split(",")[0].strip()
	if defect not in defects:
		defects.add(defect)

for line in allpatchresults:
	if "project" in line: 
		continue
	defect = line.split(",")[1].strip()
	if defect in defects:
		print line.strip() + "," + technique


nversionresults = open(sys.argv[2])
for line in nversionresults:
	# Bug,TotalTestCases,FailedTestCases,GenProg(n-version)
	if "Bug" in line:
		continue	
	record = line.split(",")
	defect = record[0].strip()
	project = ""
	if "Chart" in defect:
		project = "Chart"
	elif "Closure" in defect:
		project = "Closure"
	elif "Lang" in defect:
		project = "Lang"
	elif "Math" in defect:
		project = "Math"
	elif "Time" in defect:
		project = "Time"

	totaltests = float(record[1].strip())
	failingtests = float(record[2].strip())
	passingtests = totaltests - failingtests
	failpercentage = failingtests/totaltests * 100.0 
	passpercentage = passingtests/totaltests * 100.0 

	print project + "," + defect + "," + "," + str(totaltests) + "," + str(failingtests) + "," + str(passingtests) + "," + str(failpercentage) + "," + str(passpercentage) + "," + technique + "(n-version)"
