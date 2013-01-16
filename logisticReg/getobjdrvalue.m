function objdrvalue = getobjdrvalue(features, tr_pair, model, sum_expvalue)
%
% GETOBJDRVALUE means computing the value of derivative of the
% objective function.
%
% author: anthonylife
% date  : 1/16/2013


pos_idx = tr_pair(1);
neg_idx = tr_pair(2);
pos_value = getnodevalue(features, pos_idx, model.w);
neg_value = getnodevalue(features, neg_idx, model.w);
logis_drvalue = model.beta*exp(-model.beta*(neg_value-pos_value))...
              / (1 + exp(-model.beta*(neg_value-pos_value)));
exp_drvalue = (-features(neg_idx,:)*exp(-model.w'*features(neg_idx,:)')...
            + features(pos_idx,:)*exp(-model.w'*features(pos_idx,:)'))...
            * sum_expvalue - (exp(-model.w'*features(neg_idx,:)')...
            - exp(-model.w'*features(pos_idx,:)'))...
            * (-features'*exp(-model.w'*features')')';
objdrvalue = logis_drvalue .* exp_drvalue' / sum_expvalue^2;
