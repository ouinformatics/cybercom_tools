       program TECOS
       implicit none
       integer, parameter :: No_site=1     ! the sites to run
       integer, parameter :: iiterms=15     ! total iterms
       integer, parameter :: iterms_NEE=13 ! total iterms
       integer, parameter :: ilines=1402560  ! the maxmum records
       integer, parameter :: dlines=58440  ! the maxmum records, added by myself
       real, parameter:: times_storage_use=600  !1080.  !hours
       integer dayCount ! added by myself
       integer nonValidCount ! added by myself
       integer nValid  ! added by myself
       real sValid,varValue,paramspec,slope,sTotal  ! added by myself
       real sumObs,sumSim,sumObsObs,sumSimObs  ! added by myself
       real NEE_diff,bestSum,NEE_dif_sum ! added by myself !neeAccumulated
       integer lines,idays
       real inputstep,step_NEE
       integer,dimension(ilines):: year_data,year_NEE
       real,dimension(ilines) :: doy_data,hour_data
       real,dimension(ilines) :: doy_NEE,hour_NEE
       character(len=10) s_dlines
       character(len=10) s_ilines
       real NEE_obs(ilines) ! neeObserved(dlines) ! added by myself
       real neeSim_daily,neeObs_daily! added by myself
       real neeDif_day,neeDif_year,neeDif_all ! added by myself
       real,dimension(dlines)::neeSim_days,neeObs_days ! added by myself
       real input_data(iiterms,ilines)
       real reader_NEE(iterms_NEE)
!      site specific parameters
       real lat,longi,rdepth,LAIMAX,LAIMIN
       real wsmax,wsmin,co2ca
       real tau_R1,tau_R2,tau_R3 ! tau_L,tau_W,
       real tau_S1,tau_S2,tau_S3 ! tau_F,tau_C,
       real tau_L,tau_W,tau_R
       real tau_F,tau_C,tau_Micr,tau_Slow,tau_Pass

       real Q_leaf,Q_wood,Q_root
       real Q_fine,Q_coarse,Q_Micr,Q_Slow,Q_Pass
       real Rh_f,Rh_c,Rh_Micr,Rh_Slow,Rh_Pass
!      added 6 parameters ! added  by myself
       real TminV,TmaxV,ToptV,Tcold,Gamma_Wmax,Gamma_Tmax

       character(len=6) vegtype
       character(len=6) site
!      for soil conditions
       real WILTPT,FILDCP
       real fwsoil,topfws,wscontent,omega,omega_s
       real WaterR,WaterS(10),SatFracL(10)
!      for plant growth and allocation
       real NSC,NSCmin,NSCmax,add       ! none structural carbon pool
       real Growth,Groot,Gshoot,GRmax   ! growth rate of plant,root,shoot,and max of root
       real St,Sw,Ss,Sn,Srs,Sps,fnsc,Weight ! scaling factors for growth
       real Twsoil(7),Tavg,Tcur
!      variables for canopy model
       real evap,transp,ET,G,Qh,Qle 
       real wind,windu0,eairp,esat,wethr,rnet
       real LWdown,Pa_air,Qair  !  Near surface specific humidity
       real gpp,NPP,NEE,gpp_t,evap_t,transp_t
       real,dimension(3):: tauL,rhoL,rhoS,reffbm
       real,dimension(3):: reffdf,extkbm,extkdm
       real,dimension(2):: Radabv,Acan,Ecan,Hcan
       real,dimension(2):: Tcan,Gbwcan,Gswcan
       real Qcan(3,2),Qcan0(3)
!      parameters for photosynthesis model
       real stom_n,a1,Ds0,Vcmx0,extkU,xfang,alpha
       real pi,emleaf,emsoil
       real Rconst,sigma,cpair,Patm,Trefk,H2OLv0
       real airMa,H2OMw,chi,Dheat
       real wleaf,gsw0,eJmx0,theta,conKc0,conKo0,Ekc,Eko,o2ci
       real Eavm,Edvm,Eajm,Edjm,Entrpy,gam0,gam1,gam2
!      additional arrays to allow output of info for each layer
       real,dimension(5):: RnStL,QcanL,RcanL,AcanL,EcanL,HcanL
       real,dimension(5):: GbwcL,GswcL,hG,hIL
       real,dimension(5):: Gaussx,Gaussw,Gaussw_cum 
!      parameters to tune
       real,dimension(32):: randnums	! added by myself
       real,dimension(1,32):: params	! added by myself
!      for phenology
       real LAI,bmroot,bmstem,bmleaf,bmplant
       real SLA,L_fall,L_add,litter,seeds
       real GDDonset,GDD5,accumulation,storage,stor_use,store
       real RaL,RaS,RaR  !allocation to respiration
       real alpha_L,alpha_W,alpha_R ! allocation ratio to Leaf, stem, and Root
       real RaLeaf,RaStem,RaRoot,Rsoil,Rauto,Rhetero,Rtotal !respirations
       real gpp_yr,NPP_yr,NEE_yr,RaL_yr,RaR_yr,RaS_yr,Rh_yr
       real NPPL_yr,NPPR_yr,NPPS_yr,NPP_L,NPP_R,NPP_W
       real Rootmax,Stemmax,SapS,SapR,StemSap,RootSap
       REAL ws,wdepth
!      climate variables for every day
       real Ta,Tair,Tavg72,Ts
       real doy,hour,Tsoil,Dair,Rh,rain,radsol,rain_t
!      output daily means of driving variables
       real CO2air_d_avg,LWdown_d_avg,SWdown_d_avg,Psurf_d_avg
       real Qair_d_avg,Rain_d_avg,Tair_d_avg,Wind_d_avg
!      the variables that should be initialized in the begining
!      L:leaf,W:wood,R:root,F:fine litter,C:coarse,litter,S:soil
       real Q_root1,Q_root2,Q_root3 ! Q_leaf,Q_root,Q_wood,
       real Q_soil,Q_soil1,Q_soil2,Q_soil3 ! Q_fine,Q_coarse,
       real PlantC
!      output from canopy model
       real TEVAP,AEVAP,evap_yr,transp_yr
       real,dimension(10):: thksl,wupl,evapl,wcl,FRLEN
       real runoff,Trunoff,runoff_yr,rain_yr
       real wsc(10),ws1,ws2,dws,net_dws
       real gc_wengL,gp_wengL,gc_wengD,gp_wengD
       real gcgp_D,gcgp_yr,gcgp
       real Esoil,Hcrop,ecstot,Anet,DEPH2O,Acanop
       real Hcanop,Hcanop_d
       real Raplant,Glmax,Gsmax,Rh_d,ET_d
!      scenario
       real Sc_co2,Sc_T,Sc_prcp,CO2
!      for NACP output
       real tranformer
       real NACP_L,NACP_W,NACP_R,NACP_F
       real NACP_C,NACP_S1,NACP_S2,NACP_S3
       real NACP_GPP,NACP_NPP,NACP_NEE
       real NACP_Ra,NACP_Rh,NACP_Rt   ! check units
       real NACP_ET,NACP_TR,NACP_Run
       real NA_L,NA_W,NA_R,NA_can,NA_BM
       real NA_C,NA_F,NA_Micr,NA_Slow,NA_Pass,NA_S
       real NA_GPP,NA_NPP,NA_NEE
       real NA_Ra,NA_Rh,NA_Rt
       real NA_ET,NA_TR,NA_Run
       real NA_WC_soil,NA_WC_root,NA_wcLayer(10) ! kg/m2
!      NEE observation
       real NEE_annual,Cumol2gram
       real NEE_annual_array(30)
       integer year_array(30),year_obs
!      for loops
       integer jrain,num_gcgp,W_flag(7)
       integer onset,duration,offset,dormancy  !flag of phenological stage
       integer year,yr,days,i,j,k,m,n,irunmean,writer
       integer lines_NEE,yr_NEE
       integer istat1,istat2,istat3,istat4
       integer dtimes,yr_data
       integer num_scen,isite
       integer idoy,ihour,ileaf,num

       character(len=150) climfile,NEE_file,out_yr,out_d
       character(len=150) parafile,logfile       ! parameter file
       character(len=400) Variables,Units       ! head of output files
       character(len=80) commts
!      define input files
!      open input file for getting climate data
       call getarg(1,parafile)
       open(10,file=parafile,status='old',ACTION='read',IOSTAT=istat1)
       if(istat1==0)then
       else
         close(10)
         goto 9999
       endif
!      open input and output files and read in data
       read(10,11)commts
       do isite=1,No_site  ! run model site by site
         read(10,*,IOSTAT=istat1)site,vegtype,climfile,NEE_file,out_d,
     &     lat,longi,wsmax,wsmin,gddonset,LAIMAX,LAIMIN,rdepth,
     &     Rootmax,Stemmax,SapR,SapS,SLA,GLmax,GRmax,Gsmax,
     &     stom_n,a1,Ds0,Vcmx0,extkU,xfang,alpha,co2ca,
     &     tau_L,tau_W,tau_R,
     &     tau_F,tau_C,tau_Micr,tau_Slow,tau_Pass             ! the unit is year
         if(istat1 /= 0)then
           goto 999
         endif
       close(10) ! close the parameter file

       call getarg(2,out_d)
!       print *, out_d

!        the unit of residence time is transformed from yearly to hourly
         tau_L =tau_L *8760.                          
         tau_W =tau_W *8760.
         tau_R =tau_R *8760.
         tau_F =tau_F *8760.
         tau_C =tau_C *8760.
         tau_Micr=tau_Micr*8760.
         tau_Slow=tau_Slow*8760.
         tau_Pass=tau_Pass*8760.
!        growth rates of plant
         GLmax=GLmax/24.
         GRmax=GRmax/24.
         Gsmax=GSmax/24.
! 	   set initial valus by myself
	 dayCount = 1
         nonValidCount=0 
         sumObs=0.0	!for slope
         sumSim=0.0
         sumObsObs=0.0
         sumSimObs=0.0

         co2=co2ca
         site=trim(site)
         vegtype=trim(vegtype)
         climfile=trim(climfile)
         open(11,file=climfile,status='old',
     &     ACTION='read',IOSTAT=istat2)
         if(istat2==0)then
         else
           close(11)
           goto 999
         endif
!        skip 2 lines of input met data file
         read(11,'(a160)') commts
         read(11,'(a160)') commts
11       format(a160)
         m=0  ! to record the lines in a file
         yr_data=0 ! to record years of a dataset
!         print *, "before forcing"
         do    ! read forcing files
           m=m+1
           read(11,*,IOSTAT=istat3)year_data(m),
     &       doy_data(m),hour_data(m),
     &       (input_data(n,m),n=1,iiterms)
           hour_data(m)=hour_data(m)+1
           if(istat3<0)exit
         enddo ! end of reading the forcing file
         close(11)    ! close forcing file
!         print *, "after forcing"
         lines=m-1
         yr_data=(year_data(lines)-year_data(1))+1
         inputstep=hour_data(2)-hour_data(1)
         if (inputstep==1.0)then
         else
           goto 999
         endif


!        open eddy covariance data
         open(12,file=NEE_file,status='old',ACTION='read',
     &     IOSTAT=istat2)
         if(istat2==0)then
           read(12,11) commts
           m=0
           do 
             m=m+1
             read(12,*,IOSTAT=istat3)year_NEE(m),doy_NEE(m),
     &         hour_NEE(m),(reader_NEE(n),n=1,iterms_NEE)
             if(istat3<0)exit
             if(reader_NEE(11)==-999.0)reader_NEE(11)=0
             NEE_obs(m)=reader_NEE(11)*12./1000./1000000.   ! u mol-->kg C m-2 s-1
           enddo
         endif
         lines_NEE=m-1
         yr_NEE=(year_NEE(lines_NEE)-year_NEE(1))+1
         step_NEE=hour_NEE(2)-hour_NEE(1)
         close(12)

         Cumol2gram=3600.*Step_NEE*1000
         NEE_annual=0.0
         m=0
         year_obs=year_NEE(1)
         do i=1,lines_NEE
           if(year_obs.eq.year_NEE(i)) then
             if(NEE_obs(i)<-500.*12./1000./1000000)then
               NEE_obs(i)=0.0
               nonValidCount=nonValidCount+1
             else
               NEE_annual=NEE_annual+NEE_obs(i)*Cumol2gram
             end if
           else
             m=m+1
             NEE_annual_array(m)=NEE_annual
             year_array(m)=year_obs
             NEE_annual=0
             year_obs=year_NEE(i)
             NEE_annual=NEE_annual+NEE_obs(i)*Cumol2gram
           endif
         enddo
!        define head of output
         open(21,file=out_d)
         write(21,'(56(a15,1X))')'year','doy','hour',
     &     'carbon_Leaf','carbon_Wood','carbon_Root','carbon_Flitter',
     &     'carbon_Clitter','SOM_Miro','SOM_SLOW','SOM_Pass',
     &     'carbon_canopy','carbon_biomass','carbon_soil',
     &     'gpp','npp','nee_simulate','nee_observe',
     &     'resp_auto','resp_hetero','resp_tot',
     &     'ET','Transpiration','Runoff','LatentHeat','LAI','RootMoist',
     &     'SoilWater','soilwater_1','soilwater_2','soilwater_3',
     &     'soilwater_4','soilwater_5','soilwater_6','soilwater_7',
     &     'soilwater_8','soilwater_9','soilwater_10',
     &     'satfrac_1','satfrac_2','satfrac_3','satfrac_4','satfrac_5',
     &     'satfrac_6','satfrac_7','satfrac_8','satfrac_9','satfrac_10',
     &     'CO2concentration','AirSpecificHumudity','rain_div_3600',
     &     'scale_sw','TairPlus273_15'

!        ==================================================
!        Initialize parameters and initial state:
!        thickness of every soil layer
         thksl(1)=10.0   ! 10cm
         thksl(2)=10.0   ! 20cm
         thksl(3)=10.0   ! 30cm
         thksl(4)=10.0   ! 40cm
         thksl(5)=10.0   ! 50cm
         thksl(6)=20.0   ! 70cm
         thksl(7)=20.0   ! 90cm
         thksl(8)=20.0   ! 110cm
         thksl(9)=20.0   ! 130cm
         thksl(10)=20.0  ! 150cm
