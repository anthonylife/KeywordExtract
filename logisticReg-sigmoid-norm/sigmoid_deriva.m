function deriva_value = sigmoid_deriva(w, x)
%
% SIGMOID_DERIVA compute the value of derivative of the sigmoid
% function.
%
% author : anthonylife
% date   : 1/17/2013


deriva_value = sigmoid(w, x).*(1-sigmoid(w,x));
