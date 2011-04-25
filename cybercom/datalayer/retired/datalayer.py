'''
Python Data Layer Generator
Mark Stacy -- markstacy@ou.edu
Created: 3/9/2011 1:34:49 PM
Cybercommons data layer generation. Create,Read,Update and Delete(CRUD) operations.
Django, cx_ORacle or psycopg2.
'''
#from django.db import connection, transaction
import cx_Oracle as db
#import psycopg2 as db
connection = db.connect('eco/b00mer@oubcf1')

class dt_catalog():
    ''' Class for table DT_CATALOG. Performs basic CRUD operation on table.'''
    def __init__(self):
        '''DT_CATALOG.columnnames - returns list of Column Names
           DT_CATALOG.pkey - returns list of tables primary key(s)
        '''
        self.columnnames = ['COMMONS_ID','CAT_ID','CAT_NAME','DATA_PROVIDER','CAT_TYPE','LOC_ID','SOURCE_ID','CAT_DESC','CAT_METHOD','OBSERVED_DATE','REMARK','OBSERVED_YEAR','CUSTOM_FIELD_1','CUSTOM_FIELD_2','STATUS_FLAG','STATUS_DATA','USERID','TIMESTAMP_CREATED']
        self.pkey =['CAT_ID','COMMONS_ID']
        self._operator = ['=','!=','>=','<=','=>','=<','>','<','IS','IS NOT']
        self._strwhere = ''
        self._param = {}
        self._paramidx = 1
    def printset(self,cur,header=True):
        '''Prints to standard out the cursor pass to function
           example: Optional variables denoted []
           dt_catalog.printset(dt_catalog.select(),[header=False])
        '''
        if header:
            temp=[]
            for row in cur.description:
                temp.append(row[0])
            print tuple(temp)
        for row in cur:
            print row
    def selectpkey(self,CAT_ID,COMMONS_ID):
        '''Returns cursor of single record with associated Pkey.
           example:
           Cursor = dt_catalog.selectpkey(CAT_ID = <AppropriateKey>,COMMONS_ID = <AppropriateKey>)
        '''
        c1= connection.cursor()
        sql = "SELECT COMMONS_ID, CAT_ID, CAT_NAME, DATA_PROVIDER, CAT_TYPE, LOC_ID, SOURCE_ID, CAT_DESC, CAT_METHOD, OBSERVED_DATE, REMARK, OBSERVED_YEAR, CUSTOM_FIELD_1, CUSTOM_FIELD_2, STATUS_FLAG, STATUS_DATA, USERID, TIMESTAMP_CREATED FROM DT_CATALOG"
        sql = sql + " WHERE CAT_ID = :CAT_ID AND COMMONS_ID = :COMMONS_ID"
        param ={'CAT_ID' : CAT_ID, 'COMMONS_ID' : COMMONS_ID}
        c1.execute(sql, param)
        return c1
    def select(self,columnList = 'ALL'):
        '''Returns cursor with all rows. Optional columnList(Python List) - List of columns to return.
           Optional - Run dt_catalog.where('COLUMN_NAME','=',AppropriateValue) function to provide a where clause.
               dt_catalog.where('CAT_ID', '=',<AppropriateValue>)
           example:		   
               Cursor = dt_catalog.select(columnList)
        '''
        if columnList == 'ALL':
            columnList= self.columnnames
        colstr=''
        c1 = connection.cursor()
        first=True
        for col in columnList:
            if not first:
                colstr=colstr + ', '
            first=False
            colstr=colstr + col
        sql = 'SELECT ' + colstr + ' FROM DT_CATALOG '
        if len(self._strwhere.strip())>0:
            sql = sql + 'WHERE ' + self._strwhere 
        c1.execute(sql,self._param)
        return c1
    #@transaction.commit_on_success()
    def update(self, CAT_ID, COMMONS_ID, datetime_format= 'YYYY-MM-DD HH24:MI:SS', **uargs):
        '''Updates record varaiables. Does not allow update of primary keys.
            example: 
            dt_catalog.update(CAT_ID = <AppropriateKey>,COMMONS_ID = <AppropriateKey>,[COLUMN_NAME = <UpdateValues>])
        '''
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
            if (colname == 'OBSERVED_DATE' or colname == 'TIMESTAMP_CREATED'):
                sql =sql +  colname + ' = to_date(:' + colname + ', :datetime_format)'
                param['datetime_format'] = datetime_format
            else:
                sql =sql +  colname + ' = :' + colname
            param[colname]=val
        sql = sql + where
        c1.execute(sql, param)
        connection.commit()
    #@transaction.commit_on_success()
    def insert(self, CAT_ID, COMMONS_ID, datetime_format= 'YYYY-MM-DD HH24:MI:SS', **iargs):
        '''Insert record varaiables.
            example: 
            dt_catalog.insert(CAT_ID = <AppropriateKey>,COMMONS_ID = <AppropriateKey>,[COLUMN_NAME = <InsertValues>])
        '''
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
            if (colname == 'OBSERVED_DATE' or colname == 'TIMESTAMP_CREATED'):
                vals = vals + ' to_date(:' + colname + ', :datetime_format)'
                param['datetime_format'] = datetime_format
            else:
                vals = vals + ':' + colname
            param[colname]=val
        sql = sql + col + ")" + vals + ")"
        c1.execute(sql,param)
        connection.commit()
    #@transaction.commit_on_success()
    def insertmany(self, ListDict , datetime_format= 'YYYY-MM-DD HH24:MI:SS'):
        '''Insert Many takes a list of Dictionaries which contain variables to insert. Must contain all columns for insertmany().
            example: 
            dt_catalog.insertmany(ListDict, datetime_format= 'YYYY-MM-DD HH24:MI:SS')
        '''
        c1 = connection.cursor()
        sql = "INSERT INTO DT_CATALOG "
        col = "("
        vals = " VALUES ("
        first=True
        for colname in self.columnnames:
            if not first:
                col=col + ", "
                vals=vals + ", "
            first=False
            col = col + colname
            if (colname == 'OBSERVED_DATE' or colname == 'TIMESTAMP_CREATED'):
                vals = vals + ' to_date(:' + colname + ' ,'
                vals = vals + "'" + datetime_format + "'" + ')'
            else:
                vals = vals + ':' + colname
        sql = sql + col + ")" + vals + ")"
        c1.executemany(sql,ListDict)
        connection.commit()
    #@transaction.commit_on_success()
    def delete(self,CAT_ID, COMMONS_ID):
        '''Deletes record with associated Pkey.
           example:
           dt_catalog.delete(CAT_ID = <AppropriateKey>, COMMONS_ID = <AppropriateKey>)
        '''
        c1 = connection.cursor()
        param={}
        param['CAT_ID'] = CAT_ID
        param['COMMONS_ID'] = COMMONS_ID
        sql= 'DELETE FROM DT_CATALOG'
        sql = sql + ' WHERE CAT_ID = :CAT_ID AND COMMONS_ID = :COMMONS_ID'
        c1.execute(sql, param)
        connection.commit()
    def where(self,columnname,operator,value,conjunction='AND'):
        ''' Sets the WHERE clause for the select function. Default Conjunction is 'AND'
            example:
                DT_CATALOG.where('COlUMNNAME','=',AppropriateValue)
                DT_CATALOG.where('COlUMNNAME','=',AppropriateValue,'OR')
        '''
        if columnname in self.columnnames:
            if operator in self._operator:
                if len(self._strwhere)>0:
                    if operator.upper()=='IS' or operator.upper()=='IS NOT':
                        self._strwhere= self._strwhere + ' ' + conjunction + ' ' + columnname + ' ' + operator + ' NULL'
                    else:
                        self._strwhere= self._strwhere + ' ' + conjunction + ' ' + columnname + ' ' + operator + ' :' + str(self._paramidx)
                        self._param[str(self._paramidx)]=value
                        self._paramidx +=1
                else:
                    if operator.upper()=='IS' or operator.upper()=='IS NOT':
                        self._strwhere= self._strwhere + columnname + ' ' + operator + ' NULL'
                    else:
                        self._strwhere= self._strwhere + columnname + ' ' + operator + ' :' + str(self._paramidx)
                        self._param[str(self._paramidx)]=value
                        self._paramidx +=1
            else:
                raise AttributeError, "'" + operator + "'" + " - Not a supported operator."
        else:
            raise AttributeError, "'" + columnname + "'" + " - Not a Valid Column Name."
    def whereclear(self):
        ''' Resets the WHERE clause'''
        self._strwhere = ''
        self._param = {}
        self._paramidx = 1
class dt_contributors():
    ''' Class for table DT_CONTRIBUTORS. Performs basic CRUD operation on table.'''
    def __init__(self):
        '''DT_CONTRIBUTORS.columnnames - returns list of Column Names
           DT_CONTRIBUTORS.pkey - returns list of tables primary key(s)
        '''
        self.columnnames = ['COMMONS_ID','CONTRIBUTOR_ID','PROJECT_TITLE','DESCRIPTION','REMARK']
        self.pkey =['COMMONS_ID','CONTRIBUTOR_ID']
        self._operator = ['=','!=','>=','<=','=>','=<','>','<','IS','IS NOT']
        self._strwhere = ''
        self._param = {}
        self._paramidx = 1
    def printset(self,cur,header=True):
        '''Prints to standard out the cursor pass to function
           example: Optional variables denoted []
           dt_contributors.printset(dt_contributors.select(),[header=False])
        '''
        if header:
            temp=[]
            for row in cur.description:
                temp.append(row[0])
            print tuple(temp)
        for row in cur:
            print row
    def selectpkey(self,COMMONS_ID,CONTRIBUTOR_ID):
        '''Returns cursor of single record with associated Pkey.
           example:
           Cursor = dt_contributors.selectpkey(COMMONS_ID = <AppropriateKey>,CONTRIBUTOR_ID = <AppropriateKey>)
        '''
        c1= connection.cursor()
        sql = "SELECT COMMONS_ID, CONTRIBUTOR_ID, PROJECT_TITLE, DESCRIPTION, REMARK FROM DT_CONTRIBUTORS"
        sql = sql + " WHERE COMMONS_ID = :COMMONS_ID AND CONTRIBUTOR_ID = :CONTRIBUTOR_ID"
        param ={'COMMONS_ID' : COMMONS_ID, 'CONTRIBUTOR_ID' : CONTRIBUTOR_ID}
        c1.execute(sql, param)
        return c1
    def select(self,columnList = 'ALL'):
        '''Returns cursor with all rows. Optional columnList(Python List) - List of columns to return.
           Optional - Run dt_contributors.where('COLUMN_NAME','=',AppropriateValue) function to provide a where clause.
               dt_contributors.where('COMMONS_ID', '=',<AppropriateValue>)
           example:		   
               Cursor = dt_contributors.select(columnList)
        '''
        if columnList == 'ALL':
            columnList= self.columnnames
        colstr=''
        c1 = connection.cursor()
        first=True
        for col in columnList:
            if not first:
                colstr=colstr + ', '
            first=False
            colstr=colstr + col
        sql = 'SELECT ' + colstr + ' FROM DT_CONTRIBUTORS '
        if len(self._strwhere.strip())>0:
            sql = sql + 'WHERE ' + self._strwhere 
        c1.execute(sql,self._param)
        return c1
    #@transaction.commit_on_success()
    def update(self, COMMONS_ID, CONTRIBUTOR_ID, **uargs):
        '''Updates record varaiables. Does not allow update of primary keys.
            example: 
            dt_contributors.update(COMMONS_ID = <AppropriateKey>,CONTRIBUTOR_ID = <AppropriateKey>,[COLUMN_NAME = <UpdateValues>])
        '''
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
        '''Insert record varaiables.
            example: 
            dt_contributors.insert(COMMONS_ID = <AppropriateKey>,CONTRIBUTOR_ID = <AppropriateKey>,[COLUMN_NAME = <InsertValues>])
        '''
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
    def insertmany(self, ListDict ):
        '''Insert Many takes a list of Dictionaries which contain variables to insert. Must contain all columns for insertmany().
            example: 
            dt_contributors.insertmany(ListDict)
        '''
        c1 = connection.cursor()
        sql = "INSERT INTO DT_CONTRIBUTORS "
        col = "("
        vals = " VALUES ("
        first=True
        for colname in self.columnnames:
            if not first:
                col=col + ", "
                vals=vals + ", "
            first=False
            col = col + colname
            vals = vals + ':' + colname
        sql = sql + col + ")" + vals + ")"
        c1.executemany(sql,ListDict)
        connection.commit()
    #@transaction.commit_on_success()
    def delete(self,COMMONS_ID, CONTRIBUTOR_ID):
        '''Deletes record with associated Pkey.
           example:
           dt_contributors.delete(COMMONS_ID = <AppropriateKey>, CONTRIBUTOR_ID = <AppropriateKey>)
        '''
        c1 = connection.cursor()
        param={}
        param['COMMONS_ID'] = COMMONS_ID
        param['CONTRIBUTOR_ID'] = CONTRIBUTOR_ID
        sql= 'DELETE FROM DT_CONTRIBUTORS'
        sql = sql + ' WHERE COMMONS_ID = :COMMONS_ID AND CONTRIBUTOR_ID = :CONTRIBUTOR_ID'
        c1.execute(sql, param)
        connection.commit()
    def where(self,columnname,operator,value,conjunction='AND'):
        ''' Sets the WHERE clause for the select function. Default Conjunction is 'AND'
            example:
                DT_CONTRIBUTORS.where('COlUMNNAME','=',AppropriateValue)
                DT_CONTRIBUTORS.where('COlUMNNAME','=',AppropriateValue,'OR')
        '''
        if columnname in self.columnnames:
            if operator in self._operator:
                if len(self._strwhere)>0:
                    if operator.upper()=='IS' or operator.upper()=='IS NOT':
                        self._strwhere= self._strwhere + ' ' + conjunction + ' ' + columnname + ' ' + operator + ' NULL'
                    else:
                        self._strwhere= self._strwhere + ' ' + conjunction + ' ' + columnname + ' ' + operator + ' :' + str(self._paramidx)
                        self._param[str(self._paramidx)]=value
                        self._paramidx +=1
                else:
                    if operator.upper()=='IS' or operator.upper()=='IS NOT':
                        self._strwhere= self._strwhere + columnname + ' ' + operator + ' NULL'
                    else:
                        self._strwhere= self._strwhere + columnname + ' ' + operator + ' :' + str(self._paramidx)
                        self._param[str(self._paramidx)]=value
                        self._paramidx +=1
            else:
                raise AttributeError, "'" + operator + "'" + " - Not a supported operator."
        else:
            raise AttributeError, "'" + columnname + "'" + " - Not a Valid Column Name."
    def whereclear(self):
        ''' Resets the WHERE clause'''
        self._strwhere = ''
        self._param = {}
        self._paramidx = 1
class dt_coordinate():
    ''' Class for table DT_COORDINATE. Performs basic CRUD operation on table.'''
    def __init__(self):
        '''DT_COORDINATE.columnnames - returns list of Column Names
           DT_COORDINATE.pkey - returns list of tables primary key(s)
        '''
        self.columnnames = ['COMMONS_ID','LOC_ID','COORD_TYPE_CODE','OBSERVATION_DATE','IDENTIFIER','X_COORD','Y_COORD','ELEV','ELEV_UNIT','HORZ_COLLECT_METHOD_CODE','COORD_ZONE','HORZ_ACCURACY_VALUE','HORZ_ACCURACY_UNIT','ELEV_ACCURACY_UNIT','HORZ_DATUM_CODE','ELEV_COLLECT_METHOD_CODE','ELEV_ACCURACY_VALUE','ELEV_DATUM_CODE','SOURCE_SCALE','ORG_CODE','VERIFICATION_CODE','DATA_POINT_SEQUENCE','REFERENCE_POINT','GEOMETRIC_TYPE_CODE','SURVEYOR_NAME','RANK','REMARK']
        self.pkey =['COMMONS_ID','COORD_TYPE_CODE','IDENTIFIER','LOC_ID']
        self._operator = ['=','!=','>=','<=','=>','=<','>','<','IS','IS NOT']
        self._strwhere = ''
        self._param = {}
        self._paramidx = 1
    def printset(self,cur,header=True):
        '''Prints to standard out the cursor pass to function
           example: Optional variables denoted []
           dt_coordinate.printset(dt_coordinate.select(),[header=False])
        '''
        if header:
            temp=[]
            for row in cur.description:
                temp.append(row[0])
            print tuple(temp)
        for row in cur:
            print row
    def selectpkey(self,COMMONS_ID,COORD_TYPE_CODE,IDENTIFIER,LOC_ID):
        '''Returns cursor of single record with associated Pkey.
           example:
           Cursor = dt_coordinate.selectpkey(COMMONS_ID = <AppropriateKey>,COORD_TYPE_CODE = <AppropriateKey>,IDENTIFIER = <AppropriateKey>,LOC_ID = <AppropriateKey>)
        '''
        c1= connection.cursor()
        sql = "SELECT COMMONS_ID, LOC_ID, COORD_TYPE_CODE, OBSERVATION_DATE, IDENTIFIER, X_COORD, Y_COORD, ELEV, ELEV_UNIT, HORZ_COLLECT_METHOD_CODE, COORD_ZONE, HORZ_ACCURACY_VALUE, HORZ_ACCURACY_UNIT, ELEV_ACCURACY_UNIT, HORZ_DATUM_CODE, ELEV_COLLECT_METHOD_CODE, ELEV_ACCURACY_VALUE, ELEV_DATUM_CODE, SOURCE_SCALE, ORG_CODE, VERIFICATION_CODE, DATA_POINT_SEQUENCE, REFERENCE_POINT, GEOMETRIC_TYPE_CODE, SURVEYOR_NAME, RANK, REMARK FROM DT_COORDINATE"
        sql = sql + " WHERE COMMONS_ID = :COMMONS_ID AND COORD_TYPE_CODE = :COORD_TYPE_CODE AND IDENTIFIER = :IDENTIFIER AND LOC_ID = :LOC_ID"
        param ={'COMMONS_ID' : COMMONS_ID, 'COORD_TYPE_CODE' : COORD_TYPE_CODE, 'IDENTIFIER' : IDENTIFIER, 'LOC_ID' : LOC_ID}
        c1.execute(sql, param)
        return c1
    def select(self,columnList = 'ALL'):
        '''Returns cursor with all rows. Optional columnList(Python List) - List of columns to return.
           Optional - Run dt_coordinate.where('COLUMN_NAME','=',AppropriateValue) function to provide a where clause.
               dt_coordinate.where('COMMONS_ID', '=',<AppropriateValue>)
           example:		   
               Cursor = dt_coordinate.select(columnList)
        '''
        if columnList == 'ALL':
            columnList= self.columnnames
        colstr=''
        c1 = connection.cursor()
        first=True
        for col in columnList:
            if not first:
                colstr=colstr + ', '
            first=False
            colstr=colstr + col
        sql = 'SELECT ' + colstr + ' FROM DT_COORDINATE '
        if len(self._strwhere.strip())>0:
            sql = sql + 'WHERE ' + self._strwhere 
        c1.execute(sql,self._param)
        return c1
    #@transaction.commit_on_success()
    def update(self, COMMONS_ID, COORD_TYPE_CODE, IDENTIFIER, LOC_ID, datetime_format= 'YYYY-MM-DD HH24:MI:SS', **uargs):
        '''Updates record varaiables. Does not allow update of primary keys.
            example: 
            dt_coordinate.update(COMMONS_ID = <AppropriateKey>,COORD_TYPE_CODE = <AppropriateKey>,IDENTIFIER = <AppropriateKey>,LOC_ID = <AppropriateKey>,[COLUMN_NAME = <UpdateValues>])
        '''
        c1 = connection.cursor()
        param={}
        sql = "UPDATE DT_COORDINATE SET "
        where = " WHERE COMMONS_ID = :COMMONS_ID AND COORD_TYPE_CODE = :COORD_TYPE_CODE AND IDENTIFIER = :IDENTIFIER AND LOC_ID = :LOC_ID"
        param['COMMONS_ID'] = COMMONS_ID
        param['COORD_TYPE_CODE'] = COORD_TYPE_CODE
        param['IDENTIFIER'] = IDENTIFIER
        param['LOC_ID'] = LOC_ID
        first=True
        for colname,val in uargs.items():
            if not first:
                sql=sql + ", "
            first=False
            if (colname == 'OBSERVATION_DATE'):
                sql =sql +  colname + ' = to_date(:' + colname + ', :datetime_format)'
                param['datetime_format'] = datetime_format
            else:
                sql =sql +  colname + ' = :' + colname
            param[colname]=val
        sql = sql + where
        c1.execute(sql, param)
        connection.commit()
    #@transaction.commit_on_success()
    def insert(self, COMMONS_ID, COORD_TYPE_CODE, IDENTIFIER, LOC_ID, datetime_format= 'YYYY-MM-DD HH24:MI:SS', **iargs):
        '''Insert record varaiables.
            example: 
            dt_coordinate.insert(COMMONS_ID = <AppropriateKey>,COORD_TYPE_CODE = <AppropriateKey>,IDENTIFIER = <AppropriateKey>,LOC_ID = <AppropriateKey>,[COLUMN_NAME = <InsertValues>])
        '''
        c1 = connection.cursor()
        sql = "INSERT INTO DT_COORDINATE "
        col = "(COMMONS_ID,COORD_TYPE_CODE,IDENTIFIER,LOC_ID, "
        vals = " VALUES (:COMMONS_ID,:COORD_TYPE_CODE,:IDENTIFIER,:LOC_ID, "
        first=True
        param={}
        param['COMMONS_ID'] = COMMONS_ID
        param['COORD_TYPE_CODE'] = COORD_TYPE_CODE
        param['IDENTIFIER'] = IDENTIFIER
        param['LOC_ID'] = LOC_ID
        for colname,val in iargs.items():
            if not first:
                col=col + ", "
                vals=vals + ", "
            first=False
            col = col + colname
            if (colname == 'OBSERVATION_DATE'):
                vals = vals + ' to_date(:' + colname + ', :datetime_format)'
                param['datetime_format'] = datetime_format
            else:
                vals = vals + ':' + colname
            param[colname]=val
        sql = sql + col + ")" + vals + ")"
        c1.execute(sql,param)
        connection.commit()
    #@transaction.commit_on_success()
    def insertmany(self, ListDict , datetime_format= 'YYYY-MM-DD HH24:MI:SS'):
        '''Insert Many takes a list of Dictionaries which contain variables to insert. Must contain all columns for insertmany().
            example: 
            dt_coordinate.insertmany(ListDict, datetime_format= 'YYYY-MM-DD HH24:MI:SS')
        '''
        c1 = connection.cursor()
        sql = "INSERT INTO DT_COORDINATE "
        col = "("
        vals = " VALUES ("
        first=True
        for colname in self.columnnames:
            if not first:
                col=col + ", "
                vals=vals + ", "
            first=False
            col = col + colname
            if (colname == 'OBSERVATION_DATE'):
                vals = vals + ' to_date(:' + colname + ' ,'
                vals = vals + "'" + datetime_format + "'" + ')'
            else:
                vals = vals + ':' + colname
        sql = sql + col + ")" + vals + ")"
        c1.executemany(sql,ListDict)
        connection.commit()
    #@transaction.commit_on_success()
    def delete(self,COMMONS_ID, COORD_TYPE_CODE, IDENTIFIER, LOC_ID):
        '''Deletes record with associated Pkey.
           example:
           dt_coordinate.delete(COMMONS_ID = <AppropriateKey>, COORD_TYPE_CODE = <AppropriateKey>, IDENTIFIER = <AppropriateKey>, LOC_ID = <AppropriateKey>)
        '''
        c1 = connection.cursor()
        param={}
        param['COMMONS_ID'] = COMMONS_ID
        param['COORD_TYPE_CODE'] = COORD_TYPE_CODE
        param['IDENTIFIER'] = IDENTIFIER
        param['LOC_ID'] = LOC_ID
        sql= 'DELETE FROM DT_COORDINATE'
        sql = sql + ' WHERE COMMONS_ID = :COMMONS_ID AND COORD_TYPE_CODE = :COORD_TYPE_CODE AND IDENTIFIER = :IDENTIFIER AND LOC_ID = :LOC_ID'
        c1.execute(sql, param)
        connection.commit()
    def where(self,columnname,operator,value,conjunction='AND'):
        ''' Sets the WHERE clause for the select function. Default Conjunction is 'AND'
            example:
                DT_COORDINATE.where('COlUMNNAME','=',AppropriateValue)
                DT_COORDINATE.where('COlUMNNAME','=',AppropriateValue,'OR')
        '''
        if columnname in self.columnnames:
            if operator in self._operator:
                if len(self._strwhere)>0:
                    if operator.upper()=='IS' or operator.upper()=='IS NOT':
                        self._strwhere= self._strwhere + ' ' + conjunction + ' ' + columnname + ' ' + operator + ' NULL'
                    else:
                        self._strwhere= self._strwhere + ' ' + conjunction + ' ' + columnname + ' ' + operator + ' :' + str(self._paramidx)
                        self._param[str(self._paramidx)]=value
                        self._paramidx +=1
                else:
                    if operator.upper()=='IS' or operator.upper()=='IS NOT':
                        self._strwhere= self._strwhere + columnname + ' ' + operator + ' NULL'
                    else:
                        self._strwhere= self._strwhere + columnname + ' ' + operator + ' :' + str(self._paramidx)
                        self._param[str(self._paramidx)]=value
                        self._paramidx +=1
            else:
                raise AttributeError, "'" + operator + "'" + " - Not a supported operator."
        else:
            raise AttributeError, "'" + columnname + "'" + " - Not a Valid Column Name."
    def whereclear(self):
        ''' Resets the WHERE clause'''
        self._strwhere = ''
        self._param = {}
        self._paramidx = 1
