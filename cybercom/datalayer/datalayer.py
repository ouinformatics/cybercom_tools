'''
Python Data Layer Generator
Mark Stacy -- markstacy@ou.edu

'''
#from django.db import connection, transaction
import cx_Oracle as db
connection = db.connect('eco/b00mer@oubcf1')

class dt_catalog():
    def __init__(self):
        self.columnnames = ['COMMONS_ID','CAT_ID','CAT_NAME','DATA_PROVIDER','CAT_TYPE','LOC_ID','SOURCE_ID','CAT_DESC','CAT_METHOD','OBSERVE_DATE','REMARK','YEAR','CUSTOM_FIELD_1','CUSTOM_FIELD_2','STATUS_FLAG','STATUS_DATA']
        self.pkeys =['CAT_ID','COMMONS_ID']
    def printset(self,cur,header=True):
        if header:
            print tuple(self.columnnames)
        for row in cur:
            print row
    def selectpkey(self,CAT_ID,COMMONS_ID):
        c1= connection.cursor()
        sql = "SELECT COMMONS_ID, CAT_ID, CAT_NAME, DATA_PROVIDER, CAT_TYPE, LOC_ID, SOURCE_ID, CAT_DESC, CAT_METHOD, OBSERVE_DATE, REMARK, YEAR, CUSTOM_FIELD_1, CUSTOM_FIELD_2, STATUS_FLAG, STATUS_DATA FROM DT_CATALOG"
        sql = sql + " WHERE CAT_ID = :CAT_ID AND COMMONS_ID = :COMMONS_ID"
        param ={'CAT_ID' : CAT_ID, 'COMMONS_ID' : COMMONS_ID}
        c1.execute(sql, param)
        return c1
    def select(self,**where):
        c1 = connection.cursor()
        sql = "SELECT COMMONS_ID, CAT_ID, CAT_NAME, DATA_PROVIDER, CAT_TYPE, LOC_ID, SOURCE_ID, CAT_DESC, CAT_METHOD, OBSERVE_DATE, REMARK, YEAR, CUSTOM_FIELD_1, CUSTOM_FIELD_2, STATUS_FLAG, STATUS_DATA FROM DT_CATALOG "
        first=True
        param={}
        for colname,val in where.items():
            if first:
                sql=sql + "WHERE "
            if not first:
                sql=sql + " AND "
            first=False
            if val[0].upper().strip()=='IS':
                sql=sql + colname + " IS NULL"
            else:
                sql = sql + colname + val[0] + " :" + colname
                param[colname]=val[1]
        c1.execute(sql, param)
        return c1
    #@transaction.commit_on_success()
    def update(self, CAT_ID, COMMONS_ID, datetime_format= 'YYYY-MM-DD HH24:MI:SS', **uargs):
        c1 = connection.cursor()
        param={}
        sql = "UPDATE DT_CATALOG SET "
        where = " WHERE CAT_ID = :CAT_ID AND COMMONS_ID = :COMMONS_ID"
        param['CAT_ID'] = CAT_ID
        param['COMMONS_ID'] = COMMONS_ID
        first=True
        for colname,val in uargs.items():
            if not first:
                sql=sql + ", "
            first=False
            if (colname == OBSERVE_DATE):
                sql =sql +  colname + ' = to_date(:' + colname + ' ,' + datetime_format + ')'
            else:
                sql =sql +  colname + ' = :' + colname
            param[colname]=val
        sql = sql + where
        c1.execute(sql, param)
        connection.commit()


    #@transaction.commit_on_success()
    def insert(self, CAT_ID, COMMONS_ID, datetime_format= 'YYYY-MM-DD HH24:MI:SS', **iargs):
        c1 = connection.cursor()
        sql = "INSERT INTO DT_CATALOG "
        col = "(CAT_ID,COMMONS_ID, "
        vals = " VALUES (:CAT_ID,:COMMONS_ID, "
        first=True
        param={}
        param['CAT_ID'] = CAT_ID
        param['COMMONS_ID'] = COMMONS_ID
        for colname,val in iargs.items():
            if not first:
                col=col + ", "
                vals=vals + ", "
            first=False
            col = col + colname
            if (colname == OBSERVE_DATE):
                vals = vals + ' to_date(:' + colname + ' ,' + datetime_format + ')'
            else:
                vals = vals + ':' + colname
            param[colname]=val
        sql = sql + col + ")" + vals + ")"
        c1.execute(sql,param)
        connection.commit()

    #@transaction.commit_on_success()
    def delete(self,CAT_ID, COMMONS_ID):
        c1 = connection.cursor()
        param={}
        param['CAT_ID'] = CAT_ID
        param['COMMONS_ID'] = COMMONS_ID
        sql= 'DELETE FROM DT_CATALOG'
        sql = sql + ' WHERE CAT_ID = :CAT_ID AND COMMONS_ID = :COMMONS_ID'
        c1.execute(sql, param)

class dt_contributors():
    def __init__(self):
        self.columnnames = ['COMMONS_ID','CONTRIBUTOR_ID','PROJECT_TITLE','DESCRIPTION','REMARK']
        self.pkeys =['COMMONS_ID','CONTRIBUTOR_ID']
    def printset(self,cur,header=True):
        if header:
            print tuple(self.columnnames)
        for row in cur:
            print row
    def selectpkey(self,COMMONS_ID,CONTRIBUTOR_ID):
        c1= connection.cursor()
        sql = "SELECT COMMONS_ID, CONTRIBUTOR_ID, PROJECT_TITLE, DESCRIPTION, REMARK FROM DT_CONTRIBUTORS"
        sql = sql + " WHERE COMMONS_ID = :COMMONS_ID AND CONTRIBUTOR_ID = :CONTRIBUTOR_ID"
        param ={'COMMONS_ID' : COMMONS_ID, 'CONTRIBUTOR_ID' : CONTRIBUTOR_ID}
        c1.execute(sql, param)
        return c1
    def select(self,**where):
        c1 = connection.cursor()
        sql = "SELECT COMMONS_ID, CONTRIBUTOR_ID, PROJECT_TITLE, DESCRIPTION, REMARK FROM DT_CONTRIBUTORS "
        first=True
        param={}
        for colname,val in where.items():
            if first:
                sql=sql + "WHERE "
            if not first:
                sql=sql + " AND "
            first=False
            if val[0].upper().strip()=='IS':
                sql=sql + colname + " IS NULL"
            else:
                sql = sql + colname + val[0] + " :" + colname
                param[colname]=val[1]
        c1.execute(sql, param)
        return c1
    #@transaction.commit_on_success()
    def update(self, COMMONS_ID, CONTRIBUTOR_ID, **uargs):
        c1 = connection.cursor()
        param={}
        sql = "UPDATE DT_CONTRIBUTORS SET "
        where = " WHERE COMMONS_ID = :COMMONS_ID AND CONTRIBUTOR_ID = :CONTRIBUTOR_ID"
        param['COMMONS_ID'] = COMMONS_ID
        param['CONTRIBUTOR_ID'] = CONTRIBUTOR_ID
        first=True
        for colname,val in uargs.items():
            if not first:
                sql=sql + ", "
            first=False
            sql =sql +  colname + ' = :' + colname
            param[colname]=val
        sql = sql + where
        c1.execute(sql, param)
        connection.commit()


    #@transaction.commit_on_success()
    def insert(self, COMMONS_ID, CONTRIBUTOR_ID, **iargs):
        c1 = connection.cursor()
        sql = "INSERT INTO DT_CONTRIBUTORS "
        col = "(COMMONS_ID,CONTRIBUTOR_ID, "
        vals = " VALUES (:COMMONS_ID,:CONTRIBUTOR_ID, "
        first=True
        param={}
        param['COMMONS_ID'] = COMMONS_ID
        param['CONTRIBUTOR_ID'] = CONTRIBUTOR_ID
        for colname,val in iargs.items():
            if not first:
                col=col + ", "
                vals=vals + ", "
            first=False
            col = col + colname
            vals = vals + ':' + colname
            param[colname]=val
        sql = sql + col + ")" + vals + ")"
        c1.execute(sql,param)
        connection.commit()

    #@transaction.commit_on_success()
    def delete(self,COMMONS_ID, CONTRIBUTOR_ID):
        c1 = connection.cursor()
        param={}
        param['COMMONS_ID'] = COMMONS_ID
        param['CONTRIBUTOR_ID'] = CONTRIBUTOR_ID
        sql= 'DELETE FROM DT_CONTRIBUTORS'
        sql = sql + ' WHERE COMMONS_ID = :COMMONS_ID AND CONTRIBUTOR_ID = :CONTRIBUTOR_ID'
        c1.execute(sql, param)

