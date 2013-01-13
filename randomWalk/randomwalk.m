%function randomwalk()
% RANDWALK implements the basic randomwalk algorithm as the
% paper <EMNLP, 2004> introduced.
%
% Procedures:
%   (1)Model parameters setting and global variables set-
%      ting
%   (2)Load infomation (including graph matrix, words to 
%      dictionary map)
%   (3)Normalization the graph (we leave the computation
%      here to avoid accuracy loss.)
%   (4)Run random walk
%   (5)Output them to file
%   (6)Call python function to evaluate the final results
%
%
% Author: anthonylife
% Date: 1/12/2013


% (1)Model parameters setting and global variables setting.
% ---------------------------------------------------------
alpha       = 0.85;
maxiter     = 500;
threshold   = 1e-5;
num_pre     = 1e-9;

dir_graph           = '../features/randomWalk/';
dir_map             = '../features/randomWalk/';
dir_result          = '../result/randomWalk/';
dense_graph_suffix  = 'dense';
sparse_graph_suffix = 'sparse';
map_suffix          = 'idmap';
result_suffix       = 'keyword.pv';

% (2)Load infomation (including graph matrix, words to 
%    dictionary map);
% ----------------------------------------------------
docinfo = loadinfo(dir_graph, dir_map, ...
    dense_graph_suffix, map_suffix);

% (3)Normalization the graph (we leave the computation
%    here to avoid accuracy loss.)
% ----------------------------------------------------
for i = 1:length(docinfo),
    docinfo(i).graph = mynormalize(docinfo(i).graph, 2);
end

% (4)Run random walk
% ------------------
for i = 1:length(docinfo),
    node_num = length(docinfo(i).graph);
    pv_old = repmat(1 / node_num, 1, node_num); 
    pv_new = repmat(0.0, 1, node_num); 
    for j=1:maxiter,
        pv_new = alpha*pv_old*docinfo(i).graph...
               + (1-alpha)*1/node_num;
        sum(pv_new)
        pause;
        assert(abs(sum(pv_new)-1)<num_pre, 'Sum value of nodes invalid');
        diff = sum(abs(pv_new - pv_old));
        fprintf('Iteration: %d, difference value: %f\n', j, diff);        
        pv_old = pv_new;    % update
        if diff < threshold,
            break;
        end
    end
    docinfo(i).pv = pv_new;
end

% (5)Output them to file
% ----------------------
outputinfo(docinfo, dir_result, result_suffix);

% (6)Call python function to evaluate the final results
% -----------------------------------------------------
cmd = ;
system(cmd)