class dt_data_commons():
    ''' Class for table DT_DATA_COMMONS. Performs basic CRUD operation on table.'''
    def __init__(self):
        '''DT_DATA_COMMONS.columnnames - returns list of Column Names
           DT_DATA_COMMONS.pkey - returns list of tables primary key(s)
        '''
        self.columnnames = ['COMMONS_ID','COMMONS_CODE','DATA_PROVIDER','COMMONS_TYPE','PROGRAM_CODE','COMMONS_NAME','EMAIL_ADDRESS','DESCRIPTION','CLIENT','PROJECT_MANAGER','START_DATE','STATUS_FLAG','CONTRIBUTOR_ID']
        self.pkey =['COMMONS_ID']
        self._operator = ['=','!=','>=','<=','=>','=<','>','<','IS','IS NOT']
        self._strwhere = ''
        self._param = {}
        self._paramidx = 1
    def printset(self,cur,header=True):
        '''Prints to standard out the cursor pass to function
           example: Optional variables denoted []
           dt_data_commons.printset(dt_data_commons.select(),[header=False])
        '''
        if header:
            temp=[]
            for row in cur.description:
                temp.append(row[0])
            print tuple(temp)
        for row in cur:
            print row
    def selectpkey(self,COMMONS_ID):
        '''Returns cursor of single record with associated Pkey.
           example:
           Cursor = dt_data_commons.selectpkey(COMMONS_ID = <AppropriateKey>)
        '''
        c1= connection.cursor()
        sql = "SELECT COMMONS_ID, COMMONS_CODE, DATA_PROVIDER, COMMONS_TYPE, PROGRAM_CODE, COMMONS_NAME, EMAIL_ADDRESS, DESCRIPTION, CLIENT, PROJECT_MANAGER, START_DATE, STATUS_FLAG, CONTRIBUTOR_ID FROM DT_DATA_COMMONS"
        sql = sql + " WHERE COMMONS_ID = :COMMONS_ID"
        param ={'COMMONS_ID' : COMMONS_ID}
        c1.execute(sql, param)
        return c1
    def select(self,columnList = 'ALL'):
        '''Returns cursor with all rows. Optional columnList(Python List) - List of columns to return.
           Optional - Run dt_data_commons.where('COLUMN_NAME','=',AppropriateValue) function to provide a where clause.
               dt_data_commons.where('COMMONS_ID', '=',<AppropriateValue>)
           example:		   
               Cursor = dt_data_commons.select(columnList)
        '''
        if columnList == 'ALL':
            columnList= self.columnnames
        colstr=''
        c1 = connection.cursor()
        first=True
        for col in columnList:
            if not first:
                colstr=colstr + ', '
            first=False
            colstr=colstr + col
        sql = 'SELECT ' + colstr + ' FROM DT_DATA_COMMONS '
        if len(self._strwhere.strip())>0:
            sql = sql + 'WHERE ' + self._strwhere 
        c1.execute(sql,self._param)
        return c1
    #@transaction.commit_on_success()
    def update(self, COMMONS_ID, datetime_format= 'YYYY-MM-DD HH24:MI:SS', **uargs):
        '''Updates record varaiables. Does not allow update of primary keys.
            example: 
            dt_data_commons.update(COMMONS_ID = <AppropriateKey>,[COLUMN_NAME = <UpdateValues>])
        '''
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
            if (colname == 'START_DATE'):
                sql =sql +  colname + ' = to_date(:' + colname + ', :datetime_format)'
                param['datetime_format'] = datetime_format
            else:
                sql =sql +  colname + ' = :' + colname
            param[colname]=val
        sql = sql + where
        c1.execute(sql, param)
        connection.commit()
    #@transaction.commit_on_success()
    def insert(self, COMMONS_ID, datetime_format= 'YYYY-MM-DD HH24:MI:SS', **iargs):
        '''Insert record varaiables.
            example: 
            dt_data_commons.insert(COMMONS_ID = <AppropriateKey>,[COLUMN_NAME = <InsertValues>])
        '''
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
            if (colname == 'START_DATE'):
                vals = vals + ' to_date(:' + colname + ', :datetime_format)'
                param['datetime_format'] = datetime_format
            else:
                vals = vals + ':' + colname
            param[colname]=val
        sql = sql + col + ")" + vals + ")"
        c1.execute(sql,param)
        connection.commit()
    #@transaction.commit_on_success()
    def insertmany(self, ListDict , datetime_format= 'YYYY-MM-DD HH24:MI:SS'):
        '''Insert Many takes a list of Dictionaries which contain variables to insert. Must contain all columns for insertmany().
            example: 
            dt_data_commons.insertmany(ListDict, datetime_format= 'YYYY-MM-DD HH24:MI:SS')
        '''
        c1 = connection.cursor()
        sql = "INSERT INTO DT_DATA_COMMONS "
        col = "("
        vals = " VALUES ("
        first=True
        for colname in self.columnnames:
            if not first:
                col=col + ", "
                vals=vals + ", "
            first=False
            col = col + colname
            if (colname == 'START_DATE'):
                vals = vals + ' to_date(:' + colname + ' ,'
                vals = vals + "'" + datetime_format + "'" + ')'
            else:
                vals = vals + ':' + colname
        sql = sql + col + ")" + vals + ")"
        c1.executemany(sql,ListDict)
        connection.commit()
    #@transaction.commit_on_success()
    def delete(self,COMMONS_ID):
        '''Deletes record with associated Pkey.
           example:
           dt_data_commons.delete(COMMONS_ID = <AppropriateKey>)
        '''
        c1 = connection.cursor()
        param={}
        param['COMMONS_ID'] = COMMONS_ID
        sql= 'DELETE FROM DT_DATA_COMMONS'
        sql = sql + ' WHERE COMMONS_ID = :COMMONS_ID'
        c1.execute(sql, param)
        connection.commit()
    def where(self,columnname,operator,value,conjunction='AND'):
        ''' Sets the WHERE clause for the select function. Default Conjunction is 'AND'
            example:
                DT_DATA_COMMONS.where('COlUMNNAME','=',AppropriateValue)
                DT_DATA_COMMONS.where('COlUMNNAME','=',AppropriateValue,'OR')
        '''
        if columnname in self.columnnames:
            if operator in self._operator:
                if len(self._strwhere)>0:
                    if operator.upper()=='IS' or operator.upper()=='IS NOT':
                        self._strwhere= self._strwhere + ' ' + conjunction + ' ' + columnname + ' ' + operator + ' NULL'
                    else:
                        self._strwhere= self._strwhere + ' ' + conjunction + ' ' + columnname + ' ' + operator + ' :' + str(self._paramidx)
                        self._param[str(self._paramidx)]=value
                        self._paramidx +=1
                else:
                    if operator.upper()=='IS' or operator.upper()=='IS NOT':
                        self._strwhere= self._strwhere + columnname + ' ' + operator + ' NULL'
                    else:
                        self._strwhere= self._strwhere + columnname + ' ' + operator + ' :' + str(self._paramidx)
                        self._param[str(self._paramidx)]=value
                        self._paramidx +=1
            else:
                raise AttributeError, "'" + operator + "'" + " - Not a supported operator."
        else:
            raise AttributeError, "'" + columnname + "'" + " - Not a Valid Column Name."
    def whereclear(self):
        ''' Resets the WHERE clause'''
        self._strwhere = ''
        self._param = {}
        self._paramidx = 1
class dt_event():
    ''' Class for table DT_EVENT. Performs basic CRUD operation on table.'''
    def __init__(self):
        '''DT_EVENT.columnnames - returns list of Column Names
           DT_EVENT.pkey - returns list of tables primary key(s)
        '''
        self.columnnames = ['COMMONS_ID','EVENT_ID','CAT_ID','EVENT_METHOD','EVENT_DATE','EVENT_DESC','EVENT_TYPE','LOC_ID','CUSTOM_1','REMARK','EVENT_NAME','STATUS_FLAG','USERID','TIMESTAMP_CREATED']
        self.pkey =['COMMONS_ID','EVENT_ID']
        self._operator = ['=','!=','>=','<=','=>','=<','>','<','IS','IS NOT']
        self._strwhere = ''
        self._param = {}
        self._paramidx = 1
    def printset(self,cur,header=True):
        '''Prints to standard out the cursor pass to function
           example: Optional variables denoted []
           dt_event.printset(dt_event.select(),[header=False])
        '''
        if header:
            temp=[]
            for row in cur.description:
                temp.append(row[0])
            print tuple(temp)
        for row in cur:
            print row
    def selectpkey(self,COMMONS_ID,EVENT_ID):
        '''Returns cursor of single record with associated Pkey.
           example:
           Cursor = dt_event.selectpkey(COMMONS_ID = <AppropriateKey>,EVENT_ID = <AppropriateKey>)
        '''
        c1= connection.cursor()
        sql = "SELECT COMMONS_ID, EVENT_ID, CAT_ID, EVENT_METHOD, EVENT_DATE, EVENT_DESC, EVENT_TYPE, LOC_ID, CUSTOM_1, REMARK, EVENT_NAME, STATUS_FLAG, USERID, TIMESTAMP_CREATED FROM DT_EVENT"
        sql = sql + " WHERE COMMONS_ID = :COMMONS_ID AND EVENT_ID = :EVENT_ID"
        param ={'COMMONS_ID' : COMMONS_ID, 'EVENT_ID' : EVENT_ID}
        c1.execute(sql, param)
        return c1
    def select(self,columnList = 'ALL'):
        '''Returns cursor with all rows. Optional columnList(Python List) - List of columns to return.
           Optional - Run dt_event.where('COLUMN_NAME','=',AppropriateValue) function to provide a where clause.
               dt_event.where('COMMONS_ID', '=',<AppropriateValue>)
           example:		   
               Cursor = dt_event.select(columnList)
        '''
        if columnList == 'ALL':
            columnList= self.columnnames
        colstr=''
        c1 = connection.cursor()
        first=True
        for col in columnList:
            if not first:
                colstr=colstr + ', '
            first=False
            colstr=colstr + col
        sql = 'SELECT ' + colstr + ' FROM DT_EVENT '
        if len(self._strwhere.strip())>0:
            sql = sql + 'WHERE ' + self._strwhere 
        c1.execute(sql,self._param)
        return c1
    #@transaction.commit_on_success()
    def update(self, COMMONS_ID, EVENT_ID, datetime_format= 'YYYY-MM-DD HH24:MI:SS', **uargs):
        '''Updates record varaiables. Does not allow update of primary keys.
            example: 
            dt_event.update(COMMONS_ID = <AppropriateKey>,EVENT_ID = <AppropriateKey>,[COLUMN_NAME = <UpdateValues>])
        '''
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
            if (colname == 'EVENT_DATE' or colname == 'TIMESTAMP_CREATED'):
                sql =sql +  colname + ' = to_date(:' + colname + ', :datetime_format)'
                param['datetime_format'] = datetime_format
            else:
                sql =sql +  colname + ' = :' + colname
            param[colname]=val
        sql = sql + where
        c1.execute(sql, param)
        connection.commit()
    #@transaction.commit_on_success()
    def insert(self, COMMONS_ID, EVENT_ID, datetime_format= 'YYYY-MM-DD HH24:MI:SS', **iargs):
        '''Insert record varaiables.
            example: 
            dt_event.insert(COMMONS_ID = <AppropriateKey>,EVENT_ID = <AppropriateKey>,[COLUMN_NAME = <InsertValues>])
        '''
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
            if (colname == 'EVENT_DATE' or colname == 'TIMESTAMP_CREATED'):
                vals = vals + ' to_date(:' + colname + ', :datetime_format)'
                param['datetime_format'] = datetime_format
            else:
                vals = vals + ':' + colname
            param[colname]=val
        sql = sql + col + ")" + vals + ")"
        c1.execute(sql,param)
        connection.commit()
    #@transaction.commit_on_success()
    def insertmany(self, ListDict , datetime_format= 'YYYY-MM-DD HH24:MI:SS'):
        '''Insert Many takes a list of Dictionaries which contain variables to insert. Must contain all columns for insertmany().
            example: 
            dt_event.insertmany(ListDict, datetime_format= 'YYYY-MM-DD HH24:MI:SS')
        '''
        c1 = connection.cursor()
        sql = "INSERT INTO DT_EVENT "
        col = "("
        vals = " VALUES ("
        first=True
        for colname in self.columnnames:
            if not first:
                col=col + ", "
                vals=vals + ", "
            first=False
            col = col + colname
            if (colname == 'EVENT_DATE' or colname == 'TIMESTAMP_CREATED'):
                vals = vals + ' to_date(:' + colname + ' ,'
                vals = vals + "'" + datetime_format + "'" + ')'
            else:
                vals = vals + ':' + colname
        sql = sql + col + ")" + vals + ")"
        c1.executemany(sql,ListDict)
        connection.commit()
    #@transaction.commit_on_success()
    def delete(self,COMMONS_ID, EVENT_ID):
        '''Deletes record with associated Pkey.
           example:
           dt_event.delete(COMMONS_ID = <AppropriateKey>, EVENT_ID = <AppropriateKey>)
        '''
        c1 = connection.cursor()
        param={}
        param['COMMONS_ID'] = COMMONS_ID
        param['EVENT_ID'] = EVENT_ID
        sql= 'DELETE FROM DT_EVENT'
        sql = sql + ' WHERE COMMONS_ID = :COMMONS_ID AND EVENT_ID = :EVENT_ID'
        c1.execute(sql, param)
        connection.commit()
    def where(self,columnname,operator,value,conjunction='AND'):
        ''' Sets the WHERE clause for the select function. Default Conjunction is 'AND'
            example:
                DT_EVENT.where('COlUMNNAME','=',AppropriateValue)
                DT_EVENT.where('COlUMNNAME','=',AppropriateValue,'OR')
        '''
        if columnname in self.columnnames:
            if operator in self._operator:
                if len(self._strwhere)>0:
                    if operator.upper()=='IS' or operator.upper()=='IS NOT':
                        self._strwhere= self._strwhere + ' ' + conjunction + ' ' + columnname + ' ' + operator + ' NULL'
                    else:
                        self._strwhere= self._strwhere + ' ' + conjunction + ' ' + columnname + ' ' + operator + ' :' + str(self._paramidx)
                        self._param[str(self._paramidx)]=value
                        self._paramidx +=1
                else:
                    if operator.upper()=='IS' or operator.upper()=='IS NOT':
                        self._strwhere= self._strwhere + columnname + ' ' + operator + ' NULL'
                    else:
                        self._strwhere= self._strwhere + columnname + ' ' + operator + ' :' + str(self._paramidx)
                        self._param[str(self._paramidx)]=value
                        self._paramidx +=1
            else:
                raise AttributeError, "'" + operator + "'" + " - Not a supported operator."
        else:
            raise AttributeError, "'" + columnname + "'" + " - Not a Valid Column Name."
    def whereclear(self):
        ''' Resets the WHERE clause'''
        self._strwhere = ''
        self._param = {}
        self._paramidx = 1
