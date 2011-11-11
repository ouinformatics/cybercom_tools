require(plyr)
require(RJSONIO)
require(ggplot2)

# Helper for 
json2df <- function(json) { return( ldply(json, data.frame) ) }

get_ym_hourly <- function(station,year,month) {
  url <- paste("http://fire.rccc.ou.edu/mongo/db_find/amf_level4/hourly/%7B'spec':%7B'location':'",station,"','observed_year':",year,",'Month':",month,"%7D%7D/",sep="")
  jsonget <- json2df(fromJSON(url))
  return(jsonget)
}

# Grab a single Julian Day across all years for given Tower ID (used to fake confidence interval visualization)
get_day_hourly <- function(station,DoY) {
  next_day <- DoY + 1
  url <- paste("http://fire.rccc.ou.edu/mongo/db_find/amf_level4/hourly/%7B'spec':%7B'location':'",station,"','DoY':{'$gte':",DoY,",'$lt':",next_day,"}}}",sep="")
  jsonget <- json2df(fromJSON(url))
  return(jsonget)
}
  
get_week_hourly <- function(station,DoY) {
  next_day <- DoY + 7
  url <- paste("http://fire.rccc.ou.edu/mongo/db_find/amf_level4/hourly/%7B'spec':%7B'location':'",station,"','DoY':{'$gte':",DoY,",'$lt':",next_day,"}}}",sep="")
  jsonget <- json2df(fromJSON(url))
  return(jsonget)
}

month <- get_ym_hourly('US-HA1',2000,6)
day <- get_day_hourly('US-HA1', 167)
week <- get_week_hourly('US-HA1', 167)

stat_sum_df <- function(fun, geom="ribbon", ...) {
     stat_summary(fun.data=fun, colour="blue", geom=geom, width=0.2, ...)
}



NEE_range <- ddply(subset(day, NEE_st_fANN > -9999), .(DoY), summarise, NEEmax=max(NEE_st_fANN), NEEmin=min(NEE_st_fANN), NEEmean=mean(NEE_st_fANN))

plotprojection()
plot <- ggplot(subset(week, NEE_st_fANN > -9999), aes(x=DoY, y=NEE_st_fANN))
current <- geom_line(aes(x=DoY, y=NEE_st_fANN), 
                      data=subset(day, observed_year==2003), 
                      color="black", 
                      size=1.5)
historic <- stat_sum_df("mean_cl_normal", alpha=0.4)
projection <- geom_line(aes(x=DoY, y=NEE_st_fANN), data=subset(week, observed_year==2003 & DoY > 168), color="orange", size=1.5)
plot + historic  + current + projection



llply(data, .(DoY), plotprojection)


pdf('out.pdf')
d_ply(month, .(Day), dailyplot, .progress=TRUE)
dev.off()

jsonget <- json2df(fromJSON(target))