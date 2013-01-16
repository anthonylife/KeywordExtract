function node_value = getnodevalue(features, node_idx, w)
%
% GETNODEVALUE compute the node (text unit) value with
% exponential family function (exp(-wx1)/sum(exp(-wx))).
%
% author: anthonylife
% date  : 1/16/2013


node_value = exp(-w'*features(node_idx,:)')...
           / sum(exp(-w'*features'));
