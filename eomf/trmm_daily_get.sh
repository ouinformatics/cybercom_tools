#!/bin/sh

if [ $# -lt 1 ]; then
    DATE=$(date -d '-1 day' +%Y.%m.%d)
    YEAR=$(date -d '-1 day' +%Y)
    DOY=$(date  -d '-1 day' +%j)
else
    DATE_IN=$1
    DATE=$(date -d"${DATE_IN}" +%Y.%m.%d)
    YEAR=$(date -d"${DATE_IN}" +%Y)
    DOY=$(date -d"${DATE_IN}" +%j)
fi


wget --content-disposition "http://disc2.nascom.nasa.gov/daac-bin/OTF/HTTP_services.cgi?FILENAME=%2Fftp%2Fdata%2Fs4pa%2FTRMM_L3%2FTRMM_3B42_daily%2F${YEAR}%2F${DOY}%2F3B42_daily.${DATE}.6.bin&FORMAT=L2d6aXA&LABEL=3B42_daily.${DATE}.6.nc.gz&SHORTNAME=TRMM_3B42_daily&SERVICE=HDF_TO_NetCDF&VERSION=1.02&DATASET_VERSION=006"


