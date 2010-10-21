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
      open(61,file='TECO_C_daily.csv')
      open(62,file='TECO_H2O_daily.csv')
      open(63,file='TECO_pools_C.csv')
      read(13,11) commts
      write(61,*)'d,LAI,GP,NP,N_L,N_S,N_R,RaL,RaR,
     &RhF,Rhs1,Rhs2,Rhs3,NE,bmR,bmL,bmS'
      write(62,*)'d,P,Tr,E,R,ws,fw,topfw,omega, 
     &wc1,wc2,wc3,wc4,wc5,wc6,wc7,wc8,wc9,wc10'
      write(63,*)'y,Q_l,Q_w,Q_r1,Q_r2,Q_r3,Q_cs,Q_f,Q_s1,Q_s2,Q_s3'

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

			 call canopy(gpp,evap,transp,Acanop,   ! outputs
     &		   fwsoil,topfws,wscontent, ! from soil model
     &		   LAI,totLAI,Sps,
     &           doy,hour,radsol,tair,dair,! from climate data file,including 
     &           windU0,rain,wethr,
     &           Rnet,G,Esoil,Hcrop,Ecstot,Anet,
     &           Tsoil,DepH2O,
     &           wsmax,wsmin,  !constants specific to soil and plant
     &		   slat,co2ca,ioput,a1,Ds0,VcmxN,extkU,xfang,alpha,
     &           stom_n,bmcrop,bmleaf,CNtop,ht_can,
     &           pi,tauL,rhoL,rhoS,emleaf,emsoil,
     &           Rconst,sigma,cpair,Patm,Trefk,H2OLv0,
     &		   airMa,H2OMw,chi,Dheat,wleaf,gsw0,eJmx0,
     &           theta,conKc0,conKo0,Ekc,Eko,o2ci,
     &           Eavm,Edvm,Eajm,Edjm,Entrpy,gam0,gam1,gam2)


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

		call plantgrowth(NSC,NSCmin,NSCmax,GLmax,GRmax,
     &                       GSmax,SNamax,SNrs,Ta,Ta_cur,
     &                       Twair,omega,LAI,LAIMAX,LAIMIN,
     &				       SLA,bmleaf,bmroot,bmstem,
     &			           bmplant,NPP,Storage,GDD5,
     &                       stor_use,onset,accumulation,
     &				       gddonset,Sps,fnsc,L_add,L_fall,
     &				       S_fall,GrowthR,RS,alpha_L,
     &                       alpha_S,alpha_R)

		NSC_bm=NSC/bmplant
		ta=Tlin
!+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
!     THE Fourth PART:
!		simulating C influx allocation in pools, step is daily

		call c_transfer(GPP,rho,NPP,			! from canopy model,C influx
     &						Ta,Ts,omega,	! from soil model, soil conditions
     &                        L_add,L_fall,S_fall,LAI,SNdcomp,
     &                        alpha_L,alpha_S,alpha_R,SLA,
     &						RaL,RaS,RaR,
     &						Q_leaf,Q_fine,Q_wood,Q_coarse, !pools size
     &						Q_root1,Q_root2,Q_root3,
     &						Q_soil1,Q_soil2,Q_soil3,
     &						d_ql,d_qw,d_qr1,d_qr2,d_qr3, ! changes of every pool
     &						d_qf,d_qc,d_qs1,d_qs2,d_qs3,
     &						zeta1,zeta2,zeta3,           ! for Nitrogen submodel
     &						tau_L,tau_W,tau_R1,tau_R2,tau_R3,
     &						tau_F_a,tau_C_a,
     &						tau_S1_a,tau_S2_a,tau_S3_a,
     &						eta,theta_F,theta_C,theta_S1,theta_S2,
     &						Resp_f,Resp_c,Resp_s1,Resp_s2,Resp_s3)

	  			Q_leaf=Q_leaf + d_ql
				Q_fine=Q_fine + d_qf
				Q_wood=Q_wood + d_qw
				Q_coarse=Q_coarse + d_qc
				Q_root1=Q_root1 + d_qr1
				Q_root2=Q_root2 + d_qr2
				Q_root3=Q_root3 + d_qr3
				Q_soil1=Q_soil1 + d_qs1
				Q_soil2=Q_soil2 + d_qs2
				Q_soil3=Q_soil3 + d_qs3
				Q_soil=Q_soil1+Q_soil2+Q_soil3
				bmroot=(Q_root1+Q_root2+Q_root3)/0.45
				bmleaf=Q_leaf/0.45
				bmstem=Q_wood/0.45
!	    intigrating annual fluxes
		NEE=NPP-Resp_f-Resp_c-Resp_s1-Resp_s2-Resp_s3
		gpp_yr=gpp_yr+gpp_t
		NPP_yr=NPP_yr+NPP
		NEE_yr=NEE_yr+NEE
		RaL_yr=RaL_yr+RaL
		RaR_yr=RaR_yr+RaR
	    RhF_yr=RhF_yr+Resp_f
		RhC_yr=RhC_yr+Resp_c
		RhS1_yr=RhS1_yr+Resp_s1
		RhS2_yr=RhS2_yr+Resp_s2
		RhS3_yr=RhS3_yr+Resp_s3
		NPPL_yr=NPPL_yr+NPP*alpha_L
		NPPR_yr=NPPR_yr+NPP*alpha_R
		NPPS_yr=NPPS_yr+NPP*alpha_S

		rain_yr=rain_yr+rain_t
		runoff_yr=runoff_yr+Trunoff
		evap_yr=evap_yr+evap_t
		transp_yr=transp_yr+transp_t
		if(days.gt.120.and.days.le.300)then
			omega_yr=omega_yr+omega_S
			ws_yr=ws_yr+wscontent
			wcl_yr=wcl_yr+wcl
			fw_yr=fw_yr+fwsoil
			AW_yr=AW_yr+AW
			if(fwsoil.lt.0.95)d_drought=d_drought+1
		endif

!	output results of canopy and soil models
		if((yr.gt.writer).and.(yr.le.(writer+yr_data)))then
			write(61,161)doy,LAI,gpp_t,NPP,alpha_L*NPP,alpha_S*NPP,
     &				alpha_R*NPP,RaL,RaR,Resp_f,Resp_s1,Resp_s2,
     &				Resp_s3,NEE,bmroot,bmleaf,bmstem
  
			write(62,162)doy,precp_t,transp_t,evap_t,Trunoff,
     &				 wscontent,fwsoil,topfws,omega,
     &                 (wcl(i),i=1,5)

		endif


	enddo	!end of a year

!	output carbon content in the carbon pools
	    write(63,163)yr,Q_leaf,Q_wood,Q_root1,Q_root2,Q_root3,
     &				 Q_coarse,Q_fine,Q_soil1,Q_soil2,Q_soil3

!	    restore the initial values of phenology
		storage=accumulation
		stor_use=Storage/25.0
		accumulation=0.0
		onset=0
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

	close(61)
	close(62)
	close(63)
	
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
!c	a sub-model for calculating C flux and H2O flux of a canopy
!	adapted from a two-leaf canopy model developed by Wang Yingping
	subroutine canopy(gpp,evap,transp,Acanop,   ! outputs
     &		   fwsoil,topfws,wscontent, ! from soil model
     &		   LAI,totLAI,Sps,
     &           doy,hour,radsol,tair,dair,! from climate data file,including 
     &           windU0,rain,wethr,
     &           Rnet,G,Esoil,Hcrop,Ecstot,Anet,
     &           Tsoil,DepH2O,
     &           wsmax,wsmin,  !constants specific to soil and plant
     &		   slat,co2ca,ioput,a1,Ds0,Vcmx0,extkU,xfang,alpha,
     &           stom_n,bmcrop,bmleaf,CNtop,ht_can,
     &           pi,tauL,rhoL,rhoS,emleaf,emsoil,
     &       Rconst,sigma,cpair,Patm,Trefk,H2OLv0,airMa,H2OMw,chi,Dheat,
     &   wleaf,gsw0,eJmx0,theta,conKc0,conKo0,Ekc,Eko,o2ci,
     &   Eavm,Edvm,Eajm,Edjm,Entrpy,gam0,gam1,gam2)

	real gpp,evap,transp,LAI
      real tauL(3),rhoL(3),rhoS(3),reffbm(3),reffdf(3)
      real extkbm(3),extkdm(3)
      real Radabv(2),Qcan(3,2),Qcan0(3)
      real Acan(2),Ecan(2),Hcan(2),Tcan(2), Gbwcan(2), Gswcan(2)

!C  extra variables used to run the model for the wagga data
      real totLAI(365),bmleaf,bmcrop(365),CNtop(365)
      real ht_can(365)
	real topfws        ! from siol subroutine	
      integer idoy,ihour,ileaf,ioput
      integer jrain,i,j,k
!c     additional arrays to allow output of info for each layer
      real RnStL(5),QcanL(5),RcanL(5),AcanL(5),EcanL(5),HcanL(5)
      real GbwcL(5),GswcL(5),hG(5),hIL(5)
      real Gaussx(5),Gaussw(5),Gaussw_cum(5)      
      character(len=80) commts