class dt_coordinate():
    def __init__(self):
        self.columnnames = ['FACILITY_ID','SYS_LOC_CODE','COORD_TYPE_CODE','OBSERVATION_DATE','IDENTIFIER','X_COORD','Y_COORD','ELEV','ELEV_UNIT','HORZ_COLLECT_METHOD_CODE','COORD_ZONE','HORZ_ACCURACY_VALUE','HORZ_ACCURACY_UNIT','ELEV_ACCURACY_UNIT','HORZ_DATUM_CODE','ELEV_COLLECT_METHOD_CODE','ELEV_ACCURACY_VALUE','ELEV_DATUM_CODE','SOURCE_SCALE','COMPANY_CODE','VERIFICATION_CODE','DATA_POINT_SEQUENCE','REFERENCE_POINT','GEOMETRIC_TYPE_CODE','SURVEYOR_NAME','RANK','REMARK','EBATCH']
        self.pkeys =['COORD_TYPE_CODE','FACILITY_ID','IDENTIFIER','SYS_LOC_CODE']
    def printset(self,cur,header=True):
        if header:
            print tuple(self.columnnames)
        for row in cur:
            print row
    def selectpkey(self,COORD_TYPE_CODE,FACILITY_ID,IDENTIFIER,SYS_LOC_CODE):
        c1= connection.cursor()
        sql = "SELECT FACILITY_ID, SYS_LOC_CODE, COORD_TYPE_CODE, OBSERVATION_DATE, IDENTIFIER, X_COORD, Y_COORD, ELEV, ELEV_UNIT, HORZ_COLLECT_METHOD_CODE, COORD_ZONE, HORZ_ACCURACY_VALUE, HORZ_ACCURACY_UNIT, ELEV_ACCURACY_UNIT, HORZ_DATUM_CODE, ELEV_COLLECT_METHOD_CODE, ELEV_ACCURACY_VALUE, ELEV_DATUM_CODE, SOURCE_SCALE, COMPANY_CODE, VERIFICATION_CODE, DATA_POINT_SEQUENCE, REFERENCE_POINT, GEOMETRIC_TYPE_CODE, SURVEYOR_NAME, RANK, REMARK, EBATCH FROM DT_COORDINATE"
        sql = sql + " WHERE COORD_TYPE_CODE = :COORD_TYPE_CODE AND FACILITY_ID = :FACILITY_ID AND IDENTIFIER = :IDENTIFIER AND SYS_LOC_CODE = :SYS_LOC_CODE"
        param ={'COORD_TYPE_CODE' : COORD_TYPE_CODE, 'FACILITY_ID' : FACILITY_ID, 'IDENTIFIER' : IDENTIFIER, 'SYS_LOC_CODE' : SYS_LOC_CODE}
        c1.execute(sql, param)
        return c1
    def select(self,**where):
        c1 = connection.cursor()
        sql = "SELECT FACILITY_ID, SYS_LOC_CODE, COORD_TYPE_CODE, OBSERVATION_DATE, IDENTIFIER, X_COORD, Y_COORD, ELEV, ELEV_UNIT, HORZ_COLLECT_METHOD_CODE, COORD_ZONE, HORZ_ACCURACY_VALUE, HORZ_ACCURACY_UNIT, ELEV_ACCURACY_UNIT, HORZ_DATUM_CODE, ELEV_COLLECT_METHOD_CODE, ELEV_ACCURACY_VALUE, ELEV_DATUM_CODE, SOURCE_SCALE, COMPANY_CODE, VERIFICATION_CODE, DATA_POINT_SEQUENCE, REFERENCE_POINT, GEOMETRIC_TYPE_CODE, SURVEYOR_NAME, RANK, REMARK, EBATCH FROM DT_COORDINATE "
        first=True
        param={}
        for colname,val in where.items():
            if first:
                sql=sql + "WHERE "
            if not first:
                sql=sql + " AND "
            first=False
            if val[0].upper().strip()=='IS':
                sql=sql + colname + " IS NULL"
            else:
                sql = sql + colname + val[0] + " :" + colname
                param[colname]=val[1]
        c1.execute(sql, param)
        return c1
    #@transaction.commit_on_success()
    def update(self, COORD_TYPE_CODE, FACILITY_ID, IDENTIFIER, SYS_LOC_CODE, datetime_format= 'YYYY-MM-DD HH24:MI:SS', **uargs):
        c1 = connection.cursor()
        param={}
        sql = "UPDATE DT_COORDINATE SET "
        where = " WHERE COORD_TYPE_CODE = :COORD_TYPE_CODE AND FACILITY_ID = :FACILITY_ID AND IDENTIFIER = :IDENTIFIER AND SYS_LOC_CODE = :SYS_LOC_CODE"
        param['COORD_TYPE_CODE'] = COORD_TYPE_CODE
        param['FACILITY_ID'] = FACILITY_ID
        param['IDENTIFIER'] = IDENTIFIER
        param['SYS_LOC_CODE'] = SYS_LOC_CODE
        first=True
        for colname,val in uargs.items():
            if not first:
                sql=sql + ", "
            first=False
            if (colname == OBSERVATION_DATE):
                sql =sql +  colname + ' = to_date(:' + colname + ' ,' + datetime_format + ')'
            else:
                sql =sql +  colname + ' = :' + colname
            param[colname]=val
        sql = sql + where
        c1.execute(sql, param)
        connection.commit()


    #@transaction.commit_on_success()
    def insert(self, COORD_TYPE_CODE, FACILITY_ID, IDENTIFIER, SYS_LOC_CODE, datetime_format= 'YYYY-MM-DD HH24:MI:SS', **iargs):
        c1 = connection.cursor()
        sql = "INSERT INTO DT_COORDINATE "
        col = "(COORD_TYPE_CODE,FACILITY_ID,IDENTIFIER,SYS_LOC_CODE, "
        vals = " VALUES (:COORD_TYPE_CODE,:FACILITY_ID,:IDENTIFIER,:SYS_LOC_CODE, "
        first=True
        param={}
        param['COORD_TYPE_CODE'] = COORD_TYPE_CODE
        param['FACILITY_ID'] = FACILITY_ID
        param['IDENTIFIER'] = IDENTIFIER
        param['SYS_LOC_CODE'] = SYS_LOC_CODE
        for colname,val in iargs.items():
            if not first:
                col=col + ", "
                vals=vals + ", "
            first=False
            col = col + colname
            if (colname == OBSERVATION_DATE):
                vals = vals + ' to_date(:' + colname + ' ,' + datetime_format + ')'
            else:
                vals = vals + ':' + colname
            param[colname]=val
        sql = sql + col + ")" + vals + ")"
        c1.execute(sql,param)
        connection.commit()

    #@transaction.commit_on_success()
    def delete(self,COORD_TYPE_CODE, FACILITY_ID, IDENTIFIER, SYS_LOC_CODE):
        c1 = connection.cursor()
        param={}
        param['COORD_TYPE_CODE'] = COORD_TYPE_CODE
        param['FACILITY_ID'] = FACILITY_ID
        param['IDENTIFIER'] = IDENTIFIER
        param['SYS_LOC_CODE'] = SYS_LOC_CODE
        sql= 'DELETE FROM DT_COORDINATE'
        sql = sql + ' WHERE COORD_TYPE_CODE = :COORD_TYPE_CODE AND FACILITY_ID = :FACILITY_ID AND IDENTIFIER = :IDENTIFIER AND SYS_LOC_CODE = :SYS_LOC_CODE'
        c1.execute(sql, param)

class dt_data_commons():
    def __init__(self):
        self.columnnames = ['COMMONS_ID','COMMONS_CODE','DATA_PROVIDER','COMMONS_TYPE','PROGRAM_CODE','COMMONS_NAME','EMAIL_ADDRESS','DESCRIPTION','CLIENT','PROJECT_MANAGER','START_DATE','STATUS_FLAG','CONTRIBUTOR_ID']
        self.pkeys =['COMMONS_ID']
    def printset(self,cur,header=True):
        if header:
            print tuple(self.columnnames)
        for row in cur:
            print row
    def selectpkey(self,COMMONS_ID):
        c1= connection.cursor()
        sql = "SELECT COMMONS_ID, COMMONS_CODE, DATA_PROVIDER, COMMONS_TYPE, PROGRAM_CODE, COMMONS_NAME, EMAIL_ADDRESS, DESCRIPTION, CLIENT, PROJECT_MANAGER, START_DATE, STATUS_FLAG, CONTRIBUTOR_ID FROM DT_DATA_COMMONS"
        sql = sql + " WHERE COMMONS_ID = :COMMONS_ID"
        param ={'COMMONS_ID' : COMMONS_ID}
        c1.execute(sql, param)
        return c1
    def select(self,**where):
        c1 = connection.cursor()
        sql = "SELECT COMMONS_ID, COMMONS_CODE, DATA_PROVIDER, COMMONS_TYPE, PROGRAM_CODE, COMMONS_NAME, EMAIL_ADDRESS, DESCRIPTION, CLIENT, PROJECT_MANAGER, START_DATE, STATUS_FLAG, CONTRIBUTOR_ID FROM DT_DATA_COMMONS "
        first=True
        param={}
        for colname,val in where.items():
            if first:
                sql=sql + "WHERE "
            if not first:
                sql=sql + " AND "
            first=False
            if val[0].upper().strip()=='IS':
                sql=sql + colname + " IS NULL"
            else:
                sql = sql + colname + val[0] + " :" + colname
                param[colname]=val[1]
        c1.execute(sql, param)
        return c1
    #@transaction.commit_on_success()
    def update(self, COMMONS_ID, datetime_format= 'YYYY-MM-DD HH24:MI:SS', **uargs):
        c1 = connection.cursor()
        param={}
        sql = "UPDATE DT_DATA_COMMONS SET "
        where = " WHERE COMMONS_ID = :COMMONS_ID"
        param['COMMONS_ID'] = COMMONS_ID
        first=True
        for colname,val in uargs.items():
            if not first:
                sql=sql + ", "
            first=False
            if (colname == START_DATE):
                sql =sql +  colname + ' = to_date(:' + colname + ' ,' + datetime_format + ')'
            else:
                sql =sql +  colname + ' = :' + colname
            param[colname]=val
        sql = sql + where
        c1.execute(sql, param)
        connection.commit()


    #@transaction.commit_on_success()
    def insert(self, COMMONS_ID, datetime_format= 'YYYY-MM-DD HH24:MI:SS', **iargs):
        c1 = connection.cursor()
        sql = "INSERT INTO DT_DATA_COMMONS "
        col = "(COMMONS_ID, "
        vals = " VALUES (:COMMONS_ID, "
        first=True
        param={}
        param['COMMONS_ID'] = COMMONS_ID
        for colname,val in iargs.items():
            if not first:
                col=col + ", "
                vals=vals + ", "
            first=False
            col = col + colname
            if (colname == START_DATE):
                vals = vals + ' to_date(:' + colname + ' ,' + datetime_format + ')'
            else:
                vals = vals + ':' + colname
            param[colname]=val
        sql = sql + col + ")" + vals + ")"
        c1.execute(sql,param)
        connection.commit()

    #@transaction.commit_on_success()
    def delete(self,COMMONS_ID):
        c1 = connection.cursor()
        param={}
        param['COMMONS_ID'] = COMMONS_ID
        sql= 'DELETE FROM DT_DATA_COMMONS'
        sql = sql + ' WHERE COMMONS_ID = :COMMONS_ID'
        c1.execute(sql, param)

