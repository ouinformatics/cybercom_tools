#!/bin/bash

## SETUP GRASS ENVIRONMENT ##
# path to GRASS binaries and libraries:
export GISBASE=/usr/lib64/grass-6.4.0/
export PATH=$PATH:$GISBASE/bin:$GISBASE/scripts
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$GISBASE/lib
# use process ID (PID) as lock file number:
export GIS_LOCK=$$

grassrc=/tmp/$RANDOM.grassrc

echo "GISDBASE: /scratch/grass" > $grassrc
echo "LOCATION_NAME: usa" >> $grassrc
echo "MAPSET: NMQ" >> $grassrc
echo "GRASS_GUI: text" >> $grassrc
export GISRC=$grassrc
## END SETUP GRASS ENVIRONMENT ##
    
DATAPATH=/scratch/data/nws/ldm/tiles
PRODUCT=$1

toUpper() {
    echo $1 | tr  "[:lower:]" "[:upper:]"
}
PRODUCT_UP=$(toUpper $PRODUCT)

inGrass() {
    g.mlist -r rast pat=^${PRODUCT_UP} |sort -n| cut -d"." -f 2,3
}

hasVRT() {
    ls -1 ${DATAPATH}/mosaic/${PRODUCT}/*_aea.vrt| sed 's/_aea//g' | cut -d'.' -f2,3 | sort -n | grep '^[0-9]\{8\}' | uniq
}

toImport() {
    comm -23 <(hasVRT) <(inGrass)
}

for vrt in $(toImport); do
    r.external input=${DATAPATH}/mosaic/${PRODUCT}/${PRODUCT_UP}.${vrt}_aea.vrt output=${PRODUCT_UP}.${vrt/_aea.vrt/}
done

# run GRASS' cleanup routine
$GISBASE/etc/clean_temp

# remove session tmp directory:
rm -rf /tmp/grass6-$USER-$GIS_LOCK
