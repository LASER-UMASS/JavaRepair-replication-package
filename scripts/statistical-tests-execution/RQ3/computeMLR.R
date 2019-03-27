# script to compute Multi Linear Regression (MLR) to identify 
# the affect of test suite coverage and test suite size on 
# the patch quality

gp_rq3_all <- read.csv(file="gp_rq3_overall.csv", head=TRUE, sep=",", stringsAsFactors=FALSE)
trp_rq3_all <- read.csv(file="trp_rq3_overall.csv", head=TRUE, sep=",", stringsAsFactors=FALSE)
par_rq3_all <- read.csv(file="par_rq3_overall.csv", head=TRUE, sep=",", stringsAsFactors=FALSE)
eval_defects <- read.csv(file = "../evaluation-defects.txt")

## comment following block of code to consider all defects and remove _all from above 3 variables
evaldefectsgp <- intersect(gp_rq3_all$defect, eval_defects$defect)
evaldefectspar <- intersect(par_rq3_all$defect, eval_defects$defect)
evaldefectstrp <- intersect(trp_rq3_all$defect, eval_defects$defect)
gp_rq3 <- subset(gp_rq3_all, gp_rq3_all$defect%in%evaldefectsgp == TRUE)
par_rq3 <- subset(par_rq3_all, par_rq3_all$defect%in%evaldefectspar == TRUE)
trp_rq3 <- subset(trp_rq3_all, trp_rq3_all$defect%in%evaldefectstrp == TRUE)
###############################################################

gp_rq3_data <- gp_rq3[,c(5,6,11)]
par_rq3_data <- par_rq3[,c(5,6,11)]
trp_rq3_data <- trp_rq3[,c(5,6,11)]

names(gp_rq3_data) <- c("coverage", "size", "patch quality")
names(par_rq3_data) <- c("coverage", "size", "patch quality")
names(trp_rq3_data) <- c("coverage", "size", "patch quality")

gp_cov = scale(gp_rq3_data$coverage, center=TRUE, scale=FALSE)
gp_size = scale(gp_rq3_data$size, center=TRUE, scale=FALSE)
gp_new_vars = cbind(gp_cov,gp_size)
gp_rq3_data = cbind(gp_rq3_data, gp_new_vars)
names(gp_rq3_data) <- c("coverage", "size", "quality", "coverage_s", "size_s")

par_cov = scale(par_rq3_data$coverage, center=TRUE, scale=FALSE)
par_size = scale(par_rq3_data$size, center=TRUE, scale=FALSE)
par_new_vars = cbind(par_cov,par_size)
par_rq3_data = cbind(par_rq3_data, par_new_vars)
names(par_rq3_data) <- c("coverage", "size", "quality", "coverage_s", "size_s")

trp_cov = scale(trp_rq3_data$coverage, center=TRUE, scale=FALSE)
trp_size = scale(trp_rq3_data$size, center=TRUE, scale=FALSE)
trp_new_vars = cbind(trp_cov,trp_size)
trp_rq3_data = cbind(trp_rq3_data, trp_new_vars)
names(trp_rq3_data) <- c("coverage", "size", "quality", "coverage_s", "size_s")

gp_mlr = lm(quality ~ coverage_s + size_s, data=gp_rq3_data)
summary(gp_mlr)

par_mlr = lm(quality ~ coverage_s + size_s, data=par_rq3_data)
summary(par_mlr)

trp_mlr = lm(quality ~ coverage_s + size_s, data=trp_rq3_data)
summary(trp_mlr)

