* `gp_rq2_overall.csv` shows the patch quality results (fraction of tests passed in held-out evaluation test suite) of GenProg-produced patches while attempting to repair 357 defects of Defects4J. 
* `par_rq2_overall.csv` shows the patch quality results of Par-produced patches while attempting to repair 357 defects of Defects4J. 
* `trp_rq2_overall.csv` shows the patch quality results of TRPAutoRepair-produced patches while attempting to repair 357 defects of Defects4J. 
* `defective_rq2_overall.csv` shows the patch quality results for the defective version of the program. 
 	compare-quality-with-defective.log 	
* `quality-stats-results.log` shows the patch quality statistics for each of the repair techniques and 
`gp_patchquality_subset.pdf, `par_patchquality_subset.pdf ,`trp_patchquality_subset.pdf show the plots 
generated for GenProg, Par, and TRPAutoRepair respectively. 

**This replicates results described in Figure 4 of the paper.**

* `compare-quality-with-defective.log` shows the results of patch quality improvement for each of the repair techniques 
when compared to the defective version of the program. The files `gp_quality_improvement_subset.pdf`, 
`par_quality_improvement_subset.pdf`, and `trp_quality_improvement_subset.pdf` show the change in patch quality 
between the defective version and patched version of the code for GenProg, Par, and TRPAutoRepair respectively.  	

**This replicates results described in Figure 5 of the paper.**
