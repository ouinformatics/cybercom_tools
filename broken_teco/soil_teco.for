	program TECO
!
!************************************************************************c
!       Terrestrial ECOsystem model (TECO) by Ensheng Weng and Yiqi Luo   
!              Version 1.0 (03-18-2008)                                      
!       Copyright (c) 2008 University of OKlahoma                         
!              All rights reserved                                           
!       THE UNIVERSITY OF OKLAHOMA MAKE NO REPRESENTATION OR WARRANTIES   
!       WITH RESPECT TO THE CONTENTS HEROF AND SPECIFICALLY DISCLAIM ANY  
!       IMPLIED WARRANTIES OR MERCHANTABILITY OR FITNESS FOR ANY 
!       PARTICULAR PURPOSE.
!       Further, we reserve the right to revise this software and/or
!       documentation and to make changes from time to time in the 
!       content without obligation to notify any person of such revision 
!       or change. 
!
!       Please cite the following reference if you use TECO model:
!       Weng E. and Luo Y., 2008. Soil hydrological properties regulate
!       grassland ecosystem responses to multifactor global change:
!       a modeling analysis. Journal of Geophysical Research (in press)
!
!       The code of canopy subroutine is the courtesy of Yingping Wang,
!       CSIRO, Australia. 
!       
!
!       If you have any problem with this model, please e-mail:
!       Ensheng Weng (esweng@ou.edu) or Yiqi Luo (yluo@ou.edu)
!************************************************************************c
!
	implicit none
      real WILTPT,FILDCP,wscontent,wsmax,wsmin,ws_yr,d_drought
      real omega,wsmaxsoil,wsminsoil,fwsoil,topfws,ws,wdepth,fw_yr
      real NSC,NSCmin,NSCmax,NSC_bm   ! none structural carbon pool
      real Growth,Groot,Gshoot,GRmax,Weight  ! growth rate of plant,root,shoot,and max of root
      real St,Sw,Ss,Sn,Srs,Sps,fnsc     ! scaling factors for growth
      real rdepth,rfibre
      real thksl(10),wupl(10),evapl(10),wcl(10),FRLEN(10),wcl_yr(10)
      real Twair(7),Twsoil(7),Ta,Tavg,Tcur,Ta_cur,Tlin,Ts
      real gpp,gpp_t,GPP_Ra,NPP
	real storage,LAI_P,RS
      real evap_t,transp_t,evap,transp,TEVAP,AEVAP
      real runoff,Trunoff,rain_yr,runoff_yr,evap_yr,transp_yr,omega_yr
      real ws1,ws2,dws,net_dws
      real wsc(10),AW(10),AW_yr(10)
      real tauL(3),rhoL(3),rhoS(3),reffbm(3),reffdf(3)
      real extkbm(3),extkdm(3)
      real Radabv(2),Qcan(3,2),Qcan0(3)
      real Acan(2),Ecan(2),Hcan(2),Tcan(2), Gbwcan(2), Gswcan(2)
      real bmcrop(365),CNtop(365),totLAI(365),ht_can(365)
      real LAI,LAIMAX,LAIMIN,bmroot,bmstem,bmleaf,bmplant
      real LAI_curr,LAI_2C,LAI_max,W_LAI(365)
      real SLA,L_fall,L_add,litter,seeds,storag1,stor_use
      real GDDonset,GDD5,accumulation
      real RaL,RaS,RaR,RaP,RaLeaf,RaStem,RaRoot,Rsoil
      real rho,alpha_L,alpha_S,alpha_R ! allocation ratio to Leaf, stem,and Root
      real ep_L,ep_S,ep_R    ! plant dependent parameters L+S+R=1
      real gpp_yr,NPP_yr,NEE_yr,RaL_yr,RaR_yr
      real RhF_yr,RhC_yr,RhS1_yr,RhS2_yr,RhS3_yr,Rh_yr
      real NPPL_yr,NPPS_yr,NPPR_yr,NPP_L,NPP_S,NPP_R,NEE
      real RnStL(5),QcanL(5),RcanL(5),AcanL(5),EcanL(5),HcanL(5)
      real GbwcL(5),GswcL(5),hG(5),hIL(5)
      real Gaussx(5),Gaussw(5),Gaussw_cum(5)
      real doy,hour,tair,Tsoil,Dair,Rh,rain,radsol,rain_t
      real d_ql,d_qw,d_qr1,d_qr2,d_qr3 ! changes of every pool
      real d_qf,d_qc,d_qs1,d_qs2,d_qs3
      real Resp_f,Resp_c,Resp_s1,Resp_s2,Resp_s3
      real Q_leaf,Q_fine,Q_wood,Q_coarse,Q_root1,Q_root2,Q_root3
      real Q_soil1,Q_soil2,Q_soil3,Q_soil
      real CNmin,CNmax
      real zeta1,zeta2,zeta3
      real tau_L,tau_W,tau_R1,tau_R2,tau_R3
      real tau_F_a,tau_C_a,tau_S1_a,tau_S2_a,tau_S3_a
      real eta,theta_F,theta_C,theta_S1,theta_S2
      real GrowthL,GrowthR,GLmax,GSmax,R_S
      real QNleaf,QNfine,QNwood,QNcoarse,QNmax
      real QNroot1,QNroot2,QNroot3
      real QNsoil1,QNsoil2,QNsoil3,QN_miner,QNplant,QNpmax
      real CN_leaf,CN_fine,CN_wood,CN_coarse
      real CN_root1,CN_root2,CN_root3
      real CN_soil1,CN_soil2,CN_soil3,CN_NPP
      real N_mi_yr,N_up_yr,N_miner,N_uptake
      real SNamax,SNrs,SNdcomp
      real N_amb,N_2C,N_S2C
