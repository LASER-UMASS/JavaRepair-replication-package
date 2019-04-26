This folder contains scripts used to evaluate the quality of the patches produced by repair techniques using held-out test suites

To get the coverage of the desired test suites: 
Per each version of Evosuite (3 and 6):
Run first the script getCoverage.py with all 10 seeds, then mergeSeveralSeedsCovFiles.sh and then methodCoverageFromMergedXML.py
Finally, to merge the coverage reports from both versions:
Run mergeSE3andSE6CovFiles.sh, and then methodCoverageFromMergedXML.py

To get the evaluation of the test suites use the script evaluateGeneratedPatchesIn10SubTestSuites.py
