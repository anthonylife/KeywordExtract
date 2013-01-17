function objdrvalue = getobjdrvalue(features, tr_pair, model, sumvalue)
%
% GETOBJDRVALUE means computing the value of derivative of the
% objective function.
%
% author: anthonylife
% date  : 1/16/2013


pos_idx = tr_pair(1);
neg_idx = tr_pair(2);
pos_value = getnodevalue(features, pos_idx, model.w, sumvalue);
neg_value = getnodevalue(features, neg_idx, model.w, sumvalue);

objfunc_deriva = model.beta*exp(-model.beta*(neg_value-pos_value))...
              / (1 + exp(-model.beta*(neg_value-pos_value)));
nodescore_deriva...
    =(features(neg_idx,:)'*sigmoid_deriva(model.w,features(neg_idx,:)')...
    -features(pos_idx,:)'*sigmoid_deriva(model.w,features(pos_idx,:)'))...
    *sumvalue - (sigmoid(model.w,features(neg_idx,:)')...
    -sigmoid(model.w,features(pos_idx,:)'))...
    *features'*sigmoid_deriva(model.w,features')';


objdrvalue = objfunc_deriva.*nodescore_deriva/sumvalue^2;