class dt_event():
    def __init__(self):
        self.columnnames = ['COMMONS_ID','EVENT_ID','CAT_ID','EVENT_METHOD','EVENT_DATE','EVENT_DESC','EVENT_TYPE','LOC_ID','CUSTOM_1','REMARK','EVENT_NAME','STATUS_FLAG']
        self.pkeys =['COMMONS_ID','EVENT_ID']
    def printset(self,cur,header=True):
        if header:
            print tuple(self.columnnames)
        for row in cur:
            print row
    def selectpkey(self,COMMONS_ID,EVENT_ID):
        c1= connection.cursor()
        sql = "SELECT COMMONS_ID, EVENT_ID, CAT_ID, EVENT_METHOD, EVENT_DATE, EVENT_DESC, EVENT_TYPE, LOC_ID, CUSTOM_1, REMARK, EVENT_NAME, STATUS_FLAG FROM DT_EVENT"
        sql = sql + " WHERE COMMONS_ID = :COMMONS_ID AND EVENT_ID = :EVENT_ID"
        param ={'COMMONS_ID' : COMMONS_ID, 'EVENT_ID' : EVENT_ID}
        c1.execute(sql, param)
        return c1
    def select(self,**where):
        c1 = connection.cursor()
        sql = "SELECT COMMONS_ID, EVENT_ID, CAT_ID, EVENT_METHOD, EVENT_DATE, EVENT_DESC, EVENT_TYPE, LOC_ID, CUSTOM_1, REMARK, EVENT_NAME, STATUS_FLAG FROM DT_EVENT "
        first=True
        param={}
        for colname,val in where.items():
            if first:
                sql=sql + "WHERE "
            if not first:
                sql=sql + " AND "
            first=False
            if val[0].upper().strip()=='IS':
                sql=sql + colname + " IS NULL"
            else:
                sql = sql + colname + val[0] + " :" + colname
                param[colname]=val[1]
        c1.execute(sql, param)
        return c1
    #@transaction.commit_on_success()
    def update(self, COMMONS_ID, EVENT_ID, datetime_format= 'YYYY-MM-DD HH24:MI:SS', **uargs):
        c1 = connection.cursor()
        param={}
        sql = "UPDATE DT_EVENT SET "
        where = " WHERE COMMONS_ID = :COMMONS_ID AND EVENT_ID = :EVENT_ID"
        param['COMMONS_ID'] = COMMONS_ID
        param['EVENT_ID'] = EVENT_ID
        first=True
        for colname,val in uargs.items():
            if not first:
                sql=sql + ", "
            first=False
            if (colname == EVENT_DATE):
                sql =sql +  colname + ' = to_date(:' + colname + ' ,' + datetime_format + ')'
            else:
                sql =sql +  colname + ' = :' + colname
            param[colname]=val
        sql = sql + where
        c1.execute(sql, param)
        connection.commit()


    #@transaction.commit_on_success()
    def insert(self, COMMONS_ID, EVENT_ID, datetime_format= 'YYYY-MM-DD HH24:MI:SS', **iargs):
        c1 = connection.cursor()
        sql = "INSERT INTO DT_EVENT "
        col = "(COMMONS_ID,EVENT_ID, "
        vals = " VALUES (:COMMONS_ID,:EVENT_ID, "
        first=True
        param={}
        param['COMMONS_ID'] = COMMONS_ID
        param['EVENT_ID'] = EVENT_ID
        for colname,val in iargs.items():
            if not first:
                col=col + ", "
                vals=vals + ", "
            first=False
            col = col + colname
            if (colname == EVENT_DATE):
                vals = vals + ' to_date(:' + colname + ' ,' + datetime_format + ')'
            else:
                vals = vals + ':' + colname
            param[colname]=val
        sql = sql + col + ")" + vals + ")"
        c1.execute(sql,param)
        connection.commit()

    #@transaction.commit_on_success()
    def delete(self,COMMONS_ID, EVENT_ID):
        c1 = connection.cursor()
        param={}
        param['COMMONS_ID'] = COMMONS_ID
        param['EVENT_ID'] = EVENT_ID
        sql= 'DELETE FROM DT_EVENT'
        sql = sql + ' WHERE COMMONS_ID = :COMMONS_ID AND EVENT_ID = :EVENT_ID'
        c1.execute(sql, param)

class dt_file():
    def __init__(self):
        self.columnnames = ['FILE_ID','FILE_TYPE','FACILITY_ID','PLACE_TYPE','PLACE_CODE','PLACE_SUBCODE','FILE_DATE','FILE_NAME','REMARK','EBATCH','CONTENT']
        self.pkeys =['FILE_ID']
    def printset(self,cur,header=True):
        if header:
            print tuple(self.columnnames)
        for row in cur:
            print row
    def selectpkey(self,FILE_ID):
        c1= connection.cursor()
        sql = "SELECT FILE_ID, FILE_TYPE, FACILITY_ID, PLACE_TYPE, PLACE_CODE, PLACE_SUBCODE, FILE_DATE, FILE_NAME, REMARK, EBATCH, CONTENT FROM DT_FILE"
        sql = sql + " WHERE FILE_ID = :FILE_ID"
        param ={'FILE_ID' : FILE_ID}
        c1.execute(sql, param)
        return c1
    def select(self,**where):
        c1 = connection.cursor()
        sql = "SELECT FILE_ID, FILE_TYPE, FACILITY_ID, PLACE_TYPE, PLACE_CODE, PLACE_SUBCODE, FILE_DATE, FILE_NAME, REMARK, EBATCH, CONTENT FROM DT_FILE "
        first=True
        param={}
        for colname,val in where.items():
            if first:
                sql=sql + "WHERE "
            if not first:
                sql=sql + " AND "
            first=False
            if val[0].upper().strip()=='IS':
                sql=sql + colname + " IS NULL"
            else:
                sql = sql + colname + val[0] + " :" + colname
                param[colname]=val[1]
        c1.execute(sql, param)
        return c1
    #@transaction.commit_on_success()
    def update(self, FILE_ID, datetime_format= 'YYYY-MM-DD HH24:MI:SS', **uargs):
        c1 = connection.cursor()
        param={}
        sql = "UPDATE DT_FILE SET "
        where = " WHERE FILE_ID = :FILE_ID"
        param['FILE_ID'] = FILE_ID
        first=True
        for colname,val in uargs.items():
            if not first:
                sql=sql + ", "
            first=False
            if (colname == FILE_DATE):
                sql =sql +  colname + ' = to_date(:' + colname + ' ,' + datetime_format + ')'
            else:
                sql =sql +  colname + ' = :' + colname
            param[colname]=val
        sql = sql + where
        c1.execute(sql, param)
        connection.commit()


    #@transaction.commit_on_success()
    def insert(self, FILE_ID, datetime_format= 'YYYY-MM-DD HH24:MI:SS', **iargs):
        c1 = connection.cursor()
        sql = "INSERT INTO DT_FILE "
        col = "(FILE_ID, "
        vals = " VALUES (:FILE_ID, "
        first=True
        param={}
        param['FILE_ID'] = FILE_ID
        for colname,val in iargs.items():
            if not first:
                col=col + ", "
                vals=vals + ", "
            first=False
            col = col + colname
            if (colname == FILE_DATE):
                vals = vals + ' to_date(:' + colname + ' ,' + datetime_format + ')'
            else:
                vals = vals + ':' + colname
            param[colname]=val
        sql = sql + col + ")" + vals + ")"
        c1.execute(sql,param)
        connection.commit()

    #@transaction.commit_on_success()
    def delete(self,FILE_ID):
        c1 = connection.cursor()
        param={}
        param['FILE_ID'] = FILE_ID
        sql= 'DELETE FROM DT_FILE'
        sql = sql + ' WHERE FILE_ID = :FILE_ID'
        c1.execute(sql, param)

class dt_location():
    def __init__(self):
        self.columnnames = ['COMMONS_ID','LOC_ID','LOC_NAME','DATA_PROVIDER','LOC_DESC','LOC_TYPE','LOC_PURPOSE','LOC_COUNTY','LOC_DISTRICT','LOC_STATE','LAT','LON','NORTHBOUNDING','SOUTHBOUNDING','EASTBOUNDING','WESTBOUNDING','REMARK','START_DATE','END_DATE','COORD_SYSTEM','PROJECTION','LOC_ORDER','BASE_LOC_ID']
        self.pkeys =['COMMONS_ID','LOC_ID']
    def printset(self,cur,header=True):
        if header:
            print tuple(self.columnnames)
        for row in cur:
            print row
    def selectpkey(self,COMMONS_ID,LOC_ID):
        c1= connection.cursor()
        sql = "SELECT COMMONS_ID, LOC_ID, LOC_NAME, DATA_PROVIDER, LOC_DESC, LOC_TYPE, LOC_PURPOSE, LOC_COUNTY, LOC_DISTRICT, LOC_STATE, LAT, LON, NORTHBOUNDING, SOUTHBOUNDING, EASTBOUNDING, WESTBOUNDING, REMARK, START_DATE, END_DATE, COORD_SYSTEM, PROJECTION, LOC_ORDER, BASE_LOC_ID FROM DT_LOCATION"
        sql = sql + " WHERE COMMONS_ID = :COMMONS_ID AND LOC_ID = :LOC_ID"
        param ={'COMMONS_ID' : COMMONS_ID, 'LOC_ID' : LOC_ID}
        c1.execute(sql, param)
        return c1
    def select(self,**where):
        c1 = connection.cursor()
        sql = "SELECT COMMONS_ID, LOC_ID, LOC_NAME, DATA_PROVIDER, LOC_DESC, LOC_TYPE, LOC_PURPOSE, LOC_COUNTY, LOC_DISTRICT, LOC_STATE, LAT, LON, NORTHBOUNDING, SOUTHBOUNDING, EASTBOUNDING, WESTBOUNDING, REMARK, START_DATE, END_DATE, COORD_SYSTEM, PROJECTION, LOC_ORDER, BASE_LOC_ID FROM DT_LOCATION "
        first=True
        param={}
        for colname,val in where.items():
            if first:
                sql=sql + "WHERE "
            if not first:
                sql=sql + " AND "
            first=False
            if val[0].upper().strip()=='IS':
                sql=sql + colname + " IS NULL"
            else:
                sql = sql + colname + val[0] + " :" + colname
                param[colname]=val[1]
        c1.execute(sql, param)
        return c1
    #@transaction.commit_on_success()
    def update(self, COMMONS_ID, LOC_ID, datetime_format= 'YYYY-MM-DD HH24:MI:SS', **uargs):
        c1 = connection.cursor()
        param={}
        sql = "UPDATE DT_LOCATION SET "
        where = " WHERE COMMONS_ID = :COMMONS_ID AND LOC_ID = :LOC_ID"
        param['COMMONS_ID'] = COMMONS_ID
        param['LOC_ID'] = LOC_ID
        first=True
        for colname,val in uargs.items():
            if not first:
                sql=sql + ", "
            first=False
            if (colname == START_DATEcolname == END_DATE):
                sql =sql +  colname + ' = to_date(:' + colname + ' ,' + datetime_format + ')'
            else:
                sql =sql +  colname + ' = :' + colname
            param[colname]=val
        sql = sql + where
        c1.execute(sql, param)
        connection.commit()


    #@transaction.commit_on_success()
    def insert(self, COMMONS_ID, LOC_ID, datetime_format= 'YYYY-MM-DD HH24:MI:SS', **iargs):
        c1 = connection.cursor()
        sql = "INSERT INTO DT_LOCATION "
        col = "(COMMONS_ID,LOC_ID, "
        vals = " VALUES (:COMMONS_ID,:LOC_ID, "
        first=True
        param={}
        param['COMMONS_ID'] = COMMONS_ID
        param['LOC_ID'] = LOC_ID
        for colname,val in iargs.items():
            if not first:
                col=col + ", "
                vals=vals + ", "
            first=False
            col = col + colname
            if (colname == START_DATEcolname == END_DATE):
                vals = vals + ' to_date(:' + colname + ' ,' + datetime_format + ')'
            else:
                vals = vals + ':' + colname
            param[colname]=val
        sql = sql + col + ")" + vals + ")"
        c1.execute(sql,param)
        connection.commit()

    #@transaction.commit_on_success()
    def delete(self,COMMONS_ID, LOC_ID):
        c1 = connection.cursor()
        param={}
        param['COMMONS_ID'] = COMMONS_ID
        param['LOC_ID'] = LOC_ID
        sql= 'DELETE FROM DT_LOCATION'
        sql = sql + ' WHERE COMMONS_ID = :COMMONS_ID AND LOC_ID = :LOC_ID'
        c1.execute(sql, param)

