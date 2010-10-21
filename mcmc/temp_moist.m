function y=temp_moist(Nt,mscut);

moist_1    =   mois5_tao(1826);
temp_1     =   tmp_tao(1826);
temp       =   temp_1(:,2);
moist      =   moist_1(:,2);

for i = 1:(Nt+1)
   sumtemp = 0;
   tmp=temp(i);
   if (i > 10)
      for j = i-9:i
         sumtemp=sumtemp+temp(j);
      end
      tmp=sumtemp/10;
   end
   tmp=0.65*2.2^((tmp-10)/10);
   moisture=1;
   if (moist(i)<mscut)
       moisture=1.0-5.0*(mscut-moist(i)); 
   end
   product(i)=tmp*moisture;
end
y=product;
  