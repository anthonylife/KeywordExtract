function nm_data = mynormalize(data, d)
%
%   NORMALIZE do normalization for tensor(1-2 dimension) accroding
%   to the specified dimension 'd'.
%
%   Input variable:
%       dataform --> data needs to be normalized.
%       d        --> specified dimension to be normalized.
%
%   Output variable:
%       nm_data --> data having been normalized.
%
%   Date: 12/12/2012

if nargin < 2,
    d = 1;
end

data = repairgraph(data);

nm_const = sum(data, d);

if d == 1,
    nm_data = data * diag(1./nm_const);
elseif d == 2,
    nm_data = diag(1./nm_const) * data;
end
