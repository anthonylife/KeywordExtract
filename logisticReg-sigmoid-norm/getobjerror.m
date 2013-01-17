function totalerror = getobjerror(docinfo, model)
%
% GETOBJERROR computes the whole error of the final ranking results.
% Note that it is the real target value that BPR learning framework
% pursues, while AUC value is approximated by it.
%
% author : anthylife
% date   : 1/17/2013


totalerror = 0.0;
for i=1:length(docinfo)
    pos_ins = find(docinfo(i).labels == 1);
    neg_ins = find(docinfo(i).labels == 0);
    sumvalue = getsumvalue(docinfo(i).features, model);
    docinfo(i).pv = getnodevalue(docinfo(i).features,...
                    1:length(docinfo(i).labels), model.w, sumvalue);
    for j=1:length(pos_ins),
        totalerror=totalerror+sum(1./(1+exp(-model.beta*...
            (docinfo(i).pv(neg_ins)-docinfo(i).pv(pos_ins(j))))));
    end
end
