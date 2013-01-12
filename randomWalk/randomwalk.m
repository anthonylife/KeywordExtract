%function randomwalk()
% RANDWALK implements the basic randomwalk algorithm as the
% paper <EMNLP, 2004> introduced.
%
% Procedures:
%   (1)Model parameters setting and global variables set-
%      ting.
%   (2)Load infomation (including graph matrix, words to 
%      dictionary map);
%   (3)Normalization the graph (we leave the computation
%      here to avoid accuracy loss.)
%   (4)Run random walk
%   (5)Gather result (merge keywords to keyphrases) and
%      ouput them to file
%   (6)Call python function to evaluate the final results
%
%
% Author: anthonylife
% Date: 1/12/2013


% (1)Model parameters setting and global variables setting.
% ---------------------------------------------------------
alpha       = 0.85;
maxiter     = 500;
threshold   = 1e-2;

dir_graph           = '../features/randomWalk/';
dir_map             = '../features/randomWalk/';
dense_graph_suffix  = 'dense';
sparse_graph_suffix = 'sparse';
map_suffix          = 'idmap';

% (2)Load infomation (including graph matrix, words to 
%    dictionary map);
% ----------------------------------------------------
[graph, ids_map] = loadinfo(dir_graph, dir_map, ...
    dense_graph_suffix, map_suffix);

% (3)Normalization the graph (we leave the computation
%    here to avoid accuracy loss.)
