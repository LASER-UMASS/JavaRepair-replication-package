library(dplyr)
library(ggplot2)
library(ggpubr)
theme_set(theme_pubr())

gp_rq3_all <- read.csv(file="gp_rq3_overall.csv", head=TRUE, sep=",", stringsAsFactors=FALSE)
trp_rq3_all <- read.csv(file="trp_rq3_overall.csv", head=TRUE, sep=",", stringsAsFactors=FALSE)
par_rq3_all <- read.csv(file="par_rq3_overall.csv", head=TRUE, sep=",", stringsAsFactors=FALSE)
sim_rq3_all <- read.csv(file="sim_rq3_overall.csv", head=TRUE, sep=",", stringsAsFactors=FALSE)
eval_defects <- read.csv(file = "../evaluation-defects.txt")
evaldefectsgp <- intersect(gp_rq3_all$defect, eval_defects$defect)
evaldefectspar <- intersect(par_rq3_all$defect, eval_defects$defect)
evaldefectstrp <- intersect(trp_rq3_all$defect, eval_defects$defect)
evaldefectssim <- intersect(sim_rq3_all$defect, eval_defects$defect)
gp_rq3 <- subset(gp_rq3_all, gp_rq3_all$defect%in%evaldefectsgp == TRUE)
par_rq3 <- subset(par_rq3_all, par_rq3_all$defect%in%evaldefectspar == TRUE)
trp_rq3 <- subset(trp_rq3_all, trp_rq3_all$defect%in%evaldefectstrp == TRUE)
sim_rq3 <- subset(sim_rq3_all, sim_rq3_all$defect%in%evaldefectssim == TRUE)

cat("GenProg")
unique(gp_rq3$defect)
length(unique(gp_rq3$defect))

cat("Par")
unique(par_rq3$defect)
length(unique(par_rq3$defect))

cat("TrpAutoRepair")
unique(trp_rq3$defect)
length(unique(trp_rq3$defect))

cat("SimFix")
unique(sim_rq3$defect)
length(unique(sim_rq3$defect))


df <- gp_rq3 %>%
  group_by(project) %>%
  summarise(counts = n())

cat("GenProg Patch Count Distribution\n")
df

pdf("gp_coverage_patchcount.pdf")
ggplot(df, aes(x = project, y = counts)) +
  geom_bar(fill = "black", stat = "identity") +
  geom_text(aes(label = counts), vjust = -0.3, size=10) + 
  theme_pubclean()+
  theme(axis.text=element_text(size=40, color="black"), axis.title=element_text(size=40)) +
  scale_y_continuous(name="patch count", limits=c(0,2200), breaks=seq(0,2200,400)) +
  xlab("project") + 
  ggtitle("GenProg") + 
  theme(plot.title = element_text(size = 40, hjust = 0.5, face="bold")) + 
  theme(axis.line = element_line(colour = "black", size = 1, linetype = "solid")) +
  theme(axis.text.x = element_text(angle = 90, hjust = 1)) +
  theme(panel.grid.minor.y=element_blank(),panel.grid.major.y=element_blank())
dev.off()

dfpar <- par_rq3 %>%
  group_by(project) %>%
  summarise(counts = n())

cat("Par Patch Count Distribution\n")
dfpar

pdf("par_coverage_patchcount.pdf")
ggplot(dfpar, aes(x = project, y = counts)) +
  geom_bar(fill = "black", stat = "identity") +
  geom_text(aes(label = counts), vjust = -0.3, size=10) + 
  theme_pubclean()+
  theme(axis.text=element_text(size=40, color="black"), axis.title=element_text(size=40)) +
  scale_y_continuous(name="patch count", limits=c(0,2200), breaks=seq(0,2200,400)) +
  xlab("project") + 
  ggtitle("Par") + 
  theme(plot.title = element_text(size = 40, hjust = 0.5, face="bold")) + 
  theme(axis.line = element_line(colour = "black", size = 1, linetype = "solid")) +
  theme(axis.text.x = element_text(angle = 90, hjust = 1)) +
  theme(panel.grid.minor.y=element_blank(),panel.grid.major.y=element_blank())
dev.off()

df <- trp_rq3 %>%
  group_by(project) %>%
  summarise(counts = n())

cat("TrpAutoRepair Patch Count Distribution\n")
df

pdf("trp_coverage_patchcount.pdf")
ggplot(df, aes(x = project, y = counts)) +
  geom_bar(fill = "black", stat = "identity") +
  geom_text(aes(label = counts), vjust = -0.3, size=10) + 
  theme_pubclean()+
  theme(axis.text=element_text(size=40, color="black"), axis.title=element_text(size=40)) +
  scale_y_continuous(name="patch count", limits=c(0,2200), breaks=seq(0,2200,400)) +
  xlab("project") + 
  ggtitle("TrpAutoRepair") + 
  theme(plot.title = element_text(size = 40, hjust = 0.5, face="bold")) + 
  theme(axis.line = element_line(colour = "black", size = 1, linetype = "solid")) +
  theme(axis.text.x = element_text(angle = 90, hjust = 1)) +
  theme(panel.grid.minor.y=element_blank(),panel.grid.major.y=element_blank())