!     appended
      real a1,a2,acanop,airma,alpha,anet,chi,co2,co2ca,conkc0,conko0
	real cpair,deph2o,dheat,ds0,eajm,eavm,ecstot,edjm,edvm,ejmx0
	real ekc,eko,emleaf,sc_fc,slat,vcmx0,extku,xfang,stom_n
	real rootmax,stemmax,sens,senr,pi,emsoil,rconst,sigma,patm
	real trefk,h2olv0,h2omx,wleaf,gsw0,theta,o2ci,entrpy,gam0
	real gam1,gam2,snamax_yr,precp_t,esat,H2OMW,windu0,wethr,Rnet
	real G,esoil,vcmxn,hcrop,Raplant,omega_s,S_fall
!     scenario
      real Sc_co2,Sc_T,Sc_prcp,Sc_S,Sc_WP
      integer num_scen,year,jrain
      integer plantonset,duration,offset,dormancy,onset  !flag of phenological stage
      integer yr,days,i,j,k,writer,equa,yr_data
      integer dtimes,idoy,ihour,ileaf,ioput,num
      character(len=80) Sc_name,climfile
      character(len=80) out_C,out_h2o,out_N,out_yr,out_pools
      character(len=80) commts
199   format(a80)

      Sc_T=0
      Sc_prcp=1
      Sc_FC=0
      Sc_WP=0
      Sc_co2=1
!===================================================
!===================================================
! open input and output files:
      open(10,file='TECO_param.txt',status='old') !parameters
	open(13, file='TECO_amb_h.txt',status='old') !climate data
	writer=3  !The years to run before recording simulation results
	yr_data=1 !How many years' data of the climate dataset has
 
!     open output files
!      open(61,file='TECO_C_daily.csv')
      open(62,file='soil_daily.csv')
!      open(63,file='TECO_pools_C.csv')
      read(13,11) commts