!        ratio of roots in every layer
         FRLEN(1)=0.30
         FRLEN(2)=0.20
         FRLEN(3)=0.15
         FRLEN(4)=0.15
         FRLEN(5)=0.1
         FRLEN(6)=0.05
         FRLEN(7)=0.05
         FRLEN(8)=0.0
         FRLEN(9)=0.0
         FRLEN(10)=0.0
!        initiations for canopy model, including canopy traits variation in a year
      call consts(pi,tauL,rhoL,rhoS,emleaf,emsoil,
     &   Rconst,sigma,cpair,Patm,Trefk,H2OLv0,airMa,H2OMw,chi,Dheat,
     &   wleaf,gsw0,Vcmx0,eJmx0,theta,conKc0,conKo0,Ekc,Eko,o2ci,
     &   Eavm,Edvm,Eajm,Edjm,Entrpy,gam0,gam1,gam2)

         OPEN(110, FILE="initial_opt.txt")
         READ(110,*)PARAMS
         close(110)
!*****************************************************************
!       write(*,*)params

!*****************************************************************

!        initial values of the C pools
         wsmax=PARAMS(1,1)
         wsmin=PARAMS(1,2)
         gddonset=PARAMS(1,3)
         LAIMAX=PARAMS(1,4)
         LAIMIN=PARAMS(1,5)
         rdepth=PARAMS(1,6)
         Rootmax=PARAMS(1,7)
         Stemmax=PARAMS(1,8)
         SapR=PARAMS(1,9)
         SapS=PARAMS(1,10)
         SLA=PARAMS(1,11)
         GLmax=PARAMS(1,12)/24.
         GRmax=PARAMS(1,13)/24.
         Gsmax=PARAMS(1,14)/24.
         a1=PARAMS(1,15)
         Ds0=PARAMS(1,16)
         Vcmx0=PARAMS(1,17)
         alpha=PARAMS(1,18)
         tau_L=PARAMS(1,19)*8760.
         tau_W=PARAMS(1,20)*8760.
         tau_R=PARAMS(1,21)*8760.
         tau_F=PARAMS(1,22)*8760.
         tau_C=PARAMS(1,23)*8760.
         tau_Micr=PARAMS(1,24)*8760.
         tau_Slow=PARAMS(1,25)*8760.
         tau_Pass=PARAMS(1,26)*8760.
         TminV=PARAMS(1,27)
         TmaxV=PARAMS(1,28)
         ToptV=PARAMS(1,29)
         Tcold=PARAMS(1,30)
         Gamma_Wmax=PARAMS(1,31)
         Gamma_Tmax=PARAMS(1,32)

!        soil field capacity and wilting point
         WILTPT=wsmin/100.0
         FILDCP=wsmax/100.0
!        define soil for export variables for satisfying usage of canopy submodel first time
         wscontent=WILTPT
         fwsoil=1.0
         topfws=1.0
         omega=1.0
         do i=1,10
           wcl(i)=FILDCP
         enddo
         Storage=32.09           !g C/m2
         stor_use=Storage/times_storage_use
         onset=0
         duration=0
         offset=0
         dormancy=1 
!        initial values of the C pools
         nsc=85.35
         Q_leaf=230.86
         Q_wood=8996.23
         Q_root1=1001.16
         Q_root2=501.3
         Q_root3=128.57
         Q_coarse=523.57
         Q_fine=192.0
         Q_micr=50.49
         Q_slow=1502.14
         Q_pass=260.43

         LAI=LAIMIN
         bmstem=Q_wood/0.45
         bmroot=(Q_root1+Q_root2+Q_root3)/0.45
         bmleaf=Q_leaf/0.45
         bmplant=bmstem+bmroot+bmleaf

!=============================================================
!        Simulating daily
         writer=yr_data*6  !00 !140*3
         num=0
         m=1
         n=1
         Tavg72=5.0
         neeDif_all=0.0 !add by myself
         do yr=1,writer+yr_data  ! how many years
!           if(year_data(m).eq.1992.OR.year_data(m).eq.1996.OR.
!     &       year_data(m).eq.2000.OR.year_data(m).eq.2004)then
!             idays=366
!           else
!             idays=365
!           endif
           if(mod(year_data(m), 4)==0) then
               if(mod(year_data(m),100)==0) then
                   if(mod(year_data(m),400)==0) then
                       idays=366
                   else
                       idays=365
                   endif
               else
                   idays=366
               endif
           else
               idays=365
           endif

           GDD5=0.0
           onset=0
           gpp_yr=0.0
           NPP_yr=0.0
           Rh_yr =0.0
           NEE_yr=0.0
           neeDif_year=0.0
           do days=1,idays !the days of a year
             StemSap=AMIN1(Stemmax,SapS*bmStem)
             RootSap=AMIN1(Rootmax,SapR*bmRoot)
             NSCmin=5. 
             NSCmax=0.05*(StemSap+RootSap+Q_leaf)
             if(Ta.gt.0.0)GDD5=GDD5+Ta-0.0 !5.0
!            THE FIRST PART:  coupled canopy and soil model
             gpp_t   =0.0   ! daily
             transp_t=0.0   ! daily
             Hcanop_d=0.0   ! daily
             evap_t  =0.0   ! daily
             ta=0.0         ! daily 
             Ts=0.0         ! daily
             rain_t=0.0     ! daily
             Trunoff=0.0    ! daily
             RaL=0.0
             RaS=0.0
             RaR=0.0
             Rauto=0.0
             neeDif_day=0.0 ! add by myself
             neeSim_daily=0.0 ! add by myself
             neeObs_daily=0.0 ! add by myself
             dtimes=24 !how many times a day,24 means every hour
             do i=1,dtimes
!              input data
               if(m > lines)then 
                 m=1
                 n=1
               endif
               year=year_data(m)
               doy=doy_data(m)
               hour =hour_data(m)
               Tair=input_data(1,m)-273.15   ! Atmean2m
               rain=input_data(7,m)*3600.    ! rain
               radsol=input_data(11,m)       ! unit?
               Qair=input_data(3,m)          ! Qair, Near surface specific humidity 
               wind=ABS(input_data(5,m))     ! wind speed
               co2ca=input_data(15,m) *1.0E-6 ! CO2 concentration, should multiply 1.0E-6
               Pa_air=101325.0   !Pa input_data(9,m)/100.*1000.0 ! 
               LWdown=input_data(13,m)
               if(inputstep.eq.1.0)then
                 m=m+1
               else
                 rain=(input_data(7,m)+input_data(7,m+1))*3600.
                 m=m+2
               endif
               n=n+1
201            format(I4,(1x,f4.0),6(1x,f8.4))
               Tsoil=Tair*0.8    ! Stmean
               windU0=Min(1.0,wind) !pre-assumed values
               if(radsol.eq.0.0) radsol=0.01
!              assume values of some variables 
!              standard atmosphere (symbol: atm) is 101.325 kPa.
               eairP=Qair/(Qair+0.62198)*Pa_air         !water vapour pressure,unit: Pa
               Dair=Max(50.01,(esat(Tair)-eairP))       !air water vapour defficit
               RH=eairP/(eairP+Dair)*100.0
               wethr=1
               Rnet=0.8*radsol
               if(radsol.gt.10.0) then
                 G=-25.0
               else
                 G=20.5
               endif
               Esoil=0.05*radsol
               if(radsol.LE.10.0) Esoil=0.5*G
               Hcrop=0.1  ! never used in routine
               Ecstot=0.1 ! never used in routine
               Anet=0.1 ! never used in routine
               DepH2O=0.2
!              for daily mean conditions
               ta= ta + tair/24.0             ! sum of a day, for calculating daily mean temperature
               Ts=Ts+Tsoil/24.0
!              calculating scaling factor of NSC
               if(NSC.le.NSCmin)fnsc=0.0
               if(NSC.ge.NSCmax)fnsc=1.0
               if((NSC.lt.NSCmax).and.(NSC.gt.NSCmin))then 
                 fnsc=(NSC-NSCmin)/(NSCmax-NSCmin)
               endif
               call canopy(gpp,evap,transp,Acanop,Hcanop,   ! outputs
     &           fwsoil,topfws,wscontent,                    ! from soil model
     &           LAI,Sps,
     &           doy,hour,radsol,tair,dair,eairP,            ! from climate data file,including 
     &           windU0,rain,wethr,
     &           Rnet,G,Esoil,Hcrop,Ecstot,Anet,
     &           Tsoil,DepH2O,
     &           wsmax,wsmin,                                !constants specific to soil and plant
     &           lat,co2ca,a1,Ds0,Vcmx0,extkU,xfang,alpha,
     &           stom_n,pi,tauL,rhoL,rhoS,emleaf,emsoil,
     &           Rconst,sigma,cpair,Patm,Trefk,H2OLv0,airMa,
     &           H2OMw,chi,Dheat,wleaf,gsw0,eJmx0,theta,
     &           conKc0,conKo0,Ekc,Eko,o2ci,Eavm,Edvm,Eajm,
     &           Edjm,Entrpy,gam0,gam1,gam2,TminV,TmaxV,ToptV)

               gpp=Amax1(0.0,gpp)
               call respiration(LAIMIN,GPP,Tair,Tsoil,DepH2O,
     &           LAI,SLA,bmstem,bmroot,bmleaf,
     &           StemSap,RootSap,NSC,fnsc,
     &           RaLeaf,RaStem,RaRoot,Rauto)

               call soilwater(wsmax,wsmin,rdepth,FRLEN,!constants specific to soil/plant
     &           rain,tair,transp,wcl,tsoil,Rh,thksl,LAI,   !inputs
     &           evap,runoff,wscontent,fwsoil,topfws,  !outputs
     &           omega,omega_S,WaterR,WaterS,SatFracL)  !outputs
               omega=omega_S
               ET=evap+transp
               NA_WC_soil=wscontent
               NA_WC_root=WaterR
               NA_wcLayer=SatFracL
!              THE Third Part: update LAI
               call plantgrowth(Tavg72,Tavg72,omega,GLmax,GRmax,
     &           GSmax,LAI,LAIMAX,LAIMIN,SLA,Tau_L,
     &           bmleaf,bmroot,bmstem,bmplant,
     &           Rootmax,Stemmax,SapS,SapR,
     &           StemSap,RootSap,Storage,GDD5,
     &           stor_use,onset,accumulation,gddonset,
     &           Sps,NSC,fnsc,NSCmin,NSCmax,
     &           store,add,L_fall,Tcold,Gamma_Wmax,Gamma_Tmax,
     &           NPP,alpha_L,alpha_W,alpha_R)
!              update NSC
               NSC=NSC+GPP-Rauto-(NPP-add)-store

!              THE Fourth PART: simulating C influx allocation in pools
               call TCS(Tair,Tsoil,omega,
     &           NPP,alpha_L,alpha_W,alpha_R,
     &           L_fall,tau_L,tau_W,tau_R,
     &           tau_F,tau_C,tau_Micr,tau_Slow,tau_Pass,
     &           Q_leaf,Q_wood,Q_root,
     &           Q_fine,Q_coarse,Q_Micr,Q_Slow,Q_Pass,
     &           Rh_f,Rh_c,Rh_Micr,Rh_Slow,Rh_Pass)

               Rhetero=Rh_f + Rh_c + Rh_Micr + Rh_Slow + Rh_Pass
               NEE=Rauto+Rhetero - GPP
               Q_soil=Q_Micr + Q_Slow + Q_Pass
               Q_root=Q_root
               bmroot=Q_root/0.45
               bmleaf=Q_leaf/0.45
               bmstem=Q_wood/0.45
               bmplant=bmleaf+bmroot+bmstem
               LAI=bmleaf*SLA
!              output
               if((yr.gt.writer).and.(yr.le.(writer+yr_data)))then
                 NA_L=Q_leaf/1000. ! g C --> kg C
                 NA_W=Q_wood/1000. ! g C --> kg C
                 NA_R=Q_root/1000. ! g C --> kg C
                 NA_F=Q_fine/1000. ! g C --> kg C
                 NA_C=Q_coarse/1000. ! g C --> kg C
                 NA_Micr=Q_Micr/1000. ! g C --> kg C
                 NA_slow=Q_Slow/1000. ! g C --> kg C
                 NA_pass=Q_Pass/1000. ! g C --> kg C
                 NA_can=NA_L+NA_W*0.7
                 NA_BM=NA_L+NA_W+NA_R
                 NA_S=NA_Micr+NA_slow+NA_pass 
                 NA_GPP=GPP/(1000.*3600.) ! g C/m2/h --> kg C/m2/s
                 NA_NPP=NPP/(1000.*3600.) ! g C/m2/h --> kg C/m2/s
                 NA_NEE=NEE/(1000.*3600.) ! g C/m2/h --> kg C/m2/s
                 NA_Ra=Rauto/(1000.*3600.) ! g C/m2/h --> kg C/m2/s
                 NA_Rh=Rhetero/(1000.*3600.) ! g C/m2/h --> kg C/m2/s
                 NA_Rt=NA_Ra+NA_Rh
                 NA_ET=ET            ! mm/m2/h
                 NA_TR=transp
                 NA_Run=runoff
                 Qle=ET*((2.501-0.00236*Tair)*1000000.0)/3600. ! w/m2
                 if(NEE_obs(n)>-500.*12./1000./1000000) then ! add by myself
                   NEE_diff = (NA_NEE-NEE_obs(n))*100000000/12. ! only for visible, add by myself
                 else
                   NEE_diff = 0.0                 
                 endif
                   write(21,121)year,doy,hour,
     &               NA_L,NA_W,NA_R,NA_F,NA_C,
     &               NA_Micr,NA_slow,NA_pass,
     &               NA_can,NA_BM,NA_S,                        
     &               NA_GPP,NA_NPP,NA_NEE,NEE_obs(n),
     &               NA_Ra,NA_Rh,NA_Rt,   ! check units
     &               NA_ET,NA_TR,NA_Run,Qle,
     &               LAI,WaterR,wscontent,
     &               (WaterS(k),k=1,10),(SatFracL(k),k=1,10),
     &               CO2ca,Qair,rain/3600.,radsol,
     &               Tair+273.15            
               endif
