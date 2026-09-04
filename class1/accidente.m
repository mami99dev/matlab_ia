%% ----------- Control difuso -----------
clear all; close all; clc;

%% -----------
max=140
x=0:1:max;
y=0:4/max:4;

A = trapmf(x, [40 120 140 140]);
B = trapmf(y, [0 2 4 4]);
%B = sigmf(y, [1, 6]);

%% -----------  Graficar ---------------
subplot(2,1,1),plot(x,A,'LineWidth',2),hold on
title('Conjunto para alta velocidad'),xlabel('horas'),ylabel('\mu(x)')

subplot(2,1,2),plot(y,B,'LineWidth',2),hold on
title('Conjunto para accidente grave'),xlabel('horas'),ylabel('\mu(x)')

%% --------------- Producto cartesiano ------------------
for i=1:length(x)
    for j=1:length(y)
        mR(i,j)=min(A(i),B(j));
    end
end

%% ---------------- Graficar Relación Difusa 3D ----------------
figure(2)
mesh(x, y, mR')
xlabel('Alta velocidad (x)')
ylabel('Accidente grave (y)')
zlabel('\mu_R(x,y)')
title('Producto Cartesiano: Mínimo Difuso R = A \times B')
colorbar
set(gca, 'FontSize', 10)

%% ---------------------- composicion -----------------
h=120;
Ap=trimf(x,[h,h,h]);

for j=1:size(mR, 2)
    for i=1:size(mR, 1)
        aux(i)=min(Ap(i), mR(i,j));
    end
    Bp(j) = max(aux);
end

figure()
subplot(2,1,1),plot(x,Ap,'LineWidth',3),set(gca,'FontSize',10)
title(['Conjunto para ', num2str(h),' km/h']),ylabel('\mu')
axis([0 4*h 0 1])
subplot(2,1,2),plot(y,Bp,'LineWidth',3),set(gca,'FontSize',10)
title('Conjunto accidentarse'), xlabel('terminar mal'),ylabel('\mu')
axis([0 4 0 1])