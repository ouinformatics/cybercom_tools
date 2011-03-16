-- BASH to import new tiles
-- cd /scratch/data/nws/ldm/tiles
-- for tile in tile{1..8}; do find ${tile} -name UNQC_CREF*.gtiff | sed "s/^/\/scratch\/data\/nws\/ldm\/tiles\//g" | sed "s/^/insert into unqc_cref (file_location) values ('/g;s/$/');/g" |psql cybercom; done

update unqc_cref SET wkb_geometry = (select wkb_geometry from unqc_cref where wkb_geometry is not null and substring(file_location, E'.*\(tile1\).*') = 'tile1' limit 1) where wkb_geometry is null and substring(file_location, E'.*\(tile1\).*') = 'tile1';
update unqc_cref SET wkb_geometry = (select wkb_geometry from unqc_cref where wkb_geometry is not null and substring(file_location, E'.*\(tile2\).*') = 'tile2' limit 1) where wkb_geometry is null and substring(file_location, E'.*\(tile2\).*') = 'tile2';
update unqc_cref SET wkb_geometry = (select wkb_geometry from unqc_cref where wkb_geometry is not null and substring(file_location, E'.*\(tile3\).*') = 'tile3' limit 1) where wkb_geometry is null and substring(file_location, E'.*\(tile3\).*') = 'tile3';
update unqc_cref SET wkb_geometry = (select wkb_geometry from unqc_cref where wkb_geometry is not null and substring(file_location, E'.*\(tile4\).*') = 'tile4' limit 1) where wkb_geometry is null and substring(file_location, E'.*\(tile4\).*') = 'tile4';
update unqc_cref SET wkb_geometry = (select wkb_geometry from unqc_cref where wkb_geometry is not null and substring(file_location, E'.*\(tile5\).*') = 'tile5' limit 1) where wkb_geometry is null and substring(file_location, E'.*\(tile5\).*') = 'tile5';
update unqc_cref SET wkb_geometry = (select wkb_geometry from unqc_cref where wkb_geometry is not null and substring(file_location, E'.*\(tile6\).*') = 'tile6' limit 1) where wkb_geometry is null and substring(file_location, E'.*\(tile6\).*') = 'tile6';
update unqc_cref SET wkb_geometry = (select wkb_geometry from unqc_cref where wkb_geometry is not null and substring(file_location, E'.*\(tile7\).*') = 'tile7' limit 1) where wkb_geometry is null and substring(file_location, E'.*\(tile7\).*') = 'tile7';
update unqc_cref SET wkb_geometry = (select wkb_geometry from unqc_cref where wkb_geometry is not null and substring(file_location, E'.*\(tile8\).*') = 'tile8' limit 1) where wkb_geometry is null and substring(file_location, E'.*\(tile8\).*') = 'tile8';


update unqc_cref set tile = substring(file_location, E'.*\(tile[0-9]\).*') where tile is null;

update unqc_cref SET datetime = to_timestamp(substring(file_location, E'UNQC_CREF.\([0-9]\{8\}.[0-9]\{6\}\)'), 'YYYYMMDD.HH24MISS') where datetime is null;