dev.off()

df <- sim_rq3 %>%
  group_by(project) %>%
  summarise(counts = n())

cat("SimFix Patch Count Distribution\n")
df

pdf("sim_coverage_patchcount.pdf")
ggplot(df, aes(x = project, y = counts)) +
  geom_bar(fill = "black", stat = "identity") +
  geom_text(aes(label = counts), vjust = -0.3, size=10) + 
  theme_pubclean()+
  theme(axis.text=element_text(size=40, color="black"), axis.title=element_text(size=40)) +
  scale_y_continuous(name="patch count", limits=c(0,2200), breaks=seq(0,2200,400)) +
  xlab("project") + 
  ggtitle("SimFix") + 
  theme(plot.title = element_text(size = 40, hjust = 0.5, face="bold")) + 
  theme(axis.line = element_line(colour = "black", size = 1, linetype = "solid")) +
  theme(axis.text.x = element_text(angle = 90, hjust = 1)) +
  theme(panel.grid.minor.y=element_blank(),panel.grid.major.y=element_blank())
dev.off()




# patch quality assessment considering the defects for 
# which we generate high-quality test suites

gp_rq3_all <- read.csv(file="gp_rq3_overall.csv", head=TRUE, sep=",", stringsAsFactors=FALSE)
trp_rq3_all <- read.csv(file="trp_rq3_overall.csv", head=TRUE, sep=",", stringsAsFactors=FALSE)
par_rq3_all <- read.csv(file="par_rq3_overall.csv", head=TRUE, sep=",", stringsAsFactors=FALSE)
sim_rq3_all <- read.csv(file="sim_rq3_overall.csv", head=TRUE, sep=",", stringsAsFactors=FALSE)
evaldefectsgp <- intersect(gp_rq3_all$defect, eval_defects$defect)
evaldefectspar <- intersect(par_rq3_all$defect, eval_defects$defect)
evaldefectstrp <- intersect(trp_rq3_all$defect, eval_defects$defect)
evaldefectssim <- intersect(sim_rq3_all$defect, eval_defects$defect)
gp_rq3 <- subset(gp_rq3_all, gp_rq3_all$defect%in%evaldefectsgp == TRUE)
par_rq3 <- subset(par_rq3_all, par_rq3_all$defect%in%evaldefectspar == TRUE)
trp_rq3 <- subset(trp_rq3_all, trp_rq3_all$defect%in%evaldefectstrp == TRUE)
sim_rq3 <- subset(sim_rq3_all, sim_rq3_all$defect%in%evaldefectssim == TRUE)

cat("\n\nGenProg Patch Quality\n")
cat("min:", min(gp_rq3$passpercentage),"\n")
cat("mean:", mean(gp_rq3$passpercentage), "\n")
cat("median:", median(gp_rq3$passpercentage), "\n")
cat("max:", max(gp_rq3$passpercentage), "\n")
cat("100%-quality:", length(which(gp_rq3$passpercentage==100))/length(gp_rq3$passpercentage),"\n")

cat("\n\nPar Patch Quality\n")
cat("min:", min(par_rq3$passpercentage),"\n")
cat("mean:", mean(par_rq3$passpercentage), "\n")
cat("median:", median(par_rq3$passpercentage), "\n")
cat("max:", max(par_rq3$passpercentage), "\n")
cat("100%-quality:", length(which(par_rq3$passpercentage==100))/length(par_rq3$passpercentage),"\n")

cat("\n\nTrpAutoRepair Patch Quality\n")
cat("min:", min(trp_rq3$passpercentage),"\n")
cat("mean:", mean(trp_rq3$passpercentage), "\n")
cat("median:", median(trp_rq3$passpercentage), "\n")
cat("max:", max(trp_rq3$passpercentage), "\n")
cat("100%-quality:", length(which(trp_rq3$passpercentage==100))/length(trp_rq3$passpercentage),"\n")

cat("\n\nSimFix Patch Quality\n")
cat("min:", min(sim_rq3$passpercentage),"\n")
cat("mean:", mean(sim_rq3$passpercentage), "\n")
cat("median:", median(sim_rq3$passpercentage), "\n")
cat("max:", max(sim_rq3$passpercentage), "\n")
cat("100%-quality:", length(which(sim_rq3$passpercentage==100))/length(sim_rq3$passpercentage),"\n")

