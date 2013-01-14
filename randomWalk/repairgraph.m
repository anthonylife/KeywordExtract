function graph = repairgraph(graph)
%
% REPAIRGRAPH examine the graph and add the edge to
% the nodes which are not connected in the original
% graph. In this function, for all those nodes, make
% them connect to all other nodes.
%

nodenum = length(graph);

for i=1:nodenum,
    if sum(graph(i,:)) == 0,
        graph(i,i) = 1;
    end
end
