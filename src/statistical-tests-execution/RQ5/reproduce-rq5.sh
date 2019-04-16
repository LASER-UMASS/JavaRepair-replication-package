#####################################
# PURPOSE: This is the driver script used to reproduce results for RQ5
# INPUT: path to directory containing patch quality assesment scores for RQ5 patches  (../../../results/RQ5/patch-quality-assessment/)
# OUTPUT: plots and results presented in paper
# CMD TO RUN: bash reproduce-rq5.sh ../../../results/RQ5/patch-quality-assessment/
# DEPENDENCIES: this script requires consolidate.py, combinepatches.py and combineresults.py scripts to pre-process input data,
#               and computeMannWhitney.R to run Mann-Whitney U test and generate boxplots
#####################################

ESPATH=$1

python consolidate.py $ESPATH/gp_rq5_es3_quality.csv > gp_rq5_es3_consolidated.csv 
python consolidate.py $ESPATH/gp_rq5_es6_quality.csv > gp_rq5_es6_consolidated.csv 
python combinepatches.py gp_rq5_es3_consolidated.csv gp_rq5_es6_consolidated.csv > gp_rq5_overall.csv
python combineresults.py gp_rq2_overall.csv gp_rq5_overall.csv 
mv results_incommon.txt gp_rq5_incommondefects.csv

python consolidate.py $ESPATH/trp_rq5_es3_quality.csv > trp_rq5_es3_consolidated.csv 
python consolidate.py $ESPATH/trp_rq5_es6_quality.csv > trp_rq5_es6_consolidated.csv 
python combinepatches.py trp_rq5_es3_consolidated.csv trp_rq5_es6_consolidated.csv > trp_rq5_overall.csv
python combineresults.py trp_rq2_overall.csv trp_rq5_overall.csv 
mv results_incommon.txt trp_rq5_incommondefects.csv

python consolidate.py $ESPATH/par_rq5_es3_quality.csv > par_rq5_es3_consolidated.csv 
python consolidate.py $ESPATH/par_rq5_es6_quality.csv > par_rq5_es6_consolidated.csv 
python combinepatches.py par_rq5_es3_consolidated.csv par_rq5_es6_consolidated.csv > par_rq5_overall.csv
python combineresults.py par_rq2_overall.csv par_rq5_overall.csv 
mv results_incommon.txt par_rq5_incommondefects.csv

Rscript repairability-stats.R
Rscript failing-test-distribution.R
Rscript quality-stats-boxplot.R

rm gp_rq5_es3_consolidated.csv
rm gp_rq5_es6_consolidated.csv
rm gp_rq5_overall.csv
rm gp_rq5_incommondefects.csv
rm trp_rq5_es3_consolidated.csv
rm trp_rq5_es6_consolidated.csv
rm trp_rq5_overall.csv
rm trp_rq5_incommondefects.csv
rm par_rq5_es3_consolidated.csv
rm par_rq5_es6_consolidated.csv
rm par_rq5_overall.csv
rm par_rq5_incommondefects.csv
