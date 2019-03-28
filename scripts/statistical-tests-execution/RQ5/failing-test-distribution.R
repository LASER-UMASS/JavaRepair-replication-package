
data <- read.csv("failing_test_comparison.csv")

defects <- data$defect 
evosuite_tests <- data$failingtestcountEvoSuite  
developer_tests <- data$failingtestcountDeveloper  

pdf("provenance_evosuite_failingtestsdistribution.pdf")
par(mgp=c(4.5,1,0))
par(mar=c(6,6,2,4.5))
barplot(evosuite_tests, las = 2, names.arg = data$defect, col="Black", xlab="defect", main="EvoSuite", ylab="failing test count", ylim=c(0,51), xlim=c(0,37), cex.lab=2, cex.axis=2, cex.main=2, cex.sub=2, yaxt="n")
axis(cex.axis=2,side=2,at=seq(0,45, by=3), labels=seq(0,45, by=3))
dev.off()

pdf("provenance_developer_failingtestsdistribution.pdf")
par(mgp=c(4.5,1,0))
par(mar=c(6,6,2,4.5))
barplot(developer_tests, las=2, names.arg = data$defect, col="Black", xlab="defect", main="Developer", ylab="failing test count", ylim=c(0,51), xlim=c(0,37), cex.lab=2, cex.axis=2, cex.main=2, cex.sub=2, yaxt="n")
axis(cex.axis=2,side=2,at=seq(0,45, by=3), labels=seq(0,45, by=3))
dev.off()

