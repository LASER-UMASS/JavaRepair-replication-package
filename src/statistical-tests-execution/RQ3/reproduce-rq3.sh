#####################################
# PURPOSE: This is the driver script used to generate results for RQ3
# INPUT: path to directory containing patch quality assesment scores for RQ3 patches  (../../../results/RQ3/patch-quality-assessment/)
# OUTPUT: plots and results presented in paper
# CMD TO RUN: bash reproduce-rq3.sh ../../../results/RQ3/patch-quality-assessment/
# DEPENDENCIES: this script requires SampledCoverage.csv, addCoverage.py, and combineresults.py scripts to pre-process input data,
#		and quality-stats.R and compare-quality-with-defective.R to generate the plots
#####################################

DIRPATH=$1

python addCoverage.py $DIRPATH/gp_rq3_es3_quality.csv SampledCoverage.csv
python addCoverage.py $DIRPATH/gp_rq3_es6_quality.csv SampledCoverage.csv
python consolidate.py gp_rq3_es3_quality_coverage.csv 1 > gp_rq3_es3_consolidated.csv
python consolidate.py gp_rq3_es6_quality_coverage.csv 1 > gp_rq3_es6_consolidated.csv
cat gp_rq3_es3_consolidated.csv > gp_rq3_es3_es6_consolidated.csv
cat gp_rq3_es6_consolidated.csv >> gp_rq3_es3_es6_consolidated.csv
sort gp_rq3_es3_es6_consolidated.csv > gp_rq3_es3_es6_consolidated_sorted.csv
python combineresults.py gp_rq3_es3_es6_consolidated_sorted.csv
mv results.csv gp_rq3_overall.csv
rm gp_rq3_es3_quality_coverage.csv
rm gp_rq3_es6_quality_coverage.csv
rm gp_rq3_es3_consolidated.csv
rm gp_rq3_es6_consolidated.csv
rm gp_rq3_es3_es6_consolidated.csv
rm gp_rq3_es3_es6_consolidated_sorted.csv

python addCoverage.py $DIRPATH/trp_rq3_es3_quality.csv SampledCoverage.csv
python addCoverage.py $DIRPATH/trp_rq3_es6_quality.csv SampledCoverage.csv
python consolidate.py trp_rq3_es3_quality_coverage.csv 3 > trp_rq3_es3_consolidated.csv
python consolidate.py trp_rq3_es6_quality_coverage.csv 3 > trp_rq3_es6_consolidated.csv
cat trp_rq3_es3_consolidated.csv > trp_rq3_es3_es6_consolidated.csv
cat trp_rq3_es6_consolidated.csv >> trp_rq3_es3_es6_consolidated.csv
sort trp_rq3_es3_es6_consolidated.csv > trp_rq3_es3_es6_consolidated_sorted.csv
python combineresults.py trp_rq3_es3_es6_consolidated_sorted.csv
mv results.csv trp_rq3_overall.csv
rm trp_rq3_es3_quality_coverage.csv
rm trp_rq3_es6_quality_coverage.csv
rm trp_rq3_es3_consolidated.csv
rm trp_rq3_es6_consolidated.csv
rm trp_rq3_es3_es6_consolidated.csv
rm trp_rq3_es3_es6_consolidated_sorted.csv

python addCoverage.py $DIRPATH/par_rq3_es3_quality.csv SampledCoverage.csv
python addCoverage.py $DIRPATH/par_rq3_es6_quality.csv SampledCoverage.csv
python consolidate.py par_rq3_es3_quality_coverage.csv 2 > par_rq3_es3_consolidated.csv
python consolidate.py par_rq3_es6_quality_coverage.csv 2 > par_rq3_es6_consolidated.csv
cat par_rq3_es3_consolidated.csv > par_rq3_es3_es6_consolidated.csv
cat par_rq3_es6_consolidated.csv >> par_rq3_es3_es6_consolidated.csv
sort par_rq3_es3_es6_consolidated.csv > par_rq3_es3_es6_consolidated_sorted.csv
python combineresults.py par_rq3_es3_es6_consolidated_sorted.csv
mv results.csv par_rq3_overall.csv
rm par_rq3_es3_quality_coverage.csv
rm par_rq3_es6_quality_coverage.csv
rm par_rq3_es3_consolidated.csv
rm par_rq3_es6_consolidated.csv
rm par_rq3_es3_es6_consolidated.csv
rm par_rq3_es3_es6_consolidated_sorted.csv

python addCoverage.py $DIRPATH/sim_rq3_es3_quality.csv SampledCoverage.csv
python addCoverage.py $DIRPATH/sim_rq3_es6_quality.csv SampledCoverage.csv
python consolidate.py sim_rq3_es3_quality_coverage.csv 4 > sim_rq3_es3_consolidated.csv
python consolidate.py sim_rq3_es6_quality_coverage.csv 4 > sim_rq3_es6_consolidated.csv
cat sim_rq3_es3_consolidated.csv > sim_rq3_es3_es6_consolidated.csv
cat sim_rq3_es6_consolidated.csv >> sim_rq3_es3_es6_consolidated.csv
sort sim_rq3_es3_es6_consolidated.csv > sim_rq3_es3_es6_consolidated_sorted.csv
python combineresults.py sim_rq3_es3_es6_consolidated_sorted.csv
mv results.csv sim_rq3_overall.csv
rm sim_rq3_es3_quality_coverage.csv
rm sim_rq3_es6_quality_coverage.csv
rm sim_rq3_es3_consolidated.csv
rm sim_rq3_es6_consolidated.csv
rm sim_rq3_es3_es6_consolidated.csv
rm sim_rq3_es3_es6_consolidated_sorted.csv


Rscript freq-distribution.R
Rscript computeMLR.R
