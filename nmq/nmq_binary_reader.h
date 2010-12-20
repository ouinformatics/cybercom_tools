#ifndef NMQ_BINARY_READER_H
#define NMQ_BINARY_READER_H

#include <iostream>
#include <fstream>
#include <zlib.h>
#include <vector>
#include <string>
#include <ctime>

using namespace std;


/*------------------------------------------------------------------

	Function:	byteswap (version 1)
		
	Purpose:	Perform byte swap operation on various data
	            types		
				
	Input:		data = some value
					
	Output:		value byte swapped
	
------------------------------------------------------------------*/
template < class Data_Type >
inline void byteswap( Data_Type &data )
{
  unsigned int num_bytes = sizeof( Data_Type );
  char *char_data = reinterpret_cast< char * >( &data );
  char *temp = new char[ num_bytes ];

  for( unsigned int i = 0; i < num_bytes; i++ )
  {
    temp[ i ] = char_data[ num_bytes - i - 1 ];
  }

  for( unsigned int i = 0; i < num_bytes; i++ )
  {
    char_data[ i ] = temp[ i ];
  }
  delete [] temp;
}
  


/*------------------------------------------------------------------

	Function:	byteswap (version 2)
		
	Purpose:	Perform byte swap operation on an array of
	            various data types		
				
	Input:		data = array of values
					
	Output:		array of byte swapped values
	
------------------------------------------------------------------*/
template < class Data_Type >
inline void byteswap( Data_Type *data_array, int num_elements )
{
  int num_bytes = sizeof( Data_Type );
  char *temp = new char[ num_bytes ];
  char *char_data;

  for( int i = 0; i < num_elements; i++ )
  {
    char_data = reinterpret_cast< char * >( &data_array[ i ] );

    for( int i = 0; i < num_bytes; i++ )
    {
      temp[ i ] = char_data[ num_bytes - i - 1 ];
    }

    for( int i = 0; i < num_bytes; i++ )
    {
      char_data[ i ] = temp[ i ];
    }
  }
  delete [] temp;
}



/*------------------------------------------------------------------

	Function: nmq_binary_reader_cart3d
		
	Purpose:  Read a NMQ Cartesian binary file and return
              it's header info and data.		
				
	Input:    vfname = input file name and path
	
              swap_flag = flag (= 0 or 1) indicating if values
                          read from the file should be byte 
                          swapped
                
                
	Output:   varname = Name of variable
	          varunit = Units of variable
	
	          nradars = Number of radars used in product
	          radarnam = List of radars used in product
	
	          var_scale = Value used to scale the variable data	
	          missing_val = Value to indicate missing data
	
	          nw_lon = Longitude of NW grid cell (center of cell)
	          nw_lat = Latitude of NW grid cell (center of cell)
	          
	          nx = Number of columns in field
	          ny = Number of rows in field
	          dx = Size of grid cell w.r.t. Longitude (degrees)
	          dy = Size of grid cell w.r.t. Latitude (degrees)
	          
	          zhgt = Height of vertical levels
	          nz = Number of vertical levels
	            
	          binary_data = Variable data (scaled) in 1D array
	
------------------------------------------------------------------*/
short int* nmq_binary_reader_cart3d(char *vfname,                     
                     char *varname,char *varunit,
                     int &nradars, vector<string> &radarnam,
                     int &var_scale, int &missing_val,
                     float &nw_lon, float &nw_lat,
                     int &nx, int &ny, float &dx, float &dy,
                     float zhgt[], int &nz, long &epoch_seconds,
                     int swap_flag)