class dt_location_parameter():
    def __init__(self):
        self.columnnames = ['COMMONS_ID','LOC_ID','PARAM_ID','PARAM_NAME','PARAM_VALUE','PARAM_UNIT','REMARK']
        self.pkeys =['COMMONS_ID','LOC_ID','PARAM_ID']
    def printset(self,cur,header=True):
        if header:
            print tuple(self.columnnames)
        for row in cur:
            print row
    def selectpkey(self,COMMONS_ID,LOC_ID,PARAM_ID):
        c1= connection.cursor()
        sql = "SELECT COMMONS_ID, LOC_ID, PARAM_ID, PARAM_NAME, PARAM_VALUE, PARAM_UNIT, REMARK FROM DT_LOCATION_PARAMETER"
        sql = sql + " WHERE COMMONS_ID = :COMMONS_ID AND LOC_ID = :LOC_ID AND PARAM_ID = :PARAM_ID"
        param ={'COMMONS_ID' : COMMONS_ID, 'LOC_ID' : LOC_ID, 'PARAM_ID' : PARAM_ID}
        c1.execute(sql, param)
        return c1
    def select(self,**where):
        c1 = connection.cursor()
        sql = "SELECT COMMONS_ID, LOC_ID, PARAM_ID, PARAM_NAME, PARAM_VALUE, PARAM_UNIT, REMARK FROM DT_LOCATION_PARAMETER "
        first=True
        param={}
        for colname,val in where.items():
            if first:
                sql=sql + "WHERE "
            if not first:
                sql=sql + " AND "
            first=False
            if val[0].upper().strip()=='IS':
                sql=sql + colname + " IS NULL"
            else:
                sql = sql + colname + val[0] + " :" + colname
                param[colname]=val[1]
        c1.execute(sql, param)
        return c1
    #@transaction.commit_on_success()
    def update(self, COMMONS_ID, LOC_ID, PARAM_ID, **uargs):
        c1 = connection.cursor()
        param={}
        sql = "UPDATE DT_LOCATION_PARAMETER SET "
        where = " WHERE COMMONS_ID = :COMMONS_ID AND LOC_ID = :LOC_ID AND PARAM_ID = :PARAM_ID"
        param['COMMONS_ID'] = COMMONS_ID
        param['LOC_ID'] = LOC_ID
        param['PARAM_ID'] = PARAM_ID
        first=True
        for colname,val in uargs.items():
            if not first:
                sql=sql + ", "
            first=False
            sql =sql +  colname + ' = :' + colname
            param[colname]=val
        sql = sql + where
        c1.execute(sql, param)
        connection.commit()


    #@transaction.commit_on_success()
    def insert(self, COMMONS_ID, LOC_ID, PARAM_ID, **iargs):
        c1 = connection.cursor()
        sql = "INSERT INTO DT_LOCATION_PARAMETER "
        col = "(COMMONS_ID,LOC_ID,PARAM_ID, "
        vals = " VALUES (:COMMONS_ID,:LOC_ID,:PARAM_ID, "
        first=True
        param={}
        param['COMMONS_ID'] = COMMONS_ID
        param['LOC_ID'] = LOC_ID
        param['PARAM_ID'] = PARAM_ID
        for colname,val in iargs.items():
            if not first:
                col=col + ", "
                vals=vals + ", "
            first=False
            col = col + colname
            vals = vals + ':' + colname
            param[colname]=val
        sql = sql + col + ")" + vals + ")"
        c1.execute(sql,param)
        connection.commit()

    #@transaction.commit_on_success()
    def delete(self,COMMONS_ID, LOC_ID, PARAM_ID):
        c1 = connection.cursor()
        param={}
        param['COMMONS_ID'] = COMMONS_ID
        param['LOC_ID'] = LOC_ID
        param['PARAM_ID'] = PARAM_ID
        sql= 'DELETE FROM DT_LOCATION_PARAMETER'
        sql = sql + ' WHERE COMMONS_ID = :COMMONS_ID AND LOC_ID = :LOC_ID AND PARAM_ID = :PARAM_ID'
        c1.execute(sql, param)

class dt_person():
    def __init__(self):
        self.columnnames = ['PERSON_NAME','TITLE','ADDRESS1','ADDRESS2','CITY','STATE','POSTAL_CODE','COUNTRY','PHONE_NUMBER','FAX_NUMBER','ALT_PHONE_NUMBER','EMAIL_ADDRESS','COMPANY_CODE','PEOPLE_ID']
        self.pkeys =['PEOPLE_ID']
    def printset(self,cur,header=True):
        if header:
            print tuple(self.columnnames)
        for row in cur:
            print row
    def selectpkey(self,PEOPLE_ID):
        c1= connection.cursor()
        sql = "SELECT PERSON_NAME, TITLE, ADDRESS1, ADDRESS2, CITY, STATE, POSTAL_CODE, COUNTRY, PHONE_NUMBER, FAX_NUMBER, ALT_PHONE_NUMBER, EMAIL_ADDRESS, COMPANY_CODE, PEOPLE_ID FROM DT_PERSON"
        sql = sql + " WHERE PEOPLE_ID = :PEOPLE_ID"
        param ={'PEOPLE_ID' : PEOPLE_ID}
        c1.execute(sql, param)
        return c1
    def select(self,**where):
        c1 = connection.cursor()
        sql = "SELECT PERSON_NAME, TITLE, ADDRESS1, ADDRESS2, CITY, STATE, POSTAL_CODE, COUNTRY, PHONE_NUMBER, FAX_NUMBER, ALT_PHONE_NUMBER, EMAIL_ADDRESS, COMPANY_CODE, PEOPLE_ID FROM DT_PERSON "
        first=True
        param={}
        for colname,val in where.items():
            if first:
                sql=sql + "WHERE "
            if not first:
                sql=sql + " AND "
            first=False
            if val[0].upper().strip()=='IS':
                sql=sql + colname + " IS NULL"
            else:
                sql = sql + colname + val[0] + " :" + colname
                param[colname]=val[1]
        c1.execute(sql, param)
        return c1
    #@transaction.commit_on_success()
    def update(self, PEOPLE_ID, **uargs):
        c1 = connection.cursor()
        param={}
        sql = "UPDATE DT_PERSON SET "
        where = " WHERE PEOPLE_ID = :PEOPLE_ID"
        param['PEOPLE_ID'] = PEOPLE_ID
        first=True
        for colname,val in uargs.items():
            if not first:
                sql=sql + ", "
            first=False
            sql =sql +  colname + ' = :' + colname
            param[colname]=val
        sql = sql + where
        c1.execute(sql, param)
        connection.commit()


    #@transaction.commit_on_success()
    def insert(self, PEOPLE_ID, **iargs):
        c1 = connection.cursor()
        sql = "INSERT INTO DT_PERSON "
        col = "(PEOPLE_ID, "
        vals = " VALUES (:PEOPLE_ID, "
        first=True
        param={}
        param['PEOPLE_ID'] = PEOPLE_ID
        for colname,val in iargs.items():
            if not first:
                col=col + ", "
                vals=vals + ", "
            first=False
            col = col + colname
            vals = vals + ':' + colname
            param[colname]=val
        sql = sql + col + ")" + vals + ")"
        c1.execute(sql,param)
        connection.commit()

    #@transaction.commit_on_success()
    def delete(self,PEOPLE_ID):
        c1 = connection.cursor()
        param={}
        param['PEOPLE_ID'] = PEOPLE_ID
        sql= 'DELETE FROM DT_PERSON'
        sql = sql + ' WHERE PEOPLE_ID = :PEOPLE_ID'
        c1.execute(sql, param)

