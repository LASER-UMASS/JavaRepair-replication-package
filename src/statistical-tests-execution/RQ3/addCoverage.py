import sys

resultfile = sys.argv[1]
coveragefile = sys.argv[2]
defectCoverage = {}
fc = open(coveragefile)
for line in fc:
	row = line.split("\t") # defect  mincov  maxcov  targetcov       normcov actualcov       numnegtests     numpostests     samplesize      sampledtests
	defect = str(row[0].split("Buggy")[0]).lower()
        targetCov = row[3]
	actualCov = row[5]
	sampleSize = row[8]
        if defect + "_" + targetCov not in defectCoverage:
		defectCoverage[defect + "_" + targetCov] = (targetCov.split("_")[0].strip(), actualCov.strip(), sampleSize.strip())	
fc.close()

outputfile = resultfile.split("/")[-1].split(".")[0] + "_coverage.csv"

fo = open(outputfile, "w")
outstr = "Project,Bug,Patch,TSSeed,NumberOfTests,NumberOfFailingTests,TargetCoverage,RealCoverage,SampleSize\n"
fo.write(outstr)	

fr = open(resultfile)
for line in fr:
	if "Patch" in line:
		continue
	row = line.split(",") # Project,Bug,Patch,TSSeed,NumberOfTests,NumberOfFailingTests
	defect = ""
	if "seed" in line:
		defect = row[2].split("_seed")[0]
	else:
		defect = '_'.join(row[2].split(".")[0].split("_")[:-1])
	
	targetcov = defectCoverage[defect][0]
	realcov = defectCoverage[defect][1]
	samplesize = defectCoverage[defect][2]
	outstr = line.strip() + "," + targetcov + "," + realcov + "," + samplesize + "\n"
	fo.write(outstr)

fr.close()
fo.close()	
