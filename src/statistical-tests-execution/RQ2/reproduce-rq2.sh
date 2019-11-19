#####################################
# PURPOSE: This is the driver script used to generate results for RQ2
# INPUT: path to directory containing patch quality assesment scores for RQ2 patches  (../../../results/RQ2/patch-quality-assessment/)
# OUTPUT: plots and results presented in paper
# CMD TO RUN: bash reproduce-rq2.sh ../../../results/RQ2/patch-quality-assessment/
# NOTE: this depends on consolidate.py and combineresults.py scripts to pre-process input data,
#	and on quality-stats.R and compare-quality-with-defective.R to generate the plots
#####################################

DIRPATH=$1

python consolidate.py $DIRPATH/gp_rq2_es3_quality.csv > gp_rq2_es3_consolidated.csv 
python consolidate.py $DIRPATH/gp_rq2_es6_quality.csv > gp_rq2_es6_consolidated.csv 
cat gp_rq2_es3_consolidated.csv > gp_rq2_es3_es6_consolidated.csv
cat gp_rq2_es6_consolidated.csv >> gp_rq2_es3_es6_consolidated.csv
sort gp_rq2_es3_es6_consolidated.csv > gp_rq2_es3_es6_consolidated_sorted.csv
python combineresults.py gp_rq2_es3_es6_consolidated_sorted.csv
mv results.csv gp_rq2_overall.csv
rm gp_rq2_es3_consolidated.csv
rm gp_rq2_es6_consolidated.csv
rm gp_rq2_es3_es6_consolidated.csv
rm gp_rq2_es3_es6_consolidated_sorted.csv

python consolidate.py $DIRPATH/trp_rq2_es3_quality.csv > trp_rq2_es3_consolidated.csv 
python consolidate.py $DIRPATH/trp_rq2_es6_quality.csv > trp_rq2_es6_consolidated.csv 
cat trp_rq2_es3_consolidated.csv > trp_rq2_es3_es6_consolidated.csv
cat trp_rq2_es6_consolidated.csv >> trp_rq2_es3_es6_consolidated.csv
sort trp_rq2_es3_es6_consolidated.csv > trp_rq2_es3_es6_consolidated_sorted.csv
python combineresults.py trp_rq2_es3_es6_consolidated_sorted.csv
mv results.csv trp_rq2_overall.csv
rm trp_rq2_es3_consolidated.csv
rm trp_rq2_es6_consolidated.csv
rm trp_rq2_es3_es6_consolidated.csv
rm trp_rq2_es3_es6_consolidated_sorted.csv

python consolidate.py $DIRPATH/par_rq2_es3_quality.csv > par_rq2_es3_consolidated.csv 
python consolidate.py $DIRPATH/par_rq2_es6_quality.csv > par_rq2_es6_consolidated.csv 
cat par_rq2_es3_consolidated.csv > par_rq2_es3_es6_consolidated.csv
cat par_rq2_es6_consolidated.csv >> par_rq2_es3_es6_consolidated.csv
sort par_rq2_es3_es6_consolidated.csv > par_rq2_es3_es6_consolidated_sorted.csv
python combineresults.py par_rq2_es3_es6_consolidated_sorted.csv
mv results.csv par_rq2_overall.csv
rm par_rq2_es3_consolidated.csv
rm par_rq2_es6_consolidated.csv
rm par_rq2_es3_es6_consolidated.csv
rm par_rq2_es3_es6_consolidated_sorted.csv

python consolidate.py $DIRPATH/sim_rq2_es3_quality.csv > sim_rq2_es3_consolidated.csv 
python consolidate.py $DIRPATH/sim_rq2_es6_quality.csv > sim_rq2_es6_consolidated.csv 
cat sim_rq2_es3_consolidated.csv > sim_rq2_es3_es6_consolidated.csv
cat sim_rq2_es6_consolidated.csv >> sim_rq2_es3_es6_consolidated.csv
sort sim_rq2_es3_es6_consolidated.csv > sim_rq2_es3_es6_consolidated_sorted.csv
python combineresults.py sim_rq2_es3_es6_consolidated_sorted.csv
mv results.csv sim_rq2_overall.csv
rm sim_rq2_es3_consolidated.csv
rm sim_rq2_es6_consolidated.csv
rm sim_rq2_es3_es6_consolidated.csv
rm sim_rq2_es3_es6_consolidated_sorted.csv

python consolidate-defective.py $DIRPATH/defective_rq2_es3_quality.csv > defective_rq2_es3_consolidated.csv 
python consolidate-defective.py $DIRPATH/defective_rq2_es6_quality.csv > defective_rq2_es6_consolidated.csv 
cat defective_rq2_es3_consolidated.csv > defective_rq2_es3_es6_consolidated.csv
cat defective_rq2_es6_consolidated.csv >> defective_rq2_es3_es6_consolidated.csv
sort defective_rq2_es3_es6_consolidated.csv > defective_rq2_es3_es6_consolidated_sorted.csv
python combineresults-defective.py defective_rq2_es3_es6_consolidated_sorted.csv
mv results.csv defective_rq2_overall.csv
rm defective_rq2_es3_consolidated.csv
rm defective_rq2_es6_consolidated.csv
rm defective_rq2_es3_es6_consolidated.csv
rm defective_rq2_es3_es6_consolidated_sorted.csv

Rscript quality-stats.R
Rscript compare-quality-with-defective.R

#rm gp_rq2_overall.csv
#rm par_rq2_overall.csv
#rm trp_rq2_overall.csv
#rm sim_rq2_overall.csv
#rm defective_rq2_overall.csv


