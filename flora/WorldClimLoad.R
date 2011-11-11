# install.packages('RJSONIO') if you don't have this already
library(RJSONIO)
# install.packages('plyr') if you don't have it
library(plyr)
# Convert from JSON to R Dataframe
json2df <- function(json) { return( ldply(json, data.frame) ) }

# This pulls raster summary data from cybercommons API 
floraworldclim <- function(worldclim_layer) {
  target <- paste('http://fire.rccc.ou.edu/mongo/db_find/flora/worldclim/{\'spec\':{\'RID\':\'', worldclim_layer ,'\'}}', sep="")
  jsonget <- json2df(fromJSON(target))
  colnames(jsonget) <- c('FID', 'REF_NO', 'RID', paste(worldclim_layer,'_avg',sep=""), 
                                              paste(worldclim_layer,'_max',sep=""),
                                              paste(worldclim_layer,'_median',sep=""),
                                              paste(worldclim_layer, '_min', sep=""),
                                              paste(worldclim_layer, '_count', sep=""),
                                              paste(worldclim_layer, '_stdev', sep=""),
                                              paste(worldclim_layer, '_sum', sep=""))
  return(jsonget[c(1:2,4:10)])
}

# example 

# Loading core Flora's Table, Note: State Column will be reduced to first state listed.
flora <- function() { return(json2df(fromJSON('http://fire.rccc.ou.edu/mongo/db_find/flora/data/'))) }

# List layers we want to model with
bioclim <- list('bio_1.bil','bio_2.bil','bio_3.bil','bio_4.bil','bio_5.bil','bio_6.bil','bio_7.bil','bio_8.bil','bio_9.bil','bio_10.bil','bio_11.bil','bio_12.bil','bio_13.bil','bio_14.bil','bio_15.bil','bio_16.bil','bio_17.bil','bio_18.bil','bio_19.bil')
bioclimvars <- function(bioclim) { return(data.frame(llply(bioclim, floraworldclim))) }

# Create dataframe with all data
flora.exp <- merge(flora(), bioclimvars(bioclim), all.x = TRUE)
write.csv(flora.exp, '~/tmp/flora_experiment.csv')


