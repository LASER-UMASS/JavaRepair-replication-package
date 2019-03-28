import sys

c = 0
r1 = ""
r2 = ""
out = open("results_incommon.txt", "w")
out.write("project,defect,patch,totaltests,failingtests,passingtests,failpercentage,passpercentage,provenance\n")

defects1 = []
defects2 = []

f1 = open(sys.argv[1])
for line in f1:
	if "project" in line:
		continue
	else:
		r1 = line.split(",")
		defect1 = r1[1]
		defects1.append(defect1)	
f1.close()

f2 = open(sys.argv[2])
for line in f2:
	if "project" in line:
		continue
	else:
		r2 = line.split(",")
		defect2 = r2[1]
		defects2.append(defect2)	
f2.close()	


commondefects = list(set(defects1) & set(defects2))

print(commondefects)
print(len(commondefects))

f1 = open(sys.argv[1])
for line in f1:
	if "project" in line:
		continue
	else:
		r1 = line.split(",")
		defect1 = r1[1]
		if defect1 in commondefects:
			out.write(line.strip() + ",developer\n")
f1.close()

f2 = open(sys.argv[2])
for line in f2:
	if "project" in line:
		continue
	else:
		r2 = line.split(",")
		defect2 = r2[1]
		if defect2 in commondefects:
			out.write(line.strip() + ",EvoSuite\n")
f2.close()