!     Normalised Gaussian points and weights (Goudriaan & van Laar, 1993, P98)
!     5-point
      data Gaussx/0.0469101,0.2307534,0.5,0.7692465,0.9530899/
      data Gaussw/0.1184635,0.2393144,0.2844444,0.2393144,0.1184635/
	data Gaussw_cum/0.11846,0.35777,0.64222,0.88153,1.0/
!     calculate beam fraction in incoming solar radiation
      call  yrday(doy,hour,slat,radsol,fbeam)
!     check if canopy wet (wethr =-1)  - if so skip it
      jrain=int(wethr)
      if(jrain.ge.0)then
         idoy=int(doy)
         hours=idoy*1.0+hour/24.0
         coszen=sinbet(doy,slat,pi,hour)             !cos zenith angle of sun
!        set windspeed to the minimum speed to avoid zero Gb
         if(windU0.lt.0.01) windU0=0.01
!        calculate soil albedo for NIR as a function of soil water (Garratt pp292)
         if(topfws.gt.0.5) then
            rhoS(2)=0.18
         else
            rhoS(2)=0.52-0.68*topfws
         endif

!        assign plant biomass and leaf area index at time t
!        assume leaf biomass = root biomass
         FLAIT =LAI ! totLAI(idoy)
         bmstem= bmcrop(idoy) - bmleaf
         bmroot= bmleaf
         eairP=esat(Tair)-Dair                !air water vapour pressure
         radabv(1)=0.5*radsol                 !(1) - solar radn
         radabv(2)=0.5*radsol                 !(2) - NIR

!        reset variables
         Acanop=0.0
         Ecanop=0.0
         Hcanop=0.0
         fslt=0.0
         fsltx=0.0

!        call multilayer model of Leuning - uses Gaussian integration but radiation scheme
         call xlayers(Sps,Tair,Dair,radabv,G,Esoil,fbeam,eairP,
     &		   windU0,co2ca,fwsoil,FLAIT,coszen,idoy,hours,
     &           tauL,rhoL,rhoS,xfang,extkd,extkU,wleaf,
     &           Rconst,sigma,emleaf,emsoil,theta,a1,Ds0,
     &           cpair,Patm,Trefk,H2OLv0,AirMa,H2OMw,Dheat,
     &           gsw0,alpha,stom_n,
     &           Vcmx0,eJmx0,conKc0,conKo0,Ekc,Eko,o2ci,
     &           Eavm,Edvm,Eajm,Edjm,Entrpy,gam0,gam1,gam2,
     &           extKb,
     &           Rnst1,Qcan1,Acan1,Ecan1,Hcan1,Gbwc1,Gswc1,Tleaf1,
     &           Rnst2,Qcan2,Acan2,Ecan2,Hcan2,Gbwc2,Gswc2,Tleaf2,
     &           Rcan1,Rcan2,Rsoilabs,Hsoil,
     &           RnStL,QcanL,RcanL,AcanL,EcanL,HcanL,GbwcL,GswcL)

!         convert from LAI to height (m) for IREX (LAI accumulated from bottom up)
	    do ng=1,5  
             hG(ng)=Gaussw_cum(ng)  !normalised heights in weight domain
             hIL(ng)=0.2*ng         !normalised heights for Inverse Lagrangian analysis
	    end do	    
!         Interpolate between Gaussian distances to those used in Inverse analysis.
!         Note the use of Gaussw_cum. These are the normalised distances on the integration function
!         Integral = sum(Yi*Wgi), where Y is the function and W is the weight.
	    AcanL(1)=AcanL(1)+(hIL(1)-hG(1))*(AcanL(2)-AcanL(1))
     &                     /(hG(2)-hG(1))
	    AcanL(2)=AcanL(2)+(hIL(2)-hG(2))*(AcanL(3)-AcanL(2))
     &                     /(hG(3)-hG(2))
	    AcanL(3)=AcanL(2)+(hIL(3)-hG(2))*(AcanL(3)-AcanL(2))
     &                     /(hG(3)-hG(2))
	    AcanL(4)=AcanL(3)+(hIL(4)-hG(3))*(AcanL(4)-AcanL(3))
     &                     /(hG(4)-hG(3))

	    EcanL(1)=EcanL(1)+(hIL(1)-hG(1))*(EcanL(2)-EcanL(1))
     &                     /(hG(2)-hG(1))
	    EcanL(2)=EcanL(2)+(hIL(2)-hG(2))*(EcanL(3)-EcanL(2))
     &                     /(hG(3)-hG(2))
	    EcanL(3)=EcanL(2)+(hIL(3)-hG(2))*(EcanL(3)-EcanL(2))
     &                     /(hG(3)-hG(2))
	    EcanL(4)=EcanL(3)+(hIL(4)-hG(3))*(EcanL(4)-EcanL(3))
     &                     /(hG(4)-hG(3))
	    HcanL(1)=HcanL(1)+(hIL(1)-hG(1))*(HcanL(2)-HcanL(1))
     &                     /(hG(2)-hG(1))
	    HcanL(2)=HcanL(2)+(hIL(2)-hG(2))*(HcanL(3)-HcanL(2))
     &                     /(hG(3)-hG(2))
	    HcanL(3)=HcanL(2)+(hIL(3)-hG(2))*(HcanL(3)-HcanL(2))
     &                     /(hG(3)-hG(2))
	    HcanL(4)=HcanL(3)+(hIL(4)-hG(3))*(HcanL(4)-HcanL(3))
     &                     /(hG(4)-hG(3))
!c        adjust CO2 fluxes for each Layer for soil respiration
!c        and adjust LE and H as well
          mol_mass=44.0/1000.0
          do ng=1,5
!c           AcanL(ng)=(-AcanL(ng)*1.e6+Rsoil+Rcrop)*mol_mass       ! CO2 flux at top of each layer mg CO2/m2/s
	       EcanL(ng)=EcanL(ng)+Esoil
	       HcanL(ng)=HcanL(ng)+Hsoil
	    end do
!         fraction sunlit leaves integrated over canopy
          fsltx=(1.0-exp(-flait*extkb))/(extkb*flait)  
!         sum sunlit & shaded fluxes, & mean canopy temperature
!         multilayer model 
          Acan1=Acan1*1.0e6                     !umol CO2/m2/s    
          Acan2=Acan2*1.0e6
          Acanop=Acan1+Acan2					 ! 03/21/2006 Weng 
          Qcan1=Qcan1                           !umol quanta/m2/s
          Qcan2=Qcan2                 
          Qcanop=Qcan1+Qcan2 
          Ecanop=Ecan1+Ecan2                    !W/m2
          Tcanop=Tleaf1*fsltx+Tleaf2*(1.0-fsltx) !correction by ypw(12/9/96)
          Hcanop=Hcan1+Hcan2                    !W/m2
	    if(Rsoilabs.LT.0.0) Rsoilabs=0.0
	    if(Ecanop.LT.0.0)Ecanop=0.0
	    gpp=Acanop*3600.0*12.0/1.0e6 ! every hour
	    transp=Ecanop*3600.0/((2.501-0.00236*Tair)*1000000.0)  ! mm H2O /hour
	    if(transp.lt.0.0)transp=0.0
	    evap=0.9*Rsoilabs*3600.0/2260.0/1000.0     ! EVERY hour
	    if(evap.lt.0.0)evap=0.0
      else
19       continue
      endif

101   format(1x,f7.2,1x,i4,2x,f5.1,1x,40(f8.4,2x))
201   format(1x,f7.2,1x,i4,2x,f5.1,1x,40(f10.4,2x))
301   format(1x,f8.3,1x,i4,2x,7(f8.3,2x))
401   format(15(f8.3,2x))

	return
      end

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
	subroutine plantgrowth(NSC,NSCmin,NSCmax,GLmax,GRmax,
     &                       GSmax,SNamax,SNrs,Ta,Ta_cur,
     &                       Twair,omega,LAI,LAIMAX,LAIMIN,
     &				       SLA,bmleaf,bmroot,bmstem,
     &			           bmplant,NPP,Storage,GDD5,
     &                       stor_use,onset,accumulation,
     &				       gddonset,Sps,fnsc,L_add,L_fall,
     &				       S_fall,GrowthR,RS,alpha_L,
     &                       alpha_S,alpha_R)

	implicit none
	real NSC,NSCmin,NSCmax,fnsc,NSC_bm,SNamax,SNrs
	real Storage,GDD5,stor_use,accumulation,gddonset
	integer onset,duration,offset,dormancy
	real GLmax,GRmax,GSmax
	real GrowthL,GrowthR,GrowthS,GrowthP
      real Ta,Ta_cur,omega,LAI,LAIMAX,LAIMIN,SLA
      real bmleaf,bmroot,bmstem,bmplant,NPP
	real bmL,bmR,bmP,bmS
      real St,Sw,Ss,Sn,SL_rs,SR_rs,Slai,Sps
	real RS,RS0,RSw,RSwn
	real gamma_W,gamma_Wmax,gamma_T,gamma_Tmax,gamma_N
	real beta_T,Tcold
	real bW,bT,W
	real L_fall,L_add,add,NL_fall,NL_add,S_fall
	real alpha_L,alpha_S,alpha_R,alpha_St
	real Twair(7),Twsoil(7),Tavg
	integer i

	bmL=bmleaf
	bmR=bmRoot
	bmS=bmStem
	bmP=bmPlant

	if(bmL.lt.NSC/0.45*0.5)bmL=NSC/0.45*0.5
	if(bmR.lt.NSC/0.45*0.5)bmR=NSC/0.45*0.5

	GLmax=0.1  !relative growth rate
	GRmax=0.1 !
	GSmax=0.1

	gamma_Wmax=0.05
	gamma_Tmax=0.2

	gamma_N=1.0/(365.0*0.75)
	bW=4.0
	bT=3.0
	Tcold=17.0
	RS0=0.75


