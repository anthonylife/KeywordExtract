function auc = getaucvalue(docinfo, model)
%
% GETAUCVALUE computes the AUC value of ranking results, which
% means that positive instances should have higher values than
% negative instances.
%
% author: anthonylife
% date  : 1/16/2013

auc = 0.0;
for i=1:length(docinfo),
    pos_ins = find(docinfo(i).labels == 1);
    neg_ins = find(docinfo(i).labels == 0);
    sumvalue = getsumvalue(docinfo(i).features, model);
    docinfo(i).pv = getnodevalue(docinfo(i).features,...
                    1:length(docinfo(i).labels),model.w,sumvalue);
    acc_num = 0;
    for j=1:length(pos_ins),
        acc_num = acc_num+length(find(docinfo(i).pv(pos_ins(j))...
                >docinfo(i).pv(neg_ins)));
    end
    if length(pos_ins) == 0,
        auc = auc + 0;
    elseif length(neg_ins) == 0,
        auc = auc + 1;
    else,
        auc = auc + acc_num/(length(pos_ins)*length(neg_ins));
    end
end
auc = auc/length(docinfo);