class dt_file():
    ''' Class for table DT_FILE. Performs basic CRUD operation on table.'''
    def __init__(self):
        '''DT_FILE.columnnames - returns list of Column Names
           DT_FILE.pkey - returns list of tables primary key(s)
        '''
        self.columnnames = ['FILE_ID','FILE_TYPE','FACILITY_ID','PLACE_TYPE','PLACE_CODE','PLACE_SUBCODE','FILE_DATE','FILE_NAME','REMARK','EBATCH','CONTENT']
        self.pkey =['FILE_ID']
        self._operator = ['=','!=','>=','<=','=>','=<','>','<','IS','IS NOT']
        self._strwhere = ''
        self._param = {}
        self._paramidx = 1
    def printset(self,cur,header=True):
        '''Prints to standard out the cursor pass to function
           example: Optional variables denoted []
           dt_file.printset(dt_file.select(),[header=False])
        '''
        if header:
            temp=[]
            for row in cur.description:
                temp.append(row[0])
            print tuple(temp)
        for row in cur:
            print row
    def selectpkey(self,FILE_ID):
        '''Returns cursor of single record with associated Pkey.
           example:
           Cursor = dt_file.selectpkey(FILE_ID = <AppropriateKey>)
        '''
        c1= connection.cursor()
        sql = "SELECT FILE_ID, FILE_TYPE, FACILITY_ID, PLACE_TYPE, PLACE_CODE, PLACE_SUBCODE, FILE_DATE, FILE_NAME, REMARK, EBATCH, CONTENT FROM DT_FILE"
        sql = sql + " WHERE FILE_ID = :FILE_ID"
        param ={'FILE_ID' : FILE_ID}
        c1.execute(sql, param)
        return c1
    def select(self,columnList = 'ALL'):
        '''Returns cursor with all rows. Optional columnList(Python List) - List of columns to return.
           Optional - Run dt_file.where('COLUMN_NAME','=',AppropriateValue) function to provide a where clause.
               dt_file.where('FILE_ID', '=',<AppropriateValue>)
           example:		   
               Cursor = dt_file.select(columnList)
        '''
        if columnList == 'ALL':
            columnList= self.columnnames
        colstr=''
        c1 = connection.cursor()
        first=True
        for col in columnList:
            if not first:
                colstr=colstr + ', '
            first=False
            colstr=colstr + col
        sql = 'SELECT ' + colstr + ' FROM DT_FILE '
        if len(self._strwhere.strip())>0:
            sql = sql + 'WHERE ' + self._strwhere 
        c1.execute(sql,self._param)
        return c1
    #@transaction.commit_on_success()
    def update(self, FILE_ID, datetime_format= 'YYYY-MM-DD HH24:MI:SS', **uargs):
        '''Updates record varaiables. Does not allow update of primary keys.
            example: 
            dt_file.update(FILE_ID = <AppropriateKey>,[COLUMN_NAME = <UpdateValues>])
        '''
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
            if (colname == 'FILE_DATE'):
                sql =sql +  colname + ' = to_date(:' + colname + ', :datetime_format)'
                param['datetime_format'] = datetime_format
            else:
                sql =sql +  colname + ' = :' + colname
            param[colname]=val
        sql = sql + where
        c1.execute(sql, param)
        connection.commit()
    #@transaction.commit_on_success()
    def insert(self, FILE_ID, datetime_format= 'YYYY-MM-DD HH24:MI:SS', **iargs):
        '''Insert record varaiables.
            example: 
            dt_file.insert(FILE_ID = <AppropriateKey>,[COLUMN_NAME = <InsertValues>])
        '''
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
            if (colname == 'FILE_DATE'):
                vals = vals + ' to_date(:' + colname + ', :datetime_format)'
                param['datetime_format'] = datetime_format
            else:
                vals = vals + ':' + colname
            param[colname]=val
        sql = sql + col + ")" + vals + ")"
        c1.execute(sql,param)
        connection.commit()
    #@transaction.commit_on_success()
    def insertmany(self, ListDict , datetime_format= 'YYYY-MM-DD HH24:MI:SS'):
        '''Insert Many takes a list of Dictionaries which contain variables to insert. Must contain all columns for insertmany().
            example: 
            dt_file.insertmany(ListDict, datetime_format= 'YYYY-MM-DD HH24:MI:SS')
        '''
        c1 = connection.cursor()
        sql = "INSERT INTO DT_FILE "
        col = "("
        vals = " VALUES ("
        first=True
        for colname in self.columnnames:
            if not first:
                col=col + ", "
                vals=vals + ", "
            first=False
            col = col + colname
            if (colname == 'FILE_DATE'):
                vals = vals + ' to_date(:' + colname + ' ,'
                vals = vals + "'" + datetime_format + "'" + ')'
            else:
                vals = vals + ':' + colname
        sql = sql + col + ")" + vals + ")"
        c1.executemany(sql,ListDict)
        connection.commit()
    #@transaction.commit_on_success()
    def delete(self,FILE_ID):
        '''Deletes record with associated Pkey.
           example:
           dt_file.delete(FILE_ID = <AppropriateKey>)
        '''
        c1 = connection.cursor()
        param={}
        param['FILE_ID'] = FILE_ID
        sql= 'DELETE FROM DT_FILE'
        sql = sql + ' WHERE FILE_ID = :FILE_ID'
        c1.execute(sql, param)
        connection.commit()
    def where(self,columnname,operator,value,conjunction='AND'):
        ''' Sets the WHERE clause for the select function. Default Conjunction is 'AND'
            example:
                DT_FILE.where('COlUMNNAME','=',AppropriateValue)
                DT_FILE.where('COlUMNNAME','=',AppropriateValue,'OR')
        '''
        if columnname in self.columnnames:
            if operator in self._operator:
                if len(self._strwhere)>0:
                    if operator.upper()=='IS' or operator.upper()=='IS NOT':
                        self._strwhere= self._strwhere + ' ' + conjunction + ' ' + columnname + ' ' + operator + ' NULL'
                    else:
                        self._strwhere= self._strwhere + ' ' + conjunction + ' ' + columnname + ' ' + operator + ' :' + str(self._paramidx)
                        self._param[str(self._paramidx)]=value
                        self._paramidx +=1
                else:
                    if operator.upper()=='IS' or operator.upper()=='IS NOT':
                        self._strwhere= self._strwhere + columnname + ' ' + operator + ' NULL'
                    else:
                        self._strwhere= self._strwhere + columnname + ' ' + operator + ' :' + str(self._paramidx)
                        self._param[str(self._paramidx)]=value
                        self._paramidx +=1
            else:
                raise AttributeError, "'" + operator + "'" + " - Not a supported operator."
        else:
            raise AttributeError, "'" + columnname + "'" + " - Not a Valid Column Name."
    def whereclear(self):
        ''' Resets the WHERE clause'''
        self._strwhere = ''
        self._param = {}
        self._paramidx = 1
class dt_location():
    ''' Class for table DT_LOCATION. Performs basic CRUD operation on table.'''
    def __init__(self):
        '''DT_LOCATION.columnnames - returns list of Column Names
           DT_LOCATION.pkey - returns list of tables primary key(s)
        '''
        self.columnnames = ['COMMONS_ID','LOC_ID','LOC_NAME','DATA_PROVIDER','LOC_DESC','LOC_TYPE','LOC_PURPOSE','LOC_COUNTY','LOC_DISTRICT','LOC_STATE','LAT','LON','NORTHBOUNDING','SOUTHBOUNDING','EASTBOUNDING','WESTBOUNDING','REMARK','START_DATE','END_DATE','COORD_SYSTEM','PROJECTION','LOC_ORDER','BASE_LOC_ID']
        self.pkey =['COMMONS_ID','LOC_ID']
        self._operator = ['=','!=','>=','<=','=>','=<','>','<','IS','IS NOT']
        self._strwhere = ''
        self._param = {}
        self._paramidx = 1
    def printset(self,cur,header=True):
        '''Prints to standard out the cursor pass to function
           example: Optional variables denoted []
           dt_location.printset(dt_location.select(),[header=False])
        '''
        if header:
            temp=[]
            for row in cur.description:
                temp.append(row[0])
            print tuple(temp)
        for row in cur:
            print row
    def selectpkey(self,COMMONS_ID,LOC_ID):
        '''Returns cursor of single record with associated Pkey.
           example:
           Cursor = dt_location.selectpkey(COMMONS_ID = <AppropriateKey>,LOC_ID = <AppropriateKey>)
        '''
        c1= connection.cursor()
        sql = "SELECT COMMONS_ID, LOC_ID, LOC_NAME, DATA_PROVIDER, LOC_DESC, LOC_TYPE, LOC_PURPOSE, LOC_COUNTY, LOC_DISTRICT, LOC_STATE, LAT, LON, NORTHBOUNDING, SOUTHBOUNDING, EASTBOUNDING, WESTBOUNDING, REMARK, START_DATE, END_DATE, COORD_SYSTEM, PROJECTION, LOC_ORDER, BASE_LOC_ID FROM DT_LOCATION"
        sql = sql + " WHERE COMMONS_ID = :COMMONS_ID AND LOC_ID = :LOC_ID"
        param ={'COMMONS_ID' : COMMONS_ID, 'LOC_ID' : LOC_ID}
        c1.execute(sql, param)
        return c1
    def select(self,columnList = 'ALL'):
        '''Returns cursor with all rows. Optional columnList(Python List) - List of columns to return.
           Optional - Run dt_location.where('COLUMN_NAME','=',AppropriateValue) function to provide a where clause.
               dt_location.where('COMMONS_ID', '=',<AppropriateValue>)
           example:		   
               Cursor = dt_location.select(columnList)
        '''
        if columnList == 'ALL':
            columnList= self.columnnames
        colstr=''
        c1 = connection.cursor()
        first=True
        for col in columnList:
            if not first:
                colstr=colstr + ', '
            first=False
            colstr=colstr + col
        sql = 'SELECT ' + colstr + ' FROM DT_LOCATION '
        if len(self._strwhere.strip())>0:
            sql = sql + 'WHERE ' + self._strwhere 
        c1.execute(sql,self._param)
        return c1
    #@transaction.commit_on_success()
    def update(self, COMMONS_ID, LOC_ID, datetime_format= 'YYYY-MM-DD HH24:MI:SS', **uargs):
        '''Updates record varaiables. Does not allow update of primary keys.
            example: 
            dt_location.update(COMMONS_ID = <AppropriateKey>,LOC_ID = <AppropriateKey>,[COLUMN_NAME = <UpdateValues>])
        '''
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
            if (colname == 'START_DATE' or colname == 'END_DATE'):
                sql =sql +  colname + ' = to_date(:' + colname + ', :datetime_format)'
                param['datetime_format'] = datetime_format
            else:
                sql =sql +  colname + ' = :' + colname
            param[colname]=val
        sql = sql + where
        c1.execute(sql, param)
        connection.commit()
    #@transaction.commit_on_success()
    def insert(self, COMMONS_ID, LOC_ID, datetime_format= 'YYYY-MM-DD HH24:MI:SS', **iargs):
        '''Insert record varaiables.
            example: 
            dt_location.insert(COMMONS_ID = <AppropriateKey>,LOC_ID = <AppropriateKey>,[COLUMN_NAME = <InsertValues>])
        '''
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
            if (colname == 'START_DATE' or colname == 'END_DATE'):
                vals = vals + ' to_date(:' + colname + ', :datetime_format)'
                param['datetime_format'] = datetime_format
            else:
                vals = vals + ':' + colname
            param[colname]=val
        sql = sql + col + ")" + vals + ")"
        c1.execute(sql,param)
        connection.commit()
    #@transaction.commit_on_success()
    def insertmany(self, ListDict , datetime_format= 'YYYY-MM-DD HH24:MI:SS'):
        '''Insert Many takes a list of Dictionaries which contain variables to insert. Must contain all columns for insertmany().
            example: 
            dt_location.insertmany(ListDict, datetime_format= 'YYYY-MM-DD HH24:MI:SS')
        '''
        c1 = connection.cursor()
        sql = "INSERT INTO DT_LOCATION "
        col = "("
        vals = " VALUES ("
        first=True
        for colname in self.columnnames:
            if not first:
                col=col + ", "
                vals=vals + ", "
            first=False
            col = col + colname
            if (colname == 'START_DATE' or colname == 'END_DATE'):
                vals = vals + ' to_date(:' + colname + ' ,'
                vals = vals + "'" + datetime_format + "'" + ')'
            else:
                vals = vals + ':' + colname
        sql = sql + col + ")" + vals + ")"
        c1.executemany(sql,ListDict)
        connection.commit()
    #@transaction.commit_on_success()
    def delete(self,COMMONS_ID, LOC_ID):
        '''Deletes record with associated Pkey.
           example:
           dt_location.delete(COMMONS_ID = <AppropriateKey>, LOC_ID = <AppropriateKey>)
        '''
        c1 = connection.cursor()
        param={}
        param['COMMONS_ID'] = COMMONS_ID
        param['LOC_ID'] = LOC_ID
        sql= 'DELETE FROM DT_LOCATION'
        sql = sql + ' WHERE COMMONS_ID = :COMMONS_ID AND LOC_ID = :LOC_ID'
        c1.execute(sql, param)
        connection.commit()
    def where(self,columnname,operator,value,conjunction='AND'):
        ''' Sets the WHERE clause for the select function. Default Conjunction is 'AND'
            example:
                DT_LOCATION.where('COlUMNNAME','=',AppropriateValue)
                DT_LOCATION.where('COlUMNNAME','=',AppropriateValue,'OR')
        '''
        if columnname in self.columnnames:
            if operator in self._operator:
                if len(self._strwhere)>0:
                    if operator.upper()=='IS' or operator.upper()=='IS NOT':
                        self._strwhere= self._strwhere + ' ' + conjunction + ' ' + columnname + ' ' + operator + ' NULL'
                    else:
                        self._strwhere= self._strwhere + ' ' + conjunction + ' ' + columnname + ' ' + operator + ' :' + str(self._paramidx)
                        self._param[str(self._paramidx)]=value
                        self._paramidx +=1
                else:
                    if operator.upper()=='IS' or operator.upper()=='IS NOT':
                        self._strwhere= self._strwhere + columnname + ' ' + operator + ' NULL'
                    else:
                        self._strwhere= self._strwhere + columnname + ' ' + operator + ' :' + str(self._paramidx)
                        self._param[str(self._paramidx)]=value
                        self._paramidx +=1
            else:
                raise AttributeError, "'" + operator + "'" + " - Not a supported operator."
        else:
            raise AttributeError, "'" + columnname + "'" + " - Not a Valid Column Name."
    def whereclear(self):
        ''' Resets the WHERE clause'''
        self._strwhere = ''
        self._param = {}
        self._paramidx = 1
class dt_location_parameter():
    ''' Class for table DT_LOCATION_PARAMETER. Performs basic CRUD operation on table.'''
    def __init__(self):
        '''DT_LOCATION_PARAMETER.columnnames - returns list of Column Names
           DT_LOCATION_PARAMETER.pkey - returns list of tables primary key(s)
        '''
        self.columnnames = ['COMMONS_ID','LOC_ID','PARAM_ID','PARAM_NAME','PARAM_VALUE','PARAM_UNIT','REMARK']
        self.pkey =['COMMONS_ID','LOC_ID','PARAM_ID']
        self._operator = ['=','!=','>=','<=','=>','=<','>','<','IS','IS NOT']
        self._strwhere = ''
        self._param = {}
        self._paramidx = 1
    def printset(self,cur,header=True):
        '''Prints to standard out the cursor pass to function
           example: Optional variables denoted []
           dt_location_parameter.printset(dt_location_parameter.select(),[header=False])
        '''
        if header:
            temp=[]
            for row in cur.description:
                temp.append(row[0])
            print tuple(temp)
        for row in cur:
            print row
    def selectpkey(self,COMMONS_ID,LOC_ID,PARAM_ID):
        '''Returns cursor of single record with associated Pkey.
           example:
           Cursor = dt_location_parameter.selectpkey(COMMONS_ID = <AppropriateKey>,LOC_ID = <AppropriateKey>,PARAM_ID = <AppropriateKey>)
        '''
        c1= connection.cursor()
        sql = "SELECT COMMONS_ID, LOC_ID, PARAM_ID, PARAM_NAME, PARAM_VALUE, PARAM_UNIT, REMARK FROM DT_LOCATION_PARAMETER"
        sql = sql + " WHERE COMMONS_ID = :COMMONS_ID AND LOC_ID = :LOC_ID AND PARAM_ID = :PARAM_ID"
        param ={'COMMONS_ID' : COMMONS_ID, 'LOC_ID' : LOC_ID, 'PARAM_ID' : PARAM_ID}
        c1.execute(sql, param)
        return c1
    def select(self,columnList = 'ALL'):
        '''Returns cursor with all rows. Optional columnList(Python List) - List of columns to return.
           Optional - Run dt_location_parameter.where('COLUMN_NAME','=',AppropriateValue) function to provide a where clause.
               dt_location_parameter.where('COMMONS_ID', '=',<AppropriateValue>)
           example:		   
               Cursor = dt_location_parameter.select(columnList)
        '''
        if columnList == 'ALL':
            columnList= self.columnnames
        colstr=''
        c1 = connection.cursor()
        first=True
        for col in columnList:
            if not first:
                colstr=colstr + ', '
            first=False
            colstr=colstr + col
        sql = 'SELECT ' + colstr + ' FROM DT_LOCATION_PARAMETER '
        if len(self._strwhere.strip())>0:
            sql = sql + 'WHERE ' + self._strwhere 
        c1.execute(sql,self._param)
        return c1
    #@transaction.commit_on_success()
    def update(self, COMMONS_ID, LOC_ID, PARAM_ID, **uargs):
        '''Updates record varaiables. Does not allow update of primary keys.
            example: 
            dt_location_parameter.update(COMMONS_ID = <AppropriateKey>,LOC_ID = <AppropriateKey>,PARAM_ID = <AppropriateKey>,[COLUMN_NAME = <UpdateValues>])
        '''
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
        '''Insert record varaiables.
            example: 
            dt_location_parameter.insert(COMMONS_ID = <AppropriateKey>,LOC_ID = <AppropriateKey>,PARAM_ID = <AppropriateKey>,[COLUMN_NAME = <InsertValues>])
        '''
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
    def insertmany(self, ListDict ):
        '''Insert Many takes a list of Dictionaries which contain variables to insert. Must contain all columns for insertmany().
            example: 
            dt_location_parameter.insertmany(ListDict)
        '''
        c1 = connection.cursor()
        sql = "INSERT INTO DT_LOCATION_PARAMETER "
        col = "("
        vals = " VALUES ("
        first=True
        for colname in self.columnnames:
            if not first:
                col=col + ", "
                vals=vals + ", "
            first=False
            col = col + colname
            vals = vals + ':' + colname
        sql = sql + col + ")" + vals + ")"
        c1.executemany(sql,ListDict)
        connection.commit()
    #@transaction.commit_on_success()
    def delete(self,COMMONS_ID, LOC_ID, PARAM_ID):
        '''Deletes record with associated Pkey.
           example:
           dt_location_parameter.delete(COMMONS_ID = <AppropriateKey>, LOC_ID = <AppropriateKey>, PARAM_ID = <AppropriateKey>)
        '''
        c1 = connection.cursor()
        param={}
        param['COMMONS_ID'] = COMMONS_ID
        param['LOC_ID'] = LOC_ID
        param['PARAM_ID'] = PARAM_ID
        sql= 'DELETE FROM DT_LOCATION_PARAMETER'
        sql = sql + ' WHERE COMMONS_ID = :COMMONS_ID AND LOC_ID = :LOC_ID AND PARAM_ID = :PARAM_ID'
        c1.execute(sql, param)
        connection.commit()
    def where(self,columnname,operator,value,conjunction='AND'):
        ''' Sets the WHERE clause for the select function. Default Conjunction is 'AND'
            example:
                DT_LOCATION_PARAMETER.where('COlUMNNAME','=',AppropriateValue)
                DT_LOCATION_PARAMETER.where('COlUMNNAME','=',AppropriateValue,'OR')
        '''
        if columnname in self.columnnames:
            if operator in self._operator:
                if len(self._strwhere)>0:
                    if operator.upper()=='IS' or operator.upper()=='IS NOT':
                        self._strwhere= self._strwhere + ' ' + conjunction + ' ' + columnname + ' ' + operator + ' NULL'
                    else:
                        self._strwhere= self._strwhere + ' ' + conjunction + ' ' + columnname + ' ' + operator + ' :' + str(self._paramidx)
                        self._param[str(self._paramidx)]=value
                        self._paramidx +=1
                else:
                    if operator.upper()=='IS' or operator.upper()=='IS NOT':
                        self._strwhere= self._strwhere + columnname + ' ' + operator + ' NULL'
                    else:
                        self._strwhere= self._strwhere + columnname + ' ' + operator + ' :' + str(self._paramidx)
                        self._param[str(self._paramidx)]=value
                        self._paramidx +=1
            else:
                raise AttributeError, "'" + operator + "'" + " - Not a supported operator."
        else:
            raise AttributeError, "'" + columnname + "'" + " - Not a Valid Column Name."
    def whereclear(self):
        ''' Resets the WHERE clause'''
        self._strwhere = ''
        self._param = {}
        self._paramidx = 1
