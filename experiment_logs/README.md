This directory contains the logs generated while executing the repair techniques---GenProg, Par, and TRPAutoRepair to address each of the research questions listed above. 
The logs are organized in terms of research questions.
  - RQ1: Do G&V techniques produce patches for real-world defects?
  - RQ2: How often and how much do the patches produced by G&V techniques overfit to the developer-written test suite and fail to generalize to the evaluation test suite, and thus ultimately to the program specification?
  - RQ3: How do the coverage and size of the test suite used to produce the patch affect patch quality?
  - RQ4: How does the number of tests that a buggy program fails affect the degree to which the generated patches overfit?
  - RQ5: How does the test suite provenance (whether it is written by developers or generated automatically) influence patch quality?
  
 For RQ1 and RQ2, we execute repair techniques on 357 Defects4J defects. 
 The directory __RQ1_RQ2__ contains the logs for the 68 defects which could be patched using at least one 
 of the three repair techniques.
 
 For RQ3, we execute repair techniques on 45 Defects4J defects for which we could sample test suites 
 using varying levels of code coverage and which could be patched by any of the repair techniques. 
 
 The directory __RQ3__ contains the logs for these defects organized in terms of the repair techniques. 
 
 For RQ4,  we execute repair techniques on 3 Defects4J defects for which we could sample test suites 
 using varying number of failing tests and which could be patched by any of the repair techniques. 
 
 The directory __RQ4__ contains the logs for these defects organized in terms of the repair techniques. 
 
 For RQ5, we execute repair techniques on 37 Defects4J defects for which the EvoSuite-generated test suite
 failed at least one test on the buggy version of the program. The EvoSuite-generated test suites are 
 used to guide the repair techniques in these experiments. As we cannot merge the test suites generated 
 using EvoSuite versions 3 and 6 (https://github.com/EvoSuite/evosuite/issues/128) we run separate experiments
 using both kinds of test suite. We then combine the patches using following approach. 
 For all the defects which are patched using either of the test suites, we consider all the patches of such defects
 and for the defects which could be patched using both of the test suites, we only consider the patches obtained 
 using EvoSuite version 6 test suite.  To evaluate the quality of the patches we do the following. 
 We evaluate the patch quality (fraction of tests passing) on the test suites generated using EvoSuite version 3 (ES v3) 
 and using EvoSuite version 4 (ES v4) separately and then combine the two results by adding the total tests 
 and failing (and passing) tests. For example, if a patch fails 2/10 tests in ES v3 test suite and 
 fails 3/15 tests in ES v6 test suite then the quality of that patch is (10 + 15 - 2 - 3)/(10 + 15) = 0.8 or 80%. 
 We would obtain the same patch quality results if we could merge the test suites. 
 
 The directory __RQ5__ contains the logs for these defects organized in terms of the repair techniques and EvoSuite versions. 
