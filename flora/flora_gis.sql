-- Used pentaho to move floras table from FLORAINPUT on OUBCF to cybercom PostGIS
-- Then add geometry column to floras table 
select AddGeometryColumn('cybercom','floras','wkb_geometry',4326, 'POLYGON',2);
-- Populate geometry column by building polygons from corners
update cybercom.floras set wkb_geometry = setsrid(polygonfromtext('POLYGON(('||longitudewedge||' '||latitudesedge||','||longitudewedge||' '||latitudenedge||','||longitudeeedge||' '||latitudenedge||','||longitudeeedge||' '||latitudesedge||','||longitudewedge||' '||latitudesedge||'))'),4326);

-- Drop eroneous rows for now:
delete from cybercom.floras where longitudeeedge::numeric < -180;
delete from cybercom.floras where ref_no::real = 20403;
delete from cybercom.floras where ref_no::real = 21592;