class dt_result():
    def __init__(self):
        self.columnnames = ['COMMONS_ID','EVENT_ID','VAR_ID','RESULT_TEXT','RESULT_NUMERIC','RESULT_ERROR','RESULT_DATE','STAT_RESULT','RESULT_ORDER','RESULT_UNIT','REMARK','VALUE_TYPE','STAT_TYPE','VALIDATED']
        self.pkeys =['COMMONS_ID','EVENT_ID','VAR_ID']
    def printset(self,cur,header=True):
        if header:
            print tuple(self.columnnames)
        for row in cur:
            print row
    def selectpkey(self,COMMONS_ID,EVENT_ID,VAR_ID):
        c1= connection.cursor()
        sql = "SELECT COMMONS_ID, EVENT_ID, VAR_ID, RESULT_TEXT, RESULT_NUMERIC, RESULT_ERROR, RESULT_DATE, STAT_RESULT, RESULT_ORDER, RESULT_UNIT, REMARK, VALUE_TYPE, STAT_TYPE, VALIDATED FROM DT_RESULT"
        sql = sql + " WHERE COMMONS_ID = :COMMONS_ID AND EVENT_ID = :EVENT_ID AND VAR_ID = :VAR_ID"
        param ={'COMMONS_ID' : COMMONS_ID, 'EVENT_ID' : EVENT_ID, 'VAR_ID' : VAR_ID}
        c1.execute(sql, param)
        return c1
    def select(self,**where):
        c1 = connection.cursor()
        sql = "SELECT COMMONS_ID, EVENT_ID, VAR_ID, RESULT_TEXT, RESULT_NUMERIC, RESULT_ERROR, RESULT_DATE, STAT_RESULT, RESULT_ORDER, RESULT_UNIT, REMARK, VALUE_TYPE, STAT_TYPE, VALIDATED FROM DT_RESULT "
        first=True
        param={}
        for colname,val in where.items():
            if first:
                sql=sql + "WHERE "
            if not first:
                sql=sql + " AND "
            first=False
            if val[0].upper().strip()=='IS':
                sql=sql + colname + " IS NULL"
            else:
                sql = sql + colname + val[0] + " :" + colname
                param[colname]=val[1]
        c1.execute(sql, param)
        return c1
    #@transaction.commit_on_success()
    def update(self, COMMONS_ID, EVENT_ID, VAR_ID, datetime_format= 'YYYY-MM-DD HH24:MI:SS', **uargs):
        c1 = connection.cursor()
        param={}
        sql = "UPDATE DT_RESULT SET "
        where = " WHERE COMMONS_ID = :COMMONS_ID AND EVENT_ID = :EVENT_ID AND VAR_ID = :VAR_ID"
        param['COMMONS_ID'] = COMMONS_ID
        param['EVENT_ID'] = EVENT_ID
        param['VAR_ID'] = VAR_ID
        first=True
        for colname,val in uargs.items():
            if not first:
                sql=sql + ", "
            first=False
            if (colname == RESULT_DATE):
                sql =sql +  colname + ' = to_date(:' + colname + ' ,' + datetime_format + ')'
            else:
                sql =sql +  colname + ' = :' + colname
            param[colname]=val
        sql = sql + where
        c1.execute(sql, param)
        connection.commit()


    #@transaction.commit_on_success()
    def insert(self, COMMONS_ID, EVENT_ID, VAR_ID, datetime_format= 'YYYY-MM-DD HH24:MI:SS', **iargs):
        c1 = connection.cursor()
        sql = "INSERT INTO DT_RESULT "
        col = "(COMMONS_ID,EVENT_ID,VAR_ID, "
        vals = " VALUES (:COMMONS_ID,:EVENT_ID,:VAR_ID, "
        first=True
        param={}
        param['COMMONS_ID'] = COMMONS_ID
        param['EVENT_ID'] = EVENT_ID
        param['VAR_ID'] = VAR_ID
        for colname,val in iargs.items():
            if not first:
                col=col + ", "
                vals=vals + ", "
            first=False
            col = col + colname
            if (colname == RESULT_DATE):
                vals = vals + ' to_date(:' + colname + ' ,' + datetime_format + ')'
            else:
                vals = vals + ':' + colname
            param[colname]=val
        sql = sql + col + ")" + vals + ")"
        c1.execute(sql,param)
        connection.commit()

    #@transaction.commit_on_success()
    def delete(self,COMMONS_ID, EVENT_ID, VAR_ID):
        c1 = connection.cursor()
        param={}
        param['COMMONS_ID'] = COMMONS_ID
        param['EVENT_ID'] = EVENT_ID
        param['VAR_ID'] = VAR_ID
        sql= 'DELETE FROM DT_RESULT'
        sql = sql + ' WHERE COMMONS_ID = :COMMONS_ID AND EVENT_ID = :EVENT_ID AND VAR_ID = :VAR_ID'
        c1.execute(sql, param)

class dt_type():
    def __init__(self):
        self.columnnames = ['TYPE_ID','TYPE_NAME','PRODUCT','DESCRIPTION','RESOLUTION','RES_UNIT','OBJECT_TYPE','OBJECT_DATA_OPT1','OBJECT_DATA_OPT1_UNIT']
        self.pkeys =['TYPE_ID']
    def printset(self,cur,header=True):
        if header:
            print tuple(self.columnnames)
        for row in cur:
            print row
    def selectpkey(self,TYPE_ID):
        c1= connection.cursor()
        sql = "SELECT TYPE_ID, TYPE_NAME, PRODUCT, DESCRIPTION, RESOLUTION, RES_UNIT, OBJECT_TYPE, OBJECT_DATA_OPT1, OBJECT_DATA_OPT1_UNIT FROM DT_TYPE"
        sql = sql + " WHERE TYPE_ID = :TYPE_ID"
        param ={'TYPE_ID' : TYPE_ID}
        c1.execute(sql, param)
        return c1
    def select(self,**where):
        c1 = connection.cursor()
        sql = "SELECT TYPE_ID, TYPE_NAME, PRODUCT, DESCRIPTION, RESOLUTION, RES_UNIT, OBJECT_TYPE, OBJECT_DATA_OPT1, OBJECT_DATA_OPT1_UNIT FROM DT_TYPE "
        first=True
        param={}
        for colname,val in where.items():
            if first:
                sql=sql + "WHERE "
            if not first:
                sql=sql + " AND "
            first=False
            if val[0].upper().strip()=='IS':
                sql=sql + colname + " IS NULL"
            else:
                sql = sql + colname + val[0] + " :" + colname
                param[colname]=val[1]
        c1.execute(sql, param)
        return c1
    #@transaction.commit_on_success()
    def update(self, TYPE_ID, **uargs):
        c1 = connection.cursor()
        param={}
        sql = "UPDATE DT_TYPE SET "
        where = " WHERE TYPE_ID = :TYPE_ID"
        param['TYPE_ID'] = TYPE_ID
        first=True
        for colname,val in uargs.items():
            if not first:
                sql=sql + ", "
            first=False
            sql =sql +  colname + ' = :' + colname
            param[colname]=val
        sql = sql + where
        c1.execute(sql, param)
        connection.commit()


    #@transaction.commit_on_success()
    def insert(self, TYPE_ID, **iargs):
        c1 = connection.cursor()
        sql = "INSERT INTO DT_TYPE "
        col = "(TYPE_ID, "
        vals = " VALUES (:TYPE_ID, "
        first=True
        param={}
        param['TYPE_ID'] = TYPE_ID
        for colname,val in iargs.items():
            if not first:
                col=col + ", "
                vals=vals + ", "
            first=False
            col = col + colname
            vals = vals + ':' + colname
            param[colname]=val
        sql = sql + col + ")" + vals + ")"
        c1.execute(sql,param)
        connection.commit()

    #@transaction.commit_on_success()
    def delete(self,TYPE_ID):
        c1 = connection.cursor()
        param={}
        param['TYPE_ID'] = TYPE_ID
        sql= 'DELETE FROM DT_TYPE'
        sql = sql + ' WHERE TYPE_ID = :TYPE_ID'
        c1.execute(sql, param)

class rt_company():
    def __init__(self):
        self.columnnames = ['COMPANY_CODE','COMPANY_TYPE','COMPANY_NAME','CONTACT_NAME','LICENSE_NBR','ADDRESS_1','ADDRESS_2','CITY','COUNTY','STATE','COUNTRY','POSTAL_CODE','PHONE_NUMBER','ALT_PHONE_NUMBER','FAX_NUMBER','EMAIL_ADDRESS','CUSTOM_FIELD_1','CUSTOM_FIELD_2','CUSTOM_FIELD_3','CUSTOM_FIELD_4','CUSTOM_FIELD_5','STATUS_FLAG','EBATCH','REMARK']
        self.pkeys =['COMPANY_CODE']
    def printset(self,cur,header=True):
        if header:
            print tuple(self.columnnames)
        for row in cur:
            print row
    def selectpkey(self,COMPANY_CODE):
        c1= connection.cursor()
        sql = "SELECT COMPANY_CODE, COMPANY_TYPE, COMPANY_NAME, CONTACT_NAME, LICENSE_NBR, ADDRESS_1, ADDRESS_2, CITY, COUNTY, STATE, COUNTRY, POSTAL_CODE, PHONE_NUMBER, ALT_PHONE_NUMBER, FAX_NUMBER, EMAIL_ADDRESS, CUSTOM_FIELD_1, CUSTOM_FIELD_2, CUSTOM_FIELD_3, CUSTOM_FIELD_4, CUSTOM_FIELD_5, STATUS_FLAG, EBATCH, REMARK FROM RT_COMPANY"
        sql = sql + " WHERE COMPANY_CODE = :COMPANY_CODE"
        param ={'COMPANY_CODE' : COMPANY_CODE}
        c1.execute(sql, param)
        return c1
    def select(self,**where):
        c1 = connection.cursor()
        sql = "SELECT COMPANY_CODE, COMPANY_TYPE, COMPANY_NAME, CONTACT_NAME, LICENSE_NBR, ADDRESS_1, ADDRESS_2, CITY, COUNTY, STATE, COUNTRY, POSTAL_CODE, PHONE_NUMBER, ALT_PHONE_NUMBER, FAX_NUMBER, EMAIL_ADDRESS, CUSTOM_FIELD_1, CUSTOM_FIELD_2, CUSTOM_FIELD_3, CUSTOM_FIELD_4, CUSTOM_FIELD_5, STATUS_FLAG, EBATCH, REMARK FROM RT_COMPANY "
        first=True
        param={}
        for colname,val in where.items():
            if first:
                sql=sql + "WHERE "
            if not first:
                sql=sql + " AND "
            first=False
            if val[0].upper().strip()=='IS':
                sql=sql + colname + " IS NULL"
            else:
                sql = sql + colname + val[0] + " :" + colname
                param[colname]=val[1]
        c1.execute(sql, param)
        return c1
    #@transaction.commit_on_success()
    def update(self, COMPANY_CODE, **uargs):
        c1 = connection.cursor()
        param={}
        sql = "UPDATE RT_COMPANY SET "
        where = " WHERE COMPANY_CODE = :COMPANY_CODE"
        param['COMPANY_CODE'] = COMPANY_CODE
        first=True
        for colname,val in uargs.items():
            if not first:
                sql=sql + ", "
            first=False
            sql =sql +  colname + ' = :' + colname
            param[colname]=val
        sql = sql + where
        c1.execute(sql, param)
        connection.commit()


    #@transaction.commit_on_success()
    def insert(self, COMPANY_CODE, **iargs):
        c1 = connection.cursor()
        sql = "INSERT INTO RT_COMPANY "
        col = "(COMPANY_CODE, "
        vals = " VALUES (:COMPANY_CODE, "
        first=True
        param={}
        param['COMPANY_CODE'] = COMPANY_CODE
        for colname,val in iargs.items():
            if not first:
                col=col + ", "
                vals=vals + ", "
            first=False
            col = col + colname
            vals = vals + ':' + colname
            param[colname]=val
        sql = sql + col + ")" + vals + ")"
        c1.execute(sql,param)
        connection.commit()

    #@transaction.commit_on_success()
    def delete(self,COMPANY_CODE):
        c1 = connection.cursor()
        param={}
        param['COMPANY_CODE'] = COMPANY_CODE
        sql= 'DELETE FROM RT_COMPANY'
        sql = sql + ' WHERE COMPANY_CODE = :COMPANY_CODE'
        c1.execute(sql, param)

