function sum_expvalue = getsum_expvalue(features, model)
%
% GETSUM_EXPVALUE get the sum value of the exponential formual of
% each word in the specified document. This value will be used in
% model parameters updating later.
%
% author: anthonylife
% date  : 1/16/2013


sum_expvalue = sum(exp(-model.w'*features'));
