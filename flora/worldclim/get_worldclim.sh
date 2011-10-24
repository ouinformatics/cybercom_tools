#!/bin/bash
for file in $(cat WORLDCLIM_FILES); do 
    wget -nc $file; 
done
