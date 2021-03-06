function docinfo = loadinfo(dir_graph, dir_map, rep_choice, map_suffix)
%
% LOADINFO loads graph information and map information which will be used
% in the random walk model.
%
% Input:
%   dir_graph   --> the directory of graph files of all documents
%   dir_map     --> the directory of map files of all documents
%   rep_choice  --> graph storage representation in memeory: 'sprase' or 'dense'
%   map_suffix  --> map between words id in document to global dictionary
%
% Output:
%   docinfo, a structure which has the following two attributes:
%       graph       --> graph data stored in memory
%       ids_map     --> map relation stored in memory
%       pv          --> pagerank value for each text unit in documents
%   
% @auhtor : anthonylife
% @data   : 1/12/2013

doc = struct('graph', [], 'ids_map', [], 'pv', []);

if rep_choice == 'dense',
    graph_file = getdocname([dir_graph '*dense'], dir_graph);
    map_file = getdocname([dir_map '*' map_suffix], dir_map);
    docnum = length(graph_file);
    docinfo = repmat(doc, 1, docnum);

    for i=1:docnum,
        docinfo(i).graph_file = graph_file{i};
        docinfo(i).graph = load(graph_file{i});
        docinfo(i).map_file = map_file{i};
        docinfo(i).ids_map = load(map_file{i});
        docinfo(i).pv = repmat(0.0, 1, length(docinfo(i).graph));
    end

elseif rep_choice == 'sparse',
    graph_file = getdocname([dir_graph '*sparse'], dir_graph);
    map_file = getdocname([dir_map '*' map_suffix], dir_map);
    docnum = length(graph_file);
    docinfo = repmat(doc, 1, docnum);

    for i=1:docnum,
        docinfo(i).graph_file = graph_file{i};
        temp = load(graph_file{i});
        docinfo(i).graph = spconvert(temp);
        docinfo(i).map_file = map_file{i};
        docinfo(i).ids_map = load(map_file{i});
        docinfo(i).pv = repmat(0.0, 1, length(docinfo(i).graph));
    end

else,
    error('Invalid choice for graph representation.');
    exit(0)
end
