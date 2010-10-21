%This program was written by Tao Xu to study the inverse problem of seven pool model using MCMC 
% 10/10/2004
clear all;
close all;
format long e;

RandSeed=clock;
rand('seed',RandSeed(6));
nput=input('Enter 2 or 3: 2 -- ambient inversion, 3 -- elevated inversion\n');

Nt      =   1825;
m       =   7;              %seven compartments
mscut   =   0.2; 
cbnScale=   1.5;            %2 for nput=2 and 1.5 for nput=3
x0      =   [469 4100 64 694 123 1385 923]'; %initial value of states
%*********prior c--the transfer coefficients**********************
if nput == 2 
    c   =   [0.00176 0.000100104 0.021468 0.000845 0.008534 8.976e-005 3.09564e-006]';
else
    c   =   [0.00217 0.0001410104 0.02268 0.000965 0.002534 5.576e-005 2.65640e-006]';
end
cmin(1) = 0.0001764; cmin(2) = 0.0000548; cmin(3) = 0.005479;  cmin(4) = 0.000548;
cmin(5) = 0.00274;   cmin(6) = 0.0000548; cmin(7) = 0.00000137;
cmax(1) = 0.00295;   cmax(2) = 0.000274;  cmax(3) = 0.02734;   cmax(4) = 0.00274;
cmax(5) = 0.00685;   cmax(6) = 0.000274;  cmax(7) = 0.00000913;

%***********set input matrix and input carbon***************
b       =   [0.25 0.30 0 0 0 0 0]';  
cbn     =   carbon(1826);
if nput == 2
    u = cbn(:,2);           %ambient carbon
else
    u = cbn(:,3);           %elevated carbon
end
tau=temp_moist(Nt,mscut);
%data sets below
soil_respration =   soil_resp(55);
soilTime        =   soil_respration(:,1);
soilResValue    =   soil_respration(:,nput);
bioMass         =   biom(58);
biomTime        =   bioMass(:,1);
woodyValue      =   (1-0.085)*bioMass(:,nput);
foilageValue    =   0.085*bioMass(:,nput);
litterFall      =   litter_fall(63);
litterTime      =   litterFall(:,2);
litterValue     =   litterFall(:,nput+1);
litter5Y_lump   =   litterLump(litterTime,litterValue);
soilMineralCarbonTime   =   [240 1368];
if nput==2 
   soilCbnValue     =   [569 701];
   mineralCbnValue  =   [2455 2724];
else
   soilCbnValue     =   [569.0000 884.0000];
   mineralCbnValue  =   [2455   3135];
end

%The mappings
phi_slResp          = [0.25*c(1) 0.25*c(2)  0.55*c(3)   0.45*c(4)   0.7*c(5)    0.55*c(6)   0.55*c(7)];
phi_woodBiom        = [0         1         0         0         0        0         0];
phi_foilageBiom     = [0.75       0         0         0         0        0         0];
phi_litterfall      = [0.75*c(1) 0.75*c(2) 0         0         0        0         0];
phi_cMineral        = [0         0         0         0         1        1         1];
phi_cForestFloor    = [0         0         0.75      0.75      0        0         0];
cdif  = (cmax-cmin)';

%simulation starts
c_op=cmin'+rand*cdif;
J_last = 300000;
c_new=zeros(7,1);
nsim    = 20000;
record_index=1;
DJ1=2*var(soilResValue);
DJ2=2*var(woodyValue);
DJ3=2*var(foilageValue);
DJ4=2*var(litter5Y_lump);
DJ5=2*var(soilCbnValue);
DJ6=2*var(mineralCbnValue);

%Prior estimate of covariance matrix of parameters (from previous uniform run)
if nput==2
    cov_c_rec=[ 1.2989e-009	    -6.7878e-012	5.2957e-009	    1.7167e-011	    5.3156e-010	    2.5561e-011	    1.2144e-012
                -6.7878e-012	1.1862e-010	    5.7477e-009	    6.3075e-010	    4.5307e-010	    1.3128e-010	    1.719e-013
                5.2957e-009	    5.7477e-009	    3.4585e-005	    -2.2082e-007	-6.2344e-007	-2.7854e-010	9.0464e-010
                1.7167e-011	    6.3075e-010	    -2.2082e-007	8.3933e-009	    8.6988e-009	    1.023e-009	    -4.0094e-012
                5.3156e-010	    4.5307e-010	    -6.2344e-007	8.6988e-009	    1.0611e-006	    -1.299e-008	    2.097e-010
                2.5561e-011	    1.3128e-010	    -2.7854e-010	1.023e-009	    -1.299e-008	    1.0477e-009	    -2.0955e-012
                1.2144e-012	    1.719e-013	    9.0464e-010	    -4.0094e-012	2.097e-010	    -2.0955e-012	4.6867e-012];
