import numpy as np
import pandas as pd

def prepare_resultlist_cq(result_set=None, cq_satisfied=None, quality_measure=None, q=None, w=None):

    # add rules to result set - then order - then select q first as the current result set  
    result_set.append(cq_satisfied) # creates a nested list
    result_set = [item for sublist in result_set for item in sublist] # unlist alle elements
    result_set_ordered = sorted(result_set, key = lambda i: i['qualities'][quality_measure], reverse=True) # sort each description according to the sort var
    result_set = [result_set_ordered[0:q]] # Add descriptions to result set based on priority and q and save as a list for next iteration
        
    beam = sorted(cq_satisfied, key = lambda i: i['qualities'][quality_measure], reverse=True) 
    candidate_queue = beam[0:w] # Bring the beam as the candidate queue to the next iteration

    return result_set, candidate_queue

def resultlist_emm(result_set=None):

    if len(result_set[0]) == 0:
        print('Empty result set')
        result_emm = None
    else:
        result_set = result_set[0]
        result_emm = pd.DataFrame.from_dict(result_set[0]).T
        for sg in np.arange(1, len(result_set)):
            result_emm = result_emm.append(pd.DataFrame.from_dict(result_set[sg]).T)
        result_emm['sg'] = np.repeat(np.arange(len(result_set)), 2)

    return result_emm

def rank_result_emm(result_emm=None, quality_measure=None):

    # sometimes none of the subgroups containS x0 or x1 (true subgroup has a 1 for these two variables)
    # this can be problematic when searching for the rank
    # therefore we add these columns manually with NaN values
    if 'x1' not in result_emm:
        result_emm['x1'] = np.nan
    if 'x0' not in result_emm:
        result_emm['x0'] = np.nan

    # get the idx of the subgroup of interest
    selection = result_emm.loc[(result_emm['x0'] == 1) & (result_emm['x1'] == 1)]
    if selection.size == 0:
        idx = len(result_emm) + 1
    else: 
        idx = selection['sg'].values[0] # not the real idx, but the number of the subgroup

    # order the output and select the rank of the subgroup
    result_emm_qualities = result_emm.loc['qualities']
    result_col_rank = result_emm_qualities[quality_measure].rank(ascending=False)
    if idx == len(result_emm) + 1:
        col_rank = len(result_emm_qualities) + 1 # for q = 25, this will give 26
    else: 
        col_rank = result_col_rank[idx]
    
    rank_subgroup = {quality_measure: col_rank}

    return rank_subgroup

def join_result_emm(result_emm=None, result_rw_analysis=None, quality_measure=None, q=None):

    if result_emm is not None:
        if len(result_emm) < q*2:
            l = len(result_emm)
        else: 
            l = q*2

        result_emm = result_emm.rename(columns={quality_measure:'qm_value'})
        result_emm['qm'] = np.repeat(quality_measure, l)

        result_rw_analysis = result_rw_analysis.append(result_emm)

    return result_rw_analysis

def join_general_params(general_params=None, result_rw_analysis=None):

    print(general_params)

    return result_rw_analysis


