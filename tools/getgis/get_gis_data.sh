#!/bin/bash

# Base data to store downloads in:
DATA_BASE='/scratch/data'
# Target projection to use for GRASS mapset
TARGET_PROJ=${DATA_BASE}/'aea.proj4'
# GRASS Location
GRASS_LOCATION='/scratch/grass/usa'
# Check if GNU Parallel is installed
GNU_PARALLEL=$(type -P parallel)

# Load helper functions:
. get_lib

# Select GIS layers to download and grab:
. srtm1_v2_1; get_srtm1_v2_1
#. srtm3_v2_1
#. cdl2009



