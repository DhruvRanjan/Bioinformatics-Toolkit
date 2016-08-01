require(ggplot2)
library(ggplot2)

plotScores<-function(seqData){
  
  plot <- ggplot(seqData, aes(x=seqData$Position,y=seqData$Score))
  plot <- plot +geom_point(size=1.5)
  plot <- plot + geom_smooth(method="lm")
  plot <- plot + xlab("Position") + ylab("Score")
  plot <- plot+theme_bw()
  return(plot)
  
}