!      write(61,*)'d,LAI,GP,NP,N_L,N_S,N_R,RaL,RaR,
!     &RhF,Rhs1,Rhs2,Rhs3,NE,bmR,bmL,bmS'
      write(62,*)'d,P,Tr,E,R,ws,fw,topfw,omega, 
     &wc1,wc2,wc3,wc4,wc5,wc6,wc7,wc8,wc9,wc10'
!      write(63,*)'y,Q_l,Q_w,Q_r1,Q_r2,Q_r3,Q_cs,Q_f,Q_s1,Q_s2,Q_s3'

!c===================================================
!c Initialize parameters and initial states
!c	the thickness of every soil layer
	thksl(1)=10.0   !cm
	thksl(2)=20.0
	thksl(3)=20.0
	thksl(4)=20.0    !root
	thksl(5)=20.0
	thksl(6)=20.0
	thksl(7)=20.0
	thksl(8)=20.0
	thksl(9)=20.0
	thksl(10)=20.0
!c	ratio of roots in every layer
	FRLEN(1)=0.4
	FRLEN(2)=0.4
	FRLEN(3)=0.15
	FRLEN(4)=0.05
	FRLEN(5)=0.0
	FRLEN(6)=0.0
	FRLEN(7)=0.0
	FRLEN(8)=0.0
	FRLEN(9)=0.0
	FRLEN(10)=0.0
 
	Twair=0.0
	gddonset=600.0  !GDD for grassland greening up
	stor_use=Storage/25.0
	onset=0
	duration=0
	offset=0
	dormancy=1

!c	initiations for canopy model,
!c	including canopy traits variation in a year	
      call setup(slat,co2,ioput,a1,Ds0,Vcmx0,extkU,xfang,alpha,
     &           stom_n,wsmaxsoil,wsminsoil,rdepth,rfibre,SLA,
     &           LAIMAX,LAIMIN,Rootmax,Stemmax,SenS,SenR)

	co2ca=co2
	a2=a1
	wsmax=wsmaxsoil 
	wsmin=wsminsoil
	WILTPT=wsmin/100.0
	FILDCP=wsmax/100.0
	do i=1,10
		wcl(i)=FILDCP
	enddo

	wscontent=1.0 !amin1(0.3241,FILDCP)
	fwsoil=1.0
	topfws=0.9965
	omega=0.7628

      call consts(pi,tauL,rhoL,rhoS,emleaf,emsoil,
     &   Rconst,sigma,cpair,Patm,Trefk,H2OLv0,airMa,H2OMw,chi,Dheat,
     &   wleaf,gsw0,Vcmx0,eJmx0,theta,conKc0,conKo0,Ekc,Eko,o2ci,
     &   Eavm,Edvm,Eajm,Edjm,Entrpy,gam0,gam1,gam2)

!     initial values of the C pools
	nsc=40.74
	Storage=57.6     !g C/m2
	Q_leaf=3.3334    !g C/m2
	Q_wood=0.9981    !g C/m2
	Q_root1=62.41    !g C/m2
	Q_root2=35.1517  !g C/m2
	Q_root3=11.0793  !g C/m2
	Q_coarse=0.0     !g C/m2
	Q_fine=369.9881  !g C/m2
	Q_soil1=4869.856 !g C/m2
	Q_soil2=2304.713 !g C/m2
	Q_soil3=1397.098 !g C/m2

	LAI=LAIMIN
	bmleaf=Q_leaf/0.45
	bmstem=0.2 * bmleaf
	bmroot=(Q_root1+Q_root2+Q_root3)/0.45
	bmplant=bmstem+bmroot+bmleaf

