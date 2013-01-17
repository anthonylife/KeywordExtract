function datapairs = fullpairgenerator(pos_ins, neg_ins)
%
% FULLPAIRGENERATOR generate all candidate pairs based
% on the two input id sets.
%

datapairs = repmat(0, length(pos_ins)*length(neg_ins), 2);
idx = 1;
for i=1:length(pos_ins),
    for j=1:length(neg_ins),
        datapairs(idx,1) = pos_ins(i);
        datapairs(idx,2) = neg_ins(j);
        idx = idx + 1;
    end
end

seq = randperm(length(pos_ins)*length(neg_ins));
datapairs = datapairs(seq,:);