class dt_person():
    ''' Class for table DT_PERSON. Performs basic CRUD operation on table.'''
    def __init__(self):
        '''DT_PERSON.columnnames - returns list of Column Names
           DT_PERSON.pkey - returns list of tables primary key(s)
        '''
        self.columnnames = ['PERSON_NAME','TITLE','ADDRESS1','ADDRESS2','CITY','STATE','POSTAL_CODE','COUNTRY','PHONE_NUMBER','FAX_NUMBER','ALT_PHONE_NUMBER','EMAIL_ADDRESS','COMPANY_CODE','PEOPLE_ID','USER_ID']
        self.pkey =['PEOPLE_ID']
        self._operator = ['=','!=','>=','<=','=>','=<','>','<','IS','IS NOT']
        self._strwhere = ''
        self._param = {}
        self._paramidx = 1
    def printset(self,cur,header=True):
        '''Prints to standard out the cursor pass to function
           example: Optional variables denoted []
           dt_person.printset(dt_person.select(),[header=False])
        '''
        if header:
            temp=[]
            for row in cur.description:
                temp.append(row[0])
            print tuple(temp)
        for row in cur:
            print row
    def selectpkey(self,PEOPLE_ID):
        '''Returns cursor of single record with associated Pkey.
           example:
           Cursor = dt_person.selectpkey(PEOPLE_ID = <AppropriateKey>)
        '''
        c1= connection.cursor()
        sql = "SELECT PERSON_NAME, TITLE, ADDRESS1, ADDRESS2, CITY, STATE, POSTAL_CODE, COUNTRY, PHONE_NUMBER, FAX_NUMBER, ALT_PHONE_NUMBER, EMAIL_ADDRESS, COMPANY_CODE, PEOPLE_ID, USER_ID FROM DT_PERSON"
        sql = sql + " WHERE PEOPLE_ID = :PEOPLE_ID"
        param ={'PEOPLE_ID' : PEOPLE_ID}
        c1.execute(sql, param)
        return c1
    def select(self,columnList = 'ALL'):
        '''Returns cursor with all rows. Optional columnList(Python List) - List of columns to return.
           Optional - Run dt_person.where('COLUMN_NAME','=',AppropriateValue) function to provide a where clause.
               dt_person.where('PEOPLE_ID', '=',<AppropriateValue>)
           example:		   
               Cursor = dt_person.select(columnList)
        '''
        if columnList == 'ALL':
            columnList= self.columnnames
        colstr=''
        c1 = connection.cursor()
        first=True
        for col in columnList:
            if not first:
                colstr=colstr + ', '
            first=False
            colstr=colstr + col
        sql = 'SELECT ' + colstr + ' FROM DT_PERSON '
        if len(self._strwhere.strip())>0:
            sql = sql + 'WHERE ' + self._strwhere 
        c1.execute(sql,self._param)
        return c1
    #@transaction.commit_on_success()
    def update(self, PEOPLE_ID, **uargs):
        '''Updates record varaiables. Does not allow update of primary keys.
            example: 
            dt_person.update(PEOPLE_ID = <AppropriateKey>,[COLUMN_NAME = <UpdateValues>])
        '''
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
        '''Insert record varaiables.
            example: 
            dt_person.insert(PEOPLE_ID = <AppropriateKey>,[COLUMN_NAME = <InsertValues>])
        '''
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
    def insertmany(self, ListDict ):
        '''Insert Many takes a list of Dictionaries which contain variables to insert. Must contain all columns for insertmany().
            example: 
            dt_person.insertmany(ListDict)
        '''
        c1 = connection.cursor()
        sql = "INSERT INTO DT_PERSON "
        col = "("
        vals = " VALUES ("
        first=True
        for colname in self.columnnames:
            if not first:
                col=col + ", "
                vals=vals + ", "
            first=False
            col = col + colname
            vals = vals + ':' + colname
        sql = sql + col + ")" + vals + ")"
        c1.executemany(sql,ListDict)
        connection.commit()
    #@transaction.commit_on_success()
    def delete(self,PEOPLE_ID):
        '''Deletes record with associated Pkey.
           example:
           dt_person.delete(PEOPLE_ID = <AppropriateKey>)
        '''
        c1 = connection.cursor()
        param={}
        param['PEOPLE_ID'] = PEOPLE_ID
        sql= 'DELETE FROM DT_PERSON'
        sql = sql + ' WHERE PEOPLE_ID = :PEOPLE_ID'
        c1.execute(sql, param)
        connection.commit()
    def where(self,columnname,operator,value,conjunction='AND'):
        ''' Sets the WHERE clause for the select function. Default Conjunction is 'AND'
            example:
                DT_PERSON.where('COlUMNNAME','=',AppropriateValue)
                DT_PERSON.where('COlUMNNAME','=',AppropriateValue,'OR')
        '''
        if columnname in self.columnnames:
            if operator in self._operator:
                if len(self._strwhere)>0:
                    if operator.upper()=='IS' or operator.upper()=='IS NOT':
                        self._strwhere= self._strwhere + ' ' + conjunction + ' ' + columnname + ' ' + operator + ' NULL'
                    else:
                        self._strwhere= self._strwhere + ' ' + conjunction + ' ' + columnname + ' ' + operator + ' :' + str(self._paramidx)
                        self._param[str(self._paramidx)]=value
                        self._paramidx +=1
                else:
                    if operator.upper()=='IS' or operator.upper()=='IS NOT':
                        self._strwhere= self._strwhere + columnname + ' ' + operator + ' NULL'
                    else:
                        self._strwhere= self._strwhere + columnname + ' ' + operator + ' :' + str(self._paramidx)
                        self._param[str(self._paramidx)]=value
                        self._paramidx +=1
            else:
                raise AttributeError, "'" + operator + "'" + " - Not a supported operator."
        else:
            raise AttributeError, "'" + columnname + "'" + " - Not a Valid Column Name."
    def whereclear(self):
        ''' Resets the WHERE clause'''
        self._strwhere = ''
        self._param = {}
        self._paramidx = 1
class dt_result():
    ''' Class for table DT_RESULT. Performs basic CRUD operation on table.'''
    def __init__(self):
        '''DT_RESULT.columnnames - returns list of Column Names
           DT_RESULT.pkey - returns list of tables primary key(s)
        '''
        self.columnnames = ['COMMONS_ID','EVENT_ID','VAR_ID','RESULT_TEXT','RESULT_NUMERIC','RESULT_ERROR','RESULT_DATE','STAT_RESULT','RESULT_ORDER','RESULT_UNIT','REMARK','VALUE_TYPE','STAT_TYPE','VALIDATED']
        self.pkey =['COMMONS_ID','EVENT_ID','VAR_ID']
        self._operator = ['=','!=','>=','<=','=>','=<','>','<','IS','IS NOT']
        self._strwhere = ''
        self._param = {}
        self._paramidx = 1
    def printset(self,cur,header=True):
        '''Prints to standard out the cursor pass to function
           example: Optional variables denoted []
           dt_result.printset(dt_result.select(),[header=False])
        '''
        if header:
            temp=[]
            for row in cur.description:
                temp.append(row[0])
            print tuple(temp)
        for row in cur:
            print row
    def selectpkey(self,COMMONS_ID,EVENT_ID,VAR_ID):
        '''Returns cursor of single record with associated Pkey.
           example:
           Cursor = dt_result.selectpkey(COMMONS_ID = <AppropriateKey>,EVENT_ID = <AppropriateKey>,VAR_ID = <AppropriateKey>)
        '''
        c1= connection.cursor()
        sql = "SELECT COMMONS_ID, EVENT_ID, VAR_ID, RESULT_TEXT, RESULT_NUMERIC, RESULT_ERROR, RESULT_DATE, STAT_RESULT, RESULT_ORDER, RESULT_UNIT, REMARK, VALUE_TYPE, STAT_TYPE, VALIDATED FROM DT_RESULT"
        sql = sql + " WHERE COMMONS_ID = :COMMONS_ID AND EVENT_ID = :EVENT_ID AND VAR_ID = :VAR_ID"
        param ={'COMMONS_ID' : COMMONS_ID, 'EVENT_ID' : EVENT_ID, 'VAR_ID' : VAR_ID}
        c1.execute(sql, param)
        return c1
    def select(self,columnList = 'ALL'):
        '''Returns cursor with all rows. Optional columnList(Python List) - List of columns to return.
           Optional - Run dt_result.where('COLUMN_NAME','=',AppropriateValue) function to provide a where clause.
               dt_result.where('COMMONS_ID', '=',<AppropriateValue>)
           example:		   
               Cursor = dt_result.select(columnList)
        '''
        if columnList == 'ALL':
            columnList= self.columnnames
        colstr=''
        c1 = connection.cursor()
        first=True
        for col in columnList:
            if not first:
                colstr=colstr + ', '
            first=False
            colstr=colstr + col
        sql = 'SELECT ' + colstr + ' FROM DT_RESULT '
        if len(self._strwhere.strip())>0:
            sql = sql + 'WHERE ' + self._strwhere 
        c1.execute(sql,self._param)
        return c1
    #@transaction.commit_on_success()
    def update(self, COMMONS_ID, EVENT_ID, VAR_ID, datetime_format= 'YYYY-MM-DD HH24:MI:SS', **uargs):
        '''Updates record varaiables. Does not allow update of primary keys.
            example: 
            dt_result.update(COMMONS_ID = <AppropriateKey>,EVENT_ID = <AppropriateKey>,VAR_ID = <AppropriateKey>,[COLUMN_NAME = <UpdateValues>])
        '''
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
            if (colname == 'RESULT_DATE'):
                sql =sql +  colname + ' = to_date(:' + colname + ', :datetime_format)'
                param['datetime_format'] = datetime_format
            else:
                sql =sql +  colname + ' = :' + colname
            param[colname]=val
        sql = sql + where
        c1.execute(sql, param)
        connection.commit()
    #@transaction.commit_on_success()
    def insert(self, COMMONS_ID, EVENT_ID, VAR_ID, datetime_format= 'YYYY-MM-DD HH24:MI:SS', **iargs):
        '''Insert record varaiables.
            example: 
            dt_result.insert(COMMONS_ID = <AppropriateKey>,EVENT_ID = <AppropriateKey>,VAR_ID = <AppropriateKey>,[COLUMN_NAME = <InsertValues>])
        '''
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
            if (colname == 'RESULT_DATE'):
                vals = vals + ' to_date(:' + colname + ', :datetime_format)'
                param['datetime_format'] = datetime_format
            else:
                vals = vals + ':' + colname
            param[colname]=val
        sql = sql + col + ")" + vals + ")"
        c1.execute(sql,param)
        connection.commit()
    #@transaction.commit_on_success()
    def insertmany(self, ListDict , datetime_format= 'YYYY-MM-DD HH24:MI:SS'):
        '''Insert Many takes a list of Dictionaries which contain variables to insert. Must contain all columns for insertmany().
            example: 
            dt_result.insertmany(ListDict, datetime_format= 'YYYY-MM-DD HH24:MI:SS')
        '''
        c1 = connection.cursor()
        sql = "INSERT INTO DT_RESULT "
        col = "("
        vals = " VALUES ("
        first=True
        for colname in self.columnnames:
            if not first:
                col=col + ", "
                vals=vals + ", "
            first=False
            col = col + colname
            if (colname == 'RESULT_DATE'):
                vals = vals + ' to_date(:' + colname + ' ,'
                vals = vals + "'" + datetime_format + "'" + ')'
            else:
                vals = vals + ':' + colname
        sql = sql + col + ")" + vals + ")"
        c1.executemany(sql,ListDict)
        connection.commit()
    #@transaction.commit_on_success()
    def delete(self,COMMONS_ID, EVENT_ID, VAR_ID):
        '''Deletes record with associated Pkey.
           example:
           dt_result.delete(COMMONS_ID = <AppropriateKey>, EVENT_ID = <AppropriateKey>, VAR_ID = <AppropriateKey>)
        '''
        c1 = connection.cursor()
        param={}
        param['COMMONS_ID'] = COMMONS_ID
        param['EVENT_ID'] = EVENT_ID
        param['VAR_ID'] = VAR_ID
        sql= 'DELETE FROM DT_RESULT'
        sql = sql + ' WHERE COMMONS_ID = :COMMONS_ID AND EVENT_ID = :EVENT_ID AND VAR_ID = :VAR_ID'
        c1.execute(sql, param)
        connection.commit()
    def where(self,columnname,operator,value,conjunction='AND'):
        ''' Sets the WHERE clause for the select function. Default Conjunction is 'AND'
            example:
                DT_RESULT.where('COlUMNNAME','=',AppropriateValue)
                DT_RESULT.where('COlUMNNAME','=',AppropriateValue,'OR')
        '''
        if columnname in self.columnnames:
            if operator in self._operator:
                if len(self._strwhere)>0:
                    if operator.upper()=='IS' or operator.upper()=='IS NOT':
                        self._strwhere= self._strwhere + ' ' + conjunction + ' ' + columnname + ' ' + operator + ' NULL'
                    else:
                        self._strwhere= self._strwhere + ' ' + conjunction + ' ' + columnname + ' ' + operator + ' :' + str(self._paramidx)
                        self._param[str(self._paramidx)]=value
                        self._paramidx +=1
                else:
                    if operator.upper()=='IS' or operator.upper()=='IS NOT':
                        self._strwhere= self._strwhere + columnname + ' ' + operator + ' NULL'
                    else:
                        self._strwhere= self._strwhere + columnname + ' ' + operator + ' :' + str(self._paramidx)
                        self._param[str(self._paramidx)]=value
                        self._paramidx +=1
            else:
                raise AttributeError, "'" + operator + "'" + " - Not a supported operator."
        else:
            raise AttributeError, "'" + columnname + "'" + " - Not a Valid Column Name."
    def whereclear(self):
        ''' Resets the WHERE clause'''
        self._strwhere = ''
        self._param = {}
        self._paramidx = 1
class dt_type():
    ''' Class for table DT_TYPE. Performs basic CRUD operation on table.'''
    def __init__(self):
        '''DT_TYPE.columnnames - returns list of Column Names
           DT_TYPE.pkey - returns list of tables primary key(s)
        '''
        self.columnnames = ['TYPE_ID','TYPE_NAME','PRODUCT','DESCRIPTION','RESOLUTION','RES_UNIT','OBJECT_TYPE','OBJECT_DATA_OPT1','OBJECT_DATA_OPT1_UNIT']
        self.pkey =['TYPE_ID']
        self._operator = ['=','!=','>=','<=','=>','=<','>','<','IS','IS NOT']
        self._strwhere = ''
        self._param = {}
        self._paramidx = 1
    def printset(self,cur,header=True):
        '''Prints to standard out the cursor pass to function
           example: Optional variables denoted []
           dt_type.printset(dt_type.select(),[header=False])
        '''
        if header:
            temp=[]
            for row in cur.description:
                temp.append(row[0])
            print tuple(temp)
        for row in cur:
            print row
    def selectpkey(self,TYPE_ID):
        '''Returns cursor of single record with associated Pkey.
           example:
           Cursor = dt_type.selectpkey(TYPE_ID = <AppropriateKey>)
        '''
        c1= connection.cursor()
        sql = "SELECT TYPE_ID, TYPE_NAME, PRODUCT, DESCRIPTION, RESOLUTION, RES_UNIT, OBJECT_TYPE, OBJECT_DATA_OPT1, OBJECT_DATA_OPT1_UNIT FROM DT_TYPE"
        sql = sql + " WHERE TYPE_ID = :TYPE_ID"
        param ={'TYPE_ID' : TYPE_ID}
        c1.execute(sql, param)
        return c1
    def select(self,columnList = 'ALL'):
        '''Returns cursor with all rows. Optional columnList(Python List) - List of columns to return.
           Optional - Run dt_type.where('COLUMN_NAME','=',AppropriateValue) function to provide a where clause.
               dt_type.where('TYPE_ID', '=',<AppropriateValue>)
           example:		   
               Cursor = dt_type.select(columnList)
        '''
        if columnList == 'ALL':
            columnList= self.columnnames
        colstr=''
        c1 = connection.cursor()
        first=True
        for col in columnList:
            if not first:
                colstr=colstr + ', '
            first=False
            colstr=colstr + col
        sql = 'SELECT ' + colstr + ' FROM DT_TYPE '
        if len(self._strwhere.strip())>0:
            sql = sql + 'WHERE ' + self._strwhere 
        c1.execute(sql,self._param)
        return c1
    #@transaction.commit_on_success()
    def update(self, TYPE_ID, **uargs):
        '''Updates record varaiables. Does not allow update of primary keys.
            example: 
            dt_type.update(TYPE_ID = <AppropriateKey>,[COLUMN_NAME = <UpdateValues>])
        '''
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
        '''Insert record varaiables.
            example: 
            dt_type.insert(TYPE_ID = <AppropriateKey>,[COLUMN_NAME = <InsertValues>])
        '''
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
    def insertmany(self, ListDict ):
        '''Insert Many takes a list of Dictionaries which contain variables to insert. Must contain all columns for insertmany().
            example: 
            dt_type.insertmany(ListDict)
        '''
        c1 = connection.cursor()
        sql = "INSERT INTO DT_TYPE "
        col = "("
        vals = " VALUES ("
        first=True
        for colname in self.columnnames:
            if not first:
                col=col + ", "
                vals=vals + ", "
            first=False
            col = col + colname
            vals = vals + ':' + colname
        sql = sql + col + ")" + vals + ")"
        c1.executemany(sql,ListDict)
        connection.commit()
    #@transaction.commit_on_success()
    def delete(self,TYPE_ID):
        '''Deletes record with associated Pkey.
           example:
           dt_type.delete(TYPE_ID = <AppropriateKey>)
        '''
        c1 = connection.cursor()
        param={}
        param['TYPE_ID'] = TYPE_ID
        sql= 'DELETE FROM DT_TYPE'
        sql = sql + ' WHERE TYPE_ID = :TYPE_ID'
        c1.execute(sql, param)
        connection.commit()
    def where(self,columnname,operator,value,conjunction='AND'):
        ''' Sets the WHERE clause for the select function. Default Conjunction is 'AND'
            example:
                DT_TYPE.where('COlUMNNAME','=',AppropriateValue)
                DT_TYPE.where('COlUMNNAME','=',AppropriateValue,'OR')
        '''
        if columnname in self.columnnames:
            if operator in self._operator:
                if len(self._strwhere)>0:
                    if operator.upper()=='IS' or operator.upper()=='IS NOT':
                        self._strwhere= self._strwhere + ' ' + conjunction + ' ' + columnname + ' ' + operator + ' NULL'
                    else:
                        self._strwhere= self._strwhere + ' ' + conjunction + ' ' + columnname + ' ' + operator + ' :' + str(self._paramidx)
                        self._param[str(self._paramidx)]=value
                        self._paramidx +=1
                else:
                    if operator.upper()=='IS' or operator.upper()=='IS NOT':
                        self._strwhere= self._strwhere + columnname + ' ' + operator + ' NULL'
                    else:
                        self._strwhere= self._strwhere + columnname + ' ' + operator + ' :' + str(self._paramidx)
                        self._param[str(self._paramidx)]=value
                        self._paramidx +=1
            else:
                raise AttributeError, "'" + operator + "'" + " - Not a supported operator."
        else:
            raise AttributeError, "'" + columnname + "'" + " - Not a Valid Column Name."
    def whereclear(self):
        ''' Resets the WHERE clause'''
        self._strwhere = ''
        self._param = {}
        self._paramidx = 1
