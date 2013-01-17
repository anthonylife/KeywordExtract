function outputinfo(docinfo, model, dirdoc)
%
% OUTPUTINFO outputs the text units' (words) importance value to
% the local files, which will used by the python evaluation file.
%
% author : anthylife
% date   : 1/17/2013

for i=1:length(docinfo),
    docname = getdocprefix(docinfo(i).docname);
    sumvalue = getsumvalue(docinfo(i).features, model);
    docinfo(i).pv = getnodevalue(docinfo(i).features,...
                    1:length(docinfo(i).labels),model.w,sumvalue);
    outputfile = [dirdoc.output docname '.' dirdoc.outputsuffix];
    wfd = fopen(outputfile, 'w');
    for j=1:length(docinfo(i).pv),
        fprintf(wfd,'%d %f\n',docinfo(i).ids_map(j),docinfo(i).pv(j));
    end
    fclose(wfd);
end
