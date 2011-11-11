#!/bin/sh

# For one date
date=$1

# Create temp directory
TMPDIR=$(mktemp -d -p /data/tmp)
cd ${TMPDIR}

# Get Data
grabunqc() {
    HOST=129.15.41.75
    TILEPATH=/ldm/data/nws/ldm/tiles
    TILES="1 2 3 4 5 6 7 8"

    TIMESTAMP=$1

    for tile in ${TILES}; do 
        wget http://ldm.cybercommons.org/unqc_cref/tile${tile}/unqc_cref/UNQC_CREF.${TIMESTAMP}.gtiff
    done
}

grabunqc ${date}

# Make VRT
gdalbuildvrt mosaic.vrt *.gtiff

VRTPATH=mosaic.vrt

# Build Mapnik file (replace filename)
MAPTEMPLATE=/home/jduckles/buildtc/unqc_cref_mapnik.xml
makemapfile() {
    sed "s/##FILENAME##/${VRTPATH}/g" ${MAPTEMPLATE} > map.xml 
}
makemapfile

# Build tilecache config file
MAPTEMPLATE=/home/jduckles/buildtc/tilecache.cfg
maketilecachecfg() { 
    sed "s/##LAYERNAME##/${date}/g" ${MAPTEMPLATE} > tilecache.cfg
}
maketilecachecfg

tilecache_seed.py -c tilecache.cfg ${date} 1 6

rm -rf ${TMPDIR}