!c=============================================================
!c=============================================================
!c	Simulating begins here
	num=0
	do yr=1, writer+yr_data  ! how many years
		write(*,*)yr
		num=num+1
		if(num.GT.yr_data) then
			rewind 13
			read(13,11) commts
			num=1
		endif

		GDD5=0.0
		onset=0
		d_drought=0
		gpp_yr=0.0
		NPP_yr=0.0
		NEE_yr=0.0
		RaL_yr=0.0
		RaR_yr=0.0
	    RhF_yr=0.0
		RhC_yr=0.0
		RhS1_yr=0.0
		RhS2_yr=0.0
		RhS3_yr=0.0
		NPPL_yr=0.0
		NPPS_yr=0.0
		NPPR_yr=0.0
		rain_yr=0.0
		runoff_yr=0.0
		evap_yr=0.0
		transp_yr=0.0

		N_up_yr=0.0
		N_mi_yr=0.0
		SNamax_yr=0.0
		omega_yr=0.0
		fw_yr=0.0
		ws_yr=0.0

		wcl_yr=0.0
		AW_yr=0.0

	do days=1,365 !the days of a year
		LAI_p=W_LAI(days)
		NSCmin=0.05*bmplant*0.45
		NSCmax=0.2*bmplant*0.45
		SNamax=0.5
		SNrs=0.5
		SNdcomp=0.5

!         THE FIRST PART:	    
!         coupled canopy and soil model
	    gpp_t=0.0
	    transp_t=0.0
	    evap_t=0.0
	    ta=0.0
          Ta_cur=0.0
	    precp_t=0.0
          Ts=0.0
          rain_t=0.0
	    Trunoff=0.0
          RaL=0.0
          RaS=0.0
          RaR=0.0
          GPP_Ra=0.0
          QNmax=0.0
          QNpmax=0.0

	    dtimes=24 !how many times a day,24 means every hour
	    do i=1,dtimes
              read(13,*,end=999)year,doy,hour,Tair,Tsoil,
     &              Dair,Rh,rain,radsol
			 Tcur=Tair
!c	         assume the values of some variables 
	         if(radsol.eq.0.0)radsol=0.01
			 dair=Rh/100.0*esat(tair)  !water vapour pressure, RH=30
	         windU0=0.01 !pre-assumed values
			 wethr=1
			 Rnet=0.8*radsol
			 if(radsol.gt.10.0) then
	             G=-25.0
			 else
				 G=20.5
			 endif
			 Esoil=0.05*radsol
			 if(radsol.LE.10.0) Esoil=0.5*G

			 DepH2O=0.2
			 ta=ta+tair ! sum of a day, for calculating daily mean temperature
			 Ta_cur=Ta_cur+Tcur
			 Ts=Ts+Tsoil
			 precp_t=precp_t+rain
			 VcmxN=Vcmx0 *SNamax

			call respiration(LAIMIN,GPP,Tair,Tsoil,DepH2O,
     &                       LAI,SLA,bmstem,bmroot,bmleaf,fnsc,
     &					   RaLeaf,RaStem,RaRoot,Raplant,Rsoil)

			RaL=RaL+RaLeaf*3600.0*12.0/1000000.0
			RaS=RaS+RaStem*3600.0*12.0/1000000.0
			RaR=RaR+RaRoot*3600.0*12.0/1000000.0

	    	call soil(wsmax,wsmin,rdepth,rfibre,FRLEN,!constants specific to soil/plant
     &                rain,tair,transp,wcl,tsoil,Rh,thksl,LAI,	      !inputs
     &				evap,wscontent,fwsoil,topfws,omega,omega_S,runoff)!outputs

!c			sums of a day
			 gpp_t=gpp + gpp_t
			 transp_t=transp + transp_t
			 evap_t=evap + evap_t
			 rain_t=rain_t+rain
			 Trunoff=Trunoff+runoff		         
		enddo
		GPP_Ra=RaL+RaS+RaR
		if(GPP_Ra.gt.NSC*0.6)then
			RaL=RaL*NSC*0.6/GPP_Ra
			RaS=RaS*NSC*0.6/GPP_Ra
			RaR=RaR*NSC*0.6/GPP_Ra
			GPP_Ra=RaL+RaS+RaR
		endif
		RaP=RaL+RaS+RaR
!c		update NSC
		NSC=NSC+GPP_t-GPP_Ra

