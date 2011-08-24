cd radar_wms
for i in *.map; do 
    psql cybercom -c "create or replace view unqc_cref_view_${i/.map/} as select * from unqc_cref_view where datetime >= '${i:0:4}-${i:5:2}-${i:8:2}' and datetime < date '${i:0:4}-${i:5:2}-${i:8:2}' + interval '1 day'"; 
    psql cybercom -c "insert into geometry_columns values ('','public', 'unqc_cref_view_${i:0:4}_${i:5:2}_${i:8:2}', 'wkb_geometry', 2, 4326, 'POLYGON');"
    psql cybercom -c "grant select on unqc_cref_view_${i/.map/} to cybercom, apache;"
    #psql cybercom -c "delete from geometry_columns where f_table_name = 'unqc_cref_view_${i:0:4}-${i:5:2}-${i:8:2}';"
done
