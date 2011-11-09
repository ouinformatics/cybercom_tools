#!/bin/bash
# Run on gproc0 (129.15.41.74) inside of grass64 /data/grass/usa_wgs84
rm window layers methods # remove any old copies of the files still laying around
# Generate files used by parallel for creating combinations
for layer in BIO1_30s BIO3_30s BIO7_302 BIO9_30s BIO12_30s BIO19_30s; do echo $layer >> layers; done
for window in 3 5 15 47 141; do echo $window >> window; done
for methods in average range stddev; do echo $methods >> methods; done

# Use 10 CPU cores to split jobs 
parallel -P 10 'r.neighbors input={2}@WORLDCLIM output={2}_{3}_{1}_km size={1} method={3}' :::: window layers methods
