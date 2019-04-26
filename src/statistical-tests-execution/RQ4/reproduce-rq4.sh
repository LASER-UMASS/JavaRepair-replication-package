#####################################
# PURPOSE: This is the driver script used to generate results for RQ4
# INPUT: path to directory containing patch quality assesment scores for RQ4 patches  (../../../results/RQ4/patch-quality-assessment/)
# OUTPUT: plots and results presented in paper
# CMD TO RUN: bash reproduce-rq4.sh ../../../results/RQ4/patch-quality-assessment/
# DEPENDENCIES: this script requires consolidate.py and combineresults.py scripts to pre-process input data,
#               and freq-distribution.R and computePearson.R to generate the plots
#####################################

DIRPATH=$1

python consolidate.py $DIRPATH/gp_rq4_es3_quality.csv 1 > gp_rq4_es3_consolidated.csv 
python consolidate.py $DIRPATH/gp_rq4_es6_quality.csv 1 > gp_rq4_es6_consolidated.csv 
cat gp_rq4_es3_consolidated.csv > gp_rq4_es3_es6_consolidated.csv
cat gp_rq4_es6_consolidated.csv >> gp_rq4_es3_es6_consolidated.csv
sort gp_rq4_es3_es6_consolidated.csv > gp_rq4_es3_es6_consolidated_sorted.csv
python combineresults.py gp_rq4_es3_es6_consolidated_sorted.csv
mv results.txt gp_rq4_overall.csv
python addFailingTest.py gp_rq4_overall.csv 
mv triggering_test_results.csv gp_rq4_overall_failingtests.csv 
rm gp_rq4_es3_consolidated.csv
rm gp_rq4_es6_consolidated.csv
rm gp_rq4_es3_es6_consolidated.csv
rm gp_rq4_es3_es6_consolidated_sorted.csv

python consolidate.py $DIRPATH/par_rq4_es3_quality.csv 2 > par_rq4_es3_consolidated.csv 
python consolidate.py $DIRPATH/par_rq4_es6_quality.csv 2 > par_rq4_es6_consolidated.csv 
cat par_rq4_es3_consolidated.csv > par_rq4_es3_es6_consolidated.csv
cat par_rq4_es6_consolidated.csv >> par_rq4_es3_es6_consolidated.csv
sort par_rq4_es3_es6_consolidated.csv > par_rq4_es3_es6_consolidated_sorted.csv
python combineresults.py par_rq4_es3_es6_consolidated_sorted.csv
mv results.txt par_rq4_overall.csv
python addFailingTest.py par_rq4_overall.csv 
mv triggering_test_results.csv par_rq4_overall_failingtests.csv 
rm par_rq4_es3_consolidated.csv
rm par_rq4_es6_consolidated.csv
rm par_rq4_es3_es6_consolidated.csv
rm par_rq4_es3_es6_consolidated_sorted.csv

python consolidate.py $DIRPATH/trp_rq4_es3_quality.csv 3 > trp_rq4_es3_consolidated.csv 
python consolidate.py $DIRPATH/trp_rq4_es6_quality.csv 3 > trp_rq4_es6_consolidated.csv 
cat trp_rq4_es3_consolidated.csv > trp_rq4_es3_es6_consolidated.csv
cat trp_rq4_es6_consolidated.csv >> trp_rq4_es3_es6_consolidated.csv
sort trp_rq4_es3_es6_consolidated.csv > trp_rq4_es3_es6_consolidated_sorted.csv
python combineresults.py trp_rq4_es3_es6_consolidated_sorted.csv
mv results.txt trp_rq4_overall.csv
python addFailingTest.py trp_rq4_overall.csv
mv triggering_test_results.csv trp_rq4_overall_failingtests.csv
rm trp_rq4_es3_consolidated.csv
rm trp_rq4_es6_consolidated.csv
rm trp_rq4_es3_es6_consolidated.csv
rm trp_rq4_es3_es6_consolidated_sorted.csv

cat gp_rq4_overall_failingtests.csv > rq4_results.csv
tail --lines=+2 par_rq4_overall_failingtests.csv >> rq4_results.csv
tail --lines=+2 trp_rq4_overall_failingtests.csv >> rq4_results.csv
rm gp_rq4_overall.csv
rm par_rq4_overall.csv
rm trp_rq4_overall.csv

Rscript computePearson.R
Rscript freq-distribution.R 
