#!/bin/sh

HOST=129.15.41.75
TILEPATH=/ldm/data/nws/ldm/tiles
TILES="1 2 3 4 5 6 7 8"

TIMESTAMP=$1

for tile in ${TILES}; do 
    scp ${HOST}:${TILEPATH}/tile${tile}/unqc_cref/UNQC_CREF.${TIMESTAMP}.gtiff UNQC_CREF.${TIMESTAMP}.${tile}.gtiff
done
