library(plyr)
library(xyplot)
#library(doMC)
#registerDoMC(10)

time_convert <- function(timein) { strptime(timein,  '%Y%m%d.%H%M%S') }

filename <- '~/data/merged.csv'
ingest_data <- function(filename) {
    df <- read.csv(filename,  col.names=c('timestamp','loc_id','lat','lon','rain','refl'), colClasses = c('character','integer','numeric','numeric','numeric','numeric'))
    df$ts <- strptime(df$timestamp, '%Y%m%d.%H%M%S')
    df$month <- cut(df$ts, "months")
    df$day <- cut(df$ts, "days")
    df$week <- cut(df$ts, "weeks")
    df
}


a <- ingest_data(filename)

plot_week <- function(df) {
    lat <- df$lat[1]
    lon <- df$lon[1]
    loc_id <- df$loc_id[1]
    xyplot( rain + refl ~ ts | factor(week), data=df, auto.key=T, main=paste('Location:',loc_id,'\n',lat,",",lon))
}

plot_loc <- function(df) {
    loc <- unique(df$loc_id)
    pdf(paste('~/tmp/martin_',loc,'.pdf', sep=""), width=17, height=11)
    loc <- unique(df$loc_id)
    d_ply(df, .(week), plot_week, .print=TRUE)
    dev.off()
}

make_plots <- function(df) {
    pdf('~/tmp/martin_roosts.pdf', width=17, height=11); 
    d_ply( df, .(loc_id), plot_loc, .progress="text" )
    dev.off()
}

make_plots(a)







