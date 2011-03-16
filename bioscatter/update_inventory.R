library(ggplot2)
library(RPostgreSQL)

drv <- dbDriver('PostgreSQL')
con <- dbConnect(drv, dbname='cybercom', host='fire', port='5432')

q <- dbSendQuery(con, "select tile, datetime from unqc_cref")

df <- fetch(q, n=-1)

p <- ggplot(df, aes(x = datetime, y=tile) ) 
pdf('update_inventory.pdf', width=11, height=8.5)
p + geom_point(position='jitter', alpha=0.1, color='blue')
dev.off()