class rt_company_type():
    def __init__(self):
        self.columnnames = ['COMPANY_TYPE','COMPANY_TYPE_DESC','STATUS_FLAG','EBATCH','REMARK']
        self.pkeys =['COMPANY_TYPE']
    def printset(self,cur,header=True):
        if header:
            print tuple(self.columnnames)
        for row in cur:
            print row
    def selectpkey(self,COMPANY_TYPE):
        c1= connection.cursor()
        sql = "SELECT COMPANY_TYPE, COMPANY_TYPE_DESC, STATUS_FLAG, EBATCH, REMARK FROM RT_COMPANY_TYPE"
        sql = sql + " WHERE COMPANY_TYPE = :COMPANY_TYPE"
        param ={'COMPANY_TYPE' : COMPANY_TYPE}
        c1.execute(sql, param)
        return c1
    def select(self,**where):
        c1 = connection.cursor()
        sql = "SELECT COMPANY_TYPE, COMPANY_TYPE_DESC, STATUS_FLAG, EBATCH, REMARK FROM RT_COMPANY_TYPE "
        first=True
        param={}
        for colname,val in where.items():
            if first:
                sql=sql + "WHERE "
            if not first:
                sql=sql + " AND "
            first=False
            if val[0].upper().strip()=='IS':
                sql=sql + colname + " IS NULL"
            else:
                sql = sql + colname + val[0] + " :" + colname
                param[colname]=val[1]
        c1.execute(sql, param)
        return c1
    #@transaction.commit_on_success()
    def update(self, COMPANY_TYPE, **uargs):
        c1 = connection.cursor()
        param={}
        sql = "UPDATE RT_COMPANY_TYPE SET "
        where = " WHERE COMPANY_TYPE = :COMPANY_TYPE"
        param['COMPANY_TYPE'] = COMPANY_TYPE
        first=True
        for colname,val in uargs.items():
            if not first:
                sql=sql + ", "
            first=False
            sql =sql +  colname + ' = :' + colname
            param[colname]=val
        sql = sql + where
        c1.execute(sql, param)
        connection.commit()


    #@transaction.commit_on_success()
    def insert(self, COMPANY_TYPE, **iargs):
        c1 = connection.cursor()
        sql = "INSERT INTO RT_COMPANY_TYPE "
        col = "(COMPANY_TYPE, "
        vals = " VALUES (:COMPANY_TYPE, "
        first=True
        param={}
        param['COMPANY_TYPE'] = COMPANY_TYPE
        for colname,val in iargs.items():
            if not first:
                col=col + ", "
                vals=vals + ", "
            first=False
            col = col + colname
            vals = vals + ':' + colname
            param[colname]=val
        sql = sql + col + ")" + vals + ")"
        c1.execute(sql,param)
        connection.commit()

    #@transaction.commit_on_success()
    def delete(self,COMPANY_TYPE):
        c1 = connection.cursor()
        param={}
        param['COMPANY_TYPE'] = COMPANY_TYPE
        sql= 'DELETE FROM RT_COMPANY_TYPE'
        sql = sql + ' WHERE COMPANY_TYPE = :COMPANY_TYPE'
        c1.execute(sql, param)

class rt_file_type():
    def __init__(self):
        self.columnnames = ['FILE_TYPE','APP_CODE','FILE_TYPE_DESC','STATUS_FLAG','EBATCH','REMARK','MIME_TYPE']
        self.pkeys =['FILE_TYPE']
    def printset(self,cur,header=True):
        if header:
            print tuple(self.columnnames)
        for row in cur:
            print row
    def selectpkey(self,FILE_TYPE):
        c1= connection.cursor()
        sql = "SELECT FILE_TYPE, APP_CODE, FILE_TYPE_DESC, STATUS_FLAG, EBATCH, REMARK, MIME_TYPE FROM RT_FILE_TYPE"
        sql = sql + " WHERE FILE_TYPE = :FILE_TYPE"
        param ={'FILE_TYPE' : FILE_TYPE}
        c1.execute(sql, param)
        return c1
    def select(self,**where):
        c1 = connection.cursor()
        sql = "SELECT FILE_TYPE, APP_CODE, FILE_TYPE_DESC, STATUS_FLAG, EBATCH, REMARK, MIME_TYPE FROM RT_FILE_TYPE "
        first=True
        param={}
        for colname,val in where.items():
            if first:
                sql=sql + "WHERE "
            if not first:
                sql=sql + " AND "
            first=False
            if val[0].upper().strip()=='IS':
                sql=sql + colname + " IS NULL"
            else:
                sql = sql + colname + val[0] + " :" + colname
                param[colname]=val[1]
        c1.execute(sql, param)
        return c1
    #@transaction.commit_on_success()
    def update(self, FILE_TYPE, **uargs):
        c1 = connection.cursor()
        param={}
        sql = "UPDATE RT_FILE_TYPE SET "
        where = " WHERE FILE_TYPE = :FILE_TYPE"
        param['FILE_TYPE'] = FILE_TYPE
        first=True
        for colname,val in uargs.items():
            if not first:
                sql=sql + ", "
            first=False
            sql =sql +  colname + ' = :' + colname
            param[colname]=val
        sql = sql + where
        c1.execute(sql, param)
        connection.commit()


    #@transaction.commit_on_success()
    def insert(self, FILE_TYPE, **iargs):
        c1 = connection.cursor()
        sql = "INSERT INTO RT_FILE_TYPE "
        col = "(FILE_TYPE, "
        vals = " VALUES (:FILE_TYPE, "
        first=True
        param={}
        param['FILE_TYPE'] = FILE_TYPE
        for colname,val in iargs.items():
            if not first:
                col=col + ", "
                vals=vals + ", "
            first=False
            col = col + colname
            vals = vals + ':' + colname
            param[colname]=val
        sql = sql + col + ")" + vals + ")"
        c1.execute(sql,param)
        connection.commit()

    #@transaction.commit_on_success()
    def delete(self,FILE_TYPE):
        c1 = connection.cursor()
        param={}
        param['FILE_TYPE'] = FILE_TYPE
        sql= 'DELETE FROM RT_FILE_TYPE'
        sql = sql + ' WHERE FILE_TYPE = :FILE_TYPE'
        c1.execute(sql, param)

class rt_location_param_type():
    def __init__(self):
        self.columnnames = ['PARAM_CODE','PARAM_DESC','STATUS_FLAG','EBATCH','STANDARD_UNIT','REMARK']
        self.pkeys =['PARAM_CODE']
    def printset(self,cur,header=True):
        if header:
            print tuple(self.columnnames)
        for row in cur:
            print row
    def selectpkey(self,PARAM_CODE):
        c1= connection.cursor()
        sql = "SELECT PARAM_CODE, PARAM_DESC, STATUS_FLAG, EBATCH, STANDARD_UNIT, REMARK FROM RT_LOCATION_PARAM_TYPE"
        sql = sql + " WHERE PARAM_CODE = :PARAM_CODE"
        param ={'PARAM_CODE' : PARAM_CODE}
        c1.execute(sql, param)
        return c1
    def select(self,**where):
        c1 = connection.cursor()
        sql = "SELECT PARAM_CODE, PARAM_DESC, STATUS_FLAG, EBATCH, STANDARD_UNIT, REMARK FROM RT_LOCATION_PARAM_TYPE "
        first=True
        param={}
        for colname,val in where.items():
            if first:
                sql=sql + "WHERE "
            if not first:
                sql=sql + " AND "
            first=False
            if val[0].upper().strip()=='IS':
                sql=sql + colname + " IS NULL"
            else:
                sql = sql + colname + val[0] + " :" + colname
                param[colname]=val[1]
        c1.execute(sql, param)
        return c1
    #@transaction.commit_on_success()
    def update(self, PARAM_CODE, **uargs):
        c1 = connection.cursor()
        param={}
        sql = "UPDATE RT_LOCATION_PARAM_TYPE SET "
        where = " WHERE PARAM_CODE = :PARAM_CODE"
        param['PARAM_CODE'] = PARAM_CODE
        first=True
        for colname,val in uargs.items():
            if not first:
                sql=sql + ", "
            first=False
            sql =sql +  colname + ' = :' + colname
            param[colname]=val
        sql = sql + where
        c1.execute(sql, param)
        connection.commit()


    #@transaction.commit_on_success()
    def insert(self, PARAM_CODE, **iargs):
        c1 = connection.cursor()
        sql = "INSERT INTO RT_LOCATION_PARAM_TYPE "
        col = "(PARAM_CODE, "
        vals = " VALUES (:PARAM_CODE, "
        first=True
        param={}
        param['PARAM_CODE'] = PARAM_CODE
        for colname,val in iargs.items():
            if not first:
                col=col + ", "
                vals=vals + ", "
            first=False
            col = col + colname
            vals = vals + ':' + colname
            param[colname]=val
        sql = sql + col + ")" + vals + ")"
        c1.execute(sql,param)
        connection.commit()

    #@transaction.commit_on_success()
    def delete(self,PARAM_CODE):
        c1 = connection.cursor()
        param={}
        param['PARAM_CODE'] = PARAM_CODE
        sql= 'DELETE FROM RT_LOCATION_PARAM_TYPE'
        sql = sql + ' WHERE PARAM_CODE = :PARAM_CODE'
        c1.execute(sql, param)