!c	mean temperature of a day
	    ta=ta/dtimes
		Ta_cur=Ta_cur/dtimes
		Tlin=ta
	    Ts=Ts/dtimes
		if(Ta_cur.gt.5.0)GDD5=GDD5+Ta_cur-5.0


!c	THE Third Part: update LAI
		Wdepth=0.0
		ws=0
		Do i=1,4
			wsc(i)=wcl(i)*THKSL(i)*10.0 !mm, water amount of every layer
			ws=ws+wsc(i)      !
			AW(i)=wcl(i) - WILTPT
			Wdepth=Wdepth+THKSL(i)*10.0
		enddo

!	output results of canopy and soil models
		if((yr.gt.writer).and.(yr.le.(writer+yr_data)))then
!			write(61,161)doy,LAI,gpp_t,NPP,alpha_L*NPP,alpha_S*NPP,
!     &				alpha_R*NPP,RaL,RaR,Resp_f,Resp_s1,Resp_s2,
!     &				Resp_s3,NEE,bmroot,bmleaf,bmstem
!  
			write(62,162)doy,precp_t,transp_t,evap_t,Trunoff,
     &				 wscontent,fwsoil,topfws,omega,
     &                 (wcl(i),i=1,5)
!
		endif
!
!
!	print *, evap
!	print *, omega_S
!	print *, runoff
!	print *, wscontent
!	print *, fwsoil
!	print *, topfws
!	print *, omega
	enddo	!end of a year

	enddo !end of simulation years

11    format(a80)
161	format(17(f11.4,","))
162	format(19(f11.4,","))
163	format(i4,",",10(f11.4,","))

999	continue
9999	continue

	close(10)
	close(11)
	close(13)

!	close(61)
!	close(62)
!	close(63)
	
	end
!     *******************************************************************************
      subroutine setup(slat,co2ca,ioput,a1,Ds0,Vcmx0,extkU,xfang,alpha,
     &           stom_n,wsmax,wsmin,rdepth,rfibre,SLA,LAIMAX,LAIMIN,
     &		   Rootmax,Stemmax,SenS,SenR)
	implicit none
	INTEGER ioput
      real slat,co2ca,a1,Ds0,Vcmx0,extkU,xfang,alpha
      real stom_n,wsmax,wsmin,rdepth,rfibre,SLA,LAIMAX,LAIMIN
	REAL Rootmax,Stemmax,SenS,SenR
	character(len=80) commts

!     read in plant and soil traits and daily LAI,TBM,LBM,%N and ht_can for a year 
!     read in parameters
11    format(a80)
      read(10,11) commts
      read(10,*) slat,co2ca,ioput

      read(10,11) commts
      read(10,*) a1,Ds0,Vcmx0,extkU,xfang,alpha,stom_n
      
	read(10,11) commts
      read(10,*) wsmax,wsmin
      
	read(10,11) commts
      read(10,*)rdepth,rfibre 
      
	read(10,11) commts
      read(10,*)SLA,LAIMAX,LAIMIN
      
!      read(10,11) commts
!      read(10,*)Rootmax,Stemmax,SenS,SenR

      close(10)
      return
      end


!****************************************************************************
!============================================================================
!============================================================================

      subroutine respiration(LAIMIN,GPP,Tair,Tsoil,DepH2O,
     &                       LAI,SLA,bmstem,bmroot,bmleaf,fnsc,
     &					   RaLeaf,RaStem,RaRoot,Raplant,Rsoil)
!     calculate plant and soil respiration
	implicit none
	real LAIMIN,LAI,GPP,SLA
	real Tair,Tsoil,DepH2O
	real bmstem,bmroot,bmleaf,fnsc
	real RaLeaf,RaStem,RaRoot,Raplant,Rsoil
	real Rl0,Rs0,Rr0

	if(LAI.gt.LAIMIN) then
