"""
Functions for accessing dataportal views from cybercom metadata repository.

Examples:

Import module:
>>> from cybercom.data.catalog import portal

"""
from cybercom.data.catalog import datalayer, dataloader

def datacommons():
    md=datalayer.Metadata()
    return md.Search('dt_data_commons',where="Status_flag='A' ORDER BY commons_code",column=['commons_id','commons_code','commons_name']) 
def locations(commons_id):
    if not checkparam(str(commons_id)): return []
    md=datalayer.Metadata()
    return md.Search('dt_location',where="commons_id=" + str(commons_id) + " ORDER BY loc_order,loc_name",column=['loc_id','loc_name','loc_state','lat','lon'])
def products(commons_id):
    if not checkparam(str(commons_id)): return []
    md=datalayer.Metadata()
    return md.Search('dt_type',where="type_id in (select distinct cat_type as type_id from dt_catalog where commons_id=" + str(commons_id) + ") ORDER BY type_id",column=['product'])
def prodyear(commons_id,prod):
    if not (checkparam(str(commons_id)) or checkparam(str(prod))): return []
    md=datalayer.Metadata()
    return md.Search('dt_catalog',where="commons_id=" + str(commons_id) + " and cat_type ='" + str(prod) + "' group by observed_year  ORDER BY observed_year",column=['observed_year'])
def locyear(commons_id,loc):
    if not (checkparam(str(commons_id)) or checkparam(str(loc))): return []
    md=datalayer.Metadata()
    return md.Search('dt_catalog',where="commons_id=" + str(commons_id) + " and loc_id  ='" + str(loc) + "' group by observed_year  ORDER BY observed_year",column=['observed_year'])
def catalog(commons_id,loc,year):
    if not (checkparam(str(commons_id)) or checkparam(str(loc)) or checkparam(str(year))): return []
    md=datalayer.Metadata()
    if commons_id == str(401):
        return md.Search('dt_catalog',
            where="commons_id=" + str(commons_id) + " and cat_type  ='" + str(loc) + "' and observed_year = " + str(year) + " ORDER BY observed_date",
            column=['cat_id','cat_name','loc_id','cat_type'])
    else:
        return md.Search('dt_catalog',
            where="commons_id=" + str(commons_id) + " and loc_id  ='" + str(loc) + "' and observed_year = " + str(year) + " ORDER BY observed_date",
            column=['cat_id','cat_name','loc_id','cat_type'])
def metadata(cat_id):
    if not checkparam(str(cat_id)): return []
    md=datalayer.Metadata()
    return md.metadata(cat_id)
def checkparam(param):
    '''quick, ugly  and dirty way to kill sql-injection. Need to fix with SQLalchemey text expression class -- ON TODO list'''
    val=param.find(';')
    if val<0:
        return True
    else:
        return False
