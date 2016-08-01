library(ggplot2)

plotDiamonds<-function(){
  sp<-ggplot(diamonds,aes(x=diamonds$carat,y=diamonds$price))+
    geom_point(shape=1)
  sp <- sp + facet_grid(clarity~.)
  sp
}

plotDiamonds2<-function(){
  g<-ggplot(diamonds,aes(diamonds$carat,diamonds$price))
  g<-g+geom_point(aes(color=clarity),alpha=1/2)
  g<-g+facet_grid(.~clarity)
  g<-g+geom_smooth(size=0.5,linetype=1,method="lm")
  g<-g+xlab("Carat")+ylab("Price")
  g<-g+theme_bw()
  g
}

plotDiamonds2()