!	    Rl0=LAI*0.1                 !umol/m2/s
	    Rl0=bmleaf*SLA*0.1                 !umol/m2/s
	    Rs0=bmstem*0.006*0.1          !umol/m2/s
	    Rr0=bmroot*0.006*0.1          !umol/m2/s
	    RaLeaf=Rl0*exp(0.084*Tair)*fnsc
	    RaStem=Rs0*exp(0.084*Tair)*fnsc
	    RaRoot=Rr0*exp(0.084*Tair)*fnsc
	else
	    RaLeaf=0.5*GPP
	    RaStem=0.0
	    RaRoot=0.5*GPP

	endif
      RaPlant=Raleaf+Rastem+Raroot       !umol/m2/s
!    special for IREX
      if(DepH2O.gt.0.5) then
	  Rsoil=0.0                    !flooded
	else
	  Rsoil=0.017*exp(0.221*Tsoil)  !umol/m2/s
	end if

      return
      end
!
!=======================================================================
!=======================================================================
!	subroutine for soil moisture

	subroutine soil(wsmax,wsmin,rdepth,rfibre,FRLEN,!constants specific to soil/plant
     &                rain,tair,transp,wcl,tsoil,Rh,thksl,LAI,	!inputs
     &				evap,wscontent,fwsoil,topfws,omega,omega_S,runoff)  !outputs

! **  All of inputs, the unit of water is 'mm', soil moisture or soil water content is a ratio

	implicit none
!	soil traits
	real wsmax,wsmin,wsmaxL(10),wsminL(10) !from input percent x%
	real FLDCAP,WILTPT,FLDCAPL(10),WILTPTL(10) ! ie. 0.xx

!	plant traits
	real LAI,rdepth
	real rfibre
	integer nfr
!	real eflflr,elnfr

!	climate conditions
	real precp,rain ! mm/hour
	real tair,TSOIL,ts	   ! updated every hour
!	output from canopy model
	real evap,transp
	real evaptr,TEVAP,AEVAP
!	output variables
	real wscontent,fwsoil,topfws,omega,topomega,omega_S
	real fw(10),ome(10),W_signal

!	omega: (wscontent-wiltpt)/(fldcap-wiltpt)
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


	WILTPT=wsmin/100.0
	FLDCAP=wsmax/100.0
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

!C ** Determine which layer has been reached by the root system. 
!    Layer volume (cm3)
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

! *** water infiltration through layers

       infilt=precp  !mm/hour
!
!     Loop over all soil layers.
	TWTADD=0
	roff_layer=0.0
      do i=1,10 

         IF(infilt.GT.0.0)THEN
!		  Add water to this layer, pass extra water to the next.
            WTADD=AMIN1(INFILT,wtdeficit(i)*thksl(i)*10.0) ! from cm to mm
!			change water content of this layer
            WCL(i)=(WCL(i)*(thksl(i)*10.0)+WTADD)/(thksl(i)*10.0)
            FWCLN(I)=WCL(I)       !  /VOLUM(I)! update fwcln of this layer
		  TWTADD=TWTADD+WTADD	!calculating total added water to soil layers (mm)
            INFILT=INFILT-WTADD !update infilt
         END IF

!	produce runoff during infiltration
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

!	runoff
	runoff=INFILT + roff_layer   !precp-TWTADD + roff_layer   !weng 10072006

!	water redistribution among soil layers
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
     &				  *(1.0-omegaL(i+1))
			exchangeL=AMIN1(supply,demand)
			wsc(i)=wsc(i)- exchangeL
			wsc(i+1)=wsc(i+1)+ exchangeL
			wcl(i)=wsc(i)/(THKSL(i)*10.0)+wiltpt
			wcl(i+1)=wsc(i+1)/(THKSL(i+1)*10.0)+wiltpt
		endif
	enddo

