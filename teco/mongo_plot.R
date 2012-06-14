if(!require(ggplot2)) {
  install.packages(ggplot2)
}
if(!require(manipulate)){
  install.packages(manipulate)
}

datahost <- "http://test.cybercommons.org/"        

buildurl <- function(task_id,yvar,xvar) {
     url <- paste(datahost,"/mongo/group_by/teco/taskresults/['year','",xvar,"']/",yvar,"/%7B%22task_id%22:%22",task_id,"%22%7D/?outtype=csv", sep="")
     return(url)
}

doPlot <- function(task_id,yvar,xvar,method,viztype) {
  url <- buildurl(task_id,yvar,xvar)
  data <- read.csv(url, header=T, sep=",")
  if (viztype == 'facet') {
  print(ggplot(data, aes_string( x=xvar, y=method )) + geom_line() + facet_wrap(as.formula(paste("~", 'year')) ))
  }
  else if (viztype == 'overplot') {
    print(ggplot(data, aes_string( x=xvar, y=method)) + geom_line(aes(color=factor(year))) )
  }
}

manipulate(doPlot(task_id,yvar,xvar,method,viztype), viztype=picker('facet', 'overplot'), yvar=picker('gpp','npp','nee_simulate','nee_observed','LAI'), xvar=picker('month','day','week'), method=picker("Sum","Avg" ))



