#library("PerformanceAnalytics")
library("ggpubr")
require(plyr)
library(Hmisc)

rq4_results <- read.csv(file="rq4_results.csv", head=TRUE, sep=",", stringsAsFactors=FALSE)
gp_results <- subset(rq4_results, technique=="GenProg") #read.csv(file="gp_rq4_overall.csv", head=TRUE, sep=",", stringsAsFactors=FALSE)
trp_results <- subset(rq4_results, technique=="TrpAutoRepair") # read.csv(file="trp_rq4_overall.csv", head=TRUE, sep=",", stringsAsFactors=FALSE)
#sim_results <- subset(rq4_results, technique=="SimFix") #read.csv(file="par_rq4_overall.csv", head=TRUE, sep=",", stringsAsFactors=FALSE)

pdf("triggeringtest_corr_overall.pdf", width=12, height=12)
ggscatter(rq4_results, x = "normalizednegtestcount", y = "passpercentage",
                add = "reg.line",               
		conf.int = TRUE,                
                color = "technique", palette = c("red", "blue"), 
                shape = "technique",
		xlab="normalized failing test count",                  
                ylab = "patch quality (%)",
		size = 3,
		xlim=c(0.2,1.0),
		xticks.by = 0.2,
		ylim=c(75,101),
		)+
font("xlab", size = 45, color = "black") +
font("ylab", size = 45, color = "black") +
font("xy.text", size = 45, color = "black") +
font("legend.text", size = 35) + 
font("legend.title", size = 35) +
font("title", size = 45) 
dev.off()

cat("\n\nGenProg:\n")
print(cor.test(gp_results$normalizednegtestcount,gp_results$passpercentage))
#cat("\n\nSimFix:\n\n")
#print(cor.test(sim_results$normalizednegtestcount,sim_results$passpercentage))
cat("\n\nTrpAutoRepair:\n\n")
print(cor.test(trp_results$normalizednegtestcount,trp_results$passpercentage))

