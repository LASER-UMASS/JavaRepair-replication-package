`RQ5-results.log` contains (a) the statistics about defects patched and generated patches,
(b) the statistics about the patch quality for each provenance, and (c) the Mann-Whitney U test
results comparing the patch quality obtained using different provenance for each of the three repair techniques. 

`provenance_developer_failingtestsdistribution.pdf` and `provenance_evosuite_failingtestsdistribution.pdf`
show the distribution of failing tests in developer-written and EvoSuite-generated tests respectively 
for the 37 defects used for this experiment 

`gp_provenance_boxplot.pdf`, `par_provenance_boxplot.pdf`, and `trp_provenance_boxplot.pdf` show the boxplots
comparing the quality of patches produced for commonly patched defects by GenProg, Par, and TRPAutoRepair respectively. 

**This replicates results described in Figure 8 of the paper.**