else
    cov_c_rec=[ 8.2095e-009	    -1.721e-010	    8.3563e-009	    -2.7488e-009	-4.2713e-009	-2.813e-010	    -1.6096e-012
                -1.721e-010	    1.2324e-010	    1.6925e-009	    2.8643e-010	    6.5954e-011	    3.7524e-011	    -4.3795e-014
                8.3563e-009	    1.6925e-009	    3.3459e-005	    -7.6044e-008	7.243e-008	    1.811e-009	    3.1149e-010
                -2.7488e-009	2.8643e-010	    -7.6044e-008	4.4221e-008	    7.635e-010	    3.186e-010	    5.4717e-012
                -4.2713e-009	6.5954e-011	    7.243e-008	    7.635e-010	    1.2033e-006	    -2.822e-009	    1.0246e-010
                -2.813e-010	    3.7524e-011	    1.811e-009	    3.186e-010	    -2.822e-009	    1.0416e-009	    -3.5187e-013
                -1.6096e-012	-4.3795e-014	3.1149e-010	    5.4717e-012	    1.0246e-010	    -3.5187e-013	4.2444e-012];
end
[transT, eigV]=eig(cov_c_rec);

%Simulation starts
upgraded=0;
for simu=1:nsim
    counter=simu
    upgradedd=upgraded
    c_new=Generate(c_op,transT,eigV,cmin,cmax);%generate a new point
	phi_slResp          = [0.25*c_new(1)  0.25*c_new(2)  0.55*c_new(3)   0.45*c_new(4)   0.7*c_new(5)    0.55*c_new(6)   0.55*c_new(7)];
	phi_litterfall      = [0.75*c_new(1) 0.75*c_new(2) 0         0         0        0         0];
	x=solve_forward_2(tau,c_new,b,u,x0,Nt,cbnScale);%solve forward problem    
    
    litter5Y_simu = litterFall5Year(x,tau,phi_litterfall,Nt);
	for i=1:length(soilTime)
        soilResp_simu(i)    = tau(soilTime(i))*phi_slResp*x(:,soilTime(i))+0.25*(1-b(1)-b(2))*u(soilTime(i));%
	end
	for i=1:length(biomTime)
        woodBiom_simu(i)    = phi_woodBiom*x(:,biomTime(i));
	end
	for i=1:length(biomTime)
        foilageBiom_simu(i) = phi_foilageBiom*x(:,biomTime(i));
	end
	for i=1:length(soilMineralCarbonTime)
        cForestFloor_simu(i) = phi_cForestFloor*x(:,soilMineralCarbonTime(i));
	end
 	for i=1:length(soilMineralCarbonTime)
         cMineral_simu(i)    = phi_cMineral*x(:,soilMineralCarbonTime(i));
    end

    J(1)  =   (norm(soilResp_simu-soilResValue'))^2;
  	J(2)  =   (norm(woodBiom_simu-woodyValue'))^2;
  	J(3)  =   (norm(foilageBiom_simu-foilageValue'))^2;
  	J(4)  =   (norm(litter5Y_simu-litter5Y_lump))^2;
   	J(5)  =   (norm(cForestFloor_simu-soilCbnValue))^2;
   	J(6)  =   (norm(cMineral_simu-mineralCbnValue))^2;
    
    J_new=(J(1)/DJ1+J(2)/DJ2+J(3)/DJ3+J(4)/DJ4+J(5)/DJ5+J(6)/DJ6);
 	delta_J = J_new-J_last;
	
	if min(1, exp(-delta_J)) >rand
        c_op=c_new;
        J_last=J_new;
        upgraded=upgraded+1
        c_upgraded(:,upgraded)=c_op;
    end
    c_rec(:,record_index)=c_op;
    J_record(record_index)=J_last;
    record_index=record_index+1;
end
FigurePlot(c_upgraded,cmin,cmax,J_record);
save ambient_originalVar_08_22_05_elevated;
