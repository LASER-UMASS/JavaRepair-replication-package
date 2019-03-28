This folder contains the patches produced by repair techniques--GenProg, Par, and TRPAutoRepair
using test suites generated using EvoSuite. 

We use two versions of EvoSuite (versions 3 and 6) along with specifiying different coverage criterion 
(branch coverage for EvoSuite version 3 and line coverage for EvoSuite version 6) to generate 
independent tests. 

We run repair techniques for the defects for which the generated test suite has at least one 
test that fails on the buggy version of the program. This gives us a dataset of 37 defects 
(out of the 68 defects which could be patched using at least one repair technique).

