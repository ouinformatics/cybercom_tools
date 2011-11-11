#!/bin/sh

# Connects to the cyberCommons PostGIS to extract flora polygons
INPUT_VECTOR='"PG:dbname=cybercom tables=cybercom.floras" --sql "select wkb_geometry, REF_NO from cybercom.floras"'
VECTOR_FILE=floras 
KEY_FIELD=REF_NO
STATS="avg stdev min max sum median"
OUTPUTDIR=/ddn_1/data/worldclim/floras_summary
INPUT_GLOB=/ddn_1/data/worldclim/30s/*.bil

for INPUT_RASTER in ${INPUT_GLOB}; do
    RASTER=$(basename ${INPUT_RASTER})
 
    starspan2 --verbose --vector "PG:dbname=cybercom tables=cybercom.floras" --sql "select wkb_geometry, REF_NO from cybercom.floras" \
    --raster ${INPUT_RASTER} \
    --stats ${OUTPUTDIR}/${VECTOR_FILE}_${RASTER}.csv ${STATS} \
    --fields ${KEY_FIELD}
    mongoimport -d flora -c worldclim --type csv --headerline --file ${OUTPUTDIR}/${VECTOR_FILE}_${RASTER}.csv

done
