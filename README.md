# JavaRepair-results
This repository contains the data and scripts to reproduce the results of the paper "Quality of Automated Program Repair on Real-World Defects".

- The __src__ directory contains the source code used for:  
  - patch-quality-assessment 	
  - repair-technique-execution 	
  - statistical-tests-execution
  - test-generation-and-sampling
- The __results__ directory contains the result files organized in terms of the following research questions:
  - RQ1: Do G&V techniques produce patches for real-world defects?
  - RQ2: How often and how much do the patches produced by G&V techniques overfit to the developer-written test suite and fail to generalize to the evaluation test suite, and thus ultimately to the program specification?
  - RQ3: How do the coverage and size of the test suite used to produce the patch affect patch quality?
  - RQ4: How does the number of tests that a buggy program fails affect the degree to which the generated patches overfit?
  - RQ5: How does the test suite provenance (whether it is written by developers or generated automatically) influence patch quality?
  - RQ6: Can overfitting be mitigated by exploiting randomness in the repair process? Do different random seeds overfit in different ways?
- The __test_suites__ directory contains the independely generated held-out test suites using EvoSuite version 3 optimizing the branch coverage criterion and using EvoSuite version 6 optimizing the line coverage criterion. 
- The __experiment_logs__ directory contains the logs generated while executing the repair techniques --- GenProg, Par, and TRPAutoRepair to address each of the research questions listed above. The logs are organized in terms of research questions. 