!              sums of a day
               gpp_t=gpp_t + gpp*(24./dtimes)
               transp_t=transp_t + transp*(24./dtimes)
               evap_t=evap_t + evap*(24./dtimes)
               Hcanop_d=Hcanop_d+Hcanop/(24./dtimes)
               Trunoff=Trunoff+runoff
!              sum of the whole year
               gpp_yr=gpp_yr+gpp
               NPP_yr=NPP_yr+NPP
               Rh_yr =Rh_yr +Rhetero
               NEE_yr=NEE_yr+NEE
               if((yr.gt.writer).and.(yr.le.(writer+yr_data)))then
                 neeDif_day= neeDif_day + NEE_diff*NEE_diff !add by myself
                 neeSim_daily=neeSim_daily+NA_NEE*1000000000./12. !add by myself
                 neeObs_daily=neeObs_daily+NEE_obs(n)*1000000000./12. !add by myself
               endif
                                   
             enddo              ! end of a day
             if((yr.gt.writer).and.(yr.le.(writer+yr_data)))then
               neeObs_days(dayCount) = neeObs_daily
               neeSim_days(dayCount) = neeSim_daily
               sumObs=sumObs+neeObs_daily
               sumSim=sumSim+neeSim_daily
               sumObsObs=sumObsObs+neeObs_daily*neeObs_daily
               sumSimObs=sumSimObs+neeSim_daily*neeObs_daily
		   dayCount = dayCount + 1
               neeDif_year=neeDif_year + neeDif_day !add by myself
		 endif

             Tavg72=ta
121          format(I6,1X,f15.0,1X,f15.2,1X,120(E15.8,1X))
           enddo                         ! end of a year
           storage=accumulation
           stor_use=Storage/times_storage_use
           accumulation=0.0
           onset=0
           neeDif_all=neeDif_all + neeDif_year !add by myself
         enddo            !end of simulations of a site, multiple years
         close(21)
999      continue
       enddo   ! end of one site

9999   continue
!***************************added by myself*******************************
      paramspec=0.0
      sTotal=0.0
      nValid = lines_NEE-nonValidCount
      varValue = neeDif_all/nValid
      sValid = sqrt(varValue)

!***********************************************************************

       end

!     ******************************************************************
!     ******************************************************************
      subroutine consts(pi,tauL,rhoL,rhoS,emleaf,emsoil,
     &   Rconst,sigma,cpair,Patm,Trefk,H2OLv0,airMa,H2OMw,chi,Dheat,
     &   wleaf,gsw0,Vcmx0,eJmx0,theta,conKc0,conKo0,Ekc,Eko,o2ci,
     &   Eavm,Edvm,Eajm,Edjm,Entrpy,gam0,gam1,gam2)
     
      real tauL(3), rhoL(3), rhoS(3)
      pi = 3.1415926
!     physical constants
      tauL(1)=0.1                  ! leaf transmittance for vis
      rhoL(1)=0.1                  ! leaf reflectance for vis
      rhoS(1)=0.1                  ! soil reflectance for vis
      tauL(2)=0.425                ! for NIR
      rhoL(2)=0.425                ! for NIR
      rhoS(2)=0.3                  ! for NIR - later function of soil water content
      tauL(3)=0.00                 ! for thermal
      rhoL(3)=0.00                 ! for thermal
      rhoS(3)=0.00                 ! for thermal
      emleaf=0.96
      emsoil=0.94
      Rconst=8.314                 ! universal gas constant (J/mol)
      sigma=5.67e-8                ! Steffan Boltzman constant (W/m2/K4)
      cpair=1010.                  ! heat capapcity of air (J/kg/K)
      Patm=1.e5                    ! atmospheric pressure  (Pa)
      Trefk=293.2                  !reference temp K for Kc, Ko, Rd
      H2OLv0=2.501e6               !latent heat H2O (J/kg)
      AirMa=29.e-3                 !mol mass air (kg/mol)
      H2OMw=18.e-3                 !mol mass H2O (kg/mol)
      chi=0.93                     !gbH/gbw
      Dheat=21.5e-6                !molecular diffusivity for heat
!     plant parameters
      gsw0 = 1.0e-2                !g0 for H2O in BWB model
      eJmx0 = Vcmx0*2.7            !@20C Leuning 1996 from Wullschleger (1993)
      theta = 0.9
      wleaf=0.01                   !leaf width (m)

!     thermodynamic parameters for Kc and Ko (Leuning 1990)
      conKc0 = 302.e-6                !mol mol^-1
      conKo0 = 256.e-3                !mol mol^-1
      Ekc = 59430.                    !J mol^-1
      Eko = 36000.                    !J mol^-1
      o2ci= 210.e-3                   !mol mol^-1