class rt_file_type():
    ''' Class for table RT_FILE_TYPE. Performs basic CRUD operation on table.'''
    def __init__(self):
        '''RT_FILE_TYPE.columnnames - returns list of Column Names
           RT_FILE_TYPE.pkey - returns list of tables primary key(s)
        '''
        self.columnnames = ['FILE_TYPE','APP_CODE','FILE_TYPE_DESC','STATUS_FLAG','REMARK','MIME_TYPE']
        self.pkey =['FILE_TYPE']
        self._operator = ['=','!=','>=','<=','=>','=<','>','<','IS','IS NOT']
        self._strwhere = ''
        self._param = {}
        self._paramidx = 1
    def printset(self,cur,header=True):
        '''Prints to standard out the cursor pass to function
           example: Optional variables denoted []
           rt_file_type.printset(rt_file_type.select(),[header=False])
        '''
        if header:
            temp=[]
            for row in cur.description:
                temp.append(row[0])
            print tuple(temp)
        for row in cur:
            print row
    def selectpkey(self,FILE_TYPE):
        '''Returns cursor of single record with associated Pkey.
           example:
           Cursor = rt_file_type.selectpkey(FILE_TYPE = <AppropriateKey>)
        '''
        c1= connection.cursor()
        sql = "SELECT FILE_TYPE, APP_CODE, FILE_TYPE_DESC, STATUS_FLAG, REMARK, MIME_TYPE FROM RT_FILE_TYPE"
        sql = sql + " WHERE FILE_TYPE = :FILE_TYPE"
        param ={'FILE_TYPE' : FILE_TYPE}
        c1.execute(sql, param)
        return c1
    def select(self,columnList = 'ALL'):
        '''Returns cursor with all rows. Optional columnList(Python List) - List of columns to return.
           Optional - Run rt_file_type.where('COLUMN_NAME','=',AppropriateValue) function to provide a where clause.
               rt_file_type.where('FILE_TYPE', '=',<AppropriateValue>)
           example:		   
               Cursor = rt_file_type.select(columnList)
        '''
        if columnList == 'ALL':
            columnList= self.columnnames
        colstr=''
        c1 = connection.cursor()
        first=True
        for col in columnList:
            if not first:
                colstr=colstr + ', '
            first=False
            colstr=colstr + col
        sql = 'SELECT ' + colstr + ' FROM RT_FILE_TYPE '
        if len(self._strwhere.strip())>0:
            sql = sql + 'WHERE ' + self._strwhere 
        c1.execute(sql,self._param)
        return c1
    #@transaction.commit_on_success()
    def update(self, FILE_TYPE, **uargs):
        '''Updates record varaiables. Does not allow update of primary keys.
            example: 
            rt_file_type.update(FILE_TYPE = <AppropriateKey>,[COLUMN_NAME = <UpdateValues>])
        '''
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
        '''Insert record varaiables.
            example: 
            rt_file_type.insert(FILE_TYPE = <AppropriateKey>,[COLUMN_NAME = <InsertValues>])
        '''
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
    def insertmany(self, ListDict ):
        '''Insert Many takes a list of Dictionaries which contain variables to insert. Must contain all columns for insertmany().
            example: 
            rt_file_type.insertmany(ListDict)
        '''
        c1 = connection.cursor()
        sql = "INSERT INTO RT_FILE_TYPE "
        col = "("
        vals = " VALUES ("
        first=True
        for colname in self.columnnames:
            if not first:
                col=col + ", "
                vals=vals + ", "
            first=False
            col = col + colname
            vals = vals + ':' + colname
        sql = sql + col + ")" + vals + ")"
        c1.executemany(sql,ListDict)
        connection.commit()
    #@transaction.commit_on_success()
    def delete(self,FILE_TYPE):
        '''Deletes record with associated Pkey.
           example:
           rt_file_type.delete(FILE_TYPE = <AppropriateKey>)
        '''
        c1 = connection.cursor()
        param={}
        param['FILE_TYPE'] = FILE_TYPE
        sql= 'DELETE FROM RT_FILE_TYPE'
        sql = sql + ' WHERE FILE_TYPE = :FILE_TYPE'
        c1.execute(sql, param)
        connection.commit()
    def where(self,columnname,operator,value,conjunction='AND'):
        ''' Sets the WHERE clause for the select function. Default Conjunction is 'AND'
            example:
                RT_FILE_TYPE.where('COlUMNNAME','=',AppropriateValue)
                RT_FILE_TYPE.where('COlUMNNAME','=',AppropriateValue,'OR')
        '''
        if columnname in self.columnnames:
            if operator in self._operator:
                if len(self._strwhere)>0:
                    if operator.upper()=='IS' or operator.upper()=='IS NOT':
                        self._strwhere= self._strwhere + ' ' + conjunction + ' ' + columnname + ' ' + operator + ' NULL'
                    else:
                        self._strwhere= self._strwhere + ' ' + conjunction + ' ' + columnname + ' ' + operator + ' :' + str(self._paramidx)
                        self._param[str(self._paramidx)]=value
                        self._paramidx +=1
                else:
                    if operator.upper()=='IS' or operator.upper()=='IS NOT':
                        self._strwhere= self._strwhere + columnname + ' ' + operator + ' NULL'
                    else:
                        self._strwhere= self._strwhere + columnname + ' ' + operator + ' :' + str(self._paramidx)
                        self._param[str(self._paramidx)]=value
                        self._paramidx +=1
            else:
                raise AttributeError, "'" + operator + "'" + " - Not a supported operator."
        else:
            raise AttributeError, "'" + columnname + "'" + " - Not a Valid Column Name."
    def whereclear(self):
        ''' Resets the WHERE clause'''
        self._strwhere = ''
        self._param = {}
        self._paramidx = 1
class rt_location_param_type():
    ''' Class for table RT_LOCATION_PARAM_TYPE. Performs basic CRUD operation on table.'''
    def __init__(self):
        '''RT_LOCATION_PARAM_TYPE.columnnames - returns list of Column Names
           RT_LOCATION_PARAM_TYPE.pkey - returns list of tables primary key(s)
        '''
        self.columnnames = ['PARAM_CODE','PARAM_DESC','STATUS_FLAG','STANDARD_UNIT','REMARK']
        self.pkey =['PARAM_CODE']
        self._operator = ['=','!=','>=','<=','=>','=<','>','<','IS','IS NOT']
        self._strwhere = ''
        self._param = {}
        self._paramidx = 1
    def printset(self,cur,header=True):
        '''Prints to standard out the cursor pass to function
           example: Optional variables denoted []
           rt_location_param_type.printset(rt_location_param_type.select(),[header=False])
        '''
        if header:
            temp=[]
            for row in cur.description:
                temp.append(row[0])
            print tuple(temp)
        for row in cur:
            print row
    def selectpkey(self,PARAM_CODE):
        '''Returns cursor of single record with associated Pkey.
           example:
           Cursor = rt_location_param_type.selectpkey(PARAM_CODE = <AppropriateKey>)
        '''
        c1= connection.cursor()
        sql = "SELECT PARAM_CODE, PARAM_DESC, STATUS_FLAG, STANDARD_UNIT, REMARK FROM RT_LOCATION_PARAM_TYPE"
        sql = sql + " WHERE PARAM_CODE = :PARAM_CODE"
        param ={'PARAM_CODE' : PARAM_CODE}
        c1.execute(sql, param)
        return c1
    def select(self,columnList = 'ALL'):
        '''Returns cursor with all rows. Optional columnList(Python List) - List of columns to return.
           Optional - Run rt_location_param_type.where('COLUMN_NAME','=',AppropriateValue) function to provide a where clause.
               rt_location_param_type.where('PARAM_CODE', '=',<AppropriateValue>)
           example:		   
               Cursor = rt_location_param_type.select(columnList)
        '''
        if columnList == 'ALL':
            columnList= self.columnnames
        colstr=''
        c1 = connection.cursor()
        first=True
        for col in columnList:
            if not first:
                colstr=colstr + ', '
            first=False
            colstr=colstr + col
        sql = 'SELECT ' + colstr + ' FROM RT_LOCATION_PARAM_TYPE '
        if len(self._strwhere.strip())>0:
            sql = sql + 'WHERE ' + self._strwhere 
        c1.execute(sql,self._param)
        return c1
    #@transaction.commit_on_success()
    def update(self, PARAM_CODE, **uargs):
        '''Updates record varaiables. Does not allow update of primary keys.
            example: 
            rt_location_param_type.update(PARAM_CODE = <AppropriateKey>,[COLUMN_NAME = <UpdateValues>])
        '''
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
        '''Insert record varaiables.
            example: 
            rt_location_param_type.insert(PARAM_CODE = <AppropriateKey>,[COLUMN_NAME = <InsertValues>])
        '''
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
    def insertmany(self, ListDict ):
        '''Insert Many takes a list of Dictionaries which contain variables to insert. Must contain all columns for insertmany().
            example: 
            rt_location_param_type.insertmany(ListDict)
        '''
        c1 = connection.cursor()
        sql = "INSERT INTO RT_LOCATION_PARAM_TYPE "
        col = "("
        vals = " VALUES ("
        first=True
        for colname in self.columnnames:
            if not first:
                col=col + ", "
                vals=vals + ", "
            first=False
            col = col + colname
            vals = vals + ':' + colname
        sql = sql + col + ")" + vals + ")"
        c1.executemany(sql,ListDict)
        connection.commit()
    #@transaction.commit_on_success()
    def delete(self,PARAM_CODE):
        '''Deletes record with associated Pkey.
           example:
           rt_location_param_type.delete(PARAM_CODE = <AppropriateKey>)
        '''
        c1 = connection.cursor()
        param={}
        param['PARAM_CODE'] = PARAM_CODE
        sql= 'DELETE FROM RT_LOCATION_PARAM_TYPE'
        sql = sql + ' WHERE PARAM_CODE = :PARAM_CODE'
        c1.execute(sql, param)
        connection.commit()
    def where(self,columnname,operator,value,conjunction='AND'):
        ''' Sets the WHERE clause for the select function. Default Conjunction is 'AND'
            example:
                RT_LOCATION_PARAM_TYPE.where('COlUMNNAME','=',AppropriateValue)
                RT_LOCATION_PARAM_TYPE.where('COlUMNNAME','=',AppropriateValue,'OR')
        '''
        if columnname in self.columnnames:
            if operator in self._operator:
                if len(self._strwhere)>0:
                    if operator.upper()=='IS' or operator.upper()=='IS NOT':
                        self._strwhere= self._strwhere + ' ' + conjunction + ' ' + columnname + ' ' + operator + ' NULL'
                    else:
                        self._strwhere= self._strwhere + ' ' + conjunction + ' ' + columnname + ' ' + operator + ' :' + str(self._paramidx)
                        self._param[str(self._paramidx)]=value
                        self._paramidx +=1
                else:
                    if operator.upper()=='IS' or operator.upper()=='IS NOT':
                        self._strwhere= self._strwhere + columnname + ' ' + operator + ' NULL'
                    else:
                        self._strwhere= self._strwhere + columnname + ' ' + operator + ' :' + str(self._paramidx)
                        self._param[str(self._paramidx)]=value
                        self._paramidx +=1
            else:
                raise AttributeError, "'" + operator + "'" + " - Not a supported operator."
        else:
            raise AttributeError, "'" + columnname + "'" + " - Not a Valid Column Name."
    def whereclear(self):
        ''' Resets the WHERE clause'''
        self._strwhere = ''
        self._param = {}
        self._paramidx = 1
class rt_location_type():
    ''' Class for table RT_LOCATION_TYPE. Performs basic CRUD operation on table.'''
    def __init__(self):
        '''RT_LOCATION_TYPE.columnnames - returns list of Column Names
           RT_LOCATION_TYPE.pkey - returns list of tables primary key(s)
        '''
        self.columnnames = ['LOCATION_TYPE_CODE','LOCATION_TYPE_DESC','STATUS_FLAG','REMARK']
        self.pkey =['LOCATION_TYPE_CODE']
        self._operator = ['=','!=','>=','<=','=>','=<','>','<','IS','IS NOT']
        self._strwhere = ''
        self._param = {}
        self._paramidx = 1
    def printset(self,cur,header=True):
        '''Prints to standard out the cursor pass to function
           example: Optional variables denoted []
           rt_location_type.printset(rt_location_type.select(),[header=False])
        '''
        if header:
            temp=[]
            for row in cur.description:
                temp.append(row[0])
            print tuple(temp)
        for row in cur:
            print row
    def selectpkey(self,LOCATION_TYPE_CODE):
        '''Returns cursor of single record with associated Pkey.
           example:
           Cursor = rt_location_type.selectpkey(LOCATION_TYPE_CODE = <AppropriateKey>)
        '''
        c1= connection.cursor()
        sql = "SELECT LOCATION_TYPE_CODE, LOCATION_TYPE_DESC, STATUS_FLAG, REMARK FROM RT_LOCATION_TYPE"
        sql = sql + " WHERE LOCATION_TYPE_CODE = :LOCATION_TYPE_CODE"
        param ={'LOCATION_TYPE_CODE' : LOCATION_TYPE_CODE}
        c1.execute(sql, param)
        return c1
    def select(self,columnList = 'ALL'):
        '''Returns cursor with all rows. Optional columnList(Python List) - List of columns to return.
           Optional - Run rt_location_type.where('COLUMN_NAME','=',AppropriateValue) function to provide a where clause.
               rt_location_type.where('LOCATION_TYPE_CODE', '=',<AppropriateValue>)
           example:		   
               Cursor = rt_location_type.select(columnList)
        '''
        if columnList == 'ALL':
            columnList= self.columnnames
        colstr=''
        c1 = connection.cursor()
        first=True
        for col in columnList:
            if not first:
                colstr=colstr + ', '
            first=False
            colstr=colstr + col
        sql = 'SELECT ' + colstr + ' FROM RT_LOCATION_TYPE '
        if len(self._strwhere.strip())>0:
            sql = sql + 'WHERE ' + self._strwhere 
        c1.execute(sql,self._param)
        return c1
    #@transaction.commit_on_success()
    def update(self, LOCATION_TYPE_CODE, **uargs):
        '''Updates record varaiables. Does not allow update of primary keys.
            example: 
            rt_location_type.update(LOCATION_TYPE_CODE = <AppropriateKey>,[COLUMN_NAME = <UpdateValues>])
        '''
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
        '''Insert record varaiables.
            example: 
            rt_location_type.insert(LOCATION_TYPE_CODE = <AppropriateKey>,[COLUMN_NAME = <InsertValues>])
        '''
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
    def insertmany(self, ListDict ):
        '''Insert Many takes a list of Dictionaries which contain variables to insert. Must contain all columns for insertmany().
            example: 
            rt_location_type.insertmany(ListDict)
        '''
        c1 = connection.cursor()
        sql = "INSERT INTO RT_LOCATION_TYPE "
        col = "("
        vals = " VALUES ("
        first=True
        for colname in self.columnnames:
            if not first:
                col=col + ", "
                vals=vals + ", "
            first=False
            col = col + colname
            vals = vals + ':' + colname
        sql = sql + col + ")" + vals + ")"
        c1.executemany(sql,ListDict)
        connection.commit()
    #@transaction.commit_on_success()
    def delete(self,LOCATION_TYPE_CODE):
        '''Deletes record with associated Pkey.
           example:
           rt_location_type.delete(LOCATION_TYPE_CODE = <AppropriateKey>)
        '''
        c1 = connection.cursor()
        param={}
        param['LOCATION_TYPE_CODE'] = LOCATION_TYPE_CODE
        sql= 'DELETE FROM RT_LOCATION_TYPE'
        sql = sql + ' WHERE LOCATION_TYPE_CODE = :LOCATION_TYPE_CODE'
        c1.execute(sql, param)
        connection.commit()
    def where(self,columnname,operator,value,conjunction='AND'):
        ''' Sets the WHERE clause for the select function. Default Conjunction is 'AND'
            example:
                RT_LOCATION_TYPE.where('COlUMNNAME','=',AppropriateValue)
                RT_LOCATION_TYPE.where('COlUMNNAME','=',AppropriateValue,'OR')
        '''
        if columnname in self.columnnames:
            if operator in self._operator:
                if len(self._strwhere)>0:
                    if operator.upper()=='IS' or operator.upper()=='IS NOT':
                        self._strwhere= self._strwhere + ' ' + conjunction + ' ' + columnname + ' ' + operator + ' NULL'
                    else:
                        self._strwhere= self._strwhere + ' ' + conjunction + ' ' + columnname + ' ' + operator + ' :' + str(self._paramidx)
                        self._param[str(self._paramidx)]=value
                        self._paramidx +=1
                else:
                    if operator.upper()=='IS' or operator.upper()=='IS NOT':
                        self._strwhere= self._strwhere + columnname + ' ' + operator + ' NULL'
                    else:
                        self._strwhere= self._strwhere + columnname + ' ' + operator + ' :' + str(self._paramidx)
                        self._param[str(self._paramidx)]=value
                        self._paramidx +=1
            else:
                raise AttributeError, "'" + operator + "'" + " - Not a supported operator."
        else:
            raise AttributeError, "'" + columnname + "'" + " - Not a Valid Column Name."
    def whereclear(self):
        ''' Resets the WHERE clause'''
        self._strwhere = ''
        self._param = {}
        self._paramidx = 1
class rt_method():
    ''' Class for table RT_METHOD. Performs basic CRUD operation on table.'''
    def __init__(self):
        '''RT_METHOD.columnnames - returns list of Column Names
           RT_METHOD.pkey - returns list of tables primary key(s)
        '''
        self.columnnames = ['METHOD_CODE','METHOD_NAME','METHOD_DESC','STATUS_FLAG','REMARK','BASE_METHOD']
        self.pkey =['METHOD_CODE']
        self._operator = ['=','!=','>=','<=','=>','=<','>','<','IS','IS NOT']
        self._strwhere = ''
        self._param = {}
        self._paramidx = 1
    def printset(self,cur,header=True):
        '''Prints to standard out the cursor pass to function
           example: Optional variables denoted []
           rt_method.printset(rt_method.select(),[header=False])
        '''
        if header:
            temp=[]
            for row in cur.description:
                temp.append(row[0])
            print tuple(temp)
        for row in cur:
            print row
    def selectpkey(self,METHOD_CODE):
        '''Returns cursor of single record with associated Pkey.
           example:
           Cursor = rt_method.selectpkey(METHOD_CODE = <AppropriateKey>)
        '''
        c1= connection.cursor()
        sql = "SELECT METHOD_CODE, METHOD_NAME, METHOD_DESC, STATUS_FLAG, REMARK, BASE_METHOD FROM RT_METHOD"
        sql = sql + " WHERE METHOD_CODE = :METHOD_CODE"
        param ={'METHOD_CODE' : METHOD_CODE}
        c1.execute(sql, param)
        return c1
    def select(self,columnList = 'ALL'):
        '''Returns cursor with all rows. Optional columnList(Python List) - List of columns to return.
           Optional - Run rt_method.where('COLUMN_NAME','=',AppropriateValue) function to provide a where clause.
               rt_method.where('METHOD_CODE', '=',<AppropriateValue>)
           example:		   
               Cursor = rt_method.select(columnList)
        '''
        if columnList == 'ALL':
            columnList= self.columnnames
        colstr=''
        c1 = connection.cursor()
        first=True
        for col in columnList:
            if not first:
                colstr=colstr + ', '
            first=False
            colstr=colstr + col
        sql = 'SELECT ' + colstr + ' FROM RT_METHOD '
        if len(self._strwhere.strip())>0:
            sql = sql + 'WHERE ' + self._strwhere 
        c1.execute(sql,self._param)
        return c1
    #@transaction.commit_on_success()
    def update(self, METHOD_CODE, **uargs):
        '''Updates record varaiables. Does not allow update of primary keys.
            example: 
            rt_method.update(METHOD_CODE = <AppropriateKey>,[COLUMN_NAME = <UpdateValues>])
        '''
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
        '''Insert record varaiables.
            example: 
            rt_method.insert(METHOD_CODE = <AppropriateKey>,[COLUMN_NAME = <InsertValues>])
        '''
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
    def insertmany(self, ListDict ):
        '''Insert Many takes a list of Dictionaries which contain variables to insert. Must contain all columns for insertmany().
            example: 
            rt_method.insertmany(ListDict)
        '''
        c1 = connection.cursor()
        sql = "INSERT INTO RT_METHOD "
        col = "("
        vals = " VALUES ("
        first=True
        for colname in self.columnnames:
            if not first:
                col=col + ", "
                vals=vals + ", "
            first=False
            col = col + colname
            vals = vals + ':' + colname
        sql = sql + col + ")" + vals + ")"
        c1.executemany(sql,ListDict)
        connection.commit()
    #@transaction.commit_on_success()
    def delete(self,METHOD_CODE):
        '''Deletes record with associated Pkey.
           example:
           rt_method.delete(METHOD_CODE = <AppropriateKey>)
        '''
        c1 = connection.cursor()
        param={}
        param['METHOD_CODE'] = METHOD_CODE
        sql= 'DELETE FROM RT_METHOD'
        sql = sql + ' WHERE METHOD_CODE = :METHOD_CODE'
        c1.execute(sql, param)
        connection.commit()
    def where(self,columnname,operator,value,conjunction='AND'):
        ''' Sets the WHERE clause for the select function. Default Conjunction is 'AND'
            example:
                RT_METHOD.where('COlUMNNAME','=',AppropriateValue)
                RT_METHOD.where('COlUMNNAME','=',AppropriateValue,'OR')
        '''
        if columnname in self.columnnames:
            if operator in self._operator:
                if len(self._strwhere)>0:
                    if operator.upper()=='IS' or operator.upper()=='IS NOT':
                        self._strwhere= self._strwhere + ' ' + conjunction + ' ' + columnname + ' ' + operator + ' NULL'
                    else:
                        self._strwhere= self._strwhere + ' ' + conjunction + ' ' + columnname + ' ' + operator + ' :' + str(self._paramidx)
                        self._param[str(self._paramidx)]=value
                        self._paramidx +=1
                else:
                    if operator.upper()=='IS' or operator.upper()=='IS NOT':
                        self._strwhere= self._strwhere + columnname + ' ' + operator + ' NULL'
                    else:
                        self._strwhere= self._strwhere + columnname + ' ' + operator + ' :' + str(self._paramidx)
                        self._param[str(self._paramidx)]=value
                        self._paramidx +=1
            else:
                raise AttributeError, "'" + operator + "'" + " - Not a supported operator."
        else:
            raise AttributeError, "'" + columnname + "'" + " - Not a Valid Column Name."
    def whereclear(self):
        ''' Resets the WHERE clause'''
        self._strwhere = ''
        self._param = {}
        self._paramidx = 1
