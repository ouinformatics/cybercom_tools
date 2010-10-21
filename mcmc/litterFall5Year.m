function y = litterFall5Year(x,tau,phi_litterfall,Nt)

for i=1:Nt
    litter_Fall(i)=tau(i)*phi_litterfall*x(:,i);
end
for i=1:5
    lf_Yr(i) = sum(litter_Fall((i-1)*365+1:i*365));
end
y = lf_Yr;
