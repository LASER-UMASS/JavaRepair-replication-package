import sys

defect = {}
filepath = sys.argv[1]
f = open(filepath)
for line in f:
	record = line.split(",")
	if "Project" in record:
		continue
	project = record[0]
	bug = record[1]
	patch = record[2]
	totaltests = float(record[3].strip())
	totalfailingtests = float(record[4].strip())	
	if (project,bug,patch) not in defect:
		defect[(project,bug,patch)] = (totaltests, totalfailingtests, totaltests-totalfailingtests, float(totalfailingtests/totaltests)*100.0, float((totaltests-totalfailingtests)/totaltests)*100.0)

if (project,bug,patch) not in defect:
	defect[(project,bug,patch)] = (totaltests, totalfailingtests, totaltests-totalfailingtests, float(totalfailingtests/totaltests)*100.0, float((totaltests-totalfailingtests)/totaltests)*100.0)
print "project,defect,patch,totaltests,failingtests,passingtests,failpercentage,passpercentage"
for i in sorted(defect.keys()):
	outstr = i[0] + "," + i[0] + i[1] + "," + i[2] + "," + str(defect[i][0]) + "," + str(defect[i][1]) + "," + str(defect[i][2]) + "," + str(defect[i][3]) + "," +  str(defect[i][4])
	print outstr
