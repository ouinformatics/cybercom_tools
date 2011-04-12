#!/bin/bash
PRODUCT=$1
PRODUCT=UNQC_CREF

dir=/scratch/nrdump/
find ${dir} -name *.gz |grep 'UNQC_CREF' |grep -v 'mosaic' | rl | parallel -P 7 "if [ -f {.}.gtiff ]; then echo -n '.';  else echo -n '#'; /scratch/tools/nmq.py {} {.}.gtiff; fi"