!     thermodynamic parameters for Vcmax & Jmax (Eq 9, Harley et al, 1992; #1392)
      Eavm = 116300.               !J/mol  (activation energy)
      Edvm = 202900.               !J/mol  (deactivation energy)
      Eajm = 79500.                !J/mol  (activation energy) 
      Edjm = 201000.               !J/mol  (deactivation energy)
      Entrpy = 650.                !J/mol/K (entropy term, for Jmax & Vcmax)

!     parameters for temperature dependence of gamma* (revised from von Caemmerer et al 1993)
      gam0 = 28.0e-6               !mol mol^-1 @ 20C = 36.9 @ 25C
      gam1 = .0509
      gam2 = .0010
      return
      end

!****************************************************************************
!      a sub-model for calculating C flux and H2O flux of a canopy
!      adapted from a two-leaf canopy model developed by Wang Yingping
       subroutine canopy(gpp,evap,transp,Acanop,Hcanop,   ! outputs
     &   fwsoil,topfws,wscontent,           ! from soil model
     &   LAI,Sps,
     &   doy,hour,radsol,tair,dair,eairP,! from climate data file,including 
     &   windU0,rain,wethr,
     &   Rnet,G,Esoil,Hcrop,Ecstot,Anet,
     &   Tsoil,DepH2O,
     &   wsmax,wsmin,  !constants specific to soil and plant
     &   lat,co2ca,a1,Ds0,Vcmx0,extkU,xfang,alpha,
     &   stom_n,pi,tauL,rhoL,rhoS,emleaf,emsoil,
     &   Rconst,sigma,cpair,Patm,Trefk,H2OLv0,airMa,
     &   H2OMw,chi,Dheat,wleaf,gsw0,eJmx0,theta,
     &   conKc0,conKo0,Ekc,Eko,o2ci,Eavm,Edvm,Eajm,
     &   Edjm,Entrpy,gam0,gam1,gam2,TminV,TmaxV,ToptV)

       real lat
       real gpp,evap,transp,LAI
       real tauL(3),rhoL(3),rhoS(3),reffbm(3),reffdf(3)
       real extkbm(3),extkdm(3)
       real Radabv(2),Qcan(3,2),Qcan0(3)
       real Acan(2),Ecan(2),Hcan(2),Tcan(2), Gbwcan(2), Gswcan(2)
!      extra variables used to run the model for the wagga data
       real topfws        ! from siol subroutine       
       integer idoy,ihour,ileaf
       integer jrain,i,j,k

!      additional arrays to allow output of info for each layer
       real RnStL(5),QcanL(5),RcanL(5),AcanL(5),EcanL(5),HcanL(5),
     &   GbwcL(5),GswcL(5),hG(5),hIL(5)
       real Gaussx(5),Gaussw(5),Gaussw_cum(5)
      
       character*80 commts
!
!      Normalised Gaussian points and weights (Goudriaan & van Laar, 1993, P98)
!      5-point
       data Gaussx/0.0469101,0.2307534,0.5,0.7692465,0.9530899/
       data Gaussw/0.1184635,0.2393144,0.2844444,0.2393144,0.1184635/
       data Gaussw_cum/0.11846,0.35777,0.64222,0.88153,1.0/

!      calculate beam fraction in incoming solar radiation
       call  yrday(doy,hour,lat,radsol,fbeam)
                
!      check if canopy wet (wethr =-1)  - if so skip it
       jrain=int(wethr)
       if(jrain.lt.0) goto 19
       idoy=int(doy)
       hours=idoy*1.0+hour/24.0
       coszen=sinbet(doy,lat,pi,hour)             !cos zenith angle of sun
!      set windspeed to the minimum speed to avoid zero Gb
       if(windU0.lt.0.01) windU0=0.01
!      calculate soil albedo for NIR as a function of soil water (Garratt pp292)
       if(topfws.gt.0.5) then
         rhoS(2)=0.18
       else
         rhoS(2)=0.52-0.68*topfws
       endif
!      assign plant biomass and leaf area index at time t
!      assume leaf biomass = root biomass
       FLAIT =LAI 
       radabv(1)=0.5*radsol                 !(1) - solar radn
       radabv(2)=0.5*radsol                 !(2) - NIR
!        reset variables
       Acanop=0.0
       Ecanop=0.0
       Hcanop=0.0
       fslt=0.0
       fsltx=0.0
!      call multilayer model of Leuning - uses Gaussian integration but radiation scheme
!      is that of Goudriaan

       call xlayers(Sps,Tair,Dair,radabv,G,Esoil,fbeam,eairP,
     &   windU0,co2ca,fwsoil,LAI,coszen,idoy,hours,
     &   tauL,rhoL,rhoS,xfang,extkd,extkU,wleaf,
     &   Rconst,sigma,emleaf,emsoil,theta,a1,Ds0,
     &   cpair,Patm,Trefk,H2OLv0,AirMa,H2OMw,Dheat,
     &   gsw0,alpha,stom_n,
     &   Vcmx0,eJmx0,conKc0,conKo0,Ekc,Eko,o2ci,
     &   Eavm,Edvm,Eajm,Edjm,Entrpy,gam0,gam1,gam2,
     &   extKb,
     &   Rnst1,Qcan1,Acan1,Ecan1,Hcan1,Gbwc1,Gswc1,Tleaf1,
     &   Rnst2,Qcan2,Acan2,Ecan2,Hcan2,Gbwc2,Gswc2,Tleaf2,
     &   Rcan1,Rcan2,Rsoilabs,Hsoil,
     &   RnStL,QcanL,RcanL,AcanL,EcanL,HcanL,GbwcL,GswcL,
     &   TminV,TmaxV,ToptV)

!      convert from LAI to height (m) for IREX (LAI accumulated from bottom up)
       do ng=1,5  
         hG(ng)=Gaussw_cum(ng)                   !normalised heights in weight domain
         hIL(ng)=0.2*ng                          !normalised heights for Inverse Lagrangian analysis
       enddo
           
!      Interpolate between Gaussian distances to those used in Inverse analysis.
!      Note the use of Gaussw_cum. These are the normalised distances on the integration function
!      Integral = sum(Yi*Wgi), where Y is the function and W is the weight.
       AcanL(1)=AcanL(1)+(hIL(1)-hG(1))*(AcanL(2)-AcanL(1))
     &   /(hG(2)-hG(1))
       AcanL(2)=AcanL(2)+(hIL(2)-hG(2))*(AcanL(3)-AcanL(2))
     &   /(hG(3)-hG(2))
       AcanL(3)=AcanL(2)+(hIL(3)-hG(2))*(AcanL(3)-AcanL(2))
     &   /(hG(3)-hG(2))
       AcanL(4)=AcanL(3)+(hIL(4)-hG(3))*(AcanL(4)-AcanL(3))
     &   /(hG(4)-hG(3))
       EcanL(1)=EcanL(1)+(hIL(1)-hG(1))*(EcanL(2)-EcanL(1))
     &   /(hG(2)-hG(1))
       EcanL(2)=EcanL(2)+(hIL(2)-hG(2))*(EcanL(3)-EcanL(2))
     &   /(hG(3)-hG(2))
       EcanL(3)=EcanL(2)+(hIL(3)-hG(2))*(EcanL(3)-EcanL(2))
     &   /(hG(3)-hG(2))
       EcanL(4)=EcanL(3)+(hIL(4)-hG(3))*(EcanL(4)-EcanL(3))
     &   /(hG(4)-hG(3))
       HcanL(1)=HcanL(1)+(hIL(1)-hG(1))*(HcanL(2)-HcanL(1))
     &   /(hG(2)-hG(1))
       HcanL(2)=HcanL(2)+(hIL(2)-hG(2))*(HcanL(3)-HcanL(2))
     &   /(hG(3)-hG(2))
       HcanL(3)=HcanL(2)+(hIL(3)-hG(2))*(HcanL(3)-HcanL(2))
     &   /(hG(3)-hG(2))
       HcanL(4)=HcanL(3)+(hIL(4)-hG(3))*(HcanL(4)-HcanL(3))
     &   /(hG(4)-hG(3))

!        adjust CO2 fluxes for each Layer for soil respiration
!        and adjust LE and H as well
         mol_mass=44./1000.
         do ng=1,5
            EcanL(ng)=EcanL(ng)+Esoil
            HcanL(ng)=HcanL(ng)+Hsoil
          end do

!        fraction sunlit leaves integrated over canopy
         fsltx=(1.0-exp(-LAI*extkb))/(extkb*LAI)  
!        sum sunlit & shaded fluxes, & mean canopy temperature
!        multilayer model 
       Acan1=Acan1*1.0e6                     !umol CO2/m2/s    
       Acan2=Acan2*1.0e6
       Acanop=(Acan1+Acan2)       ! 03/21/2006 Weng 
       Qcan1=Qcan1                           !umol quanta/m2/s
       Qcan2=Qcan2                 
       Qcanop=Qcan1+Qcan2 
       Ecanop=Ecan1+Ecan2                    !W/m2
       Tcanop=Tleaf1*fsltx+Tleaf2*(1.0-fsltx)!correction by ypw(12/9/96)
       Hcanop=Hcan1+Hcan2                    !W/m2
       if(Rsoilabs.LT.0.0) Rsoilabs=0.0
       if(Ecanop.LT.0.0)Ecanop=0.0

       gpp=Acanop*3600.0*12.0/1.0e6          ! every hour
       transp=Ecanop*3600.0/((2.501-0.00236*Tair)*1000000.0)  ! mm H2O /hour
       if(transp.lt.0.0)transp=0.0
       evap=0.9*Rsoilabs*3600.0/2260.0/1000.0     ! EVERY hour
       if(evap.lt.0.0)evap=0.0

19     continue
       return
       end
c============================================================================

       subroutine respiration(LAIMIN,GPP,Tair,Tsoil,DepH2O,
     &   LAI,SLA,bmstem,bmroot,bmleaf,
     &   StemSap,RootSap,NSC,fnsc,
     &   RaLeaf,RaStem,RaRoot,Rauto)
!      calculate plant and soil respiration by the following equation:
!      RD=BM*Rd*Q10**((T-25)/10) (Sun et al. 2005. Acta Ecologica Sinica)
       implicit none
       real LAIMIN,LAI,GPP,SLA
       real Tair,Tsoil,DepH2O
       real bmstem,bmroot,bmleaf,StemSap,RootSap
       real NSC,fnsc
       real Q10
       real RaLeaf,RaStem,RaRoot,Rauto
       real Rl0,Rs0,Rr0
       real c                  ! converter from "umol C /m2/s" to "gC/m2/hour"

       c=3600.*12./1000000.    ! umol C /m2/s--> gC/m2/hour
       Q10=2.0
       if(LAI.gt.LAIMIN) then
         Rl0=3.              ! umolCO2*kg-1*m-2*s-1
         Rs0=1.5
         Rr0=3.
         RaLeaf=Rl0*bmleaf*0.45*SLA*0.1*Q10**((Tair-25.)/10.)*fnsc*c
         RaStem=Rs0*StemSap*0.001 *Q10**((Tair-25.)/10.)*fnsc*c
         RaRoot=Rr0*RootSap*0.001 *Q10**((Tair-25.)/10.)*fnsc*c
       else
         RaLeaf=0.3*GPP
         RaStem=0.3*GPP
         RaRoot=0.4*GPP
       endif
       Rauto=Raleaf+Rastem+Raroot
       if(Rauto > 0.1*NSC)then
         Raleaf=Raleaf/Rauto*0.1*NSC
         Rastem=Rastem/Rauto*0.1*NSC
         Raroot=Rastem/Rauto*0.1*NSC
         Rauto=0.1*NSC
       endif
       return
       end
!=======================================================================
!      subroutine for soil moisture
       subroutine soilwater(wsmax,wsmin,rdepth,FRLEN,!constants specific to soil/plant
     &   rain,tair,transp,wcl,tsoil,Rh,thksl,LAI,       !inputs
     &   evap,runoff,wscontent,fwsoil,topfws,  !outputs
     &   omega,omega_S,WaterR,WaterS,SatFracL)  !outputs
!      All of inputs, the unit of water is 'mm', soil moisture or soil water content is a ratio

       implicit none
!      soil traits
       real wsmax,wsmin,wsmaxL(10),wsminL(10) !from input percent x%
       real FLDCAP,WILTPT,FLDCAPL(10),WILTPTL(10) ! ie. 0.xx
!      plant traits
       real LAI,rdepth
       integer nfr
!      climate conditions
       real precp,rain ! mm/hour
       real tair,TSOIL,ts          ! updated every hour
!      output from canopy model
       real evap,transp,evaptr,TEVAP,AEVAP
!      output variables
       real wscontent,fwsoil,topfws,omega,topomega,omega_S
       real fw(10),ome(10),W_signal
       real WaterR,WaterS(10),SatFracL(10)
!      omega: (wscontent-wiltpt)/(fldcap-wiltpt)
       real RAWCL(10) ! omega of every layers
       real thksl(10),depth(10),wsc(10),WUPL(10),EVAPL(10),SRDT(10)
       real plantup(10)
       real Tsrdt
       real frlen(10) !fraction of root length in every layer
       real wcl(10) !volum ratio
       real fwcln(10) !  fraction of water in layers, like field capacity
       real wtdeficit(10),DWCL(10),Tr_ratio(10)
       real Twater,Twater1,Twater2,Tthk,dWaterS,netflux
       real wtneed,wtadd,twtadd,infilt,runoff,roff_layer,tr_allo

       real RH,Rsoil,Rd,density,sp_heat,psychro,la,P
       real esat
       real exchangeL,supply,demand,omegaL(10)
       integer i,j,k

       WILTPT =wsmin/100.0
       FLDCAP =wsmax/100.0
       WILTPTL=wsmin/100.0
       FLDCAPL=wsmax/100.0

       twater=0.0
       twater1=0.0
       twater2=0.0

       precp=rain

       do i=1,10
         wtdeficit(i)=0.0
         dwcl(i)=0.0
         evapl(i)=0.0
         WUPL(i)=0.0
         SRDT(i)=0.0
         DEPTH(i)=0.0
       enddo

!      C ** Determine which layer has been reached by the root system. 
!      Layer volume (cm3)
       DEPTH(1)=10.0
       DO i=2,10
         DEPTH(i)=DEPTH(i-1)+THKSL(i)
       enddo
       do i=1,10
         IF(rdepth.GT.DEPTH(i)) nfr=i+1
       enddo
       IF (nfr.GT.10) nfr=10
       do i=1,10
         if(FLDCAPL(i).gt.wcl(i))wtdeficit(i)=FLDCAPL(i)-wcl(i)
       enddo

! ***  water infiltration through layers
       infilt=precp  !mm/hour
!      Loop over all soil layers.
       TWTADD=0
       roff_layer=0.0
       do i=1,10
         IF(infilt.GT.0.0)THEN
!          Add water to this layer, pass extra water to the next.
           WTADD=AMIN1(INFILT,wtdeficit(i)*thksl(i)*10.0) ! from cm to mm
!          change water content of this layer
           WCL(i)=(WCL(i)*(thksl(i)*10.0)+WTADD)/(thksl(i)*10.0)
           FWCLN(I)=WCL(I)       !  /VOLUM(I)! update fwcln of this layer
           TWTADD=TWTADD+WTADD       !calculating total added water to soil layers (mm)
           INFILT=INFILT-WTADD !update infilt
         END IF
!        produce runoff during infiltration
         if(infilt.GT.0.0)THEN
           roff_layer=roff_layer + INFILT*0.05*(i-1)
           INFILT=INFILT -  INFILT*0.05*(i-1)
         endif
       enddo

       if(precp.gt.0.0.and.wcl(1).gt.wcl(2))then
         supply=(wcl(1)-wcl(2))/3.0
         wcl(1)=wcl(1)-2.0*supply
         wcl(2)=wcl(2)+supply
       endif

!      runoff
       runoff=INFILT + roff_layer   !precp-TWTADD + roff_layer   !weng 10072006

!      water redistribution among soil layers
       do i=1,10
         wsc(i)=Amax1(0.00,(wcl(i)-wiltpt)*THKSL(i)*10.0)
         omegaL(i)=Amax1(0.001,(wcl(i)-WILTPT)/(FLDCAPL(i)-WILTPT))
       enddo
       supply=0.0
       demand=0.0
       do i=1,9
         if(omegaL(i).gt.0.3)then
           supply=wsc(i)/360.0*omegaL(i)
           demand=(FLDCAPL(i)-wcl(i+1))*THKSL(i+1)*10.0/360.0
     &       *(1.0-omegaL(i+1))
           exchangeL=AMIN1(supply,demand)
           wsc(i)=wsc(i)- exchangeL
           wsc(i+1)=wsc(i+1)+ exchangeL
           wcl(i)=wsc(i)/(THKSL(i)*10.0)+wiltpt
           wcl(i+1)=wsc(i+1)/(THKSL(i+1)*10.0)+wiltpt
         endif
       enddo

!      calculate evap demand by eq.24 of Seller et al. 1996 (demand)

       if(wcl(1).LT.wiltpt)then
         evap=0.0
       else
         Rsoil=10.1*exp(1.0/wcl(1))
         Rd=20.5 !*exp(LAI/1.5)!LAI is added by Weng
         P=101325.0  !Pa, atmospheric pressure
         density=1.204 !kg/m3
         la=(2.501-0.00236*Tair)*1000000.0 !J/kg
         sp_heat=1012.0  !J/kg/K
         psychro=1628.6*P/la

         evap=1.0*esat(tair)*(1.0-RH/100.0)/
     &     (Rsoil+Rd)*density*sp_heat/psychro/la*3600.0
       endif

!      *** Soil evaporation; SRDT(I) for contribution of each layer. 
!      Units here are g H2O m-2 layer-1 h-1.
       Twater=0
       do i=1,10
         wsc(i)=(wcl(i)-wiltpt)*THKSL(I)*10.0
         Twater=Twater+wsc(i)  ! total water in soils,mm
       enddo

       Tsrdt=0.0
       do i=1,10
!        Fraction of SEVAP supplied by each soil layer
         SRDT(I)=EXP(-4.73*(DEPTH(I)-THKSL(I)/2.0)/100.0)/1.987
         Tsrdt=Tsrdt+SRDT(i)/(i*i)  ! to normalize SRDT(i)
       enddo

       do i=1,10
         SRDT(i)=SRDT(i)/Tsrdt
       enddo

       do i=1,10
         EVAPL(I)=Amax1(AMIN1(evap*SRDT(i),wsc(i)),0.0)  !mm
         DWCL(I)=EVAPL(I)/(THKSL(I)*10.0) !ratio
       enddo

!      update water content of every layer
       do i=1,10
         wcl(i)=wcl(i)-DWCL(i)
       enddo
!      the actual evapration
       evap=0.0       
       do i=1,10
         evap=evap+EVAPL(I)
       enddo
!      WATER UPTAKE by plant roots,Weng, 2.13.2006, a passive proccess
       Twater=0
       do i=1,nfr
         wsc(i)=(wcl(i)-wiltpt)*THKSL(I)*10.0
         Twater=Twater+AMAX1(wsc(i),0.0) ! total water in roots reached soil,mm
       enddo
       if(transp.gt.Twater/2.0)transp=Twater/2.0                     
       tr_allo=0.0
       do i=1,nfr
         tr_ratio(i)=FRLEN(i) !*(wcl(i)-wiltpt)) !*THKSL(I))
         tr_allo=tr_allo+tr_ratio(i)
       enddo

       do i=1,nfr
         plantup(i)=AMIN1(transp* tr_ratio(i)/tr_allo, wsc(i)) !mm              
         wupl(i)=plantup(i)/(thksl(i)*10.0)
         wcl(i)=wcl(i)-wupl(i)
       end do

       transp=0.0
       do i=1,nfr
         transp=transp+plantup(i)
       enddo

!      output (fwsoil,topfws,omega) which would be used by canopy model
       Twater=0
       Tthk=0
       do i=1,nfr
         Twater=Twater+wcl(i)*THKSL(I)*10.0 ! total water in soils,mm
         Tthk=Tthk+thksl(i)*10.0 !total thicknes of soil layers, mm
       enddo
       wscontent=Twater/Tthk
       if(wscontent.lt.WILTPT) wscontent=WILTPT+0.00001
       omega_S=(wscontent-WILTPT)/(FLDCAP-WILTPT)
       fwsoil=amin1(1.0,3.333*omega)
       topfws=amin1(1.0,(wcl(1)-WILTPT)/((FLDCAP-WILTPT)))
       if(fwsoil.lt.0.0) fwsoil=0.000001
       if(topfws.lt.0.0) topfws=0.000001
       if(omega.lt.0.0) omega=0.0000001
       Twater=Twater-WILTPT*Tthk
       WaterR=Twater+WILTPT*Tthk
      
!      a new approach for calculating fwsoil
       do i=1,10 !nfr
         ome(i)=(wcl(i)-WILTPT)/(FLDCAP-WILTPT)
         WaterS(i)=wcl(i)*THKSL(I)*10.0
         ome(i)=AMIN1(1.0,AMAX1(0.0,ome(i)))
         SatFracL(i)=ome(i)
         fw(i)=amin1(1.0,3.333*ome(i))
       enddo
       fwsoil=0.0
       omega=0.0
       do i=1,nfr
         fwsoil=fwsoil+fw(i)*frlen(i)
         omega=omega+ome(i)*frlen(i)
       enddo
       return
       end

!=================================================================

!      plant growth model
       subroutine plantgrowth(Tair,Tavg72,omega,GLmax,GRmax,GSmax,
     &   LAI,LAIMAX,LAIMIN,SLA,Tau_L,
     &   bmleaf,bmroot,bmstem,bmplant,
     &   Rootmax,Stemmax,SapS,SapR,
     &   StemSap,RootSap,Storage,GDD5,
     &   stor_use,onset,accumulation,gddonset,
     &   Sps,NSC,fnsc,NSCmin,NSCmax,
     &   store,add,L_fall,Tcold,Gamma_Wmax,Gamma_Tmax,
     &   NPP,alpha_L,alpha_W,alpha_R)
       implicit none
       real NSC,NSCmin,NSCmax,fnsc
       real store,Storage,GDD5,stor_use,accumulation,gddonset
       integer onset,duration,offset,dormancy
       real GLmax,GRmax,GSmax,TauLeaf
       real GrowthP,GrowthL,GrowthR,GrowthS
       real Tair,Tavg72,T72(72)
       real omega,LAI,LAIMAX,LAIMIN,SLA
!      biomass
       real bmleaf,bmroot,bmstem,bmplant,NPP
       real Rootmax,Stemmax,SapS,SapR
       real bmL,bmR,bmP,bmS,StemSap,RootSap
