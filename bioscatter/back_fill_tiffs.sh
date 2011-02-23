#!/bin/bash
PRODUCT=$1

for tile in tile{1..8}; do 
    dir=/scratch/data/nws/ldm/tiles/${tile}/${PRODUCT};
    ls ${dir}/*.gz | parallel "if [ -f {.}.gtiff ]; then echo -n .; else echo -n '#'; /scratch/tools/nmq.py {} {.}.gtiff; fi"
done
