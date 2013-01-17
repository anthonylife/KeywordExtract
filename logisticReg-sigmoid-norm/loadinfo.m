function docinfo = loadinfo(dirdoc, datachoice)
%
% LOADINFO loads all features of text units for supervised method
% for keywords extraction.
%
% Input:
%   dirdoc     --> it is a structure which contains all the
%                  directories of features.
%   datachoice --> the choices including 'train', 'test' and 'va-
%                  lidation'.
%
% Output:
%   docinfo, a structure which has the following four attributes:
%       graph   --> graph data stored in memory
%       labels  --> labels of the text units
%       idsmap --> map relation stored in memory
%       pv      --> value for each text unit in documents
%   
% @auhtor : anthonylife
% @data   : 1/16/2013

doc = struct('features', [], 'labels', [], 'ids_map', [], ...
    'pv', [], 'docname', []);

switch datachoice,
case 'train',
    featuredoc = getdocname([dirdoc.train '*' dirdoc.docsuffix],...
        dirdoc.train);
case 'validation',
    featuredoc=getdocname([dirdoc.validation '*' dirdoc.docsuffix],...
        dirdoc.validation);
case 'test',
    [dirdoc.test '*' dirdoc.docsuffix]
    featuredoc = getdocname([dirdoc.test '*' dirdoc.docsuffix],...
        dirdoc.test);
    disp('haha');
otherwise,
    error('Invalid data choice.')
    exit(0)
end

docnum = length(featuredoc);
docinfo = repmat(doc, 1, docnum);

for i=1:docnum,
    docinfo(i).docname = featuredoc{i};
    docdata = load(featuredoc{i});
    docinfo(i).ids_map = docdata(:,1);
    docinfo(i).labels = docdata(:,2);
    docinfo(i).features = docdata(:,3:end);
    docinfo(i).pv = repmat(0.0, 1, length(docdata));
end