class rt_method_parameters():
    ''' Class for table RT_METHOD_PARAMETERS. Performs basic CRUD operation on table.'''
    def __init__(self):
        '''RT_METHOD_PARAMETERS.columnnames - returns list of Column Names
           RT_METHOD_PARAMETERS.pkey - returns list of tables primary key(s)
        '''
        self.columnnames = ['METHOD_CODE','PARAM_ID','PARAM_TYPE','PNAME','DESCRIPTION','PVALUE']
        self.pkey =['METHOD_CODE','PARAM_ID']
        self._operator = ['=','!=','>=','<=','=>','=<','>','<','IS','IS NOT']
        self._strwhere = ''
        self._param = {}
        self._paramidx = 1
    def printset(self,cur,header=True):
        '''Prints to standard out the cursor pass to function
           example: Optional variables denoted []
           rt_method_parameters.printset(rt_method_parameters.select(),[header=False])
        '''
        if header:
            temp=[]
            for row in cur.description:
                temp.append(row[0])
            print tuple(temp)
        for row in cur:
            print row
    def selectpkey(self,METHOD_CODE,PARAM_ID):
        '''Returns cursor of single record with associated Pkey.
           example:
           Cursor = rt_method_parameters.selectpkey(METHOD_CODE = <AppropriateKey>,PARAM_ID = <AppropriateKey>)
        '''
        c1= connection.cursor()
        sql = "SELECT METHOD_CODE, PARAM_ID, PARAM_TYPE, PNAME, DESCRIPTION, PVALUE FROM RT_METHOD_PARAMETERS"
        sql = sql + " WHERE METHOD_CODE = :METHOD_CODE AND PARAM_ID = :PARAM_ID"
        param ={'METHOD_CODE' : METHOD_CODE, 'PARAM_ID' : PARAM_ID}
        c1.execute(sql, param)
        return c1
    def select(self,columnList = 'ALL'):
        '''Returns cursor with all rows. Optional columnList(Python List) - List of columns to return.
           Optional - Run rt_method_parameters.where('COLUMN_NAME','=',AppropriateValue) function to provide a where clause.
               rt_method_parameters.where('METHOD_CODE', '=',<AppropriateValue>)
           example:		   
               Cursor = rt_method_parameters.select(columnList)
        '''
        if columnList == 'ALL':
            columnList= self.columnnames
        colstr=''
        c1 = connection.cursor()
        first=True
        for col in columnList:
            if not first:
                colstr=colstr + ', '
            first=False
            colstr=colstr + col
        sql = 'SELECT ' + colstr + ' FROM RT_METHOD_PARAMETERS '
        if len(self._strwhere.strip())>0:
            sql = sql + 'WHERE ' + self._strwhere 
        c1.execute(sql,self._param)
        return c1
    #@transaction.commit_on_success()
    def update(self, METHOD_CODE, PARAM_ID, **uargs):
        '''Updates record varaiables. Does not allow update of primary keys.
            example: 
            rt_method_parameters.update(METHOD_CODE = <AppropriateKey>,PARAM_ID = <AppropriateKey>,[COLUMN_NAME = <UpdateValues>])
        '''
        c1 = connection.cursor()
        param={}
        sql = "UPDATE RT_METHOD_PARAMETERS SET "
        where = " WHERE METHOD_CODE = :METHOD_CODE AND PARAM_ID = :PARAM_ID"
        param['METHOD_CODE'] = METHOD_CODE
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
    def insert(self, METHOD_CODE, PARAM_ID, **iargs):
        '''Insert record varaiables.
            example: 
            rt_method_parameters.insert(METHOD_CODE = <AppropriateKey>,PARAM_ID = <AppropriateKey>,[COLUMN_NAME = <InsertValues>])
        '''
        c1 = connection.cursor()
        sql = "INSERT INTO RT_METHOD_PARAMETERS "
        col = "(METHOD_CODE,PARAM_ID, "
        vals = " VALUES (:METHOD_CODE,:PARAM_ID, "
        first=True
        param={}
        param['METHOD_CODE'] = METHOD_CODE
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
    def insertmany(self, ListDict ):
        '''Insert Many takes a list of Dictionaries which contain variables to insert. Must contain all columns for insertmany().
            example: 
            rt_method_parameters.insertmany(ListDict)
        '''
        c1 = connection.cursor()
        sql = "INSERT INTO RT_METHOD_PARAMETERS "
        col = "("
        vals = " VALUES ("
        first=True
        for colname in self.columnnames:
            if not first:
                col=col + ", "
                vals=vals + ", "
            first=False
            col = col + colname
            vals = vals + ':' + colname
        sql = sql + col + ")" + vals + ")"
        c1.executemany(sql,ListDict)
        connection.commit()
    #@transaction.commit_on_success()
    def delete(self,METHOD_CODE, PARAM_ID):
        '''Deletes record with associated Pkey.
           example:
           rt_method_parameters.delete(METHOD_CODE = <AppropriateKey>, PARAM_ID = <AppropriateKey>)
        '''
        c1 = connection.cursor()
        param={}
        param['METHOD_CODE'] = METHOD_CODE
        param['PARAM_ID'] = PARAM_ID
        sql= 'DELETE FROM RT_METHOD_PARAMETERS'
        sql = sql + ' WHERE METHOD_CODE = :METHOD_CODE AND PARAM_ID = :PARAM_ID'
        c1.execute(sql, param)
        connection.commit()
    def where(self,columnname,operator,value,conjunction='AND'):
        ''' Sets the WHERE clause for the select function. Default Conjunction is 'AND'
            example:
                RT_METHOD_PARAMETERS.where('COlUMNNAME','=',AppropriateValue)
                RT_METHOD_PARAMETERS.where('COlUMNNAME','=',AppropriateValue,'OR')
        '''
        if columnname in self.columnnames:
            if operator in self._operator:
                if len(self._strwhere)>0:
                    if operator.upper()=='IS' or operator.upper()=='IS NOT':
                        self._strwhere= self._strwhere + ' ' + conjunction + ' ' + columnname + ' ' + operator + ' NULL'
                    else:
                        self._strwhere= self._strwhere + ' ' + conjunction + ' ' + columnname + ' ' + operator + ' :' + str(self._paramidx)
                        self._param[str(self._paramidx)]=value
                        self._paramidx +=1
                else:
                    if operator.upper()=='IS' or operator.upper()=='IS NOT':
                        self._strwhere= self._strwhere + columnname + ' ' + operator + ' NULL'
                    else:
                        self._strwhere= self._strwhere + columnname + ' ' + operator + ' :' + str(self._paramidx)
                        self._param[str(self._paramidx)]=value
                        self._paramidx +=1
            else:
                raise AttributeError, "'" + operator + "'" + " - Not a supported operator."
        else:
            raise AttributeError, "'" + columnname + "'" + " - Not a Valid Column Name."
    def whereclear(self):
        ''' Resets the WHERE clause'''
        self._strwhere = ''
        self._param = {}
        self._paramidx = 1
class rt_organization():
    ''' Class for table RT_ORGANIZATION. Performs basic CRUD operation on table.'''
    def __init__(self):
        '''RT_ORGANIZATION.columnnames - returns list of Column Names
           RT_ORGANIZATION.pkey - returns list of tables primary key(s)
        '''
        self.columnnames = ['ORG_CODE','ORG_TYPE','ORG_NAME','CONTACT_NAME','ADDRESS_1','ADDRESS_2','CITY','COUNTY','STATE','COUNTRY','POSTAL_CODE','PHONE_NUMBER','ALT_PHONE_NUMBER','EMAIL_ADDRESS','CUSTOM_FIELD_1','CUSTOM_FIELD_2','CUSTOM_FIELD_3','CUSTOM_FIELD_4','CUSTOM_FIELD_5','STATUS_FLAG','REMARK']
        self.pkey =['ORG_CODE']
        self._operator = ['=','!=','>=','<=','=>','=<','>','<','IS','IS NOT']
        self._strwhere = ''
        self._param = {}
        self._paramidx = 1
    def printset(self,cur,header=True):
        '''Prints to standard out the cursor pass to function
           example: Optional variables denoted []
           rt_organization.printset(rt_organization.select(),[header=False])
        '''
        if header:
            temp=[]
            for row in cur.description:
                temp.append(row[0])
            print tuple(temp)
        for row in cur:
            print row
    def selectpkey(self,ORG_CODE):
        '''Returns cursor of single record with associated Pkey.
           example:
           Cursor = rt_organization.selectpkey(ORG_CODE = <AppropriateKey>)
        '''
        c1= connection.cursor()
        sql = "SELECT ORG_CODE, ORG_TYPE, ORG_NAME, CONTACT_NAME, ADDRESS_1, ADDRESS_2, CITY, COUNTY, STATE, COUNTRY, POSTAL_CODE, PHONE_NUMBER, ALT_PHONE_NUMBER, EMAIL_ADDRESS, CUSTOM_FIELD_1, CUSTOM_FIELD_2, CUSTOM_FIELD_3, CUSTOM_FIELD_4, CUSTOM_FIELD_5, STATUS_FLAG, REMARK FROM RT_ORGANIZATION"
        sql = sql + " WHERE ORG_CODE = :ORG_CODE"
        param ={'ORG_CODE' : ORG_CODE}
        c1.execute(sql, param)
        return c1
    def select(self,columnList = 'ALL'):
        '''Returns cursor with all rows. Optional columnList(Python List) - List of columns to return.
           Optional - Run rt_organization.where('COLUMN_NAME','=',AppropriateValue) function to provide a where clause.
               rt_organization.where('ORG_CODE', '=',<AppropriateValue>)
           example:		   
               Cursor = rt_organization.select(columnList)
        '''
        if columnList == 'ALL':
            columnList= self.columnnames
        colstr=''
        c1 = connection.cursor()
        first=True
        for col in columnList:
            if not first:
                colstr=colstr + ', '
            first=False
            colstr=colstr + col
        sql = 'SELECT ' + colstr + ' FROM RT_ORGANIZATION '
        if len(self._strwhere.strip())>0:
            sql = sql + 'WHERE ' + self._strwhere 
        c1.execute(sql,self._param)
        return c1
    #@transaction.commit_on_success()
    def update(self, ORG_CODE, **uargs):
        '''Updates record varaiables. Does not allow update of primary keys.
            example: 
            rt_organization.update(ORG_CODE = <AppropriateKey>,[COLUMN_NAME = <UpdateValues>])
        '''
        c1 = connection.cursor()
        param={}
        sql = "UPDATE RT_ORGANIZATION SET "
        where = " WHERE ORG_CODE = :ORG_CODE"
        param['ORG_CODE'] = ORG_CODE
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
    def insert(self, ORG_CODE, **iargs):
        '''Insert record varaiables.
            example: 
            rt_organization.insert(ORG_CODE = <AppropriateKey>,[COLUMN_NAME = <InsertValues>])
        '''
        c1 = connection.cursor()
        sql = "INSERT INTO RT_ORGANIZATION "
        col = "(ORG_CODE, "
        vals = " VALUES (:ORG_CODE, "
        first=True
        param={}
        param['ORG_CODE'] = ORG_CODE
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
    def insertmany(self, ListDict ):
        '''Insert Many takes a list of Dictionaries which contain variables to insert. Must contain all columns for insertmany().
            example: 
            rt_organization.insertmany(ListDict)
        '''
        c1 = connection.cursor()
        sql = "INSERT INTO RT_ORGANIZATION "
        col = "("
        vals = " VALUES ("
        first=True
        for colname in self.columnnames:
            if not first:
                col=col + ", "
                vals=vals + ", "
            first=False
            col = col + colname
            vals = vals + ':' + colname
        sql = sql + col + ")" + vals + ")"
        c1.executemany(sql,ListDict)
        connection.commit()
    #@transaction.commit_on_success()
    def delete(self,ORG_CODE):
        '''Deletes record with associated Pkey.
           example:
           rt_organization.delete(ORG_CODE = <AppropriateKey>)
        '''
        c1 = connection.cursor()
        param={}
        param['ORG_CODE'] = ORG_CODE
        sql= 'DELETE FROM RT_ORGANIZATION'
        sql = sql + ' WHERE ORG_CODE = :ORG_CODE'
        c1.execute(sql, param)
        connection.commit()
    def where(self,columnname,operator,value,conjunction='AND'):
        ''' Sets the WHERE clause for the select function. Default Conjunction is 'AND'
            example:
                RT_ORGANIZATION.where('COlUMNNAME','=',AppropriateValue)
                RT_ORGANIZATION.where('COlUMNNAME','=',AppropriateValue,'OR')
        '''
        if columnname in self.columnnames:
            if operator in self._operator:
                if len(self._strwhere)>0:
                    if operator.upper()=='IS' or operator.upper()=='IS NOT':
                        self._strwhere= self._strwhere + ' ' + conjunction + ' ' + columnname + ' ' + operator + ' NULL'
                    else:
                        self._strwhere= self._strwhere + ' ' + conjunction + ' ' + columnname + ' ' + operator + ' :' + str(self._paramidx)
                        self._param[str(self._paramidx)]=value
                        self._paramidx +=1
                else:
                    if operator.upper()=='IS' or operator.upper()=='IS NOT':
                        self._strwhere= self._strwhere + columnname + ' ' + operator + ' NULL'
                    else:
                        self._strwhere= self._strwhere + columnname + ' ' + operator + ' :' + str(self._paramidx)
                        self._param[str(self._paramidx)]=value
                        self._paramidx +=1
            else:
                raise AttributeError, "'" + operator + "'" + " - Not a supported operator."
        else:
            raise AttributeError, "'" + columnname + "'" + " - Not a Valid Column Name."
    def whereclear(self):
        ''' Resets the WHERE clause'''
        self._strwhere = ''
        self._param = {}
        self._paramidx = 1
class rt_organization_type():
    ''' Class for table RT_ORGANIZATION_TYPE. Performs basic CRUD operation on table.'''
    def __init__(self):
        '''RT_ORGANIZATION_TYPE.columnnames - returns list of Column Names
           RT_ORGANIZATION_TYPE.pkey - returns list of tables primary key(s)
        '''
        self.columnnames = ['ORG_TYPE','ORG_TYPE_DESC','STATUS_FLAG','REMARK']
        self.pkey =['ORG_TYPE']
        self._operator = ['=','!=','>=','<=','=>','=<','>','<','IS','IS NOT']
        self._strwhere = ''
        self._param = {}
        self._paramidx = 1
    def printset(self,cur,header=True):
        '''Prints to standard out the cursor pass to function
           example: Optional variables denoted []
           rt_organization_type.printset(rt_organization_type.select(),[header=False])
        '''
        if header:
            temp=[]
            for row in cur.description:
                temp.append(row[0])
            print tuple(temp)
        for row in cur:
            print row
    def selectpkey(self,ORG_TYPE):
        '''Returns cursor of single record with associated Pkey.
           example:
           Cursor = rt_organization_type.selectpkey(ORG_TYPE = <AppropriateKey>)
        '''
        c1= connection.cursor()
        sql = "SELECT ORG_TYPE, ORG_TYPE_DESC, STATUS_FLAG, REMARK FROM RT_ORGANIZATION_TYPE"
        sql = sql + " WHERE ORG_TYPE = :ORG_TYPE"
        param ={'ORG_TYPE' : ORG_TYPE}
        c1.execute(sql, param)
        return c1
    def select(self,columnList = 'ALL'):
        '''Returns cursor with all rows. Optional columnList(Python List) - List of columns to return.
           Optional - Run rt_organization_type.where('COLUMN_NAME','=',AppropriateValue) function to provide a where clause.
               rt_organization_type.where('ORG_TYPE', '=',<AppropriateValue>)
           example:		   
               Cursor = rt_organization_type.select(columnList)
        '''
        if columnList == 'ALL':
            columnList= self.columnnames
        colstr=''
        c1 = connection.cursor()
        first=True
        for col in columnList:
            if not first:
                colstr=colstr + ', '
            first=False
            colstr=colstr + col
        sql = 'SELECT ' + colstr + ' FROM RT_ORGANIZATION_TYPE '
        if len(self._strwhere.strip())>0:
            sql = sql + 'WHERE ' + self._strwhere 
        c1.execute(sql,self._param)
        return c1
    #@transaction.commit_on_success()
    def update(self, ORG_TYPE, **uargs):
        '''Updates record varaiables. Does not allow update of primary keys.
            example: 
            rt_organization_type.update(ORG_TYPE = <AppropriateKey>,[COLUMN_NAME = <UpdateValues>])
        '''
        c1 = connection.cursor()
        param={}
        sql = "UPDATE RT_ORGANIZATION_TYPE SET "
        where = " WHERE ORG_TYPE = :ORG_TYPE"
        param['ORG_TYPE'] = ORG_TYPE
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
    def insert(self, ORG_TYPE, **iargs):
        '''Insert record varaiables.
            example: 
            rt_organization_type.insert(ORG_TYPE = <AppropriateKey>,[COLUMN_NAME = <InsertValues>])
        '''
        c1 = connection.cursor()
        sql = "INSERT INTO RT_ORGANIZATION_TYPE "
        col = "(ORG_TYPE, "
        vals = " VALUES (:ORG_TYPE, "
        first=True
        param={}
        param['ORG_TYPE'] = ORG_TYPE
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
    def insertmany(self, ListDict ):
        '''Insert Many takes a list of Dictionaries which contain variables to insert. Must contain all columns for insertmany().
            example: 
            rt_organization_type.insertmany(ListDict)
        '''
        c1 = connection.cursor()
        sql = "INSERT INTO RT_ORGANIZATION_TYPE "
        col = "("
        vals = " VALUES ("
        first=True
        for colname in self.columnnames:
            if not first:
                col=col + ", "
                vals=vals + ", "
            first=False
            col = col + colname
            vals = vals + ':' + colname
        sql = sql + col + ")" + vals + ")"
        c1.executemany(sql,ListDict)
        connection.commit()
    #@transaction.commit_on_success()
    def delete(self,ORG_TYPE):
        '''Deletes record with associated Pkey.
           example:
           rt_organization_type.delete(ORG_TYPE = <AppropriateKey>)
        '''
        c1 = connection.cursor()
        param={}
        param['ORG_TYPE'] = ORG_TYPE
        sql= 'DELETE FROM RT_ORGANIZATION_TYPE'
        sql = sql + ' WHERE ORG_TYPE = :ORG_TYPE'
        c1.execute(sql, param)
        connection.commit()
    def where(self,columnname,operator,value,conjunction='AND'):
        ''' Sets the WHERE clause for the select function. Default Conjunction is 'AND'
            example:
                RT_ORGANIZATION_TYPE.where('COlUMNNAME','=',AppropriateValue)
                RT_ORGANIZATION_TYPE.where('COlUMNNAME','=',AppropriateValue,'OR')
        '''
        if columnname in self.columnnames:
            if operator in self._operator:
                if len(self._strwhere)>0:
                    if operator.upper()=='IS' or operator.upper()=='IS NOT':
                        self._strwhere= self._strwhere + ' ' + conjunction + ' ' + columnname + ' ' + operator + ' NULL'
                    else:
                        self._strwhere= self._strwhere + ' ' + conjunction + ' ' + columnname + ' ' + operator + ' :' + str(self._paramidx)
                        self._param[str(self._paramidx)]=value
                        self._paramidx +=1
                else:
                    if operator.upper()=='IS' or operator.upper()=='IS NOT':
                        self._strwhere= self._strwhere + columnname + ' ' + operator + ' NULL'
                    else:
                        self._strwhere= self._strwhere + columnname + ' ' + operator + ' :' + str(self._paramidx)
                        self._param[str(self._paramidx)]=value
                        self._paramidx +=1
            else:
                raise AttributeError, "'" + operator + "'" + " - Not a supported operator."
        else:
            raise AttributeError, "'" + columnname + "'" + " - Not a Valid Column Name."
    def whereclear(self):
        ''' Resets the WHERE clause'''
        self._strwhere = ''
        self._param = {}
        self._paramidx = 1