!	phenology
	if((GDD5.gt.gddonset).and.onset.eq.0.and.storage.gt.stor_use) then
		onset=1
	endif

	if((onset.eq.1).and.(storage.gt.stor_use)) then
		add=stor_use
		storage=storage-add
	else
		add=0.0
		onset=0
	endif

	if((storage.LE.stor_use).and.(LAI.gt.(LAIMAX*0.3))
     &	.and.(accumulation.lt.(LAIMAX*0.25)/SLA*0.5))then	!
		alpha_St=0.015
	else
		alpha_St=0.0
	endif


	accumulation=accumulation+NSC*alpha_St
	NSC=NSC*(1-alpha_St)


!	calculating scaling factor limiting photosynthesis
	if(NSC.le.NSCmin)fnsc=0.0
	if(NSC.ge.NSCmax)fnsc=1.0
	if((NSC.lt.NSCmax).and.(NSC.gt.NSCmin))then 
		fnsc=(NSC-NSCmin)/(NSCmax-NSCmin)
	endif
	Sps=1.0-fnsc*fnsc*fnsc*fnsc
	sps=AMAX1(0.001,sps)

	St=AMAX1(0.0,AMIN1(1.0,(Ta-12.0)/(35.0-12.0)))
	Sw=omega
	W=AMIN1(1.0,3.333*omega)
	Ss=AMIN1(1.0,1.5*fnsc)

	RS=bmR/(bmS+bmL) !
	RSwn=RS0*(2.0-omega)*(SNrs+0.5)

	SL_rs=RS  /(RS+RSwn)
	SR_rs=RSwn/(RS+RSwn)
	Slai=amin1(1.0,3.33*(LAIMAX-LAI)/(LAIMAX-LAIMIN))

	GrowthL=GLmax*bmL*St*Sw*SL_rs*Ss*Slai*0.45 !*(1.5-SNrs)
	GrowthR=GRmax*bmR*St*Sw*SR_rs*Ss*0.45 !*(SNrs+0.5), 5/14/2006
	GrowthS=GSmax*bmL*St*Sw*Ss*(1.0-Slai)*0.45   !Weng 11/27/2006 *(1.0-Slai)

	if(GrowthL.LT.0.0)GrowthL=0.0
	if(GrowthR.LT.0.0)GrowthR=0.0
	if(GrowthS.LT.0.0)GrowthS=0.0

	GrowthP=GrowthL + GrowthR + GrowthS
	if(GrowthP.gt.NSC)then
		GrowthL=NSC*GrowthL/GrowthP
		GrowthR=NSC*GrowthR/GrowthP
		GrowthS=NSC*GrowthS/GrowthP
	endif
	 
	NSC=NSC - GrowthL - GrowthR - GrowthS

	bmleaf=bmleaf+(GrowthL+add)/0.45
	bmroot=bmroot+GrowthR/0.45
	bmstem=bmstem+GrowthS/0.45
	bmplant=bmleaf+bmroot+bmstem
	LAI=bmleaf*SLA

	NPP = GrowthL + add + GrowthR + GrowthS
	if(NPP.eq.0.0)then
		alpha_L=0.0
		alpha_S=0.0
		alpha_R=0.0
	else
		alpha_L=(GrowthL+add)/NPP
		alpha_S=GrowthS/NPP
		alpha_R=GrowthR/NPP
	endif

c	leaves fall
	if(Ta.gt.Tcold) then
		beta_T=1.0
	else 
		if(Ta.gt.(Tcold-5.0)) beta_T=(Ta-Tcold+5.0)/5.0
		if(Ta.LE.(Tcold-5.0)) beta_T=0.0
	endif

	if(LAI.gt.LAIMIN) then
		gamma_W=gamma_Wmax*((1-W)**bW)
		gamma_T=gamma_Tmax*((1-beta_T)**bT)
		gamma_N=1.0/(365.0*0.75)
	else
		gamma_W=0.0
		gamma_T=0.0
		gamma_N=0.0
	endif
	L_fall=bmleaf*(gamma_W+gamma_T-gamma_W*gamma_T+gamma_N)*0.45
	L_add=GrowthL + add
	S_fall=bmStem*(gamma_W+gamma_T-gamma_W*gamma_T+gamma_N)*0.45

	return
	end


c
c	***************************************************************************

c	C allocation and residence in different pools	
	subroutine c_transfer(GPP,rho,NPP,			! from canopy model,C influx
     &						Ta,Ts,omega,	! from soil model, soil conditions
     &                        L_add,L_fall,S_fall,LAI,SNdcomp,
     &                        alpha_L,alpha_S,alpha_R,SLA,
     &						RaL,RaS,RaR,
     &						Q_leaf,Q_fine,Q_wood,Q_coarse, !pools size
     &						Q_root1,Q_root2,Q_root3,
     &						Q_soil1,Q_soil2,Q_soil3,
     &						d_ql,d_qw,d_qr1,d_qr2,d_qr3, ! changes of every pool
     &						d_qf,d_qc,d_qs1,d_qs2,d_qs3,
     &						zeta1,zeta2,zeta3,           ! for Nitrogen submodel
     &						tau_L,tau_W,tau_R1,tau_R2,tau_R3,
     &						tau_F_a,tau_C_a,
     &						tau_S1_a,tau_S2_a,tau_S3_a,
     &						eta,theta_F,theta_C,theta_S1,theta_S2,
     &						Resp_f,Resp_c,Resp_s1,Resp_s2,Resp_s3)

c     dummy variables
	real GPP,L_fall,S_fall,L_add,alpha_S,LAI,SLA,SNdcomp
	real rho		! ratio of respiration to GPP
	real d_ql,d_qw,d_qr1,d_qr2,d_qr3
	real d_qf,d_qc,d_qs1,d_qs2,d_qs3

c	variables used in subroutine c_transfer()
	real NPP
	real GPP_annual,NPP_annual
	real NPP_L,NPP_W,NPP_R1,NPP_R2,NPP_R3

	real alpha_L,alpha_W,alpha_R
	real zeta1,zeta2,zeta3
	real tau_L,tau_W,tau_R1,tau_R2,tau_R3
	real tau_F,tau_C,tau_S1,tau_S2,tau_S3
	real eta
	real theta_F,theta_C,theta_S1,theta_S2


c     the fraction of annual NPP at the kth pool after traversing upstream pools
	real f_fine,f_coarse,f_soil1,f_soil2,f_soil3

c     the fraction of C-flux which enters the atmosphere from the kth pool
	real f_CO2_fine,f_CO2_coarse,f_CO2_soil1,f_CO2_soil2,f_CO2_soil3

c     monthly heterotrophic respiration of F,C,S1~3
	real Resp_f,Resp_c,Resp_s1,Resp_s2,Resp_s3

c     the actual turnover time dependented on temperature and soil moisture
	real tau_F_a,tau_C_a,tau_S1_a,tau_S2_a,tau_S3_a

c     the variables relative to soil moisture calcualtion
	real omega   !  soil moisture
	real S_omega !  average values of the moisture scaling functions
	real S_t     !  average values of temperature scaling functions
	real Ta,Ts   ! soil temperature
	real S_w_min    ! minimum decomposition rate at zero plant available water
	real texture    ! soil texture

	real Tref,T0,T,E0,mid

c     for circulation
	integer i,j,k,n,m

	integer day,week,month,year

	Tref=50.0
	T0=-2.0
	E0=2.1
	if(Ta.ge.Tref)T=Tref-0.001
	if(Ta.le.T0) then
		T=T0+0.001
	else
		T=Ta
	endif

	alpha_W=alpha_S

	zeta1=0.5
	zeta2=0.35
	zeta3=0.15

	tau_L=0.75*365.0		! the unit is daily
	tau_W=tau_L    !176.68*365.0

	tau_R1=0.6*365.0
	tau_R2=0.5*365.0
	tau_R3=0.4*365.0
	tau_F=3.1*365.0
	tau_C=22.86*365.0
	tau_S1=50.6*365.0
	tau_S2=80.94*365.0
	tau_S3=120.79*365.0

	eta=1.0 ! 0.15
	
	theta_F=0.7
	theta_C=0.0  !0.7
	theta_S1=0.05
	theta_S2=0.05

