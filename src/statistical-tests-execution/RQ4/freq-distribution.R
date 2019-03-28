
data <- read.csv("failing-test-count.dat")


defects <- data$defect 
tests <- data$failing_test_count 

pdf("failingtestsdistribution.pdf", width=12, height=6)
par(mgp=c(5,0.5,0))
par(mar=c(6,6.5,1,2.5)) 
barplot(tests, las = 2, names.arg = data$defect, col="Black", xlab="defect", ylab="failing test count", ylim=c(0,25), xlim=c(0,75), cex.lab=2, yaxt="n")
axis(cex.lab=2, side=2,at=seq(0,25, by=1))
dev.off()

