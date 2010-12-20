create table bioscatter (timestamp, loc_id, lat, lon, item, value);
.mode csv
.import rain.csv bioscatter
.import reflect.csv bioscatter
create index bio_idx on bioscatter (timestamp, loc_id);
.output merged.csv
select strftime('%Y%m%d.%H%M%S', rain.timestamp) as timestamp, rain.loc_id, rain.lat, rain.lon, rain.value, refl.value from (select * from bioscatter where item = 'rain') as rain, (select * from bioscatter where item = 'reflectivity') as refl where rain.timestamp=refl.timestamp and rain.loc_id = refl.loc_id;

