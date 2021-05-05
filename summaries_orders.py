import numpy as np
import pandas as pd

import qualities_orders as qmo

def prepare_resultlist_cq(result_set=None, cq_satisfied=None, quality_measure=None, q=None, w=None):

    # add rules to result set - then order - then select q first as the current result set  
    result_set.append(cq_satisfied) # creates a nested list
    result_set = [item for sublist in result_set for item in sublist] # unlist alle elements
    result_set_ordered = sorted(result_set, key = lambda i: i['qualities'][quality_measure], reverse=True) # sort each description according to the sort var
    
    result_set = [result_set_ordered[0:q]] # Add descriptions to result set based on priority and q and save as a list for next iteration
    beam = sorted(cq_satisfied, key = lambda i: i['qualities'][quality_measure], reverse=True) 
    candidate_queue = beam[0:w]

    return result_set, candidate_queue

def resultlist_emm(result_set=None, distribution=None, quality_measure=None, general_params=None, Z=None):

    if len(result_set[0]) == 0:
        print('Empty result set')
        result_emm = None
    else:
        # first reduce the result set if the dfd should be taken into account
        if distribution is not None:
            print('len ordered', len(result_set[0]))
            result_set_selected = qmo.check_significance(result_set_ordered=result_set[0], 
                                                         general_params=general_params, 
                                                         quality_measure=quality_measure, Z=Z)
            print('len selected', len(result_set_selected))
        else:
            result_set_selected = result_set[0]

        # then change the format of the result set
        if len(result_set_selected) == 0:
            print('Empty result set')
            result_emm = None
        else: 
            #result_set_selected = result_set_selected[0]
            result_emm = pd.DataFrame.from_dict(result_set_selected[0]).T
            for sg in np.arange(1, len(result_set_selected)):
                result_emm = result_emm.append(pd.DataFrame.from_dict(result_set_selected[sg]).T)
            result_emm['sg'] = np.repeat(np.arange(len(result_set_selected)), 2) 
            result_emm.sort_index(axis=1, inplace=True)  

    return result_emm

def rank_result_emm(result_emm=None, quality_measure=None):

    # sometimes none of the subgroups containS x0 or x1 (true subgroup has a 1 for these two variables)
    # this can be problematic when searching for the rank
    # therefore we add these columns manually with NaN values
    if 'x1' not in result_emm:
        result_emm['x1'] = np.nan
    if 'x0' not in result_emm:
        result_emm['x0'] = np.nan

    # it is important that the covs are ordered from x0 to x1 to x2, etc.
    # this is done in resultlist_emm

    # get the idx of the subgroup of interest
    # get all covariates, they all start with 'x'
    # the covariates are ordered
    cols = result_emm.dtypes.index
    covs = cols[cols.str.startswith('x')]
    
    # get all descriptions, these are ordered in the result list based on the quality measure
    # the true subgroup has a 1 for the first two covariates (x0 and x1) and NaN for the other covariates
    descriptions = result_emm.loc['description', covs]
    qualities = result_emm.loc['qualities', :]

    #selection = list(map(lambda x: all(descriptions.iloc[x, :2].values == list(np.ones(2))) & 
    #                                all(pd.isnull(descriptions.iloc[x, 2:])), np.arange(len(descriptions))))

    selection = list(map(lambda x: all([val == [1] for val in descriptions.iloc[x,:2].values]) & 
                                    all(pd.isnull(descriptions.iloc[x, 2:])), np.arange(len(descriptions))))

    # for every description, True or False is given
    # the idx of the description that is True
    # add one to make it a rank (i.e. position 0 will become 1)
    # if all values are False, set rank to q + 1
    if not any(selection):
        col_rank = len(descriptions) + 1
        order = np.nan
    else: 
        ids = np.arange(len(descriptions))
        col_rank = ids[selection][0] + 1
        order = qualities.loc[qualities.sg == col_rank-1, 'best_order'].values[0]
   
    rank_subgroup = {quality_measure + '_rank': col_rank, quality_measure + '_order': order}

    return rank_subgroup

def join_result_emm(result_emm=None, result_rw_analysis=None, quality_measure=None, q=None):

    # allow a dataset to be analyzed with multiple quality measures
    # we store the dfd of all quality measures together
    if result_emm is not None:
        if len(result_emm) < q*2:
            l = len(result_emm)
        else: 
            l = q*2

        result_emm = result_emm.rename(columns={quality_measure:'qm_value'})
        result_emm['qm'] = np.repeat(quality_measure, l)

        result_rw_analysis = result_rw_analysis.append(result_emm)

    return result_rw_analysis


