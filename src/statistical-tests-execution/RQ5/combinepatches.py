import sys

es3_patchfile = open(sys.argv[1])
es6_patchfile = open(sys.argv[2])


#project,defect,patch,totaltests,failingtests,passingtests,failpercentage,passpercentage

defects = set()

for line in es6_patchfile:
	print line.strip()
	defect = line.split(",")[1].strip()
	if defect not in defects:
		defects.add(defect)


for line in es3_patchfile:
	if "project" in line or line.split(",")[1].strip() in defects:
		continue
	print line.strip()