class rt_result_type():
    ''' Class for table RT_RESULT_TYPE. Performs basic CRUD operation on table.'''
    def __init__(self):
        '''RT_RESULT_TYPE.columnnames - returns list of Column Names
           RT_RESULT_TYPE.pkey - returns list of tables primary key(s)
        '''
        self.columnnames = ['RESULT_TYPE_CODE','RESULT_TYPE_DESC','STATUS_FLAG','REMARK']
        self.pkey =['RESULT_TYPE_CODE']
        self._operator = ['=','!=','>=','<=','=>','=<','>','<','IS','IS NOT']
        self._strwhere = ''
        self._param = {}
        self._paramidx = 1
    def printset(self,cur,header=True):
        '''Prints to standard out the cursor pass to function
           example: Optional variables denoted []
           rt_result_type.printset(rt_result_type.select(),[header=False])
        '''
        if header:
            temp=[]
            for row in cur.description:
                temp.append(row[0])
            print tuple(temp)
        for row in cur:
            print row
    def selectpkey(self,RESULT_TYPE_CODE):
        '''Returns cursor of single record with associated Pkey.
           example:
           Cursor = rt_result_type.selectpkey(RESULT_TYPE_CODE = <AppropriateKey>)
        '''
        c1= connection.cursor()
        sql = "SELECT RESULT_TYPE_CODE, RESULT_TYPE_DESC, STATUS_FLAG, REMARK FROM RT_RESULT_TYPE"
        sql = sql + " WHERE RESULT_TYPE_CODE = :RESULT_TYPE_CODE"
        param ={'RESULT_TYPE_CODE' : RESULT_TYPE_CODE}
        c1.execute(sql, param)
        return c1
    def select(self,columnList = 'ALL'):
        '''Returns cursor with all rows. Optional columnList(Python List) - List of columns to return.
           Optional - Run rt_result_type.where('COLUMN_NAME','=',AppropriateValue) function to provide a where clause.
               rt_result_type.where('RESULT_TYPE_CODE', '=',<AppropriateValue>)
           example:		   
               Cursor = rt_result_type.select(columnList)
        '''
        if columnList == 'ALL':
            columnList= self.columnnames
        colstr=''
        c1 = connection.cursor()
        first=True
        for col in columnList:
            if not first:
                colstr=colstr + ', '
            first=False
            colstr=colstr + col
        sql = 'SELECT ' + colstr + ' FROM RT_RESULT_TYPE '
        if len(self._strwhere.strip())>0:
            sql = sql + 'WHERE ' + self._strwhere 
        c1.execute(sql,self._param)
        return c1
    #@transaction.commit_on_success()
    def update(self, RESULT_TYPE_CODE, **uargs):
        '''Updates record varaiables. Does not allow update of primary keys.
            example: 
            rt_result_type.update(RESULT_TYPE_CODE = <AppropriateKey>,[COLUMN_NAME = <UpdateValues>])
        '''
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
        '''Insert record varaiables.
            example: 
            rt_result_type.insert(RESULT_TYPE_CODE = <AppropriateKey>,[COLUMN_NAME = <InsertValues>])
        '''
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
    def insertmany(self, ListDict ):
        '''Insert Many takes a list of Dictionaries which contain variables to insert. Must contain all columns for insertmany().
            example: 
            rt_result_type.insertmany(ListDict)
        '''
        c1 = connection.cursor()
        sql = "INSERT INTO RT_RESULT_TYPE "
        col = "("
        vals = " VALUES ("
        first=True
        for colname in self.columnnames:
            if not first:
                col=col + ", "
                vals=vals + ", "
            first=False
            col = col + colname
            vals = vals + ':' + colname
        sql = sql + col + ")" + vals + ")"
        c1.executemany(sql,ListDict)
        connection.commit()
    #@transaction.commit_on_success()
    def delete(self,RESULT_TYPE_CODE):
        '''Deletes record with associated Pkey.
           example:
           rt_result_type.delete(RESULT_TYPE_CODE = <AppropriateKey>)
        '''
        c1 = connection.cursor()
        param={}
        param['RESULT_TYPE_CODE'] = RESULT_TYPE_CODE
        sql= 'DELETE FROM RT_RESULT_TYPE'
        sql = sql + ' WHERE RESULT_TYPE_CODE = :RESULT_TYPE_CODE'
        c1.execute(sql, param)
        connection.commit()
    def where(self,columnname,operator,value,conjunction='AND'):
        ''' Sets the WHERE clause for the select function. Default Conjunction is 'AND'
            example:
                RT_RESULT_TYPE.where('COlUMNNAME','=',AppropriateValue)
                RT_RESULT_TYPE.where('COlUMNNAME','=',AppropriateValue,'OR')
        '''
        if columnname in self.columnnames:
            if operator in self._operator:
                if len(self._strwhere)>0:
                    if operator.upper()=='IS' or operator.upper()=='IS NOT':
                        self._strwhere= self._strwhere + ' ' + conjunction + ' ' + columnname + ' ' + operator + ' NULL'
                    else:
                        self._strwhere= self._strwhere + ' ' + conjunction + ' ' + columnname + ' ' + operator + ' :' + str(self._paramidx)
                        self._param[str(self._paramidx)]=value
                        self._paramidx +=1
                else:
                    if operator.upper()=='IS' or operator.upper()=='IS NOT':
                        self._strwhere= self._strwhere + columnname + ' ' + operator + ' NULL'
                    else:
                        self._strwhere= self._strwhere + columnname + ' ' + operator + ' :' + str(self._paramidx)
                        self._param[str(self._paramidx)]=value
                        self._paramidx +=1
            else:
                raise AttributeError, "'" + operator + "'" + " - Not a supported operator."
        else:
            raise AttributeError, "'" + columnname + "'" + " - Not a Valid Column Name."
    def whereclear(self):
        ''' Resets the WHERE clause'''
        self._strwhere = ''
        self._param = {}
        self._paramidx = 1
class rt_sources():
    ''' Class for table RT_SOURCES. Performs basic CRUD operation on table.'''
    def __init__(self):
        '''RT_SOURCES.columnnames - returns list of Column Names
           RT_SOURCES.pkey - returns list of tables primary key(s)
        '''
        self.columnnames = ['SOURCE_ID','SOURCE_NAME','URL','DESCRIPTION','CONTACT','EMAIL','ORGANIZATION']
        self.pkey =['SOURCE_ID']
        self._operator = ['=','!=','>=','<=','=>','=<','>','<','IS','IS NOT']
        self._strwhere = ''
        self._param = {}
        self._paramidx = 1
    def printset(self,cur,header=True):
        '''Prints to standard out the cursor pass to function
           example: Optional variables denoted []
           rt_sources.printset(rt_sources.select(),[header=False])
        '''
        if header:
            temp=[]
            for row in cur.description:
                temp.append(row[0])
            print tuple(temp)
        for row in cur:
            print row
    def selectpkey(self,SOURCE_ID):
        '''Returns cursor of single record with associated Pkey.
           example:
           Cursor = rt_sources.selectpkey(SOURCE_ID = <AppropriateKey>)
        '''
        c1= connection.cursor()
        sql = "SELECT SOURCE_ID, SOURCE_NAME, URL, DESCRIPTION, CONTACT, EMAIL, ORGANIZATION FROM RT_SOURCES"
        sql = sql + " WHERE SOURCE_ID = :SOURCE_ID"
        param ={'SOURCE_ID' : SOURCE_ID}
        c1.execute(sql, param)
        return c1
    def select(self,columnList = 'ALL'):
        '''Returns cursor with all rows. Optional columnList(Python List) - List of columns to return.
           Optional - Run rt_sources.where('COLUMN_NAME','=',AppropriateValue) function to provide a where clause.
               rt_sources.where('SOURCE_ID', '=',<AppropriateValue>)
           example:		   
               Cursor = rt_sources.select(columnList)
        '''
        if columnList == 'ALL':
            columnList= self.columnnames
        colstr=''
        c1 = connection.cursor()
        first=True
        for col in columnList:
            if not first:
                colstr=colstr + ', '
            first=False
            colstr=colstr + col
        sql = 'SELECT ' + colstr + ' FROM RT_SOURCES '
        if len(self._strwhere.strip())>0:
            sql = sql + 'WHERE ' + self._strwhere 
        c1.execute(sql,self._param)
        return c1
    #@transaction.commit_on_success()
    def update(self, SOURCE_ID, **uargs):
        '''Updates record varaiables. Does not allow update of primary keys.
            example: 
            rt_sources.update(SOURCE_ID = <AppropriateKey>,[COLUMN_NAME = <UpdateValues>])
        '''
        c1 = connection.cursor()
        param={}
        sql = "UPDATE RT_SOURCES SET "
        where = " WHERE SOURCE_ID = :SOURCE_ID"
        param['SOURCE_ID'] = SOURCE_ID
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
    def insert(self, SOURCE_ID, **iargs):
        '''Insert record varaiables.
            example: 
            rt_sources.insert(SOURCE_ID = <AppropriateKey>,[COLUMN_NAME = <InsertValues>])
        '''
        c1 = connection.cursor()
        sql = "INSERT INTO RT_SOURCES "
        col = "(SOURCE_ID, "
        vals = " VALUES (:SOURCE_ID, "
        first=True
        param={}
        param['SOURCE_ID'] = SOURCE_ID
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
    def insertmany(self, ListDict ):
        '''Insert Many takes a list of Dictionaries which contain variables to insert. Must contain all columns for insertmany().
            example: 
            rt_sources.insertmany(ListDict)
        '''
        c1 = connection.cursor()
        sql = "INSERT INTO RT_SOURCES "
        col = "("
        vals = " VALUES ("
        first=True
        for colname in self.columnnames:
            if not first:
                col=col + ", "
                vals=vals + ", "
            first=False
            col = col + colname
            vals = vals + ':' + colname
        sql = sql + col + ")" + vals + ")"
        c1.executemany(sql,ListDict)
        connection.commit()
    #@transaction.commit_on_success()
    def delete(self,SOURCE_ID):
        '''Deletes record with associated Pkey.
           example:
           rt_sources.delete(SOURCE_ID = <AppropriateKey>)
        '''
        c1 = connection.cursor()
        param={}
        param['SOURCE_ID'] = SOURCE_ID
        sql= 'DELETE FROM RT_SOURCES'
        sql = sql + ' WHERE SOURCE_ID = :SOURCE_ID'
        c1.execute(sql, param)
        connection.commit()
    def where(self,columnname,operator,value,conjunction='AND'):
        ''' Sets the WHERE clause for the select function. Default Conjunction is 'AND'
            example:
                RT_SOURCES.where('COlUMNNAME','=',AppropriateValue)
                RT_SOURCES.where('COlUMNNAME','=',AppropriateValue,'OR')
        '''
        if columnname in self.columnnames:
            if operator in self._operator:
                if len(self._strwhere)>0:
                    if operator.upper()=='IS' or operator.upper()=='IS NOT':
                        self._strwhere= self._strwhere + ' ' + conjunction + ' ' + columnname + ' ' + operator + ' NULL'
                    else:
                        self._strwhere= self._strwhere + ' ' + conjunction + ' ' + columnname + ' ' + operator + ' :' + str(self._paramidx)
                        self._param[str(self._paramidx)]=value
                        self._paramidx +=1
                else:
                    if operator.upper()=='IS' or operator.upper()=='IS NOT':
                        self._strwhere= self._strwhere + columnname + ' ' + operator + ' NULL'
                    else:
                        self._strwhere= self._strwhere + columnname + ' ' + operator + ' :' + str(self._paramidx)
                        self._param[str(self._paramidx)]=value
                        self._paramidx +=1
            else:
                raise AttributeError, "'" + operator + "'" + " - Not a supported operator."
        else:
            raise AttributeError, "'" + columnname + "'" + " - Not a Valid Column Name."
    def whereclear(self):
        ''' Resets the WHERE clause'''
        self._strwhere = ''
        self._param = {}
        self._paramidx = 1
class rt_state():
    ''' Class for table RT_STATE. Performs basic CRUD operation on table.'''
    def __init__(self):
        '''RT_STATE.columnnames - returns list of Column Names
           RT_STATE.pkey - returns list of tables primary key(s)
        '''
        self.columnnames = ['STATE_CODE','STATE_NAME','STATUS_FLAG','EBATCH','REMARK']
        self.pkey =['STATE_CODE']
        self._operator = ['=','!=','>=','<=','=>','=<','>','<','IS','IS NOT']
        self._strwhere = ''
        self._param = {}
        self._paramidx = 1
    def printset(self,cur,header=True):
        '''Prints to standard out the cursor pass to function
           example: Optional variables denoted []
           rt_state.printset(rt_state.select(),[header=False])
        '''
        if header:
            temp=[]
            for row in cur.description:
                temp.append(row[0])
            print tuple(temp)
        for row in cur:
            print row
    def selectpkey(self,STATE_CODE):
        '''Returns cursor of single record with associated Pkey.
           example:
           Cursor = rt_state.selectpkey(STATE_CODE = <AppropriateKey>)
        '''
        c1= connection.cursor()
        sql = "SELECT STATE_CODE, STATE_NAME, STATUS_FLAG, EBATCH, REMARK FROM RT_STATE"
        sql = sql + " WHERE STATE_CODE = :STATE_CODE"
        param ={'STATE_CODE' : STATE_CODE}
        c1.execute(sql, param)
        return c1
    def select(self,columnList = 'ALL'):
        '''Returns cursor with all rows. Optional columnList(Python List) - List of columns to return.
           Optional - Run rt_state.where('COLUMN_NAME','=',AppropriateValue) function to provide a where clause.
               rt_state.where('STATE_CODE', '=',<AppropriateValue>)
           example:		   
               Cursor = rt_state.select(columnList)
        '''
        if columnList == 'ALL':
            columnList= self.columnnames
        colstr=''
        c1 = connection.cursor()
        first=True
        for col in columnList:
            if not first:
                colstr=colstr + ', '
            first=False
            colstr=colstr + col
        sql = 'SELECT ' + colstr + ' FROM RT_STATE '
        if len(self._strwhere.strip())>0:
            sql = sql + 'WHERE ' + self._strwhere 
        c1.execute(sql,self._param)
        return c1
    #@transaction.commit_on_success()
    def update(self, STATE_CODE, **uargs):
        '''Updates record varaiables. Does not allow update of primary keys.
            example: 
            rt_state.update(STATE_CODE = <AppropriateKey>,[COLUMN_NAME = <UpdateValues>])
        '''
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
        '''Insert record varaiables.
            example: 
            rt_state.insert(STATE_CODE = <AppropriateKey>,[COLUMN_NAME = <InsertValues>])
        '''
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
    def insertmany(self, ListDict ):
        '''Insert Many takes a list of Dictionaries which contain variables to insert. Must contain all columns for insertmany().
            example: 
            rt_state.insertmany(ListDict)
        '''
        c1 = connection.cursor()
        sql = "INSERT INTO RT_STATE "
        col = "("
        vals = " VALUES ("
        first=True
        for colname in self.columnnames:
            if not first:
                col=col + ", "
                vals=vals + ", "
            first=False
            col = col + colname
            vals = vals + ':' + colname
        sql = sql + col + ")" + vals + ")"
        c1.executemany(sql,ListDict)
        connection.commit()
    #@transaction.commit_on_success()
    def delete(self,STATE_CODE):
        '''Deletes record with associated Pkey.
           example:
           rt_state.delete(STATE_CODE = <AppropriateKey>)
        '''
        c1 = connection.cursor()
        param={}
        param['STATE_CODE'] = STATE_CODE
        sql= 'DELETE FROM RT_STATE'
        sql = sql + ' WHERE STATE_CODE = :STATE_CODE'
        c1.execute(sql, param)
        connection.commit()
    def where(self,columnname,operator,value,conjunction='AND'):
        ''' Sets the WHERE clause for the select function. Default Conjunction is 'AND'
            example:
                RT_STATE.where('COlUMNNAME','=',AppropriateValue)
                RT_STATE.where('COlUMNNAME','=',AppropriateValue,'OR')
        '''
        if columnname in self.columnnames:
            if operator in self._operator:
                if len(self._strwhere)>0:
                    if operator.upper()=='IS' or operator.upper()=='IS NOT':
                        self._strwhere= self._strwhere + ' ' + conjunction + ' ' + columnname + ' ' + operator + ' NULL'
                    else:
                        self._strwhere= self._strwhere + ' ' + conjunction + ' ' + columnname + ' ' + operator + ' :' + str(self._paramidx)
                        self._param[str(self._paramidx)]=value
                        self._paramidx +=1
                else:
                    if operator.upper()=='IS' or operator.upper()=='IS NOT':
                        self._strwhere= self._strwhere + columnname + ' ' + operator + ' NULL'
                    else:
                        self._strwhere= self._strwhere + columnname + ' ' + operator + ' :' + str(self._paramidx)
                        self._param[str(self._paramidx)]=value
                        self._paramidx +=1
            else:
                raise AttributeError, "'" + operator + "'" + " - Not a supported operator."
        else:
            raise AttributeError, "'" + columnname + "'" + " - Not a Valid Column Name."
    def whereclear(self):
        ''' Resets the WHERE clause'''
        self._strwhere = ''
        self._param = {}
        self._paramidx = 1
class rt_unit():
    ''' Class for table RT_UNIT. Performs basic CRUD operation on table.'''
    def __init__(self):
        '''RT_UNIT.columnnames - returns list of Column Names
           RT_UNIT.pkey - returns list of tables primary key(s)
        '''
        self.columnnames = ['UNIT_CODE','UNIT_DESC','UNIT_TYPE','STATUS_FLAG','REMARK']
        self.pkey =['UNIT_CODE']
        self._operator = ['=','!=','>=','<=','=>','=<','>','<','IS','IS NOT']
        self._strwhere = ''
        self._param = {}
        self._paramidx = 1
    def printset(self,cur,header=True):
        '''Prints to standard out the cursor pass to function
           example: Optional variables denoted []
           rt_unit.printset(rt_unit.select(),[header=False])
        '''
        if header:
            temp=[]
            for row in cur.description:
                temp.append(row[0])
            print tuple(temp)
        for row in cur:
            print row
    def selectpkey(self,UNIT_CODE):
        '''Returns cursor of single record with associated Pkey.
           example:
           Cursor = rt_unit.selectpkey(UNIT_CODE = <AppropriateKey>)
        '''
        c1= connection.cursor()
        sql = "SELECT UNIT_CODE, UNIT_DESC, UNIT_TYPE, STATUS_FLAG, REMARK FROM RT_UNIT"
        sql = sql + " WHERE UNIT_CODE = :UNIT_CODE"
        param ={'UNIT_CODE' : UNIT_CODE}
        c1.execute(sql, param)
        return c1
    def select(self,columnList = 'ALL'):
        '''Returns cursor with all rows. Optional columnList(Python List) - List of columns to return.
           Optional - Run rt_unit.where('COLUMN_NAME','=',AppropriateValue) function to provide a where clause.
               rt_unit.where('UNIT_CODE', '=',<AppropriateValue>)
           example:		   
               Cursor = rt_unit.select(columnList)
        '''
        if columnList == 'ALL':
            columnList= self.columnnames
        colstr=''
        c1 = connection.cursor()
        first=True
        for col in columnList:
            if not first:
                colstr=colstr + ', '
            first=False
            colstr=colstr + col
        sql = 'SELECT ' + colstr + ' FROM RT_UNIT '
        if len(self._strwhere.strip())>0:
            sql = sql + 'WHERE ' + self._strwhere 
        c1.execute(sql,self._param)
        return c1
    #@transaction.commit_on_success()
    def update(self, UNIT_CODE, **uargs):
        '''Updates record varaiables. Does not allow update of primary keys.
            example: 
            rt_unit.update(UNIT_CODE = <AppropriateKey>,[COLUMN_NAME = <UpdateValues>])
        '''
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
        '''Insert record varaiables.
            example: 
            rt_unit.insert(UNIT_CODE = <AppropriateKey>,[COLUMN_NAME = <InsertValues>])
        '''
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
    def insertmany(self, ListDict ):
        '''Insert Many takes a list of Dictionaries which contain variables to insert. Must contain all columns for insertmany().
            example: 
            rt_unit.insertmany(ListDict)
        '''
        c1 = connection.cursor()
        sql = "INSERT INTO RT_UNIT "
        col = "("
        vals = " VALUES ("
        first=True
        for colname in self.columnnames:
            if not first:
                col=col + ", "
                vals=vals + ", "
            first=False
            col = col + colname
            vals = vals + ':' + colname
        sql = sql + col + ")" + vals + ")"
        c1.executemany(sql,ListDict)
        connection.commit()
    #@transaction.commit_on_success()
    def delete(self,UNIT_CODE):
        '''Deletes record with associated Pkey.
           example:
           rt_unit.delete(UNIT_CODE = <AppropriateKey>)
        '''
        c1 = connection.cursor()
        param={}
        param['UNIT_CODE'] = UNIT_CODE
        sql= 'DELETE FROM RT_UNIT'
        sql = sql + ' WHERE UNIT_CODE = :UNIT_CODE'
        c1.execute(sql, param)
        connection.commit()
    def where(self,columnname,operator,value,conjunction='AND'):
        ''' Sets the WHERE clause for the select function. Default Conjunction is 'AND'
            example:
                RT_UNIT.where('COlUMNNAME','=',AppropriateValue)
                RT_UNIT.where('COlUMNNAME','=',AppropriateValue,'OR')
        '''
        if columnname in self.columnnames:
            if operator in self._operator:
                if len(self._strwhere)>0:
                    if operator.upper()=='IS' or operator.upper()=='IS NOT':
                        self._strwhere= self._strwhere + ' ' + conjunction + ' ' + columnname + ' ' + operator + ' NULL'
                    else:
                        self._strwhere= self._strwhere + ' ' + conjunction + ' ' + columnname + ' ' + operator + ' :' + str(self._paramidx)
                        self._param[str(self._paramidx)]=value
                        self._paramidx +=1
                else:
                    if operator.upper()=='IS' or operator.upper()=='IS NOT':
                        self._strwhere= self._strwhere + columnname + ' ' + operator + ' NULL'
                    else:
                        self._strwhere= self._strwhere + columnname + ' ' + operator + ' :' + str(self._paramidx)
                        self._param[str(self._paramidx)]=value
                        self._paramidx +=1
            else:
                raise AttributeError, "'" + operator + "'" + " - Not a supported operator."
        else:
            raise AttributeError, "'" + columnname + "'" + " - Not a Valid Column Name."
    def whereclear(self):
        ''' Resets the WHERE clause'''
        self._strwhere = ''
        self._param = {}
        self._paramidx = 1
