#!/bin/sh

# Grab data from World Glacier Inventory

wget ftp://sidads.colorado.edu/pub/DATASETS/NOAA/G01130/wgi06102009.dat
sed 's/\t-9999.0000/\t/g;s/\t-9999/\t/g' wgi06102009.dat > nulled.txt
mongoimport -d flora -c glacier --type tsv --headerline --file nulled.txt --ignoreBlanks


