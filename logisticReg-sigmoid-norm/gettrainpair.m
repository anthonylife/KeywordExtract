function tr_pairs = gettrainpair(docinfo, strategy)    
%
% GETTRAINPAIR generates training pairs for each
% document accroding to the specified generating
% strategy.
%
% Input variable:
%   docinfo  --> data structure of document, including
%                'features', 'labels' and so on.
%   strategy --> training pairs generation strategy.
% Output variables:
%   tr_pairs --> generated training pairs with ids
%                in each document.
% 
% author: Anthonylife
% date  : 1/16/2013

pos_ins = find(docinfo.labels == 1);
neg_ins = find(docinfo.labels == 0);
switch strategy,
case 'full-pair',
    tr_pairs = fullpairgenerator(pos_ins, neg_ins);
case 'stocastic-pair',
    tr_pairs = partialpairgenerator(pos_ins, neg_ins);
otherwise,
    error('Invalid training pair generation method.');
    exit(1);
end
