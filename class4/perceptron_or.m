%% ---------- Red Neuronal Perceptron ------------------------------------
clear all; close all; clc;

%% --------------- inicializacon -----------------------------------------
N=20;           % epocas
Q=4;            % dimension de las entradas

p0=[1 1 1 1];        % patron de bias
p1=[0 0 1 1];        % patron uno de entrada
p2=[0 1 0 1];        % patron dos de entrada
y=[-1 -1 -1 1];    % salidas deseadas % compuerta AND
y2=[-1 1 1 1];         % salidas deseadas % compuerta OR

alfa=0.5;

% w=2*rand(1,2)-1;
% b=2*rand-1;
w=[0.5 1.5];
w1=[0.5 1.5];
b=1.3;

pr=-0.5:0.01:2;
H=plot(pr, -b/w(2)- w(1)/w(2)*pr);
H2=plot(pr, -b/w(2)- w(1)/w(2)*pr);
% ------------------- Proceso de entrenamiento ---------------------------

for Epocas=1:N
    for q=1:Q
        net=w*[p1(q) p2(q)]'+b*p0(q);
        a=hardlims(net);

        e(q)=y(q)-a;
        w(1)=w(1)+alfa*(e(q))*p1(q);
        w(2)=w(2)+alfa*(e(q))*p2(q);
        b=b+alfa*e(q);
    end

    for q=1:Q
        net=w1*[p1(q) p2(q)]'+b*p0(q);
        a=hardlims(net);

        e(q)=y2(q)-a;
        w1(1)=w1(1)+alfa*(e(q))*p1(q);
        w1(2)=w1(2)+alfa*(e(q))*p2(q);
        b=b+alfa*e(q);
    end
    % ------------------- grafica de la frontera de decision -------------
    delete(H)
    plot(p1(1),p2(1),'bo')
    grid on, hold on
    plot(p1(2),p2(2),'bo')
    plot(p1(3),p2(3),'bo')
    plot(p1(4),p2(4),'bo')
    axis([-0.5 1.5 -0.5 1.5])
    H=plot(pr, -b/w(2)- w(1)/w(2)*pr);
    %plot(pr, -b/w(2)- w(2)/w(2)*p2)
    pause(0.4)


    delete(H2)
    plot(p1(1),p2(1),'bo')
    grid on, hold on
    plot(p1(2),p2(2),'bo')
    plot(p1(3),p2(3),'bo')
    plot(p1(4),p2(4),'bo')
    axis([-0.5 1.5 -0.5 1.5])
    H2=plot(pr, -b/w1(2)- w1(1)/w1(2)*pr);
    %plot(pr, -b/w(2)- w(2)/w(2)*p2)
    pause(0.4)
end