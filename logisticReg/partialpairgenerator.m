function datapairs = fullpairgenerator(pos_ins, neg_ins)
%
% PARTIALPAIRGENERATOR generate stocastic candidate pairs based
% on the two input id sets.
%

global randompair_ratio;

datapairs = repmat(0, length(pos_ins)*randompair_ratio);
for i=1:length(pos_ins),
    datapairs(i,:)=randi(length(neg_ins), 1, randompair_ratio);
end