class rt_location_type():
    def __init__(self):
        self.columnnames = ['LOCATION_TYPE_CODE','LOCATION_TYPE_DESC','STATUS_FLAG','REMARK']
        self.pkeys =['LOCATION_TYPE_CODE']
    def printset(self,cur,header=True):
        if header:
            print tuple(self.columnnames)
        for row in cur:
            print row
    def selectpkey(self,LOCATION_TYPE_CODE):
        c1= connection.cursor()
        sql = "SELECT LOCATION_TYPE_CODE, LOCATION_TYPE_DESC, STATUS_FLAG, REMARK FROM RT_LOCATION_TYPE"
        sql = sql + " WHERE LOCATION_TYPE_CODE = :LOCATION_TYPE_CODE"
        param ={'LOCATION_TYPE_CODE' : LOCATION_TYPE_CODE}
        c1.execute(sql, param)
        return c1
    def select(self,**where):
        c1 = connection.cursor()
        sql = "SELECT LOCATION_TYPE_CODE, LOCATION_TYPE_DESC, STATUS_FLAG, REMARK FROM RT_LOCATION_TYPE "
        first=True
        param={}
        for colname,val in where.items():
            if first:
                sql=sql + "WHERE "
            if not first:
                sql=sql + " AND "
            first=False
            if val[0].upper().strip()=='IS':
                sql=sql + colname + " IS NULL"
            else:
                sql = sql + colname + val[0] + " :" + colname
                param[colname]=val[1]
        c1.execute(sql, param)
        return c1
    #@transaction.commit_on_success()
    def update(self, LOCATION_TYPE_CODE, **uargs):
        c1 = connection.cursor()
        param={}
        sql = "UPDATE RT_LOCATION_TYPE SET "
        where = " WHERE LOCATION_TYPE_CODE = :LOCATION_TYPE_CODE"
        param['LOCATION_TYPE_CODE'] = LOCATION_TYPE_CODE
        first=True
        for colname,val in uargs.items():
            if not first:
                sql=sql + ", "
            first=False
            sql =sql +  colname + ' = :' + colname
            param[colname]=val
        sql = sql + where
        c1.execute(sql, param)
        connection.commit()


    #@transaction.commit_on_success()
    def insert(self, LOCATION_TYPE_CODE, **iargs):
        c1 = connection.cursor()
        sql = "INSERT INTO RT_LOCATION_TYPE "
        col = "(LOCATION_TYPE_CODE, "
        vals = " VALUES (:LOCATION_TYPE_CODE, "
        first=True
        param={}
        param['LOCATION_TYPE_CODE'] = LOCATION_TYPE_CODE
        for colname,val in iargs.items():
            if not first:
                col=col + ", "
                vals=vals + ", "
            first=False
            col = col + colname
            vals = vals + ':' + colname
            param[colname]=val
        sql = sql + col + ")" + vals + ")"
        c1.execute(sql,param)
        connection.commit()

    #@transaction.commit_on_success()
    def delete(self,LOCATION_TYPE_CODE):
        c1 = connection.cursor()
        param={}
        param['LOCATION_TYPE_CODE'] = LOCATION_TYPE_CODE
        sql= 'DELETE FROM RT_LOCATION_TYPE'
        sql = sql + ' WHERE LOCATION_TYPE_CODE = :LOCATION_TYPE_CODE'
        c1.execute(sql, param)

class rt_method():
    def __init__(self):
        self.columnnames = ['METHOD_CODE','METHOD_NAME','STATUS_FLAG','BASE_METHOD','REMARK','METHOD_DESC']
        self.pkeys =['METHOD_CODE']
    def printset(self,cur,header=True):
        if header:
            print tuple(self.columnnames)
        for row in cur:
            print row
    def selectpkey(self,METHOD_CODE):
        c1= connection.cursor()
        sql = "SELECT METHOD_CODE, METHOD_NAME, STATUS_FLAG, BASE_METHOD, REMARK, METHOD_DESC FROM RT_METHOD"
        sql = sql + " WHERE METHOD_CODE = :METHOD_CODE"
        param ={'METHOD_CODE' : METHOD_CODE}
        c1.execute(sql, param)
        return c1
    def select(self,**where):
        c1 = connection.cursor()
        sql = "SELECT METHOD_CODE, METHOD_NAME, STATUS_FLAG, BASE_METHOD, REMARK, METHOD_DESC FROM RT_METHOD "
        first=True
        param={}
        for colname,val in where.items():
            if first:
                sql=sql + "WHERE "
            if not first:
                sql=sql + " AND "
            first=False
            if val[0].upper().strip()=='IS':
                sql=sql + colname + " IS NULL"
            else:
                sql = sql + colname + val[0] + " :" + colname
                param[colname]=val[1]
        c1.execute(sql, param)
        return c1
    #@transaction.commit_on_success()
    def update(self, METHOD_CODE, **uargs):
        c1 = connection.cursor()
        param={}
        sql = "UPDATE RT_METHOD SET "
        where = " WHERE METHOD_CODE = :METHOD_CODE"
        param['METHOD_CODE'] = METHOD_CODE
        first=True
        for colname,val in uargs.items():
            if not first:
                sql=sql + ", "
            first=False
            sql =sql +  colname + ' = :' + colname
            param[colname]=val
        sql = sql + where
        c1.execute(sql, param)
        connection.commit()


    #@transaction.commit_on_success()
    def insert(self, METHOD_CODE, **iargs):
        c1 = connection.cursor()
        sql = "INSERT INTO RT_METHOD "
        col = "(METHOD_CODE, "
        vals = " VALUES (:METHOD_CODE, "
        first=True
        param={}
        param['METHOD_CODE'] = METHOD_CODE
        for colname,val in iargs.items():
            if not first:
                col=col + ", "
                vals=vals + ", "
            first=False
            col = col + colname
            vals = vals + ':' + colname
            param[colname]=val
        sql = sql + col + ")" + vals + ")"
        c1.execute(sql,param)
        connection.commit()

    #@transaction.commit_on_success()
    def delete(self,METHOD_CODE):
        c1 = connection.cursor()
        param={}
        param['METHOD_CODE'] = METHOD_CODE
        sql= 'DELETE FROM RT_METHOD'
        sql = sql + ' WHERE METHOD_CODE = :METHOD_CODE'
        c1.execute(sql, param)

class rt_result_type():
    def __init__(self):
        self.columnnames = ['RESULT_TYPE_CODE','RESULT_TYPE_DESC','STATUS_FLAG','EBATCH','REMARK']
        self.pkeys =['RESULT_TYPE_CODE']
    def printset(self,cur,header=True):
        if header:
            print tuple(self.columnnames)
        for row in cur:
            print row
    def selectpkey(self,RESULT_TYPE_CODE):
        c1= connection.cursor()
        sql = "SELECT RESULT_TYPE_CODE, RESULT_TYPE_DESC, STATUS_FLAG, EBATCH, REMARK FROM RT_RESULT_TYPE"
        sql = sql + " WHERE RESULT_TYPE_CODE = :RESULT_TYPE_CODE"
        param ={'RESULT_TYPE_CODE' : RESULT_TYPE_CODE}
        c1.execute(sql, param)
        return c1
    def select(self,**where):
        c1 = connection.cursor()
        sql = "SELECT RESULT_TYPE_CODE, RESULT_TYPE_DESC, STATUS_FLAG, EBATCH, REMARK FROM RT_RESULT_TYPE "
        first=True
        param={}
        for colname,val in where.items():
            if first:
                sql=sql + "WHERE "
            if not first:
                sql=sql + " AND "
            first=False
            if val[0].upper().strip()=='IS':
                sql=sql + colname + " IS NULL"
            else:
                sql = sql + colname + val[0] + " :" + colname
                param[colname]=val[1]
        c1.execute(sql, param)
        return c1
    #@transaction.commit_on_success()
    def update(self, RESULT_TYPE_CODE, **uargs):
        c1 = connection.cursor()
        param={}
        sql = "UPDATE RT_RESULT_TYPE SET "
        where = " WHERE RESULT_TYPE_CODE = :RESULT_TYPE_CODE"
        param['RESULT_TYPE_CODE'] = RESULT_TYPE_CODE
        first=True
        for colname,val in uargs.items():
            if not first:
                sql=sql + ", "
            first=False
            sql =sql +  colname + ' = :' + colname
            param[colname]=val
        sql = sql + where
        c1.execute(sql, param)
        connection.commit()


    #@transaction.commit_on_success()
    def insert(self, RESULT_TYPE_CODE, **iargs):
        c1 = connection.cursor()
        sql = "INSERT INTO RT_RESULT_TYPE "
        col = "(RESULT_TYPE_CODE, "
        vals = " VALUES (:RESULT_TYPE_CODE, "
        first=True
        param={}
        param['RESULT_TYPE_CODE'] = RESULT_TYPE_CODE
        for colname,val in iargs.items():
            if not first:
                col=col + ", "
                vals=vals + ", "
            first=False
            col = col + colname
            vals = vals + ':' + colname
            param[colname]=val
        sql = sql + col + ")" + vals + ")"
        c1.execute(sql,param)
        connection.commit()

    #@transaction.commit_on_success()
    def delete(self,RESULT_TYPE_CODE):
        c1 = connection.cursor()
        param={}
        param['RESULT_TYPE_CODE'] = RESULT_TYPE_CODE
        sql= 'DELETE FROM RT_RESULT_TYPE'
        sql = sql + ' WHERE RESULT_TYPE_CODE = :RESULT_TYPE_CODE'
        c1.execute(sql, param)

class rt_state():
    def __init__(self):
        self.columnnames = ['STATE_CODE','STATE_NAME','STATUS_FLAG','EBATCH','REMARK']
        self.pkeys =['STATE_CODE']
    def printset(self,cur,header=True):
        if header:
            print tuple(self.columnnames)
        for row in cur:
            print row
    def selectpkey(self,STATE_CODE):
        c1= connection.cursor()
        sql = "SELECT STATE_CODE, STATE_NAME, STATUS_FLAG, EBATCH, REMARK FROM RT_STATE"
        sql = sql + " WHERE STATE_CODE = :STATE_CODE"
        param ={'STATE_CODE' : STATE_CODE}
        c1.execute(sql, param)
        return c1
    def select(self,**where):
        c1 = connection.cursor()
        sql = "SELECT STATE_CODE, STATE_NAME, STATUS_FLAG, EBATCH, REMARK FROM RT_STATE "
        first=True
        param={}
        for colname,val in where.items():
            if first:
                sql=sql + "WHERE "
            if not first:
                sql=sql + " AND "
            first=False
            if val[0].upper().strip()=='IS':
                sql=sql + colname + " IS NULL"
            else:
                sql = sql + colname + val[0] + " :" + colname
                param[colname]=val[1]
        c1.execute(sql, param)
        return c1
    #@transaction.commit_on_success()
    def update(self, STATE_CODE, **uargs):
        c1 = connection.cursor()
        param={}
        sql = "UPDATE RT_STATE SET "
        where = " WHERE STATE_CODE = :STATE_CODE"
        param['STATE_CODE'] = STATE_CODE
        first=True
        for colname,val in uargs.items():
            if not first:
                sql=sql + ", "
            first=False
            sql =sql +  colname + ' = :' + colname
            param[colname]=val
        sql = sql + where
        c1.execute(sql, param)
        connection.commit()


    #@transaction.commit_on_success()
    def insert(self, STATE_CODE, **iargs):
        c1 = connection.cursor()
        sql = "INSERT INTO RT_STATE "
        col = "(STATE_CODE, "
        vals = " VALUES (:STATE_CODE, "
        first=True
        param={}
        param['STATE_CODE'] = STATE_CODE
        for colname,val in iargs.items():
            if not first:
                col=col + ", "
                vals=vals + ", "
            first=False
            col = col + colname
            vals = vals + ':' + colname
            param[colname]=val
        sql = sql + col + ")" + vals + ")"
        c1.execute(sql,param)
        connection.commit()

    #@transaction.commit_on_success()
    def delete(self,STATE_CODE):
        c1 = connection.cursor()
        param={}
        param['STATE_CODE'] = STATE_CODE
        sql= 'DELETE FROM RT_STATE'
        sql = sql + ' WHERE STATE_CODE = :STATE_CODE'
        c1.execute(sql, param)

