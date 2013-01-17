function sumvalue = getsumvalue(features, model)
%
% GETSUM_EXPVALUE get the sum value of the exponential formual of
% each word in the specified document. This value will be used in
% model parameters updating later.
%
% author: anthonylife
% date  : 1/16/2013


sumvalue = sum(sigmoid(model.w, features'));