class rt_unit_conversion_factor():
    ''' Class for table RT_UNIT_CONVERSION_FACTOR. Performs basic CRUD operation on table.'''
    def __init__(self):
        '''RT_UNIT_CONVERSION_FACTOR.columnnames - returns list of Column Names
           RT_UNIT_CONVERSION_FACTOR.pkey - returns list of tables primary key(s)
        '''
        self.columnnames = ['REPORTED_UNIT','TARGET_UNIT','CONVERSION_FACTOR','DELTA','STATUS_FLAG','REMARK']
        self.pkey =['REPORTED_UNIT','TARGET_UNIT']
        self._operator = ['=','!=','>=','<=','=>','=<','>','<','IS','IS NOT']
        self._strwhere = ''
        self._param = {}
        self._paramidx = 1
    def printset(self,cur,header=True):
        '''Prints to standard out the cursor pass to function
           example: Optional variables denoted []
           rt_unit_conversion_factor.printset(rt_unit_conversion_factor.select(),[header=False])
        '''
        if header:
            temp=[]
            for row in cur.description:
                temp.append(row[0])
            print tuple(temp)
        for row in cur:
            print row
    def selectpkey(self,REPORTED_UNIT,TARGET_UNIT):
        '''Returns cursor of single record with associated Pkey.
           example:
           Cursor = rt_unit_conversion_factor.selectpkey(REPORTED_UNIT = <AppropriateKey>,TARGET_UNIT = <AppropriateKey>)
        '''
        c1= connection.cursor()
        sql = "SELECT REPORTED_UNIT, TARGET_UNIT, CONVERSION_FACTOR, DELTA, STATUS_FLAG, REMARK FROM RT_UNIT_CONVERSION_FACTOR"
        sql = sql + " WHERE REPORTED_UNIT = :REPORTED_UNIT AND TARGET_UNIT = :TARGET_UNIT"
        param ={'REPORTED_UNIT' : REPORTED_UNIT, 'TARGET_UNIT' : TARGET_UNIT}
        c1.execute(sql, param)
        return c1
    def select(self,columnList = 'ALL'):
        '''Returns cursor with all rows. Optional columnList(Python List) - List of columns to return.
           Optional - Run rt_unit_conversion_factor.where('COLUMN_NAME','=',AppropriateValue) function to provide a where clause.
               rt_unit_conversion_factor.where('REPORTED_UNIT', '=',<AppropriateValue>)
           example:		   
               Cursor = rt_unit_conversion_factor.select(columnList)
        '''
        if columnList == 'ALL':
            columnList= self.columnnames
        colstr=''
        c1 = connection.cursor()
        first=True
        for col in columnList:
            if not first:
                colstr=colstr + ', '
            first=False
            colstr=colstr + col
        sql = 'SELECT ' + colstr + ' FROM RT_UNIT_CONVERSION_FACTOR '
        if len(self._strwhere.strip())>0:
            sql = sql + 'WHERE ' + self._strwhere 
        c1.execute(sql,self._param)
        return c1
    #@transaction.commit_on_success()
    def update(self, REPORTED_UNIT, TARGET_UNIT, **uargs):
        '''Updates record varaiables. Does not allow update of primary keys.
            example: 
            rt_unit_conversion_factor.update(REPORTED_UNIT = <AppropriateKey>,TARGET_UNIT = <AppropriateKey>,[COLUMN_NAME = <UpdateValues>])
        '''
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
        '''Insert record varaiables.
            example: 
            rt_unit_conversion_factor.insert(REPORTED_UNIT = <AppropriateKey>,TARGET_UNIT = <AppropriateKey>,[COLUMN_NAME = <InsertValues>])
        '''
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
    def insertmany(self, ListDict ):
        '''Insert Many takes a list of Dictionaries which contain variables to insert. Must contain all columns for insertmany().
            example: 
            rt_unit_conversion_factor.insertmany(ListDict)
        '''
        c1 = connection.cursor()
        sql = "INSERT INTO RT_UNIT_CONVERSION_FACTOR "
        col = "("
        vals = " VALUES ("
        first=True
        for colname in self.columnnames:
            if not first:
                col=col + ", "
                vals=vals + ", "
            first=False
            col = col + colname
            vals = vals + ':' + colname
        sql = sql + col + ")" + vals + ")"
        c1.executemany(sql,ListDict)
        connection.commit()
    #@transaction.commit_on_success()
    def delete(self,REPORTED_UNIT, TARGET_UNIT):
        '''Deletes record with associated Pkey.
           example:
           rt_unit_conversion_factor.delete(REPORTED_UNIT = <AppropriateKey>, TARGET_UNIT = <AppropriateKey>)
        '''
        c1 = connection.cursor()
        param={}
        param['REPORTED_UNIT'] = REPORTED_UNIT
        param['TARGET_UNIT'] = TARGET_UNIT
        sql= 'DELETE FROM RT_UNIT_CONVERSION_FACTOR'
        sql = sql + ' WHERE REPORTED_UNIT = :REPORTED_UNIT AND TARGET_UNIT = :TARGET_UNIT'
        c1.execute(sql, param)
        connection.commit()
    def where(self,columnname,operator,value,conjunction='AND'):
        ''' Sets the WHERE clause for the select function. Default Conjunction is 'AND'
            example:
                RT_UNIT_CONVERSION_FACTOR.where('COlUMNNAME','=',AppropriateValue)
                RT_UNIT_CONVERSION_FACTOR.where('COlUMNNAME','=',AppropriateValue,'OR')
        '''
        if columnname in self.columnnames:
            if operator in self._operator:
                if len(self._strwhere)>0:
                    if operator.upper()=='IS' or operator.upper()=='IS NOT':
                        self._strwhere= self._strwhere + ' ' + conjunction + ' ' + columnname + ' ' + operator + ' NULL'
                    else:
                        self._strwhere= self._strwhere + ' ' + conjunction + ' ' + columnname + ' ' + operator + ' :' + str(self._paramidx)
                        self._param[str(self._paramidx)]=value
                        self._paramidx +=1
                else:
                    if operator.upper()=='IS' or operator.upper()=='IS NOT':
                        self._strwhere= self._strwhere + columnname + ' ' + operator + ' NULL'
                    else:
                        self._strwhere= self._strwhere + columnname + ' ' + operator + ' :' + str(self._paramidx)
                        self._param[str(self._paramidx)]=value
                        self._paramidx +=1
            else:
                raise AttributeError, "'" + operator + "'" + " - Not a supported operator."
        else:
            raise AttributeError, "'" + columnname + "'" + " - Not a Valid Column Name."
    def whereclear(self):
        ''' Resets the WHERE clause'''
        self._strwhere = ''
        self._param = {}
        self._paramidx = 1
class rt_variables():
    ''' Class for table RT_VARIABLES. Performs basic CRUD operation on table.'''
    def __init__(self):
        '''RT_VARIABLES.columnnames - returns list of Column Names
           RT_VARIABLES.pkey - returns list of tables primary key(s)
        '''
        self.columnnames = ['VAR_ID','VARIABLE_NAME','SORT_ORDER','VARIABLE_TYPE','STATUS_FLAG','VAR_SHORT_NAME','REMARK']
        self.pkey =['VAR_ID']
        self._operator = ['=','!=','>=','<=','=>','=<','>','<','IS','IS NOT']
        self._strwhere = ''
        self._param = {}
        self._paramidx = 1
    def printset(self,cur,header=True):
        '''Prints to standard out the cursor pass to function
           example: Optional variables denoted []
           rt_variables.printset(rt_variables.select(),[header=False])
        '''
        if header:
            temp=[]
            for row in cur.description:
                temp.append(row[0])
            print tuple(temp)
        for row in cur:
            print row
    def selectpkey(self,VAR_ID):
        '''Returns cursor of single record with associated Pkey.
           example:
           Cursor = rt_variables.selectpkey(VAR_ID = <AppropriateKey>)
        '''
        c1= connection.cursor()
        sql = "SELECT VAR_ID, VARIABLE_NAME, SORT_ORDER, VARIABLE_TYPE, STATUS_FLAG, VAR_SHORT_NAME, REMARK FROM RT_VARIABLES"
        sql = sql + " WHERE VAR_ID = :VAR_ID"
        param ={'VAR_ID' : VAR_ID}
        c1.execute(sql, param)
        return c1
    def select(self,columnList = 'ALL'):
        '''Returns cursor with all rows. Optional columnList(Python List) - List of columns to return.
           Optional - Run rt_variables.where('COLUMN_NAME','=',AppropriateValue) function to provide a where clause.
               rt_variables.where('VAR_ID', '=',<AppropriateValue>)
           example:		   
               Cursor = rt_variables.select(columnList)
        '''
        if columnList == 'ALL':
            columnList= self.columnnames
        colstr=''
        c1 = connection.cursor()
        first=True
        for col in columnList:
            if not first:
                colstr=colstr + ', '
            first=False
            colstr=colstr + col
        sql = 'SELECT ' + colstr + ' FROM RT_VARIABLES '
        if len(self._strwhere.strip())>0:
            sql = sql + 'WHERE ' + self._strwhere 
        c1.execute(sql,self._param)
        return c1
    #@transaction.commit_on_success()
    def update(self, VAR_ID, **uargs):
        '''Updates record varaiables. Does not allow update of primary keys.
            example: 
            rt_variables.update(VAR_ID = <AppropriateKey>,[COLUMN_NAME = <UpdateValues>])
        '''
        c1 = connection.cursor()
        param={}
        sql = "UPDATE RT_VARIABLES SET "
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
        '''Insert record varaiables.
            example: 
            rt_variables.insert(VAR_ID = <AppropriateKey>,[COLUMN_NAME = <InsertValues>])
        '''
        c1 = connection.cursor()
        sql = "INSERT INTO RT_VARIABLES "
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
    def insertmany(self, ListDict ):
        '''Insert Many takes a list of Dictionaries which contain variables to insert. Must contain all columns for insertmany().
            example: 
            rt_variables.insertmany(ListDict)
        '''
        c1 = connection.cursor()
        sql = "INSERT INTO RT_VARIABLES "
        col = "("
        vals = " VALUES ("
        first=True
        for colname in self.columnnames:
            if not first:
                col=col + ", "
                vals=vals + ", "
            first=False
            col = col + colname
            vals = vals + ':' + colname
        sql = sql + col + ")" + vals + ")"
        c1.executemany(sql,ListDict)
        connection.commit()
    #@transaction.commit_on_success()
    def delete(self,VAR_ID):
        '''Deletes record with associated Pkey.
           example:
           rt_variables.delete(VAR_ID = <AppropriateKey>)
        '''
        c1 = connection.cursor()
        param={}
        param['VAR_ID'] = VAR_ID
        sql= 'DELETE FROM RT_VARIABLES'
        sql = sql + ' WHERE VAR_ID = :VAR_ID'
        c1.execute(sql, param)
        connection.commit()
    def where(self,columnname,operator,value,conjunction='AND'):
        ''' Sets the WHERE clause for the select function. Default Conjunction is 'AND'
            example:
                RT_VARIABLES.where('COlUMNNAME','=',AppropriateValue)
                RT_VARIABLES.where('COlUMNNAME','=',AppropriateValue,'OR')
        '''
        if columnname in self.columnnames:
            if operator in self._operator:
                if len(self._strwhere)>0:
                    if operator.upper()=='IS' or operator.upper()=='IS NOT':
                        self._strwhere= self._strwhere + ' ' + conjunction + ' ' + columnname + ' ' + operator + ' NULL'
                    else:
                        self._strwhere= self._strwhere + ' ' + conjunction + ' ' + columnname + ' ' + operator + ' :' + str(self._paramidx)
                        self._param[str(self._paramidx)]=value
                        self._paramidx +=1
                else:
                    if operator.upper()=='IS' or operator.upper()=='IS NOT':
                        self._strwhere= self._strwhere + columnname + ' ' + operator + ' NULL'
                    else:
                        self._strwhere= self._strwhere + columnname + ' ' + operator + ' :' + str(self._paramidx)
                        self._param[str(self._paramidx)]=value
                        self._paramidx +=1
            else:
                raise AttributeError, "'" + operator + "'" + " - Not a supported operator."
        else:
            raise AttributeError, "'" + columnname + "'" + " - Not a Valid Column Name."
    def whereclear(self):
        ''' Resets the WHERE clause'''
        self._strwhere = ''
        self._param = {}
        self._paramidx = 1
class schema_version():
    ''' Class for table SCHEMA_VERSION. Performs basic CRUD operation on table.'''
    def __init__(self):
        '''SCHEMA_VERSION.columnnames - returns list of Column Names
           SCHEMA_VERSION.pkey - returns list of tables primary key(s)
        '''
        self.columnnames = ['TIMESTAMP','KEY','EXTRA','SFILE']
        self.pkey =['KEY']
        self._operator = ['=','!=','>=','<=','=>','=<','>','<','IS','IS NOT']
        self._strwhere = ''
        self._param = {}
        self._paramidx = 1
    def printset(self,cur,header=True):
        '''Prints to standard out the cursor pass to function
           example: Optional variables denoted []
           schema_version.printset(schema_version.select(),[header=False])
        '''
        if header:
            temp=[]
            for row in cur.description:
                temp.append(row[0])
            print tuple(temp)
        for row in cur:
            print row
    def selectpkey(self,KEY):
        '''Returns cursor of single record with associated Pkey.
           example:
           Cursor = schema_version.selectpkey(KEY = <AppropriateKey>)
        '''
        c1= connection.cursor()
        sql = "SELECT TIMESTAMP, KEY, EXTRA, SFILE FROM SCHEMA_VERSION"
        sql = sql + " WHERE KEY = :KEY"
        param ={'KEY' : KEY}
        c1.execute(sql, param)
        return c1
    def select(self,columnList = 'ALL'):
        '''Returns cursor with all rows. Optional columnList(Python List) - List of columns to return.
           Optional - Run schema_version.where('COLUMN_NAME','=',AppropriateValue) function to provide a where clause.
               schema_version.where('KEY', '=',<AppropriateValue>)
           example:		   
               Cursor = schema_version.select(columnList)
        '''
        if columnList == 'ALL':
            columnList= self.columnnames
        colstr=''
        c1 = connection.cursor()
        first=True
        for col in columnList:
            if not first:
                colstr=colstr + ', '
            first=False
            colstr=colstr + col
        sql = 'SELECT ' + colstr + ' FROM SCHEMA_VERSION '
        if len(self._strwhere.strip())>0:
            sql = sql + 'WHERE ' + self._strwhere 
        c1.execute(sql,self._param)
        return c1
    #@transaction.commit_on_success()
    def update(self, KEY, datetime_format= 'YYYY-MM-DD HH24:MI:SS', **uargs):
        '''Updates record varaiables. Does not allow update of primary keys.
            example: 
            schema_version.update(KEY = <AppropriateKey>,[COLUMN_NAME = <UpdateValues>])
        '''
        c1 = connection.cursor()
        param={}
        sql = "UPDATE SCHEMA_VERSION SET "
        where = " WHERE KEY = :KEY"
        param['KEY'] = KEY
        first=True
        for colname,val in uargs.items():
            if not first:
                sql=sql + ", "
            first=False
            if (colname == 'TIMESTAMP'):
                sql =sql +  colname + ' = to_date(:' + colname + ', :datetime_format)'
                param['datetime_format'] = datetime_format
            else:
                sql =sql +  colname + ' = :' + colname
            param[colname]=val
        sql = sql + where
        c1.execute(sql, param)
        connection.commit()
    #@transaction.commit_on_success()
    def insert(self, KEY, datetime_format= 'YYYY-MM-DD HH24:MI:SS', **iargs):
        '''Insert record varaiables.
            example: 
            schema_version.insert(KEY = <AppropriateKey>,[COLUMN_NAME = <InsertValues>])
        '''
        c1 = connection.cursor()
        sql = "INSERT INTO SCHEMA_VERSION "
        col = "(KEY, "
        vals = " VALUES (:KEY, "
        first=True
        param={}
        param['KEY'] = KEY
        for colname,val in iargs.items():
            if not first:
                col=col + ", "
                vals=vals + ", "
            first=False
            col = col + colname
            if (colname == 'TIMESTAMP'):
                vals = vals + ' to_date(:' + colname + ', :datetime_format)'
                param['datetime_format'] = datetime_format
            else:
                vals = vals + ':' + colname
            param[colname]=val
        sql = sql + col + ")" + vals + ")"
        c1.execute(sql,param)
        connection.commit()
    #@transaction.commit_on_success()
    def insertmany(self, ListDict , datetime_format= 'YYYY-MM-DD HH24:MI:SS'):
        '''Insert Many takes a list of Dictionaries which contain variables to insert. Must contain all columns for insertmany().
            example: 
            schema_version.insertmany(ListDict, datetime_format= 'YYYY-MM-DD HH24:MI:SS')
        '''
        c1 = connection.cursor()
        sql = "INSERT INTO SCHEMA_VERSION "
        col = "("
        vals = " VALUES ("
        first=True
        for colname in self.columnnames:
            if not first:
                col=col + ", "
                vals=vals + ", "
            first=False
            col = col + colname
            if (colname == 'TIMESTAMP'):
                vals = vals + ' to_date(:' + colname + ' ,'
                vals = vals + "'" + datetime_format + "'" + ')'
            else:
                vals = vals + ':' + colname
        sql = sql + col + ")" + vals + ")"
        c1.executemany(sql,ListDict)
        connection.commit()
    #@transaction.commit_on_success()
    def delete(self,KEY):
        '''Deletes record with associated Pkey.
           example:
           schema_version.delete(KEY = <AppropriateKey>)
        '''
        c1 = connection.cursor()
        param={}
        param['KEY'] = KEY
        sql= 'DELETE FROM SCHEMA_VERSION'
        sql = sql + ' WHERE KEY = :KEY'
        c1.execute(sql, param)
        connection.commit()
    def where(self,columnname,operator,value,conjunction='AND'):
        ''' Sets the WHERE clause for the select function. Default Conjunction is 'AND'
            example:
                SCHEMA_VERSION.where('COlUMNNAME','=',AppropriateValue)
                SCHEMA_VERSION.where('COlUMNNAME','=',AppropriateValue,'OR')
        '''
        if columnname in self.columnnames:
            if operator in self._operator:
                if len(self._strwhere)>0:
                    if operator.upper()=='IS' or operator.upper()=='IS NOT':
                        self._strwhere= self._strwhere + ' ' + conjunction + ' ' + columnname + ' ' + operator + ' NULL'
                    else:
                        self._strwhere= self._strwhere + ' ' + conjunction + ' ' + columnname + ' ' + operator + ' :' + str(self._paramidx)
                        self._param[str(self._paramidx)]=value
                        self._paramidx +=1
                else:
                    if operator.upper()=='IS' or operator.upper()=='IS NOT':
                        self._strwhere= self._strwhere + columnname + ' ' + operator + ' NULL'
                    else:
                        self._strwhere= self._strwhere + columnname + ' ' + operator + ' :' + str(self._paramidx)
                        self._param[str(self._paramidx)]=value
                        self._paramidx +=1
            else:
                raise AttributeError, "'" + operator + "'" + " - Not a supported operator."
        else:
            raise AttributeError, "'" + columnname + "'" + " - Not a Valid Column Name."
    def whereclear(self):
        ''' Resets the WHERE clause'''
        self._strwhere = ''
        self._param = {}
        self._paramidx = 1