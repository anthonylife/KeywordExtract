function outputinfo(docinfo, dir_result, result_suffix)
% OUTPUTINFO function outputs the pagerank value of each text unit
% to the disk files.
%
% author:anthonylife
% date  :1/13/2012


for i=1:length(docinfo),
    docname = getdocprefix(docinfo(i).graph_file);
    outputfile = [dir_result docname '.' result_suffix];
    wfd = fopen(outputfile, 'w');
    for j=1:length(docinfo(i).pv),
        fprintf(wfd, '%d %f\n', docinfo(i).ids_map(j), docinfo(i).pv(j));
    end
    fclose(wfd);
end
