CREATE TABLE ECO.DT_CATALOG ( 
    CAT_ID NUMBER NOT NULL,
    CAT_NAME VARCHAR2( 150 ) NULL,
    DESCRIPTION VARCHAR2( 1000 ) NULL,
    TYPE_ID VARCHAR2( 255 ) NULL,
    TIME_ID NUMBER NULL,
    LOC_ID NUMBER NULL,
CONSTRAINT PK_DT_CATALOG PRIMARY KEY ( CAT_ID )
 ) ;

CREATE INDEX idx_DT_CATALOG_1 ON ECO.DT_CATALOG ( TYPE_ID );

CREATE INDEX IDX_DT_CATALOG ON ECO.DT_CATALOG ( LOC_ID );

CREATE INDEX IDX_DT_CATALOG_0 ON ECO.DT_CATALOG ( TIME_ID );

COMMENT ON TABLE ECO.DT_CATALOG IS 'Catalog and Inventory of available data for Cybercommons.';

COMMENT ON COLUMN ECO.DT_CATALOG.CAT_NAME IS 'Descriptive name that logically describes data.';

COMMENT ON COLUMN ECO.DT_CATALOG.DESCRIPTION IS 'Detail Description of Data.';

COMMENT ON COLUMN ECO.DT_CATALOG.TYPE_ID IS 'Index to TYPE TABLE.';

CREATE TABLE ECO.DT_LOCATION ( 
    LOC_ID NUMBER NOT NULL,
    DT_TYPE VARCHAR2( 150 ) NULL,
    LOC_X FLOAT NULL,
    LOC_Y FLOAT NULL,
    NORTHBOUNDING FLOAT NULL,
    SOUTHBOUNDING FLOAT NULL,
    EASTBOUNDING FLOAT NULL,
    WESTBOUNDING FLOAT NULL,
    COORD_SYSTEM VARCHAR2( 255 ) NULL,
CONSTRAINT PK_DT_LOCATION PRIMARY KEY ( LOC_ID )
 ) ;

CREATE TABLE ECO.DT_PARAMETER ( 
    CAT_ID NUMBER NOT NULL,
    PARAM_ID NUMBER NOT NULL,
    DESCRIPTION VARCHAR2( 255 ) NULL,
    VALUE VARCHAR2( 255 ) NULL,
    VALUE_DTYPE VARCHAR2( 255 ) NULL,
    PARAM_ORDER NUMBER NULL,
CONSTRAINT Idx_DT_PARAMETER PRIMARY KEY ( PARAM_ID, CAT_ID )
 ) ;

COMMENT ON TABLE ECO.DT_PARAMETER IS 'Holds Parameter of data calls in which the data is stored in cache.';

COMMENT ON COLUMN ECO.DT_PARAMETER.VALUE_DTYPE IS 'INT, Double,String,...ect. 
Need to set Data Type Standard. For reading Parameter list.';

COMMENT ON COLUMN ECO.DT_PARAMETER.PARAM_ORDER IS 'ORDER TO RECIEVE IN DATA CALL';

CREATE TABLE ECO.DT_SOURCE ( 
    CAT_ID NUMBER NOT NULL,
    SOURCE_ID NUMBER NOT NULL,
    LOC_STATUS VARCHAR2( 15 ) NULL,
    SOURCE_NAME VARCHAR2( 255 ) NULL,
    PATH VARCHAR2( 255 ) NULL,
    PATH_DESC VARCHAR2( 500 ) NULL,
CONSTRAINT IDX_DT_SOURCE PRIMARY KEY ( CAT_ID, SOURCE_ID )
 ) ;

COMMENT ON TABLE ECO.DT_SOURCE IS 'Metadata describing the origin of the Data.            ';

COMMENT ON COLUMN ECO.DT_SOURCE.CAT_ID IS 'Primary Key';

COMMENT ON COLUMN ECO.DT_SOURCE.LOC_STATUS IS 'Local or Virtual';

COMMENT ON COLUMN ECO.DT_SOURCE.SOURCE_NAME IS 'Source Name';

COMMENT ON COLUMN ECO.DT_SOURCE.PATH IS 'URL or the file path and filename where data is located.';

COMMENT ON COLUMN ECO.DT_SOURCE.PATH_DESC IS 'Description of Path and need parameters. (x,y, bounding box....ect)';

CREATE TABLE ECO.DT_TEMPORAL ( 
    TIME_ID NUMBER NOT NULL,
    DESCRIPTION VARCHAR2( 255 ) NULL,
    TEMPORAL_GRANULARITY VARCHAR2( 255 ) NULL,
    ITEM_DATE VARCHAR2( 255 ) NULL,
    START_DATE DATE NULL,
    END_DATE DATE NULL,
    YEAR VARCHAR2( 25 ) NULL,
    DAY_OF_YEAR NUMBER NULL,
CONSTRAINT PK_DT_TEMPORAL PRIMARY KEY ( TIME_ID )
 ) ;

COMMENT ON TABLE ECO.DT_TEMPORAL IS 'Description of time that data covers';

COMMENT ON COLUMN ECO.DT_TEMPORAL.ITEM_DATE IS 'Date used in data item ';

CREATE TABLE ECO.DT_TYPE ( 
    TYPE_ID VARCHAR2( 255 ) NOT NULL,
    TYPE_NAME VARCHAR2( 255 ) NULL,
    PRODUCT VARCHAR2( 255 ) NULL,
    DESCRIPTION VARCHAR2( 255 ) NULL,
    RESOLUTION VARCHAR2( 255 ) NULL,
    RES_UNIT VARCHAR2( 50 ) NULL,
    OBJECT_TYPE VARCHAR2( 100 ) NULL,
    OBJECT_DATA_OPT1 VARCHAR2( 255 ) NULL,
    OBJECT_DATA_OPT1_UNIT VARCHAR2( 100 ) NULL,
CONSTRAINT PK_Table PRIMARY KEY ( TYPE_ID )
 ) ;

COMMENT ON TABLE ECO.DT_TYPE IS 'Describes the type of data that it catalogs.';

COMMENT ON COLUMN ECO.DT_TYPE.TYPE_ID IS 'PK For Types';

ALTER TABLE ECO.DT_CATALOG ADD CONSTRAINT FK_DT_CATALOG_0 FOREIGN KEY ( TYPE_ID ) REFERENCES ECO.DT_TYPE( TYPE_ID ) ON DELETE CASCADE ;

ALTER TABLE ECO.DT_CATALOG ADD CONSTRAINT FK_DT_CATALOG FOREIGN KEY ( LOC_ID ) REFERENCES ECO.DT_LOCATION( LOC_ID ) ON DELETE CASCADE ;

ALTER TABLE ECO.DT_CATALOG ADD CONSTRAINT FK_DT_CATALOG_1 FOREIGN KEY ( TIME_ID ) REFERENCES ECO.DT_TEMPORAL( TIME_ID ) ON DELETE CASCADE ;

ALTER TABLE ECO.DT_PARAMETER ADD CONSTRAINT FK_DT_PARAMETER FOREIGN KEY ( CAT_ID ) REFERENCES ECO.DT_CATALOG( CAT_ID ) ON DELETE CASCADE ;

ALTER TABLE ECO.DT_SOURCE ADD CONSTRAINT FK_DT_SOURCE FOREIGN KEY ( CAT_ID ) REFERENCES ECO.DT_CATALOG( CAT_ID ) ON DELETE CASCADE ;