!		calculate evap demand by eq.24 of Seller et al. 1996 (demand)

	if(wcl(1).LT.wiltpt)then
	     evap=0.0
	else
		Rsoil=10.1*exp(1.0/wcl(1))
		Rd=   20.5 !*exp(LAI/1.5)!LAI is added by Weng
		P=101325.0  !Pa, atmospheric pressure
		density=1.204 !kg/m3
		la=(2.501-0.00236*Tair)*1000000.0 !J/kg
		sp_heat=1012.0  !J/kg/K
		psychro=1628.6*P/la

		evap=1.0*esat(tair)*(1.0-RH/100.0)/
     &         (Rsoil+Rd)*density*sp_heat/psychro/la*3600.0
	endif

!  *** Soil evaporation; SRDT(I) for contribution of each layer. 
!     Units here are g H2O m-2 layer-1 h-1.
	Twater=0
	do i=1,10
		wsc(i)=(wcl(i)-wiltpt)*THKSL(I)*10.0
		Twater=Twater+wsc(i)  ! total water in soils,mm
	enddo

	Tsrdt=0.0
      DO i=1,10
!		Fraction of SEVAP supplied by each soil layer
			SRDT(I)=EXP(-4.73*(DEPTH(I)-THKSL(I)/2.0)/100.0)/1.987
!			SRDT(I)=AMAX1(0.0,SRDT(I)*(wcl(i)-wiltpt)) !*THKSL(I))
			Tsrdt=Tsrdt+SRDT(i)/(i*i)  ! to normalize SRDT(i)
      enddo

	do i=1,10
		SRDT(i)=SRDT(i)/Tsrdt
	enddo

	do i=1,10
         EVAPL(I)=Amax1(AMIN1(evap*SRDT(i),wsc(i)),0.0)  !mm
         DWCL(I)=EVAPL(I)/(THKSL(I)*10.0) !ratio
	enddo

!	update water content of every layer
	do i=1,10
		wcl(i)=wcl(i)-DWCL(i)
	enddo

!	the actual evapration
	evap=0.0	
	do i=1,10
         evap=evap+EVAPL(I)
	enddo


!     WATER UPTAKE by plant roots,Weng, 2.13.2006, a passive proccess
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

!     output (fwsoil,topfws,omega) which would be used by canopy model
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

!	a new approach for calculating fwsoil
	do i=1,nfr
		ome(i)=(wcl(i)-WILTPT)/(FLDCAP-WILTPT)
		ome(i)=AMIN1(1.0,AMAX1(0.0,ome(i)))
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
c
c	***************************************************************************

!=================================================================================================
!=================================================================================================
!****************************************************************************
      subroutine consts(pi,tauL,rhoL,rhoS,emleaf,emsoil,
     &   Rconst,sigma,cpair,Patm,Trefk,H2OLv0,airMa,H2OMw,chi,Dheat,
     &   wleaf,gsw0,Vcmx0,eJmx0,theta,conKc0,conKo0,Ekc,Eko,o2ci,
     &   Eavm,Edvm,Eajm,Edjm,Entrpy,gam0,gam1,gam2)
     
      real tauL(3), rhoL(3), rhoS(3)
      pi = 3.1415926
!     physical constants
!     optical properties
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
! plant parameters
      gsw0 = 1.0e-2                !g0 for H2O in BWB model
      eJmx0 = Vcmx0*2.7            !@20C Leuning 1996 from Wullschleger (1993)
      theta = 0.9
      wleaf=0.01                   !leaf width (m)

! thermodynamic parameters for Kc and Ko (Leuning 1990)
      conKc0 = 302.e-6                !mol mol^-1
      conKo0 = 256.e-3                !mol mol^-1
      Ekc = 59430.                 !J mol^-1
      Eko = 36000.                 !J mol^-1
!     Erd = 53000.                 !J mol^-1
      o2ci= 210.e-3                 !mol mol^-1

