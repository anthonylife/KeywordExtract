function f_x = sigmoid(w, x)
%
% SIGMOID return the value of sigmoid(x)
%


f_x = 1./(1 + exp(-w'*x));
