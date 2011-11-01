#!/bin/sh

bioscatter_aois() {
    RASTER=$1
    REFL_THRESH=$2
    CLUMP_SIZE=$3 # In hectares
    out_base=bioscatter_$RANDOM
    OUTNAME=$(echo $RASTER | sed 's/\./_/g')
    r.mapcalc ${out_base}_gt="if( ${RASTER} > ${REFL_THRESH}, 1, null())"
    r.clump ${out_base}_gt out=${out_base}_clump
    r.reclass.area input=${out_base}_clump out=${OUTNAME}_aoi greater=${CLUMP_SIZE}
    g.remove rast=${out_base}_gt,${out_base}_clump
    r.to.vect ${OUTNAME}_aoi out=${OUTNAME}_aoi_v feature=area
}


for i in $(seq -w 0 5 55); do
    bioscatter_aois UNQC_CREF.20110809_01${i}00 20 500
done  
