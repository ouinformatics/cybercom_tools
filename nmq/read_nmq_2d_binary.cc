#include <iostream>
#include <vector>
#include <string>

#include "nmq_binary_reader.h"

using namespace std;   

/*%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

	Program:	read_nmq_2d_binary.cc
	
	Date:		May 2006
	
	Author:		Carrie Langston (CIMMS/NSSL)
	        	
	Purpose:	This program will read in a HMRG binary file,
	            reassign the 1D input to a 2D array, and
	            unscale the data field.
		
	Input:		2 command-line arguments:
					1) input file path and name
					2) swap byte flag 
					     = 0; no
					     = 1; yes
					     
	            NOTE: You may need to set the swap byte flag to 1  
	            if the OS you're using to read the binary file 
	            differs from the one used to write the file, 
	            such that the endain order differs (i.e., 
	            "Little Endian" vs. "Big Endian").  The program 
	            will likely crash if the swap flag is set
	            incorrectly (so you'll find out quickly if it
	            needs to be set to 0 or 1). 
	                  
	Output: 	Messages to standard output
				
				
	To Compile:	If using g++ compiler...
	            g++ -o read_nmq_binary read_nmq_binary.cc -lz
	           	
	To Run:		read_nmq_binary <input file> <swap flag>
																											
	_____________________________________________________________			
	Modification History:
	       

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%*/


/************************************************/
/***  F U N C T I O N  P R O T O T Y P E (S)  ***/
/************************************************/

short int* nmq_binary_reader_cart3d(char *vfname,                     
                     char *varname,char *varunit,
                     int &nradars, vector<string> &radarnam,
                     int &var_scale, int &missing_val,
                     float &nw_lon, float &nw_lat,
                     int &nx, int &ny, float &dx, float &dy,
                     float zp[], int &nz, long &epoch_seconds,
                     int swap_flag);
                   
                   

/********************************/
/***  M A I N  P R O G R A M  ***/
/********************************/

int main(int argc,  char* argv[])
{
    cout<<"\n\n"<<endl;
    cout<<"      *************************************************"<<endl;
    cout<<"      *                                               *"<<endl;
    cout<<"      *        WELCOME TO NMQ 2D BINARY READER        *"<<endl;
    cout<<"      *                                               *"<<endl;
    cout<<"      *************************************************"<<endl;
    cout<<endl;
    


    /*---------------------------------------*/
    /*** 0. Process command-line arguments ***/ 
    /*---------------------------------------*/

    //Process command-line arguments
    if(argc!=3)
    {
      cout<<"Usage:  read_nmq_2d_binary /path/input_file swap_flag"<<endl;
      cout<<"Exiting from read_nmq_2d_binary."<<endl<<endl;
      exit(0);
    }

    char input_file[300];
    strcpy(input_file, argv[1]);

    int swap_flag = atoi(argv[2]);
    


    /*---------------------------------------------------*/
    /*** 1. Declare several variables needed by reader ***/
    /*---------------------------------------------------*/

    char varname[20];
    char varunit[6];
    int nradars;
    vector<string> radarnames;
    int var_scale, missing;
    float nw_lat, nw_lon;
    int nx, ny, nz;
    float dx, dy;
    float zhgt[1]; //expecting only 2D field
    long epoch_sec;

    short int* input_data_1D = 0;



    /*-------------------------*/
    /*** 2. Read input field ***/
    /*-------------------------*/

    //Read file
    input_data_1D = nmq_binary_reader_cart3d(input_file,                     
                           varname, varunit,
                           nradars, radarnames,
                           var_scale, missing,
                           nw_lon, nw_lat,
                           nx, ny, dx, dy,
                           zhgt, nz, epoch_sec, swap_flag);


    //Perform some error checking
    if(input_data_1D == 0)
    {
      cout<<"+++ERROR: Failed to read "<<input_file<<" Exiting!"<<endl;
      return 0;
    }
    cout<<"DONE reading file"<<endl<<endl;
    
    if(nz > 1)
    {
      cout<<"++WARNING: number of vertical levels is greater than 1"
          <<"... Indicating this is a 3D field, not 2D!!"<<endl;
    }
    

    //Print out header info.
    cout<<"Binary Header Info:"<<endl;
    cout<<" variable name = "<<varname<<endl;
    cout<<" variable unit = "<<varunit<<endl;
    cout<<" number of radars = "<<nradars<<endl;
    
    cout<<" Radars: ";
    for(size_t i = 0; i < radarnames.size(); i++)
      cout<<radarnames[i]<<" ";
    cout<<endl;
    
    cout<<" variable scale = "<<var_scale<<endl;
    cout<<" missing value = "<<missing<<endl;
    cout<<" NW latitude = "<<nw_lat<<endl;
    cout<<" NW longitude = "<<nw_lon<<endl;
    cout<<" Number of columns = "<<nx<<endl;
    cout<<" Number of rows = "<<ny<<endl;
    cout<<" Grid cell size (degree lat.) = "<<dy<<endl;
    cout<<" Grid cell size (degree lon.) = "<<dx<<endl;
    cout<<" Number of vertical levels = "<<nz<<endl;
    
    cout<<" Height = ";
    for(int i = 0; i < nz; i++) cout<<zhgt[i]<<" ";
    cout<<endl;
    
    char timestamp[20];
    strftime(timestamp, 20, "%m/%d/%Y %H%M", gmtime(&epoch_sec));
    cout<<" Time = "<<timestamp<<" UTC  (or "<<epoch_sec
        <<" epoch seconds)"<<endl<<endl;

      
    
    /*----------------------------------------------*/
    /*** 3. Reassign to 2D array and unscale data ***/
    /*----------------------------------------------*/
    
    //NOTE: The field's origin (data_2D[0][0]) is the SW corner.  
    //      As j increases so does the latitude.
    
    float **data_2D = new float* [nx];
    for(int i = 0; i < nx; i++) data_2D[i] = new float [ny];
    
    int index = -1;
    
    for(int i = 0; i < nx; i++)
    {
      for(int j = 0; j < ny; j++)
      {
        index = j*nx + i;
        data_2D[i][j] = (float)input_data_1D[index] / (float)var_scale;
        if(j !=0) cout << "\t";
	cout << data_2D[i][j];
      }
      cout << endl;
    }
    

    /*------------------------*/
    /*** 4. Free-up Memory, ***/
    /*------------------------*/

    //memory clean-up
    if(input_data_1D != 0) delete [] input_data_1D;
        
    if(data_2D != 0)
    {
      for(int i = 0; i < nx; i++) delete [] data_2D[i];
      delete [] data_2D;
    }
        

    return 1;
    
}//end main function




/**************************/
/*** F U N C T I O N S  ***/
/**************************/

//see nmq_binary_reader.h
