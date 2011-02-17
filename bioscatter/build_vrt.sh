#!/bin/bash
# Builds VRTs to have continous raster for CONUS from each of 8 NMQ tiles.
DATAPATH=/scratch/data/nws/ldm/tiles

PRODUCT=$1
FORCE=$2

toUpper() {
    echo $1 | tr  "[:lower:]" "[:upper:]"
}

findFiles() {
    PRODUCT=$1
    VRT=$2
    if [ -z $VRT ]; then
        # Count the number of files in the 8 tiles directories and only return if all 8 tiles are in place.
        ls -1 ${DATAPATH}/tile{1..8}/${PRODUCT}/*.gtiff | cut -d'.' -f2,3 |sort | grep '^[0-9]\{8\}' | uniq -c | grep '^      8 ' | sed 's/^      8 //g'
    else
        # Check if VRT has been built
        ls -1 ${DATAPATH}/mosaic/${PRODUCT}/*.vrt| sed 's/_aea//g' | cut -d'.' -f2,3 | sort | grep '^[0-9]\{8\}' | uniq
    fi
}

noVRT() {
    PRODUCT=$1
    comm -23  <(findFiles ${PRODUCT}| sort -n ) <(findFiles ${PRODUCT} 1| sort -n ) 
}

listFiles() {
    PRODUCT=$1
    DATETIME=$2
    PRODUCT_UP=$(toUpper $PRODUCT)
    for TILE in tile{1..8}; do 
        if [ -f $DATAPATH/$TILE/$PRODUCT/$PRODUCT_UP.$DATETIME.gtiff ]; then
            echo $(ls $DATAPATH/$TILE/$PRODUCT/$PRODUCT_UP.$DATETIME.gtiff)
        fi
    done
}


buildVRT() {
    PRODUCT=$1
    FORCE=$2
    PRODUCT_UP=$(toUpper $PRODUCT)
    if [ -z $FORCE ]; then
        TIMESTEPS=$(noVRT ${PRODUCT}) # Only build VRTs for those files that don't have one yet.
    else
        TIMESTEPS=$(findFiles ${PRODUCT}) # Build VRTs for all files
    fi
    for TIMESTEP in $TIMESTEPS; do 
        gdalbuildvrt -overwrite -srcnodata "-999" $DATAPATH/mosaic/$PRODUCT/$PRODUCT_UP.$TIMESTEP.vrt $(listFiles $PRODUCT $TIMESTEP)
        if [ -f $DATAPATH/mosaic/$PRODUCT/$PRODUCT_UP.$TIMESTEP_aea.vrt ]; then rm $DATAPATH/mosaic/$PRODUCT/$PRODUCT_UP.$TIMESTEP_aea.vrt; fi
        gdalwarp -t_srs /scratch/data/aea2.proj4 -srcnodata "-99" -of VRT $DATAPATH/mosaic/$PRODUCT/$PRODUCT_UP.$TIMESTEP.vrt $DATAPATH/mosaic/$PRODUCT/$PRODUCT_UP.${TIMESTEP}_aea.vrt
    done
}


buildVRT $PRODUCT $FORCE



