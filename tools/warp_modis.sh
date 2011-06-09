#!/bin/bash

for tile in $(ls ${PRODUCT}.A${DATE}.*.hdf); do
    gdalinfo ${tile}
done