! thermodynamic parameters for Vcmax & Jmax (Eq 9, Harley et al, 1992; #1392)
      Eavm = 116300.               !J/mol  (activation energy)
      Edvm = 202900.               !J/mol  (deactivation energy)
      Eajm = 79500.                !J/mol  (activation energy) 
      Edjm = 201000.               !J/mol  (deactivation energy)
      Entrpy = 650.                !J/mol/K (entropy term, for Jmax & Vcmax)

! parameters for temperature dependence of gamma* (revised from von Caemmerer et al 1993)
      gam0 = 28.0e-6               !mol mol^-1 @ 20C = 36.9 @ 25C
      gam1 = .0509
      gam2 = .0010
      return
      end



!****************************************************************************
!****************************************************************************
      real function esat(T)
!* returns sat vapour pressure in Pa
      esat=610.78*exp(17.27*T/(T+237.3))
      return
      end

!****************************************************************************
      real function evapor(Td,Tw,Patm)
!     returns vapour pressure in Pa from wet & dry bulb temperatures
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

!****************************************************************************
!c Reed et al (1976, J appl Ecol 13:925) equation for temperature response
!c used for Vcmax and Jmax
      real function VJtemp(Tlf,TminVJ,TmaxVJ,ToptVJ,VJmax0)
      if(Tlf.lt.TminVJ) Tlf=TminVJ   !constrain leaf temperatures between min and max
      if(Tlf.gt.TmaxVJ) Tlf=TmaxVJ
      pwr=(TmaxVJ-ToptVJ)/(ToptVj-TminVj)
      VJtemp=VJmax0*((Tlf-TminVJ)/(ToptVJ-TminVJ))*
     &       ((TmaxVJ-Tlf)/(TmaxVJ-ToptVJ))**pwr 
      return
      end

!****************************************************************************
      real function fJQres(eJmx,alpha,Q,theta)
      AX = theta                                 !a term in J fn
      BX = alpha*Q+eJmx                          !b term in J fn
      CX = alpha*Q*eJmx
	
	                          !c term in J fn
	if(BX*BX-4.*AX*CX.lt.0.0)then
		fJQres = BX/(2.0*AX)           !Weng 09132006
	else
	   fJQres = (BX-SQRT(BX*BX-4.*AX*CX))/(2.0*AX) !Mid=BX*BX-4.*AX*CX
	endif


      return
      end
!
*************************************************************************
      real function EnzK(Tk,Trefk,EnzK0,Rconst,Eactiv)
      EnzK = EnzK0*EXP((Eactiv/(Rconst* Trefk))*(1.-Trefk/Tk))
      return
      end
!
!*************************************************************************
      real function sinbet(doy,slat,pi,timeh)
! sin(bet), bet = elevation angle of sun
! calculations according to Goudriaan & van Laar 1994 P30
      rad = pi/180.
! sine and cosine of latitude
      sinlat = sin(rad*slat)
      coslat = cos(rad*slat)
! sine of maximum declination
      sindec=-sin(23.45*rad)*cos(2.0*pi*(doy+10.0)/365.0)
      cosdec=sqrt(1.-sindec*sindec)
!     terms A & B in Eq 3.3
      A = sinlat*sindec
      B = coslat*cosdec
      sinbet = A+B*cos(pi*(timeh-12.)/12.)
      return
      end

!*************************************************************************
      subroutine yrday(doy,hour,slat,radsol,fbeam)
      pi=3.14159256
      pidiv=pi/180.0
      slatx=slat*pidiv
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
      if(tmprat.gt.0.22.and.tmprat.le.0.35) then
        fdiff=1.0-6.4*(tmprat-0.22)*(tmprat-0.22)
      endif
      if(tmprat.gt.0.35.and.tmprat.le.tmpK) then
        fdiff=1.47-1.66*tmprat
      endif
      if(tmprat.ge.tmpK) then
        fdiff=tmpR
      endif
      fbeam=1.0-fdiff
      if(fbeam.lt.0.0) fbeam=0.0
      return
      end
!*************************************************************************
