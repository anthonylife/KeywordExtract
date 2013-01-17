function node_value=getnodevalue(features,idx,w,sumvalue)
%
% GETNODEVALUE compute the node (text unit) value with
% exponential family function (exp(-wx1)/sum(exp(-wx))).
%
% author: anthonylife
% date  : 1/16/2013


node_value = sigmoid(w, features(idx,:)') ./ sumvalue;
