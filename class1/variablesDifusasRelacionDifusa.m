%% ----------- Control difuso -----------
clear all; close all; clc;

%% ----------- 
x=0:0.01:10;
y=0:0.01:10;

A = trapmf(x, [4 6 10 10]);
B = trapmf(y, [4 6 10 10]);
%B = sigmf(y, [1, 6]);

%% -----------  Graficar ---------------
subplot(2,1,1),plot(x,A,'LineWidth',2),hold on
title('Conjunto para horas de estudio'),xlabel('horas'),ylabel('\mu(x)')

subplot(2,1,2),plot(y,B,'LineWidth',2),hold on
title('Conjunto para calificacion obtenida'),xlabel('horas'),ylabel('\mu(x)')

%% --------------- Producto cartesiano ------------------
for i=1:length(x)
    for j=1:length(y)
        mR(i,j)=min(A(i),B(j));
    end
end

%% ---------------- Graficar Relación Difusa 3D ----------------
figure(2)
mesh(x, y, mR')
xlabel('Horas de estudio (x)')
ylabel('Calificación (y)')
zlabel('\mu_R(x,y)')
title('Producto Cartesiano: Mínimo Difuso R = A \times B')
colorbar
set(gca, 'FontSize', 10)

%% ---------------------- composicion -----------------
h=4.5;
Ap=trimf(x,[h,h,h]);

for j=1:size(mR, 2)
    for i=1:size(mR, 1)
        aux(i)=min(Ap(i), mR(i,j));
    end
    Bp(j) = max(aux);
end

figure()
subplot(2,1,1),plot(x,Ap,'LineWidth',3),set(gca,'FontSize',10)
title(['Conjunto para ', num2str(h),' horas de estudio exactas']),ylabel('\mu')
subplot(2,1,2),plot(y,Bp,'LineWidth',5),set(gca,'FontSize',10)
title('Conjunto ser buen estudiante'), xlabel('buen estudiante'),ylabel('\mu')
axis([0 10 0 1])