c	calculating soil scaling factors, S_omega and S_tmperature
	S_w_min=0.6 !minimum decomposition rate at zero soil moisture
	S_omega=S_w_min + (1-S_w_min)*omega !*SQRT(4.0*omega-4.0*omega*omega)
c	S_omega=S_w_min + (1-S_w_min)*SQRT(4.0*omega-4.0*omega*omega)

	S_t=1.0-1/(1+19.0*exp(-0.18*Ts))

c		they should be coupled with theoritical tau
		tau_F_a=tau_F/S_omega* S_T/(SNdcomp+0.5)
		tau_C_a=tau_C/S_omega*S_T/(SNdcomp+0.5)
		tau_S1_a=tau_S1/S_omega*S_T/(SNdcomp+0.5)
		tau_S2_a=tau_S2/S_omega*S_T/(SNdcomp+0.5)
		tau_S3_a=tau_S3/S_omega*S_T/(SNdcomp+0.5)


!     the fraction of C-flux which enters the atmosphere from the kth pool
	f_CO2_fine  = 1 - theta_F
	f_CO2_coarse= 1 - eta - theta_C
	f_CO2_soil1 = 1 - theta_S1
	f_CO2_soil2 = 1 - theta_S2
	f_CO2_soil3 = 1


!	calculating NPP allocation and changes of each C pool


		   NPP_L=alpha_L*NPP            ! NPP allocation
		   NPP_W=alpha_S*NPP

		   NPP_R1=alpha_R*zeta1*NPP
		   NPP_R2=alpha_R*zeta2*NPP
		   NPP_R3=alpha_R*zeta3*NPP

		   d_ql=L_add - L_fall    ! daily change of each pool size
		   d_qw=NPP_W - S_fall
		   d_qR1=NPP_R1 - Q_root1/tau_R1
		   d_qR2=NPP_R2 - Q_root2/tau_R2
		   d_qR3=NPP_R3 - Q_root3/tau_R3

		   d_qf = L_fall+eta*S_fall-Q_fine/tau_F_a
		   d_qc = (1.0-eta)*S_fall-Q_coarse/tau_c_a
		   d_qs1 =Q_root1/tau_R1 + theta_F*Q_fine/tau_F_a
     &                +theta_C*Q_coarse/tau_C_a - Q_soil1/tau_S1_a
		   d_qs2 =Q_root2/tau_R2 + theta_S1*Q_soil1/tau_S1_a
     &                - Q_soil2/tau_S2_a
		   d_qs3 =Q_root3/tau_R3+theta_S2*Q_soil2/tau_S2_a 
     &                - Q_soil3/tau_S3_a


!     heterotrophic respiration from each pool
		   Resp_f =Q_fine/Tau_F_a * f_CO2_fine
		   Resp_c =Q_coarse/Tau_C_a * f_CO2_coarse
		   Resp_s1=Q_soil1/Tau_S1_a * f_CO2_soil1
		   Resp_s2=Q_soil2/Tau_S2_a * f_CO2_soil2
		   Resp_s3=Q_soil3/Tau_S3_a * f_CO2_soil3


	return
	end

!=================================================================================================
!=================================================================================================
!     subroutines used by canopy submodel


      subroutine xlayers(Sps,Tair,Dair,radabv,G,Esoil,fbeam,eairP,
     &           windU0,co2ca,fwsoil,FLAIT,coszen,idoy,hours,
     &           tauL,rhoL,rhoS,xfang,extkd,extkU,wleaf,
     &           Rconst,sigma,emleaf,emsoil,theta,a1,Ds0,
     &           cpair,Patm,Trefk,H2OLv0,AirMa,H2OMw,Dheat,
     &           gsw0,alpha,stom_n,
     &           Vcmx0,eJmx0,conKc0,conKo0,Ekc,Eko,o2ci,
     &           Eavm,Edvm,Eajm,Edjm,Entrpy,gam0,gam1,gam2,
     &           extKb,
     &           Rnst1,Qcan1,Acan1,Ecan1,Hcan1,Gbwc1,Gswc1,Tleaf1,
     &           Rnst2,Qcan2,Acan2,Ecan2,Hcan2,Gbwc2,Gswc2,Tleaf2,
     &           Rcan1,Rcan2,Rsoilabs,Hsoil,
     &           RnStL,QcanL,RcanL,AcanL,EcanL,HcanL,GbwcL,GswcL)

!     the multi-layered canopy model developed by 
!     Ray Leuning with the new radiative transfer scheme   
!     implemented by Y.P. Wang (from Sellers 1986)
!     12/Sept/96 (YPW) correction for mean surface temperature of sunlit
!     and shaded leaves
!     Tleaf,i=sum{Tleaf,i(n)*fslt*Gaussw(n)}/sum{fslt*Gaussw(n)} 
   
      real Gaussx(5),Gaussw(5)
	real layer1(5),layer2(5)
      real tauL(3),rhoL(3),rhoS(3),Qabs(3,2),Radabv(2),Rnstar(2)
      real Aleaf(2),Eleaf(2),Hleaf(2),Tleaf(2),co2ci(2)
      real gbleaf(2),gsleaf(2),QSabs(3,2),Qasoil(2)
      integer ng,nw
      real rhoc(3,2),reff(3,2),kpr(3,2),scatt(2)       !Goudriaan

!     additional arrays to allow output of info for each Layer
      real RnStL(5),QcanL(5),RcanL(5),AcanL(5),EcanL(5),HcanL(5),
     &     GbwcL(5),GswcL(5)
      
! Normalised Gaussian points and weights (Goudriaan & van Laar, 1993, P98)
! 5-point
      data Gaussx/0.0469101,0.2307534,0.5,0.7692465,0.9530899/
      data Gaussw/0.1184635,0.2393144,0.2844444,0.2393144,0.1184635/

!     reset the vairables
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
         
! aerodynamic resistance                                                
      raero=50./windU0                           

!     Ross-Goudriaan function for G(u) (see Sellers 1985, Eq 13)
      xphi1 = 0.5 - 0.633*xfang -0.33*xfang*xfang
      xphi2 = 0.877 * (1.0 - 2.0*xphi1)
      funG=xphi1 + xphi2*coszen                             !G-function: Projection of unit leaf area in direction of beam
      
      if(coszen.gt.0) then                                  !check if day or night
        extKb=funG/coszen                                   !beam extinction coeff - black leaves
	else
	  extKb=100.
	end if

! Goudriaan theory as used in Leuning et al 1995 (Eq Nos from Goudriaan & van Laar, 1994)
! Effective extinction coefficient for diffuse radiation Goudriaan & van Laar Eq 6.6)
      pi180=3.1416/180.
      cozen15=cos(pi180*15)
      cozen45=cos(pi180*45)
      cozen75=cos(pi180*75)
      xK15=xphi1/cozen15+xphi2
      xK45=xphi1/cozen45+xphi2
      xK75=xphi1/cozen75+xphi2
      transd=0.308*exp(-xK15*FLAIT)+0.514*exp(-xK45*FLAIT)+
     &       0.178*exp(-xK75*FLAIT)
      extkd=(-1./FLAIT)*alog(transd)
      extkn=extkd                                                       !N distribution coeff 