!      scalars
       real St,Sw,Ss,Sn,SL_rs,SR_rs,Slai,Sps
       real RS,RS0,RSw
       real gamma_W,gamma_Wmax,gamma_T,gamma_Tmax,gamma_N
       real beta_T,Tcold,Twarm
       real bW,bT,W
       real L_fall,L_add,add,NL_fall,NL_add,Tau_L
       real alpha_L,alpha_W,alpha_R,alpha_St
       real Twsoil(7),Tavg
       integer i

       bmL=bmleaf
       bmR=bmRoot
       bmS=bmStem
       bmP=bmPlant

       bW=2.0
       bT=2.0

       Twarm=30.0

       RS0=1.0
       RS=bmR/bmL

       if(bmL.lt.NSC/0.333*0.5)bmL=NSC/0.333*0.5
       if(bmR.lt.NSC/0.333*0.5)bmR=NSC/0.333*0.5
       if(bmS.lt.NSC/0.334*0.5)bmS=NSC/0.334*0.5
       StemSap=MIN(Stemmax,SapS*bmS)  ! Weng 12/05/2008
       RootSap=bmR
       if(StemSap.lt.0.001)StemSap=0.001
       if(RootSap.lt.0.001)RootSap=0.001

!      phenology
       if((GDD5.gt.gddonset).and.onset.eq.0.and.storage.gt.stor_use)then
         onset=1
       endif

       if((onset.eq.1).and.(storage.gt.stor_use))then
         if(LAI.lt.LAIMAX)add=stor_use
         storage=storage-add
       else
         add=0.0
         onset=0
       endif

       if(accumulation.lt.(NSCmax+0.005*RootSap))then
         store=0.005*NSC
       else
         store=0.0
       endif
       accumulation=accumulation+store

       Sps=1.0 - fnsc
       sps=AMAX1(0.001,sps)
       St=1./(1.+19.*EXP(-0.2*(Tair)))
       Sw=AMAX1(0.333, 0.333+omega)
       W=AMIN1(1.0,50.*omega)
       Ss=AMIN1(1.0,2.*fnsc)

       SL_rs=RS/(RS+RS0*(1.5-omega))
       SR_rs=(RS0*(1.5-omega))/(RS+RS0*(1.5-omega))
       Slai=amin1(1.0,2.333*(LAIMAX-LAI)/(LAIMAX-LAIMIN))

       GrowthL=GLmax*bmL    *St*Sw*fnsc*SL_rs*Slai*0.45
       GrowthR=GRmax*RootSap*St*Sw*fnsc*SR_rs*0.5 *0.45       
       GrowthS=GSmax*StemSap*St*Sw*fnsc*0.5*0.5 *0.45

       if(GrowthL.LT.0.0)GrowthL=0.0
       if(GrowthR.LT.0.0)GrowthR=0.0
       if(GrowthS.LT.0.0)GrowthS=0.0

       GrowthP=GrowthL + GrowthR + GrowthS
       if(GrowthP.gt.NSC*0.5)then
         GrowthL=0.5*NSC*GrowthL/GrowthP
         GrowthR=0.5*NSC*GrowthR/GrowthP
         GrowthS=0.5*NSC*GrowthS/GrowthP
       endif
       NPP = add + GrowthL + GrowthR + GrowthS
       if(NPP.eq.0.0)then
         alpha_L=0.333
         alpha_W=0.333
         alpha_R=0.333
       else
         alpha_L=(GrowthL+add)/NPP
         alpha_W=GrowthS/NPP
         alpha_R=GrowthR/NPP
       endif
!      Leaf litter C damages to leaves
       if(Tair.gt.(Tcold+10.)) then
         beta_T=1.
       else 
         if(Tair.gt.Tcold)beta_T=(Tair-Tcold)/10.
         if(Tair.LE.Tcold)beta_T=0.
       endif
       if (tau_L < 8760)then
         gamma_W=(1. - W)     **bW * gamma_Wmax
         gamma_T=(1. - beta_T)**bT * gamma_Tmax
         gamma_N=0.0 !1.0/(Tau_L*Sw)
       else
         gamma_W=0.
         gamma_T=0.
         gamma_N=1.0/(Tau_L*Sw)
       endif

       if(LAI < LAIMIN) then
         gamma_W=0.
         gamma_T=0.
         gamma_N=0.
       endif
       L_fall=bmleaf*0.45*AMIN1((gamma_W+gamma_T+gamma_N),0.99)
       return
       end

!===========================================================================
!      carbon transfer according to Xu et al. 2007       
       subroutine TCS(Tair,Tsoil,omega,
     &   NPP,alpha_L,alpha_W,alpha_R,
     &   L_fall,tau_L,tau_W,tau_R,
     &   tau_F,tau_C,tau_Micr,tau_Slow,tau_Pass,
     &   Q_leaf,Q_wood,Q_root,
     &   Q_fine,Q_coarse,Q_Micr,Q_Slow,Q_Pass,
     &   Rh_f,Rh_c,Rh_Micr,Rh_Slow,Rh_Pass)
       implicit none
       real NPP,NPP_L,NPP_W,NPP_R
       real L_fall,L_add,LAI,SLA
       real Tair,Tsoil,omega
!      allocation ratios
       real alpha_L,alpha_W,alpha_R
!      residence time
       real tau_L,tau_W,tau_R
       real tau_F,tau_C,tau_Micr,tau_Slow,tau_Pass
!      pools
       real Q_leaf,Q_wood,Q_root
       real Q_fine,Q_coarse,Q_Micr,Q_Slow,Q_Pass
       real eta ! the fine litter from woody biomass
       real f_F2M,f_C2M,f_C2S,f_M2S,f_M2P,f_S2P,f_S2M,f_P2M
!      the fraction of C-flux which enters the atmosphere from the kth pool
       real f_CO2_fine,f_CO2_coarse,f_CO2_Micr,f_CO2_Slow,f_CO2_Pass
!      the actual turnover time dependented on temperature and soil moisture
       real tau_L_a,tau_W_a,tau_R_a
       real tau_F_a,tau_C_a,tau_Micr_a,tau_Slow_a,tau_Pass_a
!      out flows of the pools
       real Out_leaf,Out_wood,Out_root
       real Out_fine,Out_coarse,Out_Micr,Out_Slow,Out_Pass
!      heterotrophic respiration
       real Rh_f,Rh_c,Rh_Micr,Rh_Slow,Rh_Pass,Q10_h
!      added 6 parameters ! added  by myself
       real TminV,TmaxV,ToptV,Tcold,Gamma_Wmax,Gamma_Tmax
!      the variables relative to soil moisture calcualtion
       real S_omega !  average values of the moisture scaling functions
       real S_t     !  average values of temperature scaling functions
       real Ta,Ts   !  soil temperature
       real S_w_min    ! minimum decomposition rate at zero plant available water
       real Tref,T0,T,E0,mid
       integer i,j,k,n,m
       integer day,week,month,year

!      calculating soil scaling factors, S_omega and S_tmperature
       S_w_min=0.5 !minimum decomposition rate at zero soil moisture
       S_omega=S_w_min + (1.-S_w_min)*amin1(1.0,2.0*omega)
       S_t=1.5-1./(1.+19.*exp(-0.15*(Tsoil-15.0)))

!      calculating NPP allocation and changes of each C pool
       NPP_L=alpha_L*NPP            ! NPP allocation
       NPP_W=alpha_W*NPP
       NPP_R=alpha_R*NPP

!      new 10-07-2009 weng
       Q10_h=2.2
       S_t=Q10_h**((Tsoil-25.)*0.1)
       Out_leaf=L_fall
       Out_wood=Q_wood/tau_W    * S_T*S_omega
       Out_root=Q_root/tau_R    * S_T*S_omega
       Out_fine=Q_fine/tau_F    * S_T*S_omega
       Out_coarse=Q_coarse/tau_C* S_T*S_omega
       Out_Micr=Q_micr/tau_Micr * S_T*S_omega
       Out_Slow=Q_Slow/tau_Slow * S_T*S_omega
       Out_Pass=Q_Pass/tau_Pas s* S_T*S_omega

!      partitioning coefficients
       eta=0.15 ! 15% of woody litter is fine       
       f_F2M=0.45
       f_C2M=0.275
       f_C2S=0.275
       f_M2S=0.296
       f_M2P=0.002
       f_S2P=0.015
       f_S2M=0.42
       f_P2M=0.45
!      updata plant carbon pools
       Q_leaf  =Q_leaf - Out_leaf + NPP_L    ! daily change of each pool size
       Q_wood  =Q_wood - Out_wood + NPP_W
       Q_root  =Q_root - Out_root + NPP_R

       Q_fine  =Q_fine - Out_fine + Out_leaf + eta*Out_wood + Out_root
       Q_coarse=Q_coarse - Out_coarse + (1.-eta)*Out_wood
       Q_Micr = Q_Micr - Out_Micr
     &   + f_F2M*Out_fine+f_C2M*Out_coarse
     &   + f_S2M*Out_Slow+f_P2M*Out_Pass
       Q_Slow = Q_Slow - Out_Slow
     &   + f_C2S*Out_coarse + f_M2S*Out_Micr
       Q_Pass = Q_Pass - Out_Pass
     &   + f_M2P*Out_Micr + f_S2P*Out_Slow
!      heterotrophic respiration from each pool
       Rh_f =  Out_fine   * (1. - f_F2M)
       Rh_c =  Out_coarse * (1. - f_C2M - f_C2S)
       Rh_Micr=Out_Micr   * (1. - f_M2S - f_M2P)
       Rh_Slow=Out_Slow   * (1. - f_S2P - f_S2M)
       Rh_Pass=Out_Pass   * (1. - f_P2M)

       return
       end
!=================================================================================================
!      subroutines used by canopy submodel
       subroutine xlayers(Sps,Tair,Dair,radabv,G,Esoil,fbeam,eairP,
     &   windU0,co2ca,fwsoil,FLAIT,coszen,idoy,hours,
     &   tauL,rhoL,rhoS,xfang,extkd,extkU,wleaf,
     &   Rconst,sigma,emleaf,emsoil,theta,a1,Ds0,
     &   cpair,Patm,Trefk,H2OLv0,AirMa,H2OMw,Dheat,
     &   gsw0,alpha,stom_n,
     &   Vcmx0,eJmx0,conKc0,conKo0,Ekc,Eko,o2ci,
     &   Eavm,Edvm,Eajm,Edjm,Entrpy,gam0,gam1,gam2,
     &   extKb,
     &   Rnst1,Qcan1,Acan1,Ecan1,Hcan1,Gbwc1,Gswc1,Tleaf1,
     &   Rnst2,Qcan2,Acan2,Ecan2,Hcan2,Gbwc2,Gswc2,Tleaf2,
     &   Rcan1,Rcan2,Rsoilabs,Hsoil,
     &   RnStL,QcanL,RcanL,AcanL,EcanL,HcanL,GbwcL,GswcL,
     &   TminV,TmaxV,ToptV)


!      the multi-layered canopy model developed by 
!      Ray Leuning with the new radiative transfer scheme   
!      implemented by Y.P. Wang (from Sellers 1986)
!      12/Sept/96 (YPW) correction for mean surface temperature of sunlit
!      and shaded leaves
!      Tleaf,i=sum{Tleaf,i(n)*fslt*Gaussw(n)}/sum{fslt*Gaussw(n)} 
!    
       real Gaussx(5),Gaussw(5)
       real layer1(5),layer2(5)
       real tauL(3),rhoL(3),rhoS(3),Qabs(3,2),Radabv(2),Rnstar(2)
       real Aleaf(2),Eleaf(2),Hleaf(2),Tleaf(2),co2ci(2)
       real gbleaf(2),gsleaf(2),QSabs(3,2),Qasoil(2)
       integer ng,nw
       real rhoc(3,2),reff(3,2),kpr(3,2),scatt(2)       !Goudriaan

!      additional arrays to allow output of info for each Layer
       real RnStL(5),QcanL(5),RcanL(5),AcanL(5),EcanL(5),HcanL(5),
     &   GbwcL(5),GswcL(5)
      
!      Normalised Gaussian points and weights (Goudriaan & van Laar, 1993, P98)
!      * 5-point
       data Gaussx/0.0469101,0.2307534,0.5,0.7692465,0.9530899/
       data Gaussw/0.1184635,0.2393144,0.2844444,0.2393144,0.1184635/

!      reset the vairables
       Rnst1=0.0        !net rad, sunlit
       Rnst2=0.0        !net rad, shaded
       Qcan1=0.0        !vis rad
       Qcan2=0.0
       Rcan1=0.0        !NIR rad
       Rcan2=0.0
       Acan1=0.0        !CO2
       Acan2=0.0
       Ecan1=0.0        !Evap
       Ecan2=0.0
       Hcan1=0.0        !Sens heat
       Hcan2=0.0
       Gbwc1=0.0        !Boundary layer conductance
       Gbwc2=0.0
       Gswc1=0.0        !Canopy conductance
       Gswc2=0.0
       Tleaf1=0.0       !Leaf Temp
       Tleaf2=0.0  
  
!      aerodynamic resistance                                                
       raero=50./windU0                           

!      Ross-Goudriaan function for G(u) (see Sellers 1985, Eq 13)
       xphi1 = 0.5 - 0.633*xfang -0.33*xfang*xfang
       xphi2 = 0.877 * (1.0 - 2.0*xphi1)
       funG=xphi1 + xphi2*coszen                             !G-function: Projection of unit leaf area in direction of beam
      
       if(coszen.gt.0) then                                  !check if day or night
         extKb=funG/coszen                                   !beam extinction coeff - black leaves
       else
         extKb=100.
       end if

!      Goudriaan theory as used in Leuning et al 1995 (Eq Nos from Goudriaan & van Laar, 1994)
!      Effective extinction coefficient for diffuse radiation Goudriaan & van Laar Eq 6.6)

       pi180=3.1416/180.
       cozen15=cos(pi180*15)
       cozen45=cos(pi180*45)
       cozen75=cos(pi180*75)
       xK15=xphi1/cozen15+xphi2
       xK45=xphi1/cozen45+xphi2
       xK75=xphi1/cozen75+xphi2
       transd=0.308*exp(-xK15*FLAIT)+0.514*exp(-xK45*FLAIT)+
     &   0.178*exp(-xK75*FLAIT)
       extkd=(-1./FLAIT)*alog(transd)
       extkn=extkd             !N distribution coeff 



