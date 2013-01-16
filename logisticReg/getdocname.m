function docname = getdocname(docname_pattern, dir_file)
%
% GETDOCNAME implements the function of get documents' names in the specified 
% directory.
%
% Input:
%   docname_pattern --> it decides which will be matched
%   dir_file        --> directory of files
%
% Ouput:
%   docname --> documents' name list
%
% @anthor : anthonylife
% @date   : 1/12/2013

file_struct = dir(docname_pattern);
file_cell = struct2cell(file_struct);
docname = strcat(dir_file, file_cell(1,:));
