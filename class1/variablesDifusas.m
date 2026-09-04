%% ----------- Control difuso -----------
clear all; close all; clc;

%% ----------- 
x=0:0.01:10;
y=0:0.01:10;

A = trapmf(x, [4 6 10 10]);
B = sigmf(y, [1, 6]);

%% -----------  Graficar ---------------

subplot(2,1,2),plot(x,A,'LineWidth',2),hold on
title('Conjunto para horas de estudio'),xlabel('horas'),ylabel('\mu(x)')

subplot(2,1,2),plot(y,B,'LineWidth',2),hold on
title('Conjunto para calificacion obtenida'),xlabel('horas'),ylabel('\mu(x)')