{

    /*--------------------------*/
    /*** 0. Declare variables ***/ 
    /*--------------------------*/
    
    short int *binary_data = 0;

    int yr,mo,day,hr,min,sec;
    int map_scale, xy_scale, dxy_scale, z_scale;
    int mapproj;
    float trulat1, trulat2, trulon;
    char projection[5];
    char temp_varname[20];
    char temp_varunit[6];

    int temp;



    /*-------------------------*/
    /*** 1. Open binary file ***/ 
    /*-------------------------*/
        
    char open_mode[3];
    gzFile   fp_gzip;

    sprintf(open_mode,"%s","rb");
    open_mode[2] = '\0';

    if ( (fp_gzip = gzopen(vfname,open_mode) ) == (gzFile) NULL )
    {
      cout<<"+++ERROR: Could not open "<<vfname<<endl;
      return binary_data;
    }



    /*---------------------------------------*/
    /*** 2. Read binary header information ***/ 
    /*---------------------------------------*/
    
    //reading time
    gzread( fp_gzip, &yr,sizeof(int));
    if (swap_flag==1) byteswap(yr);
    
    gzread( fp_gzip, &mo,sizeof(int));
    if (swap_flag==1) byteswap(mo);
    
    gzread( fp_gzip, &day,sizeof(int));
    if (swap_flag==1) byteswap(day);
    
    gzread( fp_gzip, &hr,sizeof(int));
    if (swap_flag==1) byteswap(hr);
    
    gzread( fp_gzip, &min,sizeof(int));
    if (swap_flag==1) byteswap(min);
    
    gzread( fp_gzip, &sec,sizeof(int));
    if (swap_flag==1) byteswap(sec);


    //Compute difference between local time and GMT
    time_t  now, now_gmt;
    now = time(NULL);
    struct tm *gmtime0 = gmtime(&now);
    gmtime0->tm_isdst   = -1;
    now_gmt = mktime (gmtime0);
    long gmt_lcl_diff = now_gmt - now;

    //Compute epoch seconds
    struct tm gmt_file_time;    
    gmt_file_time.tm_sec = sec;
    gmt_file_time.tm_min = min;
    gmt_file_time.tm_hour = hr;
    gmt_file_time.tm_mday = day;
    gmt_file_time.tm_mon  = mo-1;
    gmt_file_time.tm_year = yr-1900;

    epoch_seconds = (long)mktime(&gmt_file_time) - gmt_lcl_diff;


    //read dimensions
    gzread( fp_gzip,&temp,sizeof(int)) ;
    if (swap_flag==1) byteswap(temp);
    nx = temp;
    
    gzread( fp_gzip, &temp,sizeof(int)) ;
    if (swap_flag==1) byteswap(temp);
    ny = temp;
    
    gzread( fp_gzip, &temp,sizeof(int)) ;
    if (swap_flag==1) byteswap(temp);
    nz = temp;


    //read map projection type
    gzread(fp_gzip,&projection,4*sizeof(char));
    if (swap_flag==1) byteswap(projection, 4);
    projection[4] = '\0';
    
    if (strncmp(projection, "    ", 4)==0 ) temp=0; 
    else if (strncmp(projection, "PS  ", 4)==0 ) temp=1;
    else if (strncmp(projection, "LAMB", 4)==0 ) temp=2; 
    else if (strncmp(projection, "MERC", 4)==0 ) temp=3; 
    else if (strncmp(projection, "LL  ", 4)==0 ) temp=4; 
    else temp = -1;
    
    mapproj = temp;


    //read map scale factor
    gzread(fp_gzip,&temp,sizeof(int));
    if (swap_flag==1) byteswap(temp);
    map_scale = temp;
      
      
    //read trulat1, trulat2, trulon
    gzread( fp_gzip,&temp,sizeof(int)) ;
    if (swap_flag==1) byteswap(temp);
    trulat1 = (float)temp/(float)map_scale;
    
    gzread( fp_gzip, &temp,sizeof(int)) ;
    if (swap_flag==1) byteswap(temp);
    trulat2 = (float)temp/(float)map_scale;
    
    gzread( fp_gzip, &temp,sizeof(int)) ;
    if (swap_flag==1) byteswap(temp);
    trulon = (float)temp/(float)map_scale;
    
      
    //read nw lat/lon coordinates
    gzread(fp_gzip,&temp,sizeof(int));
    if (swap_flag==1) byteswap(temp);
    nw_lon = (float)temp/(float)map_scale;
    
    gzread(fp_gzip,&temp,sizeof(int));
    if (swap_flag==1) byteswap(temp);
    nw_lat = (float)temp/(float)map_scale;


    //read xy scale
    gzread(fp_gzip,&temp,sizeof(int));
    if (swap_flag==1) byteswap(temp);
    xy_scale = temp;


    //read dx and dy    
    gzread(fp_gzip,&temp,sizeof(int));
    if (swap_flag==1) byteswap(temp);
    dx = (float)temp;

    gzread(fp_gzip,&temp,sizeof(int));
    if (swap_flag==1) byteswap(temp);
    dy = (float)temp;


    //read dx and dy scaling factor and unscale
    gzread(fp_gzip,&temp,sizeof(int));
    if (swap_flag==1) byteswap(temp);
    dxy_scale = temp;
      
    dx = dx/float(dxy_scale);
    dy = dy/float(dxy_scale);


    //read heights      
    for(int k=0; k<nz; k++)
    {
      gzread(fp_gzip,&temp,sizeof(int));
      if (swap_flag==1) byteswap(temp);
      zhgt[k] = (float)temp;
    }


    //read z scale 
    gzread(fp_gzip,&temp,sizeof(int)); //z_scale
    if (swap_flag==1) byteswap(temp);
    z_scale = temp;
      
      
    //read junk (place holders for future use)
    for(int j = 0; j < 10; j++)
    {
      gzread(fp_gzip,&temp,sizeof(int)); 
    }
      
      
    //read variable name
    gzread(fp_gzip,temp_varname,20*sizeof(char));
    if (swap_flag==1) byteswap(temp_varname,20);    
    temp_varname[19]='\0';
    
    strcpy(varname, temp_varname);


    //read variable unit
    gzread(fp_gzip,temp_varunit,6*sizeof(char));
    if (swap_flag==1) byteswap(temp_varunit,6);    
    temp_varunit[5]='\0';
    
    strcpy(varunit, temp_varunit);


    //read variable scaling factor
    gzread(fp_gzip,&var_scale,sizeof(int));
    if (swap_flag==1) byteswap(var_scale);


    //read variable missing flag
    gzread(fp_gzip,&missing_val,sizeof(int));
    if (swap_flag==1) byteswap(missing_val);


    //read number of radars affecting this product
    gzread(fp_gzip,&nradars,sizeof(int));
    if (swap_flag==1) byteswap(nradars);
      
      
    //read in names of radars
    char temp_radarnam[5];
      
    for(int i=0;i<nradars;i++)
    {
      gzread(fp_gzip,temp_radarnam,4*sizeof(char));
      if (swap_flag==1) byteswap(temp_radarnam,4);
      temp_radarnam[4]='\0';
      
      radarnam.push_back(temp_radarnam);
    }



    /*-------------------------*/
    /*** 3. Read binary data ***/ 
    /*-------------------------*/
    
    int num = nx*ny*nz;
    binary_data = new short int[num];
      
    //read data array
    gzread(fp_gzip,binary_data,num*sizeof(short int));
    if (swap_flag==1) byteswap(binary_data,num);
      
      
      
    /*------------------------------*/
    /*** 4. Close file and return ***/ 
    /*------------------------------*/
   
    //close file      
    gzclose( fp_gzip );

    return binary_data;

}//end nmq_binary_reader_cart3d function

#endif
