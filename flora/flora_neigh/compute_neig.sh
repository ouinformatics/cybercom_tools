#!/bin/bash

rm window layers methods
for layer in BIO1_30s BIO3_30s BIO7_30s BIO9_30s BIO12_30s BIO19_30s; do echo $layer >> layers; done
for window in 3 5 15 47 141; do echo $window >> window; done
for methods in average range stddev; do echo $methods >> methods; done

parallel -P 10 'r.neighbors -c input={2}@WORLDCLIM output={2}_{3}_{1}_km size={1} method={3}' :::: window layers methods

rm elevation
for elevation in elevation; do echo elevation >> elevation; done
parallel -P 10 'r.neighbors -c input={2}@GLOBE output={2}_{3}_{1}_km size={1} method={3}' :::: window elevation methods