! canopy reflection coefficients (Array indices: first;  1=VIS,  2=NIR
!                                               second; 1=beam, 2=diffuse
      do nw=1,2                                                         !nw:1=VIS, 2=NIR
       scatt(nw)=tauL(nw)+rhoL(nw)                                      !scattering coeff
       kpr(nw,1)=extKb*sqrt(1.-scatt(nw))                               !modified k beam scattered (6.20)
       kpr(nw,2)=extkd*sqrt(1.-scatt(nw))                               !modified k diffuse (6.20)
       rhoch=(1.-sqrt(1.-scatt(nw)))/(1.+sqrt(1.-scatt(nw)))            !canopy reflection black horizontal leaves (6.19)
       rhoc15=2.*xK15*rhoch/(xK15+extkd)                                !canopy reflection (6.21) diffuse
       rhoc45=2.*xK45*rhoch/(xK45+extkd)
       rhoc75=2.*xK75*rhoch/(xK75+extkd)
       rhoc(nw,2)=0.308*rhoc15+0.514*rhoc45+0.178*rhoc75
       rhoc(nw,1)=2.*extKb/(extKb+extkd)*rhoch                          !canopy reflection (6.21) beam 
       reff(nw,1)=rhoc(nw,1)+(rhoS(nw)-rhoc(nw,1))                      !effective canopy-soil reflection coeff - beam (6.27)
     &            *exp(-2.*kpr(nw,1)*FLAIT) 
       reff(nw,2)=rhoc(nw,2)+(rhoS(nw)-rhoc(nw,2))                      !effective canopy-soil reflection coeff - diffuse (6.27)
     &            *exp(-2.*kpr(nw,2)*FLAIT)  
      enddo


!    isothermal net radiation & radiation conductance at canopy top - needed to calc emair
      call Radiso(flait,flait,Qabs,extkd,Tair,eairP,cpair,Patm,
     &            fbeam,airMa,Rconst,sigma,emleaf,emsoil,
     &            emair,Rnstar,grdn)

      TairK=Tair+273.2
      do 200 ng=1,5
         flai=gaussx(ng)*FLAIT
         call goudriaan(FLAI,coszen,radabv,fbeam,reff,kpr,
     &                  scatt,xfang,Qabs) 
     
!        isothermal net radiation & radiation conductance at canopy top
         call Radiso(flai,flait,Qabs,extkd,Tair,eairP,cpair,Patm,
     &               fbeam,airMa,Rconst,sigma,emleaf,emsoil,
     &               emair,Rnstar,grdn)
	
         windUx=windU0*exp(-extkU*flai)             !windspeed at depth xi
         scalex=exp(-extkn*flai)                    !scale Vcmx0 & Jmax0
         Vcmxx=Vcmx0*scalex
         eJmxx=eJmx0*scalex

         if(radabv(1).ge.10.0) then 	                   !check solar Radiation > 10 W/m2

!        leaf stomata-photosynthesis-transpiration model - daytime
         call agsean_day(Sps,Qabs,Rnstar,grdn,windUx,Tair,Dair,co2ca,
     &               wleaf,raero,theta,a1,Ds0,fwsoil,idoy,hours,
     &               Rconst,cpair,Patm,Trefk,H2OLv0,AirMa,H2OMw,Dheat,
     &               gsw0,alpha,stom_n,
     &               Vcmxx,eJmxx,conKc0,conKo0,Ekc,Eko,o2ci,
     &               Eavm,Edvm,Eajm,Edjm,Entrpy,gam0,gam1,gam2,
     &               Aleaf,Eleaf,Hleaf,Tleaf,gbleaf,gsleaf,co2ci)
  
	   else
  
         call agsean_ngt(Sps,Qabs,Rnstar,grdn,windUx,Tair,Dair,co2ca,
     &               wleaf,raero,theta,a1,Ds0,fwsoil,idoy,hours,
     &               Rconst,cpair,Patm,Trefk,H2OLv0,AirMa,H2OMw,Dheat,
     &               gsw0,alpha,stom_n,
     &               Vcmxx,eJmxx,conKc0,conKo0,Ekc,Eko,o2ci,
     &               Eavm,Edvm,Eajm,Edjm,Entrpy,gam0,gam1,gam2,
     &               Aleaf,Eleaf,Hleaf,Tleaf,gbleaf,gsleaf,co2ci)
	   end if

         fslt=exp(-extKb*flai)                               !fraction of sunlit leaves
         fshd=1.0-fslt                                       !fraction of shaded leaves

         Rnst1=Rnst1+fslt*Rnstar(1)*Gaussw(ng)*FLAIT         !Isothermal net rad`
         Rnst2=Rnst2+fshd*Rnstar(2)*Gaussw(ng)*FLAIT
	   RnstL(ng)=Rnst1+Rnst2

         Qcan1=Qcan1+fslt*Qabs(1,1)*Gaussw(ng)*FLAIT          !visible
         Qcan2=Qcan2+fshd*Qabs(1,2)*Gaussw(ng)*FLAIT
	   QcanL(ng)=Qcan1+Qcan2

         Rcan1=Rcan1+fslt*Qabs(2,1)*Gaussw(ng)*FLAIT          !NIR
         Rcan2=Rcan2+fshd*Qabs(2,2)*Gaussw(ng)*FLAIT
	   RcanL(ng)=Rcan1+Rcan2

		if(Aleaf(1).lt.-0.01) Aleaf(1)=0.0	!Weng 2/16/2006
		if(Aleaf(2).lt.-0.01) Aleaf(2)=0.0	!Weng 2/16/2006

         Acan1=Acan1+fslt*Aleaf(1)*Gaussw(ng)*FLAIT*stom_n    !amphi/hypostomatous
         Acan2=Acan2+fshd*Aleaf(2)*Gaussw(ng)*FLAIT*stom_n
         AcanL(ng)=Acan1+Acan2

		layer1(ng)=Aleaf(1)
		layer2(ng)=Aleaf(2)

         Ecan1=Ecan1+fslt*Eleaf(1)*Gaussw(ng)*FLAIT
         Ecan2=Ecan2+fshd*Eleaf(2)*Gaussw(ng)*FLAIT
         EcanL(ng)=Ecan1+Ecan2

         Hcan1=Hcan1+fslt*Hleaf(1)*Gaussw(ng)*FLAIT
         Hcan2=Hcan2+fshd*Hleaf(2)*Gaussw(ng)*FLAIT
         HcanL(ng)=Hcan1+Hcan2

         Gbwc1=Gbwc1+fslt*gbleaf(1)*Gaussw(ng)*FLAIT*stom_n
         Gbwc2=Gbwc2+fshd*gbleaf(2)*Gaussw(ng)*FLAIT*stom_n

         Gswc1=Gswc1+fslt*gsleaf(1)*Gaussw(ng)*FLAIT*stom_n
         Gswc2=Gswc2+fshd*gsleaf(2)*Gaussw(ng)*FLAIT*stom_n

         Tleaf1=Tleaf1+fslt*Tleaf(1)*Gaussw(ng)*FLAIT
         Tleaf2=Tleaf2+fshd*Tleaf(2)*Gaussw(ng)*FLAIT

200   continue

139		format(1x,10(f9.4,2x))
149		format(1x,7(f9.4,2x))

      FLAIT1=(1.0-exp(-extKb*FLAIT))/extkb
      Tleaf1=Tleaf1/FLAIT1
      Tleaf2=Tleaf2/(FLAIT-FLAIT1)

!     Radiation absorbed by soil
      Rsoilab1=fbeam*(1.-reff(1,1))*exp(-kpr(1,1)*FLAIT)
     &         +(1.-fbeam)*(1.-reff(1,2))*exp(-kpr(1,2)*FLAIT)              !visible
      Rsoilab2=fbeam*(1.-reff(2,1))*exp(-kpr(2,1)*FLAIT)
     &         +(1.-fbeam)*(1.-reff(2,2))*exp(-kpr(2,2)*FLAIT)              !NIR
      Rsoilab1=Rsoilab1*Radabv(1)
      Rsoilab2=Rsoilab2*Radabv(2)
!   
      Tlk1=Tleaf1+273.2
      Tlk2=Tleaf2+273.2
      QLair=emair*sigma*(TairK**4)*exp(-extkd*FLAIT)
      QLleaf=emleaf*sigma*(Tlk1**4)*exp(-extkb*FLAIT)
     &      +emleaf*sigma*(Tlk2**4)*(1.0-exp(-extkb*FLAIT))
      QLleaf=QLleaf*(1.0-exp(-extkd*FLAIT)) 
      QLsoil=emsoil*sigma*(TairK**4)
      Rsoilab3=(QLair+QLleaf)*(1.0-rhoS(3))-QLsoil

!     Net radiation absorbed by soil
!     the old version of net long-wave radiation absorbed by soils 
!     (with isothermal assumption)
!      Rsoil3=(sigma*TairK**4)*(emair-emleaf)*exp(-extkd*FLAIT)         !Longwave
!      Rsoilab3=(1-rhoS(3))*Rsoil3

!     Total radiation absorbed by soil
    
      Rsoilabs=Rsoilab1+Rsoilab2+Rsoilab3 
! sensible heat flux into air from soil

!      Hsoil=Rsoilabs-Esoil-G

! special for IREX
	Esoil=0.9*(Rsoilabs-G)
      Hsoil=0.1*(Rsoilabs-G)

!      write(*,*) Tleaf1-Tair,Tleaf2-Tair,QLleaf,Rsoilabs 
!      write(*,250) Radabv(1)+Radabv(2),Qcan1+Qcan2,Rcan1+Rcan2,albedsw,
!     &         Rsoilab1,Rsoilab2,Rsoilab3,Rsoilabs
250   format(1x,3f6.1,f6.3,4f6.1)     

      return
      end 

!
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
      subroutine goudriaan(FLAI,coszen,radabv,fbeam,reff,kpr,
     &                  scatt,xfang,Qabs)
     
!     for spheric leaf angle distribution only
!     compute within canopy radiation (PAR and near infra-red bands)
!     using two-stream approximation (Goudriaan & vanLaar 1994)
!     tauL: leaf transmittance
!     rhoL: leaf reflectance
!     rhoS: soil reflectance
!     sfang XiL function of Ross (1975) - allows for departure from spherical LAD
!          (-1 vertical, +1 horizontal leaves, 0 spherical)
!     FLAI: canopy leaf area index
!     funG: Ross' G function
!     scatB: upscatter parameter for direct beam
!     scatD: upscatter parameter for diffuse
!     albedo: single scattering albedo
!     albedo: single scattering albedo
!
!     output:
!     Qabs(nwave,type), nwave=1 for visible; =2 for NIR,
!                       type=1 for sunlit;   =2 for shaded (W/m2)

      real radabv(2)
      real Qabs(3,2),reff(3,2),kpr(3,2),scatt(2)
     
      xu=coszen                                         !cos zenith angle
      
!     Ross-Goudriaan function for G(u) (see Sellers 1985, Eq 13)
      xphi1 = 0.5 - 0.633*xfang -0.33*xfang*xfang
      xphi2 = 0.877 * (1.0 - 2.0*xphi1)
      funG=xphi1 + xphi2*xu                             !G-function: Projection of unit leaf area in direction of beam
      
      if(coszen.gt.0) then                                  !check if day or night
        extKb=funG/coszen                                   !beam extinction coeff - black leaves
	else
	  extKb=100.
	end if
                       
! Goudriaan theory as used in Leuning et al 1995 (Eq Nos from Goudriaan & van Laar, 1994)
      do nw=1,2
       Qd0=(1.-fbeam)*radabv(nw)                                          !diffuse incident radiation
       Qb0=fbeam*radabv(nw)                                               !beam incident radiation
       Qabs(nw,2)=Qd0*(kpr(nw,2)*(1.-reff(nw,2))*exp(-kpr(nw,2)*FLAI))+   !absorbed radiation - shaded leaves, diffuse
     &            Qb0*(kpr(nw,1)*(1.-reff(nw,1))*exp(-kpr(nw,1)*FLAI)-    !beam scattered
     &             extKb*(1.-scatt(nw))*exp(-extKb*FLAI))
       Qabs(nw,1)=Qabs(nw,2)+extKb*Qb0*(1.-scatt(nw))                     !absorbed radiation - sunlit leaves 
      end do
      return
      end

!     ****************************************************************************
      subroutine Radiso(flai,flait,Qabs,extkd,Tair,eairP,cpair,Patm,
     &                  fbeam,airMa,Rconst,sigma,emleaf,emsoil,
     &                  emair,Rnstar,grdn)
!C     output
!C     Rnstar(type): type=1 for sunlit; =2 for shaded leaves (W/m2)
!C     23 Dec 1994
!C     calculates isothermal net radiation for sunlit and shaded leaves under clear skies
!     implicit real (a-z)
      real Rnstar(2)
      real Qabs(3,2)
      TairK=Tair+273.2

! thermodynamic properties of air
      rhocp=cpair*Patm*airMa/(Rconst*TairK)   !volumetric heat capacity (J/m3/K)

! apparent atmospheric emissivity for clear skies (Brutsaert, 1975)
      emsky=0.642*(eairP/Tairk)**(1./7)       !note eair in Pa
     
! apparent emissivity from clouds (Kimball et al 1982)
      ep8z=0.24+2.98e-12*eairP*eairP*exp(3000/TairK)
      tau8=amin1(1.0,1.0-ep8z*(1.4-0.4*ep8z))            !ensure tau8<1
      emcloud=0.36*tau8*(1.-fbeam)*(1-10./TairK)**4      !10 from Tcloud = Tair-10

! apparent emissivity from sky plus clouds      
c      emair=emsky+emcloud
!* 20/06/96
      emair=emsky

      if(emair.gt.1.0) emair=1.0
      
! net isothermal outgoing longwave radiation per unit leaf area at canopy
! top & thin layer at flai (Note Rn* = Sn + Bn is used rather than Rn* = Sn - Bn in Leuning et al 1985)
      Bn0=sigma*(TairK**4.)
      Bnxi=Bn0*extkd*(exp(-extkd*flai)*(emair-emleaf)
     &        + exp(-extkd*(flait-flai))*(emsoil-emleaf))

!     isothermal net radiation per unit leaf area for thin layer of sunlit and
!     shaded leaves
      Rnstar(1)=Qabs(1,1)+Qabs(2,1)+Bnxi
      Rnstar(2)=Qabs(1,2)+Qabs(2,2)+Bnxi



! radiation conductance (m/s) @ flai
      grdn=4.*sigma*(TairK**3.)*extkd*emleaf*
     &    *(exp(-extkd*flai)+exp(-extkd*(flait-flai)))
     &    /rhocp
      return
      end
!c****************************************************************************
      subroutine agsean_day(Sps,Qabs,Rnstar,grdn,windUx,Tair,Dair,co2ca,
     &               wleaf,raero,theta,a1,Ds0,fwsoil,idoy,hours,
     &               Rconst,cpair,Patm,Trefk,H2OLv0,AirMa,H2OMw,Dheat,
     &               gsw0,alpha,stom_n,
     &               Vcmxx,eJmxx,conKc0,conKo0,Ekc,Eko,o2ci,
     &               Eavm,Edvm,Eajm,Edjm,Entrpy,gam0,gam1,gam2,
     &               Aleaf,Eleaf,Hleaf,Tleaf,gbleaf,gsleaf,co2ci)
!     implicit real (a-z)
      integer kr1,ileaf
      real Aleaf(2),Eleaf(2),Hleaf(2),Tleaf(2),co2ci(2)
      real gbleaf(2), gsleaf(2)
      real Qabs(3,2),Rnstar(2)

!     thermodynamic parameters for air
      TairK=Tair+273.2
      rhocp=cpair*Patm*AirMa/(Rconst*TairK)
      H2OLv=H2oLv0-2.365e3*Tair
      slope=(esat(Tair+0.1)-esat(Tair))/0.1
      psyc=Patm*cpair*AirMa/(H2OLv*H2OMw)
      Cmolar=Patm/(Rconst*TairK)
      weighJ=1.0

! boundary layer conductance for heat - single sided, forced convection
! (Monteith 1973, P106 & notes dated 23/12/94)

      gbHu=0.003*sqrt(windUx/wleaf)    !m/s
!     raero=0.0                        !aerodynamic resistance s/m

      do 10 ileaf=1,2              ! loop over sunlit and shaded leaves
!     first estimate of leaf temperature - assume air temp
         Tleaf(ileaf)=Tair
         Tlk=Tleaf(ileaf)+273.2    !Tleaf to deg K
!     first estimate of deficit at leaf surface - assume Da
         Dleaf=Dair                !Pa
!     first estimate for co2cs
         co2cs=co2ca               !mol/mol
         Qapar = (4.6e-6)*Qabs(1,ileaf)

!     ********************************************************************
         kr1=0                     !iteration counter for LE
!     return point for evaporation iteration
100   continue
!
! single-sided boundary layer conductance - free convection (see notes 23/12/94)
         Gras=1.595e8*abs(Tleaf(ileaf)-Tair)*(wleaf**3.)     !Grashof
         gbHf=0.5*Dheat*(Gras**0.25)/wleaf
         gbH=gbHu+gbHf                         !m/s
         rbH=1./gbH                            !b/l resistance to heat transfer
         rbw=0.93*rbH                          !b/l resistance to water vapour

! Y factor for leaf: stom_n = 1.0 for hypostomatous leaf;  stom_n = 2.0 for amphistomatous leaf
	   rbH_L=rbH*stom_n/2.                   !final b/l resistance for heat  
         rrdn=1./grdn
         Y=1./(1.+ (rbH_L+raero)/rrdn)

! boundary layer conductance for CO2 - single side only (mol/m2/s)
         gbc=Cmolar*gbH/1.32            !mol/m2/s
         gsc0=gsw0/1.57                        !convert conductance for H2O to that for CO2
         varQc=0.0
         weighR=1.0


         call photosyn(Sps,CO2Ca,CO2Csx,Dleaf,Tlk,Qapar,Gbc, !Qaparx<-Qapar,Gbcx<-Gsc0
     &         theta,a1,Ds0,fwsoil,varQc,weighR,
     &         gsc0,alpha,
     &         Vcmxx,eJmxx,weighJ,conKc0,conKo0,Ekc,Eko,o2ci,
     &         Rconst,Trefk,Eavm,Edvm,Eajm,Edjm,Entrpy,gam0,gam1,gam2,
     &         Aleafx,Gscx)   !outputs

!     choose smaller of Ac, Aq
         Aleaf(ileaf) = Aleafx      !0.7 Weng 3/22/2006               !mol CO2/m2/s

!     calculate new values for gsc, cs (Lohammer model)
         co2cs = co2ca-Aleaf(ileaf)/gbc
         co2Ci(ileaf) = co2cs-Aleaf(ileaf)/gsc0
! scale variables
         gsw=gscx*1.56       !gsw in mol/m2/s, oreginal:gsw=gsc0*1.56,Weng20060215
         gswv=gsw/Cmolar                           !gsw in m/s
         rswv=1./gswv

! calculate evap'n using combination equation with current estimate of gsw
         Eleaf(ileaf)=3.2*
     &   (slope*Y*Rnstar(ileaf)+rhocp*Dair/(rbH_L+raero))/    !4.0* Weng 11282006
     &   (slope*Y+psyc*(rswv+rbw+raero)/(rbH_L+raero))

! calculate sensible heat flux
         Hleaf(ileaf)=Y*(Rnstar(ileaf)-Eleaf(ileaf))

! calculate new leaf temperature (K)
         Tlk1=273.2+Tair+Hleaf(ileaf)*(rbH/2.+raero)/rhocp

! calculate Dleaf use LE=(rhocp/psyc)*gsw*Ds
         Dleaf=psyc*Eleaf(ileaf)/(rhocp*gswv)
         gbleaf(ileaf)=gbc*1.32*1.075
         gsleaf(ileaf)=gsw

! compare current and previous leaf temperatures
         if(abs(Tlk1-Tlk).le.0.05) go to 10

         if(kr1.gt.5000) then
25          format(1x,' WARNING! No convergence for Temp in day ',i4,
     &             '   hour', f7.2)
            Aleaf(ileaf)=-99.
            Eleaf(ileaf)=-999.
            co2ci(ileaf)=-999.
            gsleaf(ileaf)=-99.
            return
         end if

!        update leaf temperature
         Tlk=Tlk1
         Tleaf(ileaf)=Tlk1-273.2
         kr1=kr1+1
         goto 100                          !solution not found yet
10    continue
      return
      end

!****************************************************************************
      subroutine agsean_ngt(Sps,Qabs,Rnstar,grdn,windUx,Tair,Dair,co2ca,
     &               wleaf,raero,theta,a1,Ds0,fwsoil,idoy,hours,
     &               Rconst,cpair,Patm,Trefk,H2OLv0,AirMa,H2OMw,Dheat,
     &               gsw0,alpha,stom_n,
     &               Vcmxx,eJmxx,conKc0,conKo0,Ekc,Eko,o2ci,
     &               Eavm,Edvm,Eajm,Edjm,Entrpy,gam0,gam1,gam2,
     &               Aleaf,Eleaf,Hleaf,Tleaf,gbleaf,gsleaf,co2ci)
!     implicit real (a-z)
      integer kr1,ileaf
      real Aleaf(2),Eleaf(2),Hleaf(2),Tleaf(2),co2ci(2)
      real gbleaf(2), gsleaf(2)
      real Qabs(3,2),Rnstar(2)
!     thermodynamic parameters for air
      TairK=Tair+273.2
      rhocp=cpair*Patm*AirMa/(Rconst*TairK)
      H2OLv=H2oLv0-2.365e3*Tair
      slope=(esat(Tair+0.1)-esat(Tair))/0.1
      psyc=Patm*cpair*AirMa/(H2OLv*H2OMw)
      Cmolar=Patm/(Rconst*TairK)
      weighJ=1.0

! boundary layer conductance for heat - single sided, forced convection
! (Monteith 1973, P106 & notes dated 23/12/94)
      gbHu=0.003*sqrt(windUx/wleaf)    !m/s
!     raero=0.0                        !aerodynamic resistance s/m

      do 10 ileaf=1,2                  ! loop over sunlit and shaded leaves
!        first estimate of leaf temperature - assume air temp
         Tleaf(ileaf)=Tair
         Tlk=Tleaf(ileaf)+273.2    !Tleaf to deg K

!        first estimate of deficit at leaf surface - assume Da
         Dleaf=Dair                !Pa
!        first estimate for co2cs
         co2cs=co2ca               !mol/mol
         Qapar = (4.6e-6)*Qabs(1,ileaf)

!     ********************************************************************
         kr1=0                     !iteration counter for LE
!     return point for evaporation iteration
100   continue

!        single-sided boundary layer conductance - free convection (see notes 23/12/94)
         Gras=1.595e8*abs(Tleaf(ileaf)-Tair)*(wleaf**3.)     !Grashof
         gbHf=0.5*Dheat*(Gras**0.25)/wleaf
         gbH=gbHu+gbHf                         !m/s
         rbH=1./gbH                            !b/l resistance to heat transfer
         rbw=0.93*rbH                          !b/l resistance to water vapour

!        Y factor for leaf: stom_n = 1.0 for hypostomatous leaf;  stom_n = 2.0 for amphistomatous leaf
	   rbH_L=rbH*stom_n/2.                   !final b/l resistance for heat  
         rrdn=1./grdn
         Y=1./(1.+ (rbH_L+raero)/rrdn)

!        boundary layer conductance for CO2 - single side only (mol/m2/s)
         gbc=Cmolar*gbH/1.32            !mol/m2/s
         gsc0=gsw0/1.57                        !convert conductance for H2O to that for CO2
         varQc=0.0                  
         weighR=1.0

!        respiration
         Aleafx=-0.0089*Vcmxx*exp(0.069*(Tlk-293.2))
	   gsc=gsc0

!        choose smaller of Ac, Aq
         Aleaf(ileaf) = Aleafx                     !mol CO2/m2/s

!        calculate new values for gsc, cs (Lohammer model)
         co2cs = co2ca-Aleaf(ileaf)/gbc
         co2Ci(ileaf) = co2cs-Aleaf(ileaf)/gsc
!        scale variables
         gsw=gsc*1.56                              !gsw in mol/m2/s
         gswv=gsw/Cmolar                           !gsw in m/s
         rswv=1./gswv

!        calculate evap'n using combination equation with current estimate of gsw
         Eleaf(ileaf)=
     &   (slope*Y*Rnstar(ileaf)+rhocp*Dair/(rbH_L+raero))/
     &   (slope*Y+psyc*(rswv+rbw+raero)/(rbH_L+raero))

!        calculate sensible heat flux
         Hleaf(ileaf)=Y*(Rnstar(ileaf)-Eleaf(ileaf))

!        calculate new leaf temperature (K)
         Tlk1=273.2+Tair+Hleaf(ileaf)*(rbH/2.+raero)/rhocp

!        calculate Dleaf use LE=(rhocp/psyc)*gsw*Ds
         Dleaf=psyc*Eleaf(ileaf)/(rhocp*gswv)
         gbleaf(ileaf)=gbc*1.32*1.075
         gsleaf(ileaf)=gsw

!        compare current and previous leaf temperatures
         if(abs(Tlk1-Tlk).le.0.1) go to 10

         if(kr1.gt.5000) then
            write(*,25) idoy,hours
25          format(1x,' WARNING! No convergence for Temp in day ',i4,
     &             '   hour', f7.2)
            Aleaf(ileaf)=-99.
            Eleaf(ileaf)=-999.
            co2ci(ileaf)=-999.
            gsleaf(ileaf)=-99.
            return
         end if

!        update leaf temperature
         Tlk=Tlk1
 
         Tleaf(ileaf)=Tlk1-273.2
         kr1=kr1+1
         goto 100                          !solution not found yet
10    continue
      return
      end
!****************************************************************************
      subroutine ciandA(Gma,Bta,g0,X,Rd,co2Cs,gammas,ciquad,Aquad)
!     calculate coefficients for quadratic equation for ci
      b2 = g0+X*(Gma-Rd)
      b1 = (1.-co2cs*X)*(Gma-Rd)+g0*(Bta-co2cs)-X*(Gma*gammas+Bta*Rd)
      b0 = -(1.-co2cs*X)*(Gma*gammas+Bta*Rd)-g0*Bta*co2cs

	bx=b1*b1-4.*b2*b0
	if(bx.gt.0.0) then 
!      calculate larger root of quadratic

       ciquad = (-b1+sqrt(bx))/(2.*b2)
	end if
      IF(ciquad.lt.0.or.bx.lt.0.) THEN
        Aquad = 0.0
        ciquad = co2Cs
      ELSE
        Aquad = Gma*(ciquad-gammas)/(ciquad+Bta)
      END IF
      return
      end
!

!****************************************************************************
      subroutine goud1(FLAIT,coszen,radabv,fbeam,
     &                  Tair,eairP,emair,emsoil,emleaf,sigma,
     &                  tauL,rhoL,rhoS,xfang,extkb,extkd,
     &                  reffbm,reffdf,extkbm,extkdm,Qcan)
!     use the radiation scheme developed by
!     Goudriaan (1977, Goudriaan and van Larr 1995)
! =================================================================
!     Variable      unit      defintion
!     FLAIT         m2/m2     canopy leaf area index       
!     coszen                  cosine of the zenith angle of the sun
!     radabv(nW)    W/m2      incoming radiation above the canopy
!     fbeam                   beam fraction
!     fdiff                   diffuse fraction
!     funG(=0.5)              Ross's G function
!     extkb                   extinction coefficient for beam PAR
!     extkd                   extinction coefficient for diffuse PAR
!     albedo                  single scattering albedo
!     scatB                   upscattering parameter for beam
!     scatD                   upscattering parameter for diffuse
!  ==================================================================
!     all intermediate variables in the calculation correspond
!     to the variables in the Appendix of of Seller (1985) with
!     a prefix of "x".

      integer nW
      real radabv(3)
      real rhocbm(3),rhocdf(3)
      real reffbm(3),reffdf(3),extkbm(3),extkdm(3)
      real tauL(3),rhoL(3),rhoS(3),scatL(3)
      real Qcan(3,2),Qcan0(3)

!     for PAR: using Goudriann approximation to account for scattering
!
      fdiff=1.0-fbeam
      xu=coszen
      xphi1 = 0.5 -0.633*xfang - 0.33*xfang*xfang
      xphi2 = 0.877 * (1.0 - 2.0*xphi1)
      funG = xphi1 + xphi2*xu
      extkb=funG/xu
                       
!     Effective extinction coefficient for diffuse radiation Goudriaan & van Laar Eq 6.6)
      pi180=3.1416/180.
      cozen15=cos(pi180*15)
      cozen45=cos(pi180*45)
      cozen75=cos(pi180*75)
      xK15=xphi1/cozen15+xphi2
      xK45=xphi1/cozen45+xphi2
      xK75=xphi1/cozen75+xphi2
      transd=0.308*exp(-xK15*FLAIT)+0.514*exp(-xK45*FLAIT)+
     &       0.178*exp(-xK75*FLAIT)
      extkd=(-1./FLAIT)*alog(transd)

! canopy reflection coefficients (Array indices: 1=VIS,  2=NIR
!                                                
      do 10 nw=1,2                                                         !nw:1=VIS, 2=NIR
         scatL(nw)=tauL(nw)+rhoL(nw)                                          !scattering coeff
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
!     by the shaded leaves
         abshdn=fdiff*(1.0-reffdf(nw))*extkdm(nw)                             !absorbed NIR by shaded
     &      *(funE(extkdm(nw),FLAIT)-funE((extkb+extkdm(nw)),FLAIT))
     &      +fbeam*(1.0-reffbm(nw))*extkbm(nw)
!     &      *(funE(extkbm(nw),FLAIT)-funE((extkb+extkdm(nw)),FLAIT))  ! error found by De Pury
     &      *(funE(extkbm(nw),FLAIT)-funE((extkb+extkbm(nw)),FLAIT))
     &      -fbeam*(1.0-scatL(nw))*extkb
     &      *(funE(extkb,FLAIT)-funE(2.0*extkb,FLAIT))
!     by the sunlit leaves
         absltn=fdiff*(1.0-reffdf(nw))*extkdm(nw)                             !absorbed NIR by sunlit
     &      *funE((extkb+extkdm(nw)),FLAIT)                         
     &      +fbeam*(1.0-reffbm(nw))*extkbm(nw)
!     &      *funE((extkb+extkdm(nw)),FLAIT)                         ! error found by De Pury
     &      *funE((extkb+extkbm(nw)),FLAIT)
     &      +fbeam*(1.0-scatL(nw))*extkb
     &      *(funE(extkb,FLAIT)-funE(2.0*extkb,FLAIT))

!     scale to real flux 
!     sunlit    
          Qcan(nw,1)=absltn*radabv(nw)
!     shaded
          Qcan(nw,2)=abshdn*radabv(nw)
10    continue
!      
!     calculate the absorbed (iso)thermal radiation
      TairK=Tair+273.2
      
!     apparent atmospheric emissivity for clear skies (Brutsaert, 1975)
      emsky=0.642*(eairP/Tairk)**(1./7)      !note eair in Pa

!     apparent emissivity from clouds (Kimball et al 1982)
      ep8z=0.24+2.98e-12*eairP*eairP*exp(3000/TairK)
      tau8=amin1(1.0,1-ep8z*(1.4-0.4*ep8z))                !ensure tau8<1
      emcloud=0.36*tau8*(1.-fbeam)*(1-10./TairK)**4     !10 from Tcloud = Tair-10 

!      apparent emissivity from sky plus clouds      
!      emair=emsky+emcloud
!     20/06/96
      emair=emsky
      if(emair.gt.1.0) emair=1.0                             

      Bn0=sigma*(TairK**4.)
      QLW1=-extkd*emleaf*(1.0-emair)*funE((extkd+extkb),FLAIT)
     &     -extkd*(1.0-emsoil)*(emleaf-emair)*exp(-2.0*extkd*FLAIT)
     &     *funE((extkb-extkd),FLAIT)
      QLW2=-extkd*emleaf*(1.0-emair)*funE(extkd,FLAIT)
     &     -extkd*(1.0-emsoil)*(emleaf-emair)
     &     *(exp(-extkd*FLAIT)-exp(-2.0*extkd*FLAIT))/extkd
     &     -QLW1
      Qcan(3,1)=QLW1*Bn0
      Qcan(3,2)=QLW2*Bn0
      return
      end

!****************************************************************************
      subroutine photosyn(Sps,CO2Ca,CO2Csx,Dleafx,Tlkx,Qaparx,Gbcx,
     &         theta,a1,Ds0,fwsoil,varQc,weighR,
     &         g0,alpha,
     &         Vcmx1,eJmx1,weighJ,conKc0,conKo0,Ekc,Eko,o2ci,
     &         Rconst,Trefk,Eavm,Edvm,Eajm,Edjm,Entrpy,gam0,gam1,gam2,
     &         Aleafx,Gscx)
!     calculate Vcmax, Jmax at leaf temp (Eq 9, Harley et al 1992)
!c      VcmxT = Vjmax(Tlkx,Trefk,Vcmx1,Eavm,Edvm,Rconst,Entrpy)
!c      eJmxT = Vjmax(Tlkx,Trefk,eJmx1,Eajm,Edjm,Rconst,Entrpy)

!c     check if it is dark - if so calculate respiration and g0 to assign conductance 
      if(Qaparx.le.0.) then                         !umol quanta/m2/s
	  Aleafx=-0.0089*Vcmx1*exp(0.069*(Tlkx-293.2))   ! original: 0.0089 Weng 3/22/2006
	  Gscx=g0
	  return
	end if

! calculate  Vcmax, Jmax at leaf temp using Reed et al (1976) function J appl Ecol 13:925
      TminV=-5.
      TmaxV=45.
      ToptV=30.
      
      TminJ=TminV
      TmaxJ=TmaxV
      ToptJ=ToptV 
      
      Tlf=Tlkx-273.2
!		write(*,*)'ok1'
      VcmxT=VJtemp(Tlf,TminV,TmaxV,ToptV,Vcmx1)
!		write(*,*)'ok2'
      eJmxT=VJtemp(Tlf,TminJ,TmaxJ,ToptJ,eJmx1)
!c		write(*,*)'ok3'
      
! calculate J, the asymptote for RuBP regeneration rate at given Q
      eJ = weighJ*fJQres(eJmxT,alpha,Qaparx,theta)
!		write(*,*)'ok4'

! calculate Kc, Ko, Rd gamma*  & gamma at leaf temp
      conKcT = EnzK(Tlkx,Trefk,conKc0,Rconst,Ekc)
      conKoT = EnzK(Tlkx,Trefk,conKo0,Rconst,Eko)
!		write(*,*)'ok5'
! following de Pury 1994, eq 7, make light respiration a fixed proportion of
! Vcmax
      Rd = 0.0089*VcmxT*weighR                              !de Pury 1994, Eq7
      Tdiff=Tlkx-Trefk
      gammas = gam0*(1.+gam1*Tdiff+gam2*Tdiff*Tdiff)       !gamma*
!     gamma = (gammas+conKcT*(1.+O2ci/conKoT)*Rd/VcmxT)/(1.-Rd/VcmxT)
      gamma = 0.0

!***********************************************************************
! Analytical solution for ci. This is the ci which satisfies supply and demand
! functions simultaneously

!     calculate X using Lohammer model, and scale for soil moisture
      X = a1*fwsoil/((co2csx - gamma)*(1+Dleafx/Ds0))

!     calculate solution for ci when Rubisco activity limits A

      Gma = VcmxT  
      Bta = conKcT*(1.+ o2ci/conKoT)

      call ciandA(Gma,Bta,g0,X,Rd,co2Csx,gammas,co2ci2,Acx)
!
!     calculate +ve root for ci when RuBP regeneration limits A
      Gma = eJ/4.
      Bta = 2.*gammas
!     calculate coefficients for quadratic equation for ci		

      call ciandA(Gma,Bta,g0,X,Rd,co2Csx,gammas,co2ci4,Aqx)
!
!     choose smaller of Ac, Aq
	sps=AMAX1(0.001,sps)			!Weng, 3/30/2006
      Aleafx = (amin1(Acx,Aqx) - Rd)*sps     ! Weng 4/4/2006

!     calculate new values for gsc, cs (Lohammer model)
      CO2csx = co2ca-Aleafx/Gbcx
      Gscx=g0+X*Aleafx  ! revised by Weng

      return
      end

!     ***********************************************************************
      function funeJ(alpha,eJmxT,Qaparx)
      funeJ=alpha*Qaparx*eJmxT/(alpha*Qaparx+2.1*eJmxT)
      return
      end
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