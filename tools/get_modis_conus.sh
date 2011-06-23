#!/bin/bash
# Get MODIS

URLBASE='ftp://e4ftl01.cr.usgs.gov'
SENSOR='MOLT'
PRODUCT='MOD09Q1.005'
DATE='2011.04.07'
URL=${URLBASE}/${SENSOR}/${PRODUCT}/${DATE}/

# Regular expression to match Tiles from MODIS which cover North America
TILES='h08v04\|h09v04\|h10v04\|h11v04\|h12v04\|h13v04\|h08v05\|h09v05\|h10v05\|h11v05\|h12v05\|h08v06\|h09v06\|h10v06'

curl -l ${URL} | grep "${TILES}" >> file_dl

cat file_dl | parallel -q --progress -P 6 "curl ${URL}{} -o {}"

