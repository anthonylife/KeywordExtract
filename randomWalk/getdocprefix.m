function getdocprefix(filefullpath)
%
% GETDOCPREFIX extracts the prefix of each document.
%
% author: anthonylife
% date  : 1/13/2013


pathparts = regexp(filefullpath, '/', 'split');
docname = regexp(pathparts(end), '.', 'split');
