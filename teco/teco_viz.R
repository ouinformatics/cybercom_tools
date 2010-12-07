library(lattice)
library(plyr)
library(reshape)

input <- read.csv(URLencode('http://localhost:8080/db_get/run_id,param_id,var_name,pvalue as value,param_order,data_type,time_index/MDRI_PARAMETER/500/csv'))

output <- read.csv('http://localhost:8080/db_get/run_id,param_id,var_name,value,param_order,data_type,time_index/MDR_OUTPUT/500/csv')

clean_time <- function(df) { strptime(df$TIME_INDEX, '%Y-%m-%d %H:%M:%S') }


# 2002-03-24 00:00:00
input$TIME_INDEX <- clean_time(input) 
output$TIME_INDEX <- clean_time(output)

plot_teco <- function(df) {
    title <- as.character(unique(df$DATA_TYPE))
    print(
    xyplot(VALUE ~ TIME_INDEX | VAR_NAME, data=df, scales='free', main=title, subset=( (VAR_NAME != 'y') & (VAR_NAME != 'd') & (VAR_NAME != 'hour') & (VAR_NAME != 'doy') & (VAR_NAME != 'year') ))
    )
}

pdf('~/tmp/test.pdf', width=17, height=11)

d_ply( input, .(DATA_TYPE) , plot_teco )
d_ply( output, .(DATA_TYPE), plot_teco)

dev.off()


