%% ---------- Red Neuronal ADALINE Reconocimiento de numeros -------------
clear all; close all; clc;
%% --------------- inicializacon -----------------------------------------
load('Pesos_Neurona_Numeros.mat')

%% ---- rutina de visualizacion y reconocimiento por archivo -------------
load('xTrainImages.mat')

q=round(4999*rand + 1);
A=xTrainImages{q};
imshow(A,'InitialMagnification',300)
P1=[A(:)];

net=W*P1+b;
[a win]= max(net)
net'
NumeroReconocido= win-1

%% ------------ reconocimiento de numeros en paint ------------------------
img_ent=imread('pruebas\7.jpg');

img_ent=im2double(img_ent);
img_gris = rgb2gray(img_ent);
img_gris=imadjust(img_gris,[0.5 0.8]);
img_com = imcomplement(img_gris);
img_test = imresize(img_com,[28 28]);
imshow(img_test,'InitialMagnification',800)
size(img_test)

P1=[img_test(:)];

net=W*P1+b;
[a win]= max(net)
net'
NumeroReconocido= win-1