import numpy as np
import pandas as pd

def rank_result_emm(result_emm=None, quality_measure=None, true_desc_length=None):

    # sometimes none of the subgroups contains x0 or x1 or x2 (true subgroup has a 1 for these two variables)
    # this can be problematic when searching for the rank
    # therefore we add these columns manually with NaN values
    if 'x0' not in result_emm:
        result_emm['x0'] = np.nan
    if 'x1' not in result_emm:
        result_emm['x1'] = np.nan
    if 'x2' not in result_emm:
        result_emm['x2'] = np.nan

    # it is important that the covs are ordered from x0 to x1 to x2, etc.
    # this is done in pr.prepare_result_list

    # get the idx of the subgroup of interest
    # get all covariates, they all start with 'x'
    # the covariates are ordered
    cols = result_emm.dtypes.index
    covs = cols[cols.str.startswith('x')]
    
    # get all descriptions, these are ordered in the result list based on the quality measure
    descriptions = result_emm.loc['description', covs]
    qualities = result_emm.loc['qualities', :]

    # the true subgroup has a 1 for the first 1 or 2 covariates (x0,x1) and NaN for the other covariates
    # note that x10 is ordered behind x1. This method does not work if you want to check >2 covariates!
    # the length of the description is determined by: true_desc_length
    selection = list(map(lambda x: all([val == [1] for val in descriptions.iloc[x,:true_desc_length].values]) & 
                                    all(pd.isnull(descriptions.iloc[x, true_desc_length:])), np.arange(len(descriptions))))

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



