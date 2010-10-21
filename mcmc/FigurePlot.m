function FigurePlot(c_upgraded,cmin,cmax,J_record)
c1=c_upgraded(1,:);
c2=c_upgraded(2,:);
c3=c_upgraded(3,:);
c4=c_upgraded(4,:);
c5=c_upgraded(5,:);
c6=c_upgraded(6,:);
c7=c_upgraded(7,:);

len=length(c1);
c_1=c1(100:len);
c_2=c2(100:len);
c_3=c3(100:len);
c_4=c4(100:len);
c_5=c5(100:len);
c_6=c6(100:len);
c_7=c7(100:len);

figure(1);subplot(3,3,1);plot(c1(100:len),'k');axis([1 length(c1) cmin(1) cmax(1)]);title('c_1');
figure(1);subplot(3,3,2);plot(c2(100:len),'k');axis([1 length(c1) cmin(2) cmax(2)]);title('c_2');
figure(1);subplot(3,3,3);plot(c3(100:len),'k');axis([1 length(c1) cmin(3) cmax(3)]);title('c_3'); 
figure(1);subplot(3,3,4);plot(c4(100:len),'k');axis([1 length(c1) cmin(4) cmax(4)]);title('c_4'); 
figure(1);subplot(3,3,5);plot(c5(100:len),'k');axis([1 length(c1) cmin(5) cmax(5)]);title('c_5'); 
figure(1);subplot(3,3,6);plot(c6(100:len),'k');axis([1 length(c1) cmin(6) cmax(6)]);title('c_6'); 
figure(1);subplot(3,3,7);plot(c7(100:len),'k');axis([1 length(c1) cmin(7) cmax(7)]);title('c_7'); 
figure(1);subplot(3,3,8);plot(J_record(100:len),'k');axis([1 length(c1) 10 50]);title('values of the cost function J at the maximum likelihood area')  
figure(2);subplot(3,3,1);hist(c_1,30);xlabel('c_1');axis([cmin(1) cmax(1) 1 1500]);title('Marginal of c_1');
figure(2);subplot(3,3,2);hist(c_2,30);xlabel('c_2');axis([cmin(2) cmax(2) 1 1500]);title('Marginal of c_2');
figure(2);subplot(3,3,3);hist(c_3,30);xlabel('c_3');axis([cmin(3) cmax(3) 1 1500]);title('Marginal of c_3');
figure(2);subplot(3,3,4);hist(c_4,30);xlabel('c_4');axis([cmin(4) cmax(4) 1 1500]);title('Marginal of c_4');
figure(2);subplot(3,3,5);hist(c_5,30);xlabel('c_5');axis([cmin(5) cmax(5) 1 1500]);title('Marginal of c_5');
figure(2);subplot(3,3,6);hist(c_6,30);xlabel('c_6');axis([cmin(6) cmax(6) 1 1500]);title('Marginal of c_6');
figure(2);subplot(3,3,7);hist(c_7,30);xlabel('c_7');axis([cmin(7) cmax(7) 1 1500]);title('Marginal of c_7');