!      canopy reflection coefficients (Array indices: first;  1=VIS,  2=NIR
!      second; 1=beam, 2=diffuse
       do nw=1,2              !nw:1=VIS, 2=NIR
       scatt(nw)=tauL(nw)+rhoL(nw)                      !scattering coeff
       if((1.-scatt(nw))<0.0)scatt(nw)=0.9999           ! Weng 10/31/2008
       kpr(nw,1)=extKb*sqrt(1.-scatt(nw))               !modified k beam scattered (6.20)
       kpr(nw,2)=extkd*sqrt(1.-scatt(nw))             !modified k diffuse (6.20)
       rhoch=(1.-sqrt(1.-scatt(nw)))/(1.+sqrt(1.-scatt(nw)))            !canopy reflection black horizontal leaves (6.19)
       rhoc15=2.*xK15*rhoch/(xK15+extkd)                                !canopy reflection (6.21) diffuse
       rhoc45=2.*xK45*rhoch/(xK45+extkd)
       rhoc75=2.*xK75*rhoch/(xK75+extkd)
       rhoc(nw,2)=0.308*rhoc15+0.514*rhoc45+0.178*rhoc75
       rhoc(nw,1)=2.*extKb/(extKb+extkd)*rhoch                          !canopy reflection (6.21) beam 
       reff(nw,1)=rhoc(nw,1)+(rhoS(nw)-rhoc(nw,1))                      !effective canopy-soil reflection coeff - beam (6.27)
     &   *exp(-2.*kpr(nw,1)*FLAIT) 
       reff(nw,2)=rhoc(nw,2)+(rhoS(nw)-rhoc(nw,2))                      !effective canopy-soil reflection coeff - diffuse (6.27)
     &   *exp(-2.*kpr(nw,2)*FLAIT)  
       enddo


!      isothermal net radiation & radiation conductance at canopy top - needed to calc emair
       call Radiso(flait,flait,Qabs,extkd,Tair,eairP,cpair,Patm,
     &   fbeam,airMa,Rconst,sigma,emleaf,emsoil,
     &   emair,Rnstar,grdn)

       TairK=Tair+273.2

!      below      
       do ng=1,5
         flai=gaussx(ng)*FLAIT
!        radiation absorption for visible and near infra-red
         call goudriaan(FLAI,coszen,radabv,fbeam,reff,kpr,
     &     scatt,xfang,Qabs) 
!        isothermal net radiation & radiation conductance at canopy top
         call Radiso(flai,flait,Qabs,extkd,Tair,eairP,cpair,Patm,
     &     fbeam,airMa,Rconst,sigma,emleaf,emsoil,
     &     emair,Rnstar,grdn)
         windUx=windU0*exp(-extkU*flai)             !windspeed at depth xi
         scalex=exp(-extkn*flai)                    !scale Vcmx0 & Jmax0
         Vcmxx=Vcmx0*scalex
         eJmxx=eJmx0*scalex
         if(radabv(1).ge.10.0) then                          !check solar Radiation > 10 W/m2
!          leaf stomata-photosynthesis-transpiration model - daytime
           call agsean_day(Sps,Qabs,Rnstar,grdn,windUx,Tair,Dair,
     &       co2ca,wleaf,raero,theta,a1,Ds0,fwsoil,idoy,hours,
     &       Rconst,cpair,Patm,Trefk,H2OLv0,AirMa,H2OMw,Dheat,
     &       gsw0,alpha,stom_n,
     &       Vcmxx,eJmxx,conKc0,conKo0,Ekc,Eko,o2ci,
     &       Eavm,Edvm,Eajm,Edjm,Entrpy,gam0,gam1,gam2,
     &       Aleaf,Eleaf,Hleaf,Tleaf,gbleaf,gsleaf,co2ci,
     &       TminV,TmaxV,ToptV)
         else
           call agsean_ngt(Sps,Qabs,Rnstar,grdn,windUx,Tair,Dair,
     &       co2ca,wleaf,raero,theta,a1,Ds0,fwsoil,idoy,hours,
     &       Rconst,cpair,Patm,Trefk,H2OLv0,AirMa,H2OMw,Dheat,
     &       gsw0,alpha,stom_n,
     &       Vcmxx,eJmxx,conKc0,conKo0,Ekc,Eko,o2ci,
     &       Eavm,Edvm,Eajm,Edjm,Entrpy,gam0,gam1,gam2,
     &       Aleaf,Eleaf,Hleaf,Tleaf,gbleaf,gsleaf,co2ci)
         endif  
         fslt=exp(-extKb*flai)                        !fraction of sunlit leaves
         fshd=1.0-fslt                                !fraction of shaded leaves
         Rnst1=Rnst1+fslt*Rnstar(1)*Gaussw(ng)*FLAIT  !Isothermal net rad`
         Rnst2=Rnst2+fshd*Rnstar(2)*Gaussw(ng)*FLAIT
         RnstL(ng)=Rnst1+Rnst2
!
         Qcan1=Qcan1+fslt*Qabs(1,1)*Gaussw(ng)*FLAIT  !visible
         Qcan2=Qcan2+fshd*Qabs(1,2)*Gaussw(ng)*FLAIT
         QcanL(ng)=Qcan1+Qcan2
!
         Rcan1=Rcan1+fslt*Qabs(2,1)*Gaussw(ng)*FLAIT  !NIR
         Rcan2=Rcan2+fshd*Qabs(2,2)*Gaussw(ng)*FLAIT
         RcanL(ng)=Rcan1+Rcan2
!
         if(Aleaf(1).lt.0.0)Aleaf(1)=0.0      !Weng 2/16/2006
         if(Aleaf(2).lt.0.0)Aleaf(2)=0.0      !Weng 2/16/2006

         Acan1=Acan1+fslt*Aleaf(1)*Gaussw(ng)*FLAIT*stom_n    !amphi/hypostomatous
         Acan2=Acan2+fshd*Aleaf(2)*Gaussw(ng)*FLAIT*stom_n
         AcanL(ng)=Acan1+Acan2

         layer1(ng)=Aleaf(1)
         layer2(ng)=Aleaf(2)

         Ecan1=Ecan1+fslt*Eleaf(1)*Gaussw(ng)*FLAIT
         Ecan2=Ecan2+fshd*Eleaf(2)*Gaussw(ng)*FLAIT
         EcanL(ng)=Ecan1+Ecan2
!
         Hcan1=Hcan1+fslt*Hleaf(1)*Gaussw(ng)*FLAIT
         Hcan2=Hcan2+fshd*Hleaf(2)*Gaussw(ng)*FLAIT
         HcanL(ng)=Hcan1+Hcan2
!
         Gbwc1=Gbwc1+fslt*gbleaf(1)*Gaussw(ng)*FLAIT*stom_n
         Gbwc2=Gbwc2+fshd*gbleaf(2)*Gaussw(ng)*FLAIT*stom_n
!
         Gswc1=Gswc1+fslt*gsleaf(1)*Gaussw(ng)*FLAIT*stom_n
         Gswc2=Gswc2+fshd*gsleaf(2)*Gaussw(ng)*FLAIT*stom_n
!
         Tleaf1=Tleaf1+fslt*Tleaf(1)*Gaussw(ng)*FLAIT
         Tleaf2=Tleaf2+fshd*Tleaf(2)*Gaussw(ng)*FLAIT

200      continue
       enddo

       FLAIT1=(1.0-exp(-extKb*FLAIT))/extkb
       Tleaf1=Tleaf1/FLAIT1
       Tleaf2=Tleaf2/(FLAIT-FLAIT1)

!      Radiation absorbed by soil
       Rsoilab1=fbeam*(1.-reff(1,1))*exp(-kpr(1,1)*FLAIT)
     &   +(1.-fbeam)*(1.-reff(1,2))*exp(-kpr(1,2)*FLAIT)          !visible
       Rsoilab2=fbeam*(1.-reff(2,1))*exp(-kpr(2,1)*FLAIT)
     &   +(1.-fbeam)*(1.-reff(2,2))*exp(-kpr(2,2)*FLAIT)          !NIR
       Rsoilab1=Rsoilab1*Radabv(1)
       Rsoilab2=Rsoilab2*Radabv(2)
!  
       Tlk1=Tleaf1+273.2
       Tlk2=Tleaf2+273.2
       QLair=emair*sigma*(TairK**4)*exp(-extkd*FLAIT)
       QLleaf=emleaf*sigma*(Tlk1**4)*exp(-extkb*FLAIT)
     &   +emleaf*sigma*(Tlk2**4)*(1.0-exp(-extkb*FLAIT))
       QLleaf=QLleaf*(1.0-exp(-extkd*FLAIT)) 
       QLsoil=emsoil*sigma*(TairK**4)
       Rsoilab3=(QLair+QLleaf)*(1.0-rhoS(3))-QLsoil

!      Net radiation absorbed by soil
!      the old version of net long-wave radiation absorbed by soils 
!      (with isothermal assumption)

!      Total radiation absorbed by soil    
       Rsoilabs=Rsoilab1+Rsoilab2+Rsoilab3 
!      sensible heat flux into air from soil

!      special for IREX
       Esoil=0.9*(Rsoilabs-G)
       Hsoil=0.1*(Rsoilabs-G)

       return
       end 

!     ****************************************************************************
       subroutine goudriaan(FLAI,coszen,radabv,fbeam,reff,kpr,
     &   scatt,xfang,Qabs)
     
!      for spheric leaf angle distribution only
!      compute within canopy radiation (PAR and near infra-red bands)
!      using two-stream approximation (Goudriaan & vanLaar 1994)
!      tauL: leaf transmittance
!      rhoL: leaf reflectance
!      rhoS: soil reflectance
!      sfang XiL function of Ross (1975) - allows for departure from spherical LAD
!        (-1 vertical, +1 horizontal leaves, 0 spherical)
!      FLAI: canopy leaf area index
!      funG: Ross' G function
!      scatB: upscatter parameter for direct beam
!      scatD: upscatter parameter for diffuse
!      albedo: single scattering albedo
!      output:
!      Qabs(nwave,type), nwave=1 for visible; =2 for NIR,
!      type=1 for sunlit;   =2 for shaded (W/m2)

       real radabv(2)
       real Qabs(3,2),reff(3,2),kpr(3,2),scatt(2)
       xu=coszen                                         !cos zenith angle
      
!      Ross-Goudriaan function for G(u) (see Sellers 1985, Eq 13)
       xphi1 = 0.5 - 0.633*xfang -0.33*xfang*xfang
       xphi2 = 0.877 * (1.0 - 2.0*xphi1)
       funG=xphi1 + xphi2*xu                             !G-function: Projection of unit leaf area in direction of beam
      
       if(coszen.gt.0) then                                  !check if day or night
         extKb=funG/coszen                                   !beam extinction coeff - black leaves
       else
         extKb=100.
       end if
                       
!      Goudriaan theory as used in Leuning et al 1995 (Eq Nos from Goudriaan & van Laar, 1994)
       do nw=1,2
         Qd0=(1.-fbeam)*radabv(nw)                                          !diffuse incident radiation
         Qb0=fbeam*radabv(nw)                                               !beam incident radiation
         Qabs(nw,2)=Qd0*(kpr(nw,2)*(1.-reff(nw,2))*exp(-kpr(nw,2)*	    !absorbed radiation - shaded leaves, diffuse
     &     FLAI))+Qb0*(kpr(nw,1)*(1.-reff(nw,1))*exp(-kpr(nw,1)*FLAI)-      !beam scattered
     &     extKb*(1.-scatt(nw))*exp(-extKb*FLAI))
         Qabs(nw,1)=Qabs(nw,2)+extKb*Qb0*(1.-scatt(nw))                     !absorbed radiation - sunlit leaves 
       end do
       return
       end

!****************************************************************************
       subroutine Radiso(flai,flait,Qabs,extkd,Tair,eairP,cpair,Patm,
     &   fbeam,airMa,Rconst,sigma,emleaf,emsoil,
     &   emair,Rnstar,grdn)
!      output
!      Rnstar(type): type=1 for sunlit; =2 for shaded leaves (W/m2)
!      23 Dec 1994
!      calculates isothermal net radiation for sunlit and shaded leaves under clear skies
       real Rnstar(2)
       real Qabs(3,2)
       TairK=Tair+273.2

!      thermodynamic properties of air
       rhocp=cpair*Patm*airMa/(Rconst*TairK)   !volumetric heat capacity (J/m3/K)

!      apparent atmospheric emissivity for clear skies (Brutsaert, 1975)
       emsky=0.642*(eairP/Tairk)**(1./7)       !note eair in Pa
     
!      apparent emissivity from clouds (Kimball et al 1982)
       ep8z=0.24+2.98e-12*eairP*eairP*exp(3000/TairK)
       tau8=amin1(1.0,1.0-ep8z*(1.4-0.4*ep8z))            !ensure tau8<1
       emcloud=0.36*tau8*(1.-fbeam)*(1-10./TairK)**4      !10 from Tcloud = Tair-10

!      apparent emissivity from sky plus clouds      
!      emair=emsky+emcloud
!      20/06/96
       emair=emsky

       if(emair.gt.1.0) emair=1.0
      
!      net isothermal outgoing longwave radiation per unit leaf area at canopy
!      top & thin layer at flai (Note Rn* = Sn + Bn is used rather than Rn* = Sn - Bn in Leuning et al 1985)
       Bn0=sigma*(TairK**4.)
       Bnxi=Bn0*extkd*(exp(-extkd*flai)*(emair-emleaf)
     &   + exp(-extkd*(flait-flai))*(emsoil-emleaf))
!      isothermal net radiation per unit leaf area for thin layer of sunlit and
!      shaded leaves
       Rnstar(1)=Qabs(1,1)+Qabs(2,1)+Bnxi
       Rnstar(2)=Qabs(1,2)+Qabs(2,2)+Bnxi
!      radiation conductance (m/s) @ flai
       grdn=4.*sigma*(TairK**3.)*extkd*emleaf*
     &   *(exp(-extkd*flai)+exp(-extkd*(flait-flai)))
     &   /rhocp
       return
       end
!     ****************************************************************************
       subroutine agsean_day(Sps,Qabs,Rnstar,grdn,windUx,Tair,Dair,
     &   co2ca,wleaf,raero,theta,a1,Ds0,fwsoil,idoy,hours,
     &   Rconst,cpair,Patm,Trefk,H2OLv0,AirMa,H2OMw,Dheat,
     &   gsw0,alpha,stom_n,
     &   Vcmxx,eJmxx,conKc0,conKo0,Ekc,Eko,o2ci,
     &   Eavm,Edvm,Eajm,Edjm,Entrpy,gam0,gam1,gam2,
     &   Aleaf,Eleaf,Hleaf,Tleaf,gbleaf,gsleaf,co2ci,
     &   TminV,TmaxV,ToptV)

       integer kr1,ileaf
       real Aleaf(2),Eleaf(2),Hleaf(2),Tleaf(2),co2ci(2)
       real gbleaf(2), gsleaf(2)
       real Qabs(3,2),Rnstar(2)
!      thermodynami!parameters for air
       TairK=Tair+273.2
       rhocp=cpair*Patm*AirMa/(Rconst*TairK)
       H2OLv=H2oLv0-2.365e3*Tair
       slope=(esat(Tair+0.1)-esat(Tair))/0.1
       psyc=Patm*cpair*AirMa/(H2OLv*H2OMw)
       Cmolar=Patm/(Rconst*TairK)
       weighJ=1.0
!      boundary layer conductance for heat - single sided, forced convection
!      (Monteith 1973, P106 & notes dated 23/12/94)
       if(windUx/wleaf>=0.0)then
         gbHu=0.003*sqrt(windUx/wleaf)    !m/s
       else
         gbHu=0.003 !*sqrt(-windUx/wleaf)
       endif         ! Weng 10/31/2008
       do ileaf=1,2              ! loop over sunlit and shaded leaves
!        first estimate of leaf temperature - assume air temp
         Tleaf(ileaf)=Tair
         Tlk=Tleaf(ileaf)+273.2    !Tleaf to deg K
!        first estimate of deficit at leaf surface - assume Da
         Dleaf=Dair                !Pa
!        first estimate for co2cs
         co2cs=co2ca               !mol/mol
         Qapar = (4.6e-6)*Qabs(1,ileaf)
!    ********************************************************************
         kr1=0                     !iteration counter for LE
!        return point for evaporation iteration
         do               !iteration for leaf temperature
!          single-sided boundary layer conductance - free convection (see notes 23/12/94)
           Gras=1.595e8*abs(Tleaf(ileaf)-Tair)*(wleaf**3.)     !Grashof
           gbHf=0.5*Dheat*(Gras**0.25)/wleaf
           gbH=gbHu+gbHf                         !m/s
           rbH=1./gbH                            !b/l resistance to heat transfer
           rbw=0.93*rbH                          !b/l resistance to water vapour
!          Y factor for leaf: stom_n = 1.0 for hypostomatous leaf;  stom_n = 2.0 for amphistomatous leaf
           rbH_L=rbH*stom_n/2.                   !final b/l resistance for heat  
           rrdn=1./grdn
           Y=1./(1.+ (rbH_L+raero)/rrdn)
!          boundary layer conductance for CO2 - single side only (mol/m2/s)
           gbc=Cmolar*gbH/1.32            !mol/m2/s
           gsc0=gsw0/1.57                 !convert conductance for H2O to that for CO2
           varQc=0.0
           weighR=1.0
           call photosyn(Sps,CO2Ca,CO2Csx,Dleaf,Tlk,Qapar,Gbc, !Qaparx<-Qapar,Gbcx<-Gsc0
     &       theta,a1,Ds0,fwsoil,varQc,weighR,
     &       gsc0,alpha,Vcmxx,eJmxx,weighJ,
     &       conKc0,conKo0,Ekc,Eko,o2ci,Rconst,Trefk,
     &       Eavm,Edvm,Eajm,Edjm,Entrpy,gam0,gam1,gam2,
     &       Aleafx,Gscx,TminV,TmaxV,ToptV)  !outputs
!          choose smaller of Ac, Aq
           Aleaf(ileaf) = Aleafx      !0.7 Weng 3/22/2006          !mol CO2/m2/s
!          calculate new values for gsc, cs (Lohammer model)
           co2cs = co2ca-Aleaf(ileaf)/gbc
           co2Ci(ileaf) = co2cs-Aleaf(ileaf)/gsc0
!          scale variables
           gsw=gsc0*1.56       !gsw in mol/m2/s, oreginal:gsw=gscx*1.56,Weng20090226
           gswv=gsw/Cmolar                           !gsw in m/s
           rswv=1./gswv
!          calculate evap'n using combination equation with current estimate of gsw
           Eleaf(ileaf)=9.0*
     &     (slope*Y*Rnstar(ileaf)+rhocp*Dair/(rbH_L+raero))/    !2* Weng 0215, transpiration 
     &     (slope*Y+psyc*(rswv+rbw+raero)/(rbH_L+raero))
!          calculate sensible heat flux
           Hleaf(ileaf)=Y*(Rnstar(ileaf)-Eleaf(ileaf))
!          calculate new leaf temperature (K)
           Tlk1=273.2+Tair+Hleaf(ileaf)*(rbH/2.+raero)/rhocp
!          calculate Dleaf use LE=(rhocp/psyc)*gsw*Ds
           Dleaf=psyc*Eleaf(ileaf)/(rhocp*gswv)
           gbleaf(ileaf)=gbc*1.32*1.075
           gsleaf(ileaf)=gsw
!          compare current and previous leaf temperatures
           if(abs(Tlk1-Tlk).le.0.1) exit ! original is 0.05 C Weng 10/31/2008
!          update leaf temperature  ! leaf temperature calculation has many problems! Weng 10/31/2008
           Tlk=Tlk1
           Tleaf(ileaf)=Tlk1-273.2
           kr1=kr1+1
           if(kr1 > 500)then
             Tlk=TairK
             exit
           endif
           if(Tlk < 200.)then
             Tlk=TairK
             exit 
           endif                     ! Weng 10/31/2008
         enddo
       enddo
       return
       end
!     ****************************************************************************
       subroutine agsean_ngt(Sps,Qabs,Rnstar,grdn,windUx,Tair,Dair,
     &   co2ca,wleaf,raero,theta,a1,Ds0,fwsoil,idoy,hours,
     &   Rconst,cpair,Patm,Trefk,H2OLv0,AirMa,H2OMw,Dheat,
     &   gsw0,alpha,stom_n,
     &   Vcmxx,eJmxx,conKc0,conKo0,Ekc,Eko,o2ci,
     &   Eavm,Edvm,Eajm,Edjm,Entrpy,gam0,gam1,gam2,
     &   Aleaf,Eleaf,Hleaf,Tleaf,gbleaf,gsleaf,co2ci)
       integer kr1,ileaf
       real Aleaf(2),Eleaf(2),Hleaf(2),Tleaf(2),co2ci(2)
       real gbleaf(2), gsleaf(2)
       real Qabs(3,2),Rnstar(2)
!      thermodynamic parameters for air
       TairK=Tair+273.2
       rhocp=cpair*Patm*AirMa/(Rconst*TairK)
       H2OLv=H2oLv0-2.365e3*Tair
       slope=(esat(Tair+0.1)-esat(Tair))/0.1
       psyc=Patm*cpair*AirMa/(H2OLv*H2OMw)
       Cmolar=Patm/(Rconst*TairK)
       weighJ=1.0

!      boundary layer conductance for heat - single sided, forced convection
!      (Monteith 1973, P106 & notes dated 23/12/94)
       gbHu=0.003*sqrt(windUx/wleaf)    !m/s

       do ileaf=1,2                  ! loop over sunlit and shaded leaves
!        first estimate of leaf temperature - assume air temp
         Tleaf(ileaf)=Tair
         Tlk=Tleaf(ileaf)+273.2    !Tleaf to deg K
!        first estimate of deficit at leaf surface - assume Da
         Dleaf=Dair                !Pa
!        first estimate for co2cs
         co2cs=co2ca               !mol/mol
         Qapar = (4.6e-6)*Qabs(1,ileaf)
!        ********************************************************************
         kr1=0                     !iteration counter for LE
         do
!          single-sided boundary layer conductance - free convection (see notes 23/12/94)
           Gras=1.595e8*abs(Tleaf(ileaf)-Tair)*(wleaf**3)     !Grashof
           gbHf=0.5*Dheat*(Gras**0.25)/wleaf
           gbH=gbHu+gbHf                         !m/s
           rbH=1./gbH                            !b/l resistance to heat transfer
           rbw=0.93*rbH                          !b/l resistance to water vapour
!          Y factor for leaf: stom_n = 1.0 for hypostomatous leaf;  stom_n = 2.0 for amphistomatous leaf
           rbH_L=rbH*stom_n/2.                   !final b/l resistance for heat  
           rrdn=1./grdn
           Y=1./(1.+ (rbH_L+raero)/rrdn)
!          boundary layer conductance for CO2 - single side only (mol/m2/s)
           gbc=Cmolar*gbH/1.32            !mol/m2/s
           gsc0=gsw0/1.57                        !convert conductance for H2O to that for CO2
           varQc=0.0                  
           weighR=1.0
!          respiration      
           Aleafx=-0.0089*Vcmxx*exp(0.069*(Tlk-293.2))
           gsc=gsc0
!          choose smaller of Ac, Aq
           Aleaf(ileaf) = Aleafx                     !mol CO2/m2/s
!          calculate new values for gsc, cs (Lohammer model)
           co2cs = co2ca-Aleaf(ileaf)/gbc
           co2Ci(ileaf) = co2cs-Aleaf(ileaf)/gsc
!          scale variables
           gsw=gsc*1.56                              !gsw in mol/m2/s
           gswv=gsw/Cmolar                           !gsw in m/s
           rswv=1./gswv
!          calculate evap'n using combination equation with current estimate of gsw
           Eleaf(ileaf)=
     &     (slope*Y*Rnstar(ileaf)+rhocp*Dair/(rbH_L+raero))/
     &     (slope*Y+psyc*(rswv+rbw+raero)/(rbH_L+raero))
!          calculate sensible heat flux
           Hleaf(ileaf)=Y*(Rnstar(ileaf)-Eleaf(ileaf))
!          calculate new leaf temperature (K)
           Tlk1=273.2+Tair+Hleaf(ileaf)*(rbH/2.+raero)/rhocp
!          calculate Dleaf use LE=(rhocp/psyc)*gsw*Ds
           Dleaf=psyc*Eleaf(ileaf)/(rhocp*gswv)
           gbleaf(ileaf)=gbc*1.32*1.075
           gsleaf(ileaf)=gsw

!          compare current and previous leaf temperatures
           if(abs(Tlk1-Tlk).le.0.1)exit
           if(kr1.gt.1000)exit
!          update leaf temperature
           Tlk=Tlk1 
           Tleaf(ileaf)=Tlk1-273.2
           kr1=kr1+1
         enddo                          !solution not found yet
10       continue
       enddo
       return
       end
!     ****************************************************************************
       subroutine ciandA(Gma,Bta,g0,X,Rd,co2Cs,gammas,ciquad,Aquad)
!      calculate coefficients for quadratic equation for ci
       b2=g0+X*(Gma-Rd)
       b1=(1.-co2cs*X)*(Gma-Rd)+g0*(Bta-co2cs)-X*(Gma*gammas+Bta*Rd)
       b0=-(1.-co2cs*X)*(Gma*gammas+Bta*Rd)-g0*Bta*co2cs

       bx=b1*b1-4.*b2*b0
       if(bx.gt.0.0)then 
!        calculate larger root of quadratic
         ciquad = (-b1+sqrt(bx))/(2.*b2)
       endif

       if(ciquad.lt.0.or.bx.lt.0.)then
         Aquad = 0.0
         ciquad = co2Cs
       else
         Aquad = Gma*(ciquad-gammas)/(ciquad+Bta)
       end if
       return
       end

!****************************************************************************
       subroutine goud1(FLAIT,coszen,radabv,fbeam,
     &   Tair,eairP,emair,emsoil,emleaf,sigma,
     &   tauL,rhoL,rhoS,xfang,extkb,extkd,
     &   reffbm,reffdf,extkbm,extkdm,Qcan)
!      use the radiation scheme developed by
!      Goudriaan (1977, Goudriaan and van Larr 1995)
!=================================================================
!      Variable      unit      defintion
!      FLAIT         m2/m2     canopy leaf area index       
!      coszen                  cosine of the zenith angle of the sun
!      radabv(nW)    W/m2      incoming radiation above the canopy
!      fbeam                   beam fraction
!      fdiff                   diffuse fraction
!      funG(=0.5)              Ross's G function
!      extkb                   extinction coefficient for beam PAR
!      extkd                   extinction coefficient for diffuse PAR
!      albedo                  single scattering albedo
!      scatB                   upscattering parameter for beam
!      scatD                   upscattering parameter for diffuse
! ==================================================================
!      all intermediate variables in the calculation correspond
!      to the variables in the Appendix of of Seller (1985) with
!      a prefix of "x".
       integer nW
       real radabv(3)
       real rhocbm(3),rhocdf(3)
       real reffbm(3),reffdf(3),extkbm(3),extkdm(3)
       real tauL(3),rhoL(3),rhoS(3),scatL(3)
       real Qcan(3,2),Qcan0(3)
!
!      for PAR: using Goudriann approximation to account for scattering
       fdiff=1.0-fbeam
       xu=coszen
       xphi1 = 0.5 -0.633*xfang - 0.33*xfang*xfang
       xphi2 = 0.877 * (1.0 - 2.0*xphi1)
       funG = xphi1 + xphi2*xu
       extkb=funG/xu
                       
!      Effective extinction coefficient for diffuse radiation Goudriaan & van Laar Eq 6.6)
       pi180=3.1416/180.
       cozen15=cos(pi180*15)
       cozen45=cos(pi180*45)
       cozen75=cos(pi180*75)
       xK15=xphi1/cozen15+xphi2
       xK45=xphi1/cozen45+xphi2
       xK75=xphi1/cozen75+xphi2
       transd=0.308*exp(-xK15*FLAIT)+0.514*exp(-xK45*FLAIT)+
     &   0.178*exp(-xK75*FLAIT)
       extkd=(-1./FLAIT)*alog(transd)

!      canopy reflection coefficients (Array indices: 1=VIS,  2=NIR
       do nw=1,2                                                         !nw:1=VIS, 2=NIR
         scatL(nw)=tauL(nw)+rhoL(nw)                                          !scattering coeff
         if((1.-scatL(nw))<0.0) scatL(nw)=0.9999                               !Weng 10/31/2008
         extkbm(nw)=extkb*sqrt(1.-scatL(nw))                                  !modified k beam scattered (6.20)
         extkdm(nw)=extkd*sqrt(1.-scatL(nw))                                  !modified k diffuse (6.20)
         rhoch=(1.-sqrt(1.-scatL(nw)))/(1.+sqrt(1.-scatL(nw)))                    !canopy reflection black horizontal leaves (6.19)

         rhoc15=2.*xK15*rhoch/(xK15+extkd)                                    !canopy reflection (6.21) diffuse
         rhoc45=2.*xK45*rhoch/(xK45+extkd)
         rhoc75=2.*xK75*rhoch/(xK75+extkd)   
       
         rhocbm(nw)=2.*extkb/(extkb+extkd)*rhoch                              !canopy reflection (6.21) beam 
         rhocdf(nw)=0.308*rhoc15+0.514*rhoc45+0.178*rhoc75

         reffbm(nw)=rhocbm(nw)+(rhoS(nw)-rhocbm(nw))                          !effective canopy-soil reflection coeff - beam (6.27)
     &             *exp(-2.*extkbm(nw)*FLAIT)                              
         reffdf(nw)=rhocdf(nw)+(rhoS(nw)-rhocdf(nw))                          !effective canopy-soil reflection coeff - diffuse (6.27)
     &             *exp(-2.*extkdm(nw)*FLAIT)  

!        by the shaded leaves
         abshdn=fdiff*(1.0-reffdf(nw))*extkdm(nw)                             !absorbed NIR by shaded
     &     *(funE(extkdm(nw),FLAIT)-funE((extkb+extkdm(nw)),FLAIT))
     &     +fbeam*(1.0-reffbm(nw))*extkbm(nw)
!    &     *(funE(extkbm(nw),FLAIT)-funE((extkb+extkdm(nw)),FLAIT))  ! error found by De Pury
     &     *(funE(extkbm(nw),FLAIT)-funE((extkb+extkbm(nw)),FLAIT))
     &     -fbeam*(1.0-scatL(nw))*extkb
     &     *(funE(extkb,FLAIT)-funE(2.0*extkb,FLAIT))
!        by the sunlit leaves
         absltn=fdiff*(1.0-reffdf(nw))*extkdm(nw)                             !absorbed NIR by sunlit
     &     *funE((extkb+extkdm(nw)),FLAIT)                         
     &     +fbeam*(1.0-reffbm(nw))*extkbm(nw)
!    &     *funE((extkb+extkdm(nw)),FLAIT)                         ! error found by De Pury
     &     *funE((extkb+extkbm(nw)),FLAIT)
     &     +fbeam*(1.0-scatL(nw))*extkb
     &     *(funE(extkb,FLAIT)-funE(2.0*extkb,FLAIT))

!        scale to real flux 
!        sunlit    
         Qcan(nw,1)=absltn*radabv(nw)
!        shaded
         Qcan(nw,2)=abshdn*radabv(nw)
       enddo
!     
!      calculate the absorbed (iso)thermal radiation
       TairK=Tair+273.2
      
!      apparent atmospheric emissivity for clear skies (Brutsaert, 1975)
       emsky=0.642*(eairP/Tairk)**(1./7)      !note eair in Pa

!      apparent emissivity from clouds (Kimball et al 1982)
       ep8z=0.24+2.98e-12*eairP*eairP*exp(3000.0/TairK)
       tau8=amin1(1.0,1-ep8z*(1.4-0.4*ep8z))                !ensure tau8<1
       emcloud=0.36*tau8*(1.-fbeam)*(1-10./TairK)**4        !10 from Tcloud = Tair-10 

!      apparent emissivity from sky plus clouds      
!      emair=emsky+emcloud
!      20/06/96
       emair=emsky
       if(emair.gt.1.0) emair=1.0                             

       Bn0=sigma*(TairK**4)
       QLW1=-extkd*emleaf*(1.0-emair)*funE((extkd+extkb),FLAIT)
     &   -extkd*(1.0-emsoil)*(emleaf-emair)*exp(-2.0*extkd*FLAIT)
     &   *funE((extkb-extkd),FLAIT)
       QLW2=-extkd*emleaf*(1.0-emair)*funE(extkd,FLAIT)
     &   -extkd*(1.0-emsoil)*(emleaf-emair)
     &   *(exp(-extkd*FLAIT)-exp(-2.0*extkd*FLAIT))/extkd
     &   -QLW1
       Qcan(3,1)=QLW1*Bn0
       Qcan(3,2)=QLW2*Bn0
       return
       end

!****************************************************************************
       subroutine photosyn(Sps,CO2Ca,CO2Csx,Dleafx,Tlkx,Qaparx,Gbcx,
     &   theta,a1,Ds0,fwsoil,varQc,weighR,
     &   g0,alpha,
     &   Vcmx1,eJmx1,weighJ,conKc0,conKo0,Ekc,Eko,o2ci,
     &   Rconst,Trefk,Eavm,Edvm,Eajm,Edjm,Entrpy,gam0,gam1,gam2,
     &   Aleafx,Gscx,TminV,TmaxV,ToptV)

!      calculate Vcmax, Jmax at leaf temp (Eq 9, Harley et al 1992)
!      VcmxT = Vjmax(Tlkx,Trefk,Vcmx1,Eavm,Edvm,Rconst,Entrpy)
!      eJmxT = Vjmax(Tlkx,Trefk,eJmx1,Eajm,Edjm,Rconst,Entrpy)

!      check if it is dark - if so calculate respiration and g0 to assign conductance 
       if(Qaparx.le.0.) then                            !night, umol quanta/m2/s
         Aleafx=-0.0089*Vcmx1*exp(0.069*(Tlkx-293.2))   ! original: 0.0089 Weng 3/22/2006
         Gscx=g0
       endif
!      calculate  Vcmax, Jmax at leaf temp using Reed et al (1976) function J appl Ecol 13:925
      
       TminJ=TminV
       TmaxJ=TmaxV
       ToptJ=ToptV 
      
       Tlf=Tlkx-273.2
       VcmxT=VJtemp(Tlf,TminV,TmaxV,ToptV,Vcmx1)
       eJmxT=VJtemp(Tlf,TminJ,TmaxJ,ToptJ,eJmx1)      
!      calculate J, the asymptote for RuBP regeneration rate at given Q
       eJ = weighJ*fJQres(eJmxT,alpha,Qaparx,theta)
!      calculate Kc, Ko, Rd gamma*  & gamma at leaf temp
       conKcT = EnzK(Tlkx,Trefk,conKc0,Rconst,Ekc)
       conKoT = EnzK(Tlkx,Trefk,conKo0,Rconst,Eko)
!      following de Pury 1994, eq 7, make light respiration a fixed proportion of
!      Vcmax
       Rd = 0.0089*VcmxT*weighR                              !de Pury 1994, Eq7
       Tdiff=Tlkx-Trefk
       gammas = gam0*(1.+gam1*Tdiff+gam2*Tdiff*Tdiff)       !gamma*
!      gamma = (gammas+conKcT*(1.+O2ci/conKoT)*Rd/VcmxT)/(1.-Rd/VcmxT)
       gamma = 0.0
!     ***********************************************************************
!      Analytical solution for ci. This is the ci which satisfies supply and demand
!      functions simultaneously
!      calculate X using Lohammer model, and scale for soil moisture
       X = a1*fwsoil/((co2csx - gamma)*(1.0 + Dleafx/Ds0))
!      calculate solution for ci when Rubisco activity limits A
       Gma = VcmxT  
       Bta = conKcT*(1.0+ o2ci/conKoT)
       call ciandA(Gma,Bta,g0,X,Rd,co2Csx,gammas,co2ci2,Acx)
!      calculate +ve root for ci when RuBP regeneration limits A
       Gma = eJ/4.
       Bta = 2.*gammas
!      calculate coefficients for quadratic equation for ci
       call ciandA(Gma,Bta,g0,X,Rd,co2Csx,gammas,co2ci4,Aqx)
!      choose smaller of Ac, Aq
       sps=AMAX1(0.001,sps)                  !Weng, 3/30/2006
       Aleafx = (amin1(Acx,Aqx) - Rd)*sps     ! Weng 4/4/2006
!      calculate new values for gsc, cs (Lohammer model)
       CO2csx = co2ca-Aleafx/Gbcx
       Gscx=g0+X*Aleafx  ! revised by Weng

       return
       end
!***********************************************************************
       function funeJ(alpha,eJmxT,Qaparx)
       funeJ=alpha*Qaparx*eJmxT/(alpha*Qaparx+2.1*eJmxT)
       return
       end
!****************************************************************************
       real function esat(T)
!      returns saturation vapour pressure in Pa
       esat=610.78*exp(17.27*T/(T+237.3))
       return
       end

!****************************************************************************
       real function evapor(Td,Tw,Patm)
!      * returns vapour pressure in Pa from wet & dry bulb temperatures
       gamma = (64.6 + 0.0625*Td)/1.e5
       evapor = esat(Tw)- gamma*(Td-Tw)*Patm
       return
       end

!****************************************************************************
       real function Vjmax(Tk,Trefk,Vjmax0,Eactiv,Edeact,Rconst,Entrop)
       anum = Vjmax0*EXP((Eactiv/(Rconst*Trefk))*(1.-Trefk/Tk))
       aden = 1. + EXP((Entrop*Tk-Edeact)/(Rconst*Tk))
       Vjmax = anum/aden
       return
       end
!****************************************************************************
       real function funE(extkbd,FLAIT)
       funE=(1.0-exp(-extkbd*FLAIT))/extkbd
       return
       end

!     ****************************************************************************
!      Reed et al (1976, J appl Ecol 13:925) equation for temperature response
!      used for Vcmax and Jmax
       real function VJtemp(Tlf,TminVJ,TmaxVJ,ToptVJ,VJmax0)
       if(Tlf.lt.TminVJ) Tlf=TminVJ   !constrain leaf temperatures between min and max
       if(Tlf.gt.TmaxVJ) Tlf=TmaxVJ
       pwr=(TmaxVJ-ToptVJ)/(ToptVj-TminVj)
       VJtemp=VJmax0*((Tlf-TminVJ)/(ToptVJ-TminVJ))*
     &   ((TmaxVJ-Tlf)/(TmaxVJ-ToptVJ))**pwr 
       return
       end

!     ****************************************************************************
       real function fJQres(eJmx,alpha,Q,theta)
       AX = theta                                 !a term in J fn
       BX = alpha*Q+eJmx                          !b term in J fn
       CX = alpha*Q*eJmx                          !c term in J fn
       if((BX*BX-4.*AX*CX)>=0.0)then
         fJQres = (BX-SQRT(BX*BX-4.*AX*CX))/(2*AX)
       else
         fJQres = (BX)/(2*AX)                   !Weng 10/31/2008
       endif

       return
       end

!     *************************************************************************
       real function EnzK(Tk,Trefk,EnzK0,Rconst,Eactiv)

       temp1=(Eactiv/(Rconst* Trefk))*(1.-Trefk/Tk)
       return
       end

!     *************************************************************************
       real function sinbet(doy,lat,pi,timeh)
       real lat
!      calculations according to Goudriaan & van Laar 1994 P30
       rad = pi/180.
!      sine and cosine of latitude
       sinlat = sin(rad*lat)
       coslat = cos(rad*lat)
!      sine of maximum declination
       sindec=-sin(23.45*rad)*cos(2.0*pi*(doy+10.0)/365.0)
       cosdec=sqrt(1.-sindec*sindec)
!      terms A & B in Eq 3.3
       A = sinlat*sindec
       B = coslat*cosdec
       sinbet = A+B*cos(pi*(timeh-12.)/12.)
       return
       end

!     *************************************************************************
       subroutine yrday(doy,hour,lat,radsol,fbeam)
       real lat
       pi=3.14159256
       pidiv=pi/180.0
       slatx=lat*pidiv
       sindec=-sin(23.4*pidiv)*cos(2.0*pi*(doy+10.0)/365.0)
       cosdec=sqrt(1.-sindec*sindec)
       a=sin(slatx)*sindec
       b=cos(slatx)*cosdec
       sinbet=a+b*cos(2*pi*(hour-12.)/24.)
       solext=1370.0*(1.0+0.033*cos(2.0*pi*(doy-10.)/365.0))*sinbet
      
       tmprat=radsol/solext

       tmpR=0.847-1.61*sinbet+1.04*sinbet*sinbet
       tmpK=(1.47-tmpR)/1.66
       if(tmprat.le.0.22) fdiff=1.0
       if(tmprat.gt.0.22.and.tmprat.le.0.35)then
         fdiff=1.0-6.4*(tmprat-0.22)*(tmprat-0.22)
       endif
       if(tmprat.gt.0.35.and.tmprat.le.tmpK)then
         fdiff=1.47-1.66*tmprat
       endif
       if(tmprat.ge.tmpK) then
         fdiff=tmpR
       endif
       fbeam=1.0-fdiff
       if(fbeam.lt.0.0) fbeam=0.0
       return
       end
!     *******************added by myself**********************************
       SUBROUTINE init_random_seed()
         INTEGER :: i, n, clock
         INTEGER, DIMENSION(:), ALLOCATABLE :: seed
         
         CALL RANDOM_SEED(size = n)
         ALLOCATE(seed(n))
          
         CALL SYSTEM_CLOCK(COUNT=clock)
          
         seed = clock + 37 * (/ (i - 1, i = 1, n) /)
         CALL RANDOM_SEED(PUT = seed)
          
         DEALLOCATE(seed)
       END SUBROUTINE
!=============================================================================
