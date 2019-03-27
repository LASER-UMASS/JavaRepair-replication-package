#library("PerformanceAnalytics")
library("ggpubr")
require(plyr)
library(Hmisc)

rq4_results <- read.csv(file="rq4_results.csv", head=TRUE, sep=",", stringsAsFactors=TRUE)
gp_results <- subset(rq4_results, technique=="GenProg") #read.csv(file="gp_rq4_overall.csv", head=TRUE, sep=",", stringsAsFactors=FALSE)
trp_results <- subset(rq4_results, technique=="TRPAutoRepair") # read.csv(file="trp_rq4_overall.csv", head=TRUE, sep=",", stringsAsFactors=FALSE)
par_results <- subset(rq4_results, technique=="Par") #read.csv(file="par_rq4_overall.csv", head=TRUE, sep=",", stringsAsFactors=FALSE)

pdf("triggeringtest_corr_overall.pdf")
ggscatter(rq4_results, x = "normalizednegtestcount", y = "passpercentage",
                add = "reg.line",               
		conf.int = TRUE,                
                color = "technique", palette = c("black", "red","blue"), 
                shape = "technique",
		xlab="normalized failing test count",                  
                ylab = "patch quality (%)",
		size = 3,
		xlim=c(0.2,1.0),
		xticks.by = 0.2,
		)+
font("xlab", size = 25, color = "black") +
font("ylab", size = 25, color = "black") +
font("xy.text", size = 25, color = "black") +
font("legend.text", size = 18) + 
font("legend.title", size = 18) +
font("title", size = 18) 
dev.off()

cat("\n\nGenProg:\n")
print(cor.test(gp_results$normalizednegtestcount,gp_results$passpercentage))
cat("\n\nPar:\n\n")
print(cor.test(par_results$normalizednegtestcount,par_results$passpercentage))
cat("\n\nTRPAutoRepair:\n\n")
print(cor.test(trp_results$normalizednegtestcount,trp_results$passpercentage))

