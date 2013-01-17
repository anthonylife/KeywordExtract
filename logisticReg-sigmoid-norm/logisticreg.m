% function lgr()
% LGR implements the supervised method for keywords extraction
% with BPR learning framework.
%
% As we want to constrain that the sum of the values of text
% unit to be 1, we adopt a normalization exponential score 
% function to represent the score of text units.
%
% Note: The difference between this version (with "V1") and
% the old version (without "V1") is that the new version use
% sigmod function as score function for text units instead of
% 
%
% Procedures:
%   (1)Model parameters setting and global variables setting;
%   (2)Load the text unit features;
%   (3)Run the BPR framework with SGD learning algorithm;
%   (4)Tune the hyper-parameters on the validation data;
%   (5)Output the value of the results to the files;
%   (6)Call pathon function to evaluate the final results.
%
% Author : anthonylife
% Date   : 1/17/2013


%if 0,
clear;
% (1)Model parameters setting and global variables setting
% --------------------------------------------------------
lr      = 0.1;             % learning rate
alpha   = 0.01;                % regularization parameter
maxiter = 20;               % maximal number of iterations
threshold_diff   = 1e-3;    % difference value for termination
randompair_ratio = 2;       % ration between positive and negative
                            % when adopting 'stochastic-pair'.
featurenum   = 3;           % number of explicit features
trins_policy = 'full-pair'; % strategy of training pairs adoption
%trins_policy= 'stochastic-pair';

% model parameters
% ================
model.beta = 10;
model.w    = repmat(0.0, featurenum, 1);

% directory path setting
% ======================
dirdoc=struct('train',[],'test',[],'validation',[],'docsuffix',[]);
dirdoc.train = '../features/logisticReg/Train/';
dirdoc.validation  = '../features/logisticReg/Validation/';
dirdoc.test = '../features/logisticReg/Test/';
dirdoc.docsuffix  = 'feature';
dirdoc.output = '../result/logisticReg/';
dirdoc.outputsuffix = 'keyword.pv';

% (2)Load the text unit features of train data
% --------------------------------------------
docinfo = loadinfo(dirdoc, 'train');

% (3)Run the BPR framework with SGD learning algorithm
% ----------------------------------------------------
old_auc = 0.5;  % random guess
best_w  = repmat(0.0, featurenum, 1);
best_auc = 0;
for i=1:maxiter,
    seq = randperm(length(docinfo));
    w_old = model.w;
    auc = getaucvalue(docinfo, model);
    tic;
    s = 0;
    for j=seq,
        tr_pairs = gettrainpair(docinfo(j), trins_policy);
        if length(tr_pairs) == 0,
            continue;
        end
        objdrvalue = 0.0;
        for k=1:size(tr_pairs,1),
            sumvalue=getsumvalue(docinfo(j).features,model);
            pairdrvalue = getobjdrvalue(docinfo(j).features,...
                            tr_pairs(k,:), model, sumvalue);
            objdrvalue = objdrvalue + pairdrvalue;
            %model.w = model.w - lr*(objdrvalue+alpha*model.w);
        end
        objdrvalue = objdrvalue / length(tr_pairs);
        %model.w = model.w - lr*objdrvalue;
        model.w = model.w - lr*(objdrvalue+alpha*model.w);
        %{    
            disp('New iteration');
            objdrvalue
            model.w
            new_auc = getaucvalue(docinfo, model)
            totalerror = getobjerror(docinfo, model)
            pause;
        %}
        elapsed = toc;
        s = s+1;
        if mod(s,200) == 0,
        fprintf(1,'RTS:%s (%d sec/step)\n', ....
	    rtime(elapsed*(length(seq)/s-1)),round(elapsed/s)+1);
        end
    end
    new_auc = getaucvalue(docinfo, model);
    totalerror = getobjerror(docinfo, model);
    w_diff = sum(abs(model.w - w_old));
    auc_diff = new_auc - old_auc;
    fprintf('Iteration %d, New AUC value: %f, ', i, new_auc); 
    fprintf('Weight diff: %f, Total error: %f\n',w_diff,totalerror);
    model.w
    old_auc = new_auc;
    if new_auc > best_auc,
        best_auc = new_auc;
        best_w   = model.w;
    end
end
model.w = best_w;

% (4)Tune the hyper-parameters on the validation data
% ---------------------------------------------------
docinfo = loadinfo(dirdoc, 'validation');
valiauc = getaucvalue(docinfo, model);
fprintf('The AUC value of validation set is: %f\n', valiauc); 
%end
% (5)Output the value of the results to the files
% -----------------------------------------------
clear docinfo;
docinfo = loadinfo(dirdoc, 'test');
testauc = getaucvalue(docinfo, model);
fprintf('The AUC value of test set is: %f\n', valiauc); 
fprintf('Output the text unit values to the files.\n'); 
outputinfo(docinfo, model, dirdoc);

% (6)Call pathon function to evaluate the final results
% -----------------------------------------------------
%cmd
%system(cmd);
