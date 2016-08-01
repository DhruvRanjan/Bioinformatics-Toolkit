require(ggplot2)
library(ggplot2)

plotScores<-function(seqData){
  
  plot <- ggplot(seqData, aes(x=seqData$Position,y=seqData$Score))
  plot <- plot +geom_point(aes(color=Matrix),size=1.0)
  plot <- plot + facet_grid(.~Matrix)
  plot <- plot + geom_smooth(method="lm")
  plot <- plot + xlab("Position") + ylab("Score")
  plot <- plot+theme_bw()
  return(plot)
  
}