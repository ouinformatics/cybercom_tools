library(lattice)
library(plyr)

a <- read.csv('http://localhost:8080/db_get/run_id,param_id,var_name,value,param_order,data_type,time_index/MDR_OUTPUT/500/csv')

# 2002-03-24 00:00:00
a$TIME_INDEX <- strptime(a$TIME_INDEX, '%Y-%m-%d %H:%M:%S')

plot_teco <- function(df) {
    title <- as.character(unique(df$DATA_TYPE))
    print(
    xyplot(VALUE ~ TIME_INDEX | VAR_NAME, data=df, scales='free', main=title, subset=( (VAR_NAME != 'y') & (VAR_NAME != 'd')  ))
    )
}

pdf('~/tmp/test.pdf', width=17, height=11)
d_ply( a, .(DATA_TYPE), plot_teco)
dev.off()


