%% ---------- Red Neuronal ADALINE Reconocimiento de numeros -------------
clear all; close all; clc;
%% --------------- inicializacon -----------------------------------------
%load('xTrainImages.mat')
load('xTrainImagRand.mat')
%yd=tTest;

%% Display some of the training images
num=200;
%imshow(xTrainImages{num},'InitialMagnification',100);
size(xTrainImages{num})
yd(:,num)
%% ------------- Display en conjunto -------------------------------------

for k = 1:30
    subplot(6,5,k);
    %imshow(xTrainImages{k+1000});
end

%% ----------------- Reacomodo en vectores para P ------------------------
for j = 1:5000
    A=xTrainImages{j};
    B=[A(:)];
    P(:,j)=B;
end
%P=[P; zeros(1,5000)];
%% --------------- Organizacion de entradas -------------------------------
Q=size(P,2);    % solo la segunda dimension de P, 5000
b=ones(1,Q);
Z=[P; b];

%% --------------- Valores deseados con 10 neuronas -----------------------
%Y=yd;
Y= yd;

%% --------------- Matrices de metodo Widrow-Hoff --------------------------
R= Z*Z'/Q;
H= Z*Y'/Q;
X=pinv(R)*H;    % R es singular por lo que se usa la pseudoinversa
W=X(1:784,:)';
b=X(785,:)';

%% ----------------- verificacion del numero de aciertos --------------------
for q=1:Q
    net=W*P(:,q)+b;
    %iwin(q)= hardlims(net)
    [a(q) iwin(q)]= max(net);
    y(q)=find(yd(:,q)==1);
end
Numaciertos=sum(y==iwin);  % calcula el nnumero de aciertos de la neurona
Porcentaciertos=(Numaciertos/5000)*100

%% ----------------- Guardado de pesos para el testing -----------------------

save('Pesos_Neurona_Numeros.mat','W','b')  %% guardar las salidas deseadas

%% ----------------- Testing ------------------------ %%
%% --------------- inicializacon -----------------------------------------
load('Pesos_Neurona_Numeros.mat')

%% ---- rutina de visualizacion y reconocimiento por archivo -------------
load('xTrainImagRand.mat')

q=round(4999*rand + 1);
A=xTrainImages{q};
%imshow(A,'InitialMagnification',300)
P1=[A(:)];

net=W*P1+b;
[a win]= max(net)
net'
NumeroReconocido= win-1

%% ------------ reconocimiento de numeros en paint ------------------------
img_ent=imread('pruebas\cuatro.jpg');

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