class rt_unit():
    def __init__(self):
        self.columnnames = ['UNIT_CODE','UNIT_DESC','UNIT_TYPE','STATUS_FLAG','ESRI_XY','ESRI_Z','EBATCH','REMARK']
        self.pkeys =['UNIT_CODE']
    def printset(self,cur,header=True):
        if header:
            print tuple(self.columnnames)
        for row in cur:
            print row
    def selectpkey(self,UNIT_CODE):
        c1= connection.cursor()
        sql = "SELECT UNIT_CODE, UNIT_DESC, UNIT_TYPE, STATUS_FLAG, ESRI_XY, ESRI_Z, EBATCH, REMARK FROM RT_UNIT"
        sql = sql + " WHERE UNIT_CODE = :UNIT_CODE"
        param ={'UNIT_CODE' : UNIT_CODE}
        c1.execute(sql, param)
        return c1
    def select(self,**where):
        c1 = connection.cursor()
        sql = "SELECT UNIT_CODE, UNIT_DESC, UNIT_TYPE, STATUS_FLAG, ESRI_XY, ESRI_Z, EBATCH, REMARK FROM RT_UNIT "
        first=True
        param={}
        for colname,val in where.items():
            if first:
                sql=sql + "WHERE "
            if not first:
                sql=sql + " AND "
            first=False
            if val[0].upper().strip()=='IS':
                sql=sql + colname + " IS NULL"
            else:
                sql = sql + colname + val[0] + " :" + colname
                param[colname]=val[1]
        c1.execute(sql, param)
        return c1
    #@transaction.commit_on_success()
    def update(self, UNIT_CODE, **uargs):
        c1 = connection.cursor()
        param={}
        sql = "UPDATE RT_UNIT SET "
        where = " WHERE UNIT_CODE = :UNIT_CODE"
        param['UNIT_CODE'] = UNIT_CODE
        first=True
        for colname,val in uargs.items():
            if not first:
                sql=sql + ", "
            first=False
            sql =sql +  colname + ' = :' + colname
            param[colname]=val
        sql = sql + where
        c1.execute(sql, param)
        connection.commit()


    #@transaction.commit_on_success()
    def insert(self, UNIT_CODE, **iargs):
        c1 = connection.cursor()
        sql = "INSERT INTO RT_UNIT "
        col = "(UNIT_CODE, "
        vals = " VALUES (:UNIT_CODE, "
        first=True
        param={}
        param['UNIT_CODE'] = UNIT_CODE
        for colname,val in iargs.items():
            if not first:
                col=col + ", "
                vals=vals + ", "
            first=False
            col = col + colname
            vals = vals + ':' + colname
            param[colname]=val
        sql = sql + col + ")" + vals + ")"
        c1.execute(sql,param)
        connection.commit()

    #@transaction.commit_on_success()
    def delete(self,UNIT_CODE):
        c1 = connection.cursor()
        param={}
        param['UNIT_CODE'] = UNIT_CODE
        sql= 'DELETE FROM RT_UNIT'
        sql = sql + ' WHERE UNIT_CODE = :UNIT_CODE'
        c1.execute(sql, param)

class rt_unit_conversion_factor():
    def __init__(self):
        self.columnnames = ['REPORTED_UNIT','TARGET_UNIT','CONVERSION_FACTOR','DELTA','STATUS_FLAG','EBATCH','REMARK']
        self.pkeys =['REPORTED_UNIT','TARGET_UNIT']
    def printset(self,cur,header=True):
        if header:
            print tuple(self.columnnames)
        for row in cur:
            print row
    def selectpkey(self,REPORTED_UNIT,TARGET_UNIT):
        c1= connection.cursor()
        sql = "SELECT REPORTED_UNIT, TARGET_UNIT, CONVERSION_FACTOR, DELTA, STATUS_FLAG, EBATCH, REMARK FROM RT_UNIT_CONVERSION_FACTOR"
        sql = sql + " WHERE REPORTED_UNIT = :REPORTED_UNIT AND TARGET_UNIT = :TARGET_UNIT"
        param ={'REPORTED_UNIT' : REPORTED_UNIT, 'TARGET_UNIT' : TARGET_UNIT}
        c1.execute(sql, param)
        return c1
    def select(self,**where):
        c1 = connection.cursor()
        sql = "SELECT REPORTED_UNIT, TARGET_UNIT, CONVERSION_FACTOR, DELTA, STATUS_FLAG, EBATCH, REMARK FROM RT_UNIT_CONVERSION_FACTOR "
        first=True
        param={}
        for colname,val in where.items():
            if first:
                sql=sql + "WHERE "
            if not first:
                sql=sql + " AND "
            first=False
            if val[0].upper().strip()=='IS':
                sql=sql + colname + " IS NULL"
            else:
                sql = sql + colname + val[0] + " :" + colname
                param[colname]=val[1]
        c1.execute(sql, param)
        return c1
    #@transaction.commit_on_success()
    def update(self, REPORTED_UNIT, TARGET_UNIT, **uargs):
        c1 = connection.cursor()
        param={}
        sql = "UPDATE RT_UNIT_CONVERSION_FACTOR SET "
        where = " WHERE REPORTED_UNIT = :REPORTED_UNIT AND TARGET_UNIT = :TARGET_UNIT"
        param['REPORTED_UNIT'] = REPORTED_UNIT
        param['TARGET_UNIT'] = TARGET_UNIT
        first=True
        for colname,val in uargs.items():
            if not first:
                sql=sql + ", "
            first=False
            sql =sql +  colname + ' = :' + colname
            param[colname]=val
        sql = sql + where
        c1.execute(sql, param)
        connection.commit()


    #@transaction.commit_on_success()
    def insert(self, REPORTED_UNIT, TARGET_UNIT, **iargs):
        c1 = connection.cursor()
        sql = "INSERT INTO RT_UNIT_CONVERSION_FACTOR "
        col = "(REPORTED_UNIT,TARGET_UNIT, "
        vals = " VALUES (:REPORTED_UNIT,:TARGET_UNIT, "
        first=True
        param={}
        param['REPORTED_UNIT'] = REPORTED_UNIT
        param['TARGET_UNIT'] = TARGET_UNIT
        for colname,val in iargs.items():
            if not first:
                col=col + ", "
                vals=vals + ", "
            first=False
            col = col + colname
            vals = vals + ':' + colname
            param[colname]=val
        sql = sql + col + ")" + vals + ")"
        c1.execute(sql,param)
        connection.commit()

    #@transaction.commit_on_success()
    def delete(self,REPORTED_UNIT, TARGET_UNIT):
        c1 = connection.cursor()
        param={}
        param['REPORTED_UNIT'] = REPORTED_UNIT
        param['TARGET_UNIT'] = TARGET_UNIT
        sql= 'DELETE FROM RT_UNIT_CONVERSION_FACTOR'
        sql = sql + ' WHERE REPORTED_UNIT = :REPORTED_UNIT AND TARGET_UNIT = :TARGET_UNIT'
        c1.execute(sql, param)

class rt_varables():
    def __init__(self):
        self.columnnames = ['VAR_ID','VARABLE_NAME','SORT_ORDER','VARABLE_TYPE','STATUS_FLAG','VAR_SHORT_NAME','REMARK']
        self.pkeys =['VAR_ID']
    def printset(self,cur,header=True):
        if header:
            print tuple(self.columnnames)
        for row in cur:
            print row
    def selectpkey(self,VAR_ID):
        c1= connection.cursor()
        sql = "SELECT VAR_ID, VARABLE_NAME, SORT_ORDER, VARABLE_TYPE, STATUS_FLAG, VAR_SHORT_NAME, REMARK FROM RT_VARABLES"
        sql = sql + " WHERE VAR_ID = :VAR_ID"
        param ={'VAR_ID' : VAR_ID}
        c1.execute(sql, param)
        return c1
    def select(self,**where):
        c1 = connection.cursor()
        sql = "SELECT VAR_ID, VARABLE_NAME, SORT_ORDER, VARABLE_TYPE, STATUS_FLAG, VAR_SHORT_NAME, REMARK FROM RT_VARABLES "
        first=True
        param={}
        for colname,val in where.items():
            if first:
                sql=sql + "WHERE "
            if not first:
                sql=sql + " AND "
            first=False
            if val[0].upper().strip()=='IS':
                sql=sql + colname + " IS NULL"
            else:
                sql = sql + colname + val[0] + " :" + colname
                param[colname]=val[1]
        c1.execute(sql, param)
        return c1
    #@transaction.commit_on_success()
    def update(self, VAR_ID, **uargs):
        c1 = connection.cursor()
        param={}
        sql = "UPDATE RT_VARABLES SET "
        where = " WHERE VAR_ID = :VAR_ID"
        param['VAR_ID'] = VAR_ID
        first=True
        for colname,val in uargs.items():
            if not first:
                sql=sql + ", "
            first=False
            sql =sql +  colname + ' = :' + colname
            param[colname]=val
        sql = sql + where
        c1.execute(sql, param)
        connection.commit()


    #@transaction.commit_on_success()
    def insert(self, VAR_ID, **iargs):
        c1 = connection.cursor()
        sql = "INSERT INTO RT_VARABLES "
        col = "(VAR_ID, "
        vals = " VALUES (:VAR_ID, "
        first=True
        param={}
        param['VAR_ID'] = VAR_ID
        for colname,val in iargs.items():
            if not first:
                col=col + ", "
                vals=vals + ", "
            first=False
            col = col + colname
            vals = vals + ':' + colname
            param[colname]=val
        sql = sql + col + ")" + vals + ")"
        c1.execute(sql,param)
        connection.commit()

    #@transaction.commit_on_success()
    def delete(self,VAR_ID):
        c1 = connection.cursor()
        param={}
        param['VAR_ID'] = VAR_ID
        sql= 'DELETE FROM RT_VARABLES'
        sql = sql + ' WHERE VAR_ID = :VAR_ID'
        c1.execute(sql, param)
