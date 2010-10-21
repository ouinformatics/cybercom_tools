%this function solves the forward problem
function y = solve_forward_2(tau,c,b,u,x0,Nt,cbnScale)

AC=[-c(1)       0           0           0           0            0              0
   0            -c(2)       0           0           0            0              0
   0.7123*c(1)  0           -c(3)       0           0            0              0
   0.2877*c(1)  c(2)        0           -c(4)       0            0              0
   0            0           0.45*c(3)   0.275*c(4)  -c(5)        0.42*c(6)      0.45*c(7)
   0            0           0           0.275*c(4)  0.296*c(5)   -c(6)          0
   0            0           0           0           0.004*c(5)   0.03*c(6)      -c(7)]; %the constant matrix A

x_last=x0;
for i = 1:Nt
    x_present = [eye(7)+AC*tau(i)]*x_last + b*u(i)*cbnScale;
    x(:,i) = x_present;
    x_last = x_present;
end
y = x;