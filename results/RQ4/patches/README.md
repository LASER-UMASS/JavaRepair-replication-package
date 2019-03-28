This folder contains the patches produced by repair techniques--GenProg, Par, and TRPAutoRepair
using test suites that have varying number of failing tests. 

Only 3 out of 68 defects which could be fixed using any of these techniques 
have sufficient number (>5) of failing tests to perform this experiment hence, 
we run this experiment only for those defects (Chart 26 Closure 86, and Closure 115). 

For each defect, we have 5 data-points uniformly distributed between 1 and #failing tests
and for each data-point we have 5 sets of failing tests sampled randomly. Following are 
the details of data-points for each defect. 

- Chart 26, total #failing tests = 22, data-points = 4, 8, 13, 17, 22
- Closure 86, total #failing tests = 7, data-points = 1, 2, 4, 5, 7
- Closure 115, total #failing tests = 7, data-points = 1, 2, 4, 5, 7
