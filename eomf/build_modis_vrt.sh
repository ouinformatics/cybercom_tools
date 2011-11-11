for prod in ndvi evi lswi; do 
for year in $(seq 2011 -1 2005); do 
for doy in $(seq -w 1 8 365); do
    cd ${prod}/${year}
    find . -name MOD09A1.A${year}${doy}* > ~/input_files.txt
    gdalbuildvrt -input_file_list ~/input_files.txt /tmp/${year}${doy}_${prod}.vrt
    cat /tmp/${year}${doy}_${prod}.vrt | sed "s/.\/\(h..v..\)/\/vsicurl\/http:\/\/panda.rccc.ou.edu\/vol05\/modis\/products\/mod09a1\/geotiff\/${prod}\/${year}\/\1/g" > ~/MOD09A1.A${year}${doy}_${prod}.vrt
    cd ../..
done
done
done
