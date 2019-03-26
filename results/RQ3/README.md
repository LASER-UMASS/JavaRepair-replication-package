The folder contains results produced for,

RQ3: How do the coverage and size of the test suite used to produce
the patch affect patch quality?

The **patches** folder contains the patches produced using 
the three repair techniques---GenProg, Par, and TRPAutoRepair
for the 45 defects of Defects4J dataset (listed in file `defects-RQ3.txt`) for which we could 
sample five test suites of varying code coverage.  

The **sampled-tests-coverage** contains the files listing positive tests (filename having `pos.tests`) 
and negative tests (filename having `neg.tests`)  sampled considering code coverage ration for the 45 defects.
