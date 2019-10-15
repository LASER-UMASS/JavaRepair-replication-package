#################################
# PURPOSE: R script used to print and plot the frequency distribution of 
#	   unique patches produced by repair techniques over 
#	   five Defects4J projects. It also prints the #defects patched 
#	   out of 357 defects for each technique	 
#
#################################


library(dplyr)
library(ggplot2)
library(ggpubr)
theme_set(theme_pubr())

gp_rq1 <- read.csv(file="gp_rq1_overall.csv", head=TRUE, sep=",", stringsAsFactors=FALSE)
trp_rq1 <- read.csv(file="trp_rq1_overall.csv", head=TRUE, sep=",", stringsAsFactors=FALSE)
par_rq1 <- read.csv(file="par_rq1_overall.csv", head=TRUE, sep=",", stringsAsFactors=FALSE)
sim_rq1 <- read.csv(file="sim_rq1_overall.csv", head=TRUE, sep=",", stringsAsFactors=FALSE)

cat("#Defects patched:\n\n")
cat("GenProg:", length(unique(gp_rq1$defect)),"\n")
cat("Par:", length(unique(par_rq1$defect)), "\n")
cat("TRPAutoRepair:", length(unique(trp_rq1$defect)),"\n")
cat("SimFix:", length(unique(sim_rq1$defect)),"\n")

cat("Unique patch distribution:\n")
cat("GenProg\n")
dfgp <- gp_rq1 %>%
  group_by(project) %>%
  summarise(counts = n())
dfgp
pdf("gp_patchcount.pdf")
ggplot(dfgp, aes(x = project, y = counts)) +
  geom_bar(fill = "black", stat = "identity") +
  geom_text(aes(label = counts), vjust = -0.3, size=15) + 
  theme_pubclean()+
  theme(axis.text=element_text(size=40, color="black"), axis.title=element_text(size=40)) +
  scale_y_continuous(name="patch count", limits=c(0,120), breaks=seq(0,120,20)) +
  xlab("project") + 
  ggtitle("GenProg") + 
  theme(plot.title = element_text(size = 40, hjust = 0.5, face="bold")) + 
  theme(axis.line = element_line(colour = "black", size = 1, linetype = "solid")) +
  theme(axis.text.x = element_text(angle = 90, hjust = 1)) +
  theme(panel.grid.minor.y=element_blank(),panel.grid.major.y=element_blank())
dev.off()

cat("PAR\n")
dfpar <- par_rq1 %>%
  group_by(project) %>%
  summarise(counts = n())
dfpar
pdf("par_patchcount.pdf")
ggplot(dfpar, aes(x = project, y = counts)) +
  geom_bar(fill = "black", stat = "identity") +
  geom_text(aes(label = counts), vjust = -0.3, size=15) + 
  theme_pubclean() +
  theme(axis.text=element_text(size=40, color="black"), axis.title=element_text(size=40)) +
  scale_y_continuous(name="patch count", limits=c(0,120), breaks=seq(0,120,20)) +
  xlab("project") + 
  ggtitle("PAR") + 
  theme(plot.title = element_text(size = 40, hjust = 0.5, face="bold")) + 
  theme(axis.line = element_line(colour = "black", size = 1, linetype = "solid")) +
  theme(axis.text.x = element_text(angle = 90, hjust = 1)) +
  theme(panel.grid.minor.y=element_blank(),panel.grid.major.y=element_blank())
dev.off()

cat("TRPAutoRepair\n")
dftrp <- trp_rq1 %>%
  group_by(project) %>%
  summarise(counts = n())
dftrp
pdf("trp_patchcount.pdf")
ggplot(dftrp, aes(x = project, y = counts)) +
  geom_bar(fill = "black", stat = "identity") +
  geom_text(aes(label = counts), vjust = -0.3, size=15) + 
  theme_pubclean()+
  theme(axis.text=element_text(size=40, color="black"), axis.title=element_text(size=40)) +
  scale_y_continuous(name="patch count", limits=c(0,120), breaks=seq(0,120,20)) +
  xlab("project") + 
  ggtitle("TRPAutoRepair") + 
  theme(plot.title = element_text(size = 40, hjust = 0.5, face="bold")) + 
  theme(axis.line = element_line(colour = "black", size = 1, linetype = "solid")) + 
  theme(axis.text.x = element_text(angle = 90, hjust = 1)) +
  theme(panel.grid.minor.y=element_blank(),panel.grid.major.y=element_blank())
dev.off()

cat("SimFix\n")
dftrp <- sim_rq1 %>%
  group_by(project) %>%
  summarise(counts = n())
dftrp
pdf("sim_patchcount.pdf")
ggplot(dftrp, aes(x = project, y = counts)) +
  geom_bar(fill = "black", stat = "identity") +
  geom_text(aes(label = counts), vjust = -0.3, size=15) + 
  theme_pubclean()+
  theme(axis.text=element_text(size=40, color="black"), axis.title=element_text(size=40)) +
  scale_y_continuous(name="patch count", limits=c(0,120), breaks=seq(0,120,20)) +
  xlab("project") + 
  ggtitle("SimFix") + 
  theme(plot.title = element_text(size = 40, hjust = 0.5, face="bold")) + 
  theme(axis.line = element_line(colour = "black", size = 1, linetype = "solid")) + 
  theme(axis.text.x = element_text(angle = 90, hjust = 1)) +
  theme(panel.grid.minor.y=element_blank(),panel.grid.major.y=element_blank())
dev.off()



