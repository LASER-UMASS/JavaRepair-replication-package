#####################################
# PURPOSE: This is the driver script used to reproduce results for RQ6
# INPUT: path to directory containing patch quality assesment scores for RQ6 patches  (../../../results/RQ6/patch-quality-assessment/)
# OUTPUT: plots and results presented in paper
# CMD TO RUN: bash reproduce-rq6.sh ../../../results/RQ6/patch-quality-assessment/
# DEPENDENCIES: this script requires consolidate.py, combineresults.py and combineresults.py scripts to pre-process input data,
#               and computeMannWhitney.R to run Mann-Whitney U test and generate boxplots
#####################################

DIRPATH=$1

python consolidate.py $DIRPATH/gp_rq2_es3_quality.csv > gp_rq2_es3_consolidated.csv 
python combineresults.py gp_rq2_es3_consolidated.csv $DIRPATH/gp_rq6_es3_quality.csv > gp_rq6_overall.csv

python consolidate.py $DIRPATH/par_rq2_es3_quality.csv > par_rq2_es3_consolidated.csv 
python combineresults.py par_rq2_es3_consolidated.csv $DIRPATH/par_rq6_es3_quality.csv > par_rq6_overall.csv

python consolidate.py $DIRPATH/trp_rq2_es3_quality.csv > trp_rq2_es3_consolidated.csv 
python combineresults.py trp_rq2_es3_consolidated.csv $DIRPATH/trp_rq6_es3_quality.csv > trp_rq6_overall.csv


Rscript run-utest-generate-boxplots.R
Rscript quality-stats.R

rm gp_rq2_es3_consolidated.csv
rm gp_rq6_overall.csv
rm trp_rq2_es3_consolidated.csv
rm trp_rq6_overall.csv
rm par_rq2_es3_consolidated.csv
rm par_rq6_overall.csv
