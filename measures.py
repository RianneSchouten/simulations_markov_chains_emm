import numpy as np
import pandas as pd
#import time

def t_count_matrix(df=None, time_attributes=None, states=None, first_timepoint=None):

    s = len(states)

    ls1 = df[df[time_attributes[0]] == first_timepoint][time_attributes[1]].value_counts()
    add_states = list(set(states) - set(ls1.index.tolist()))
    ls1 = ls1.append(pd.Series(np.repeat(0, len(add_states)), index=add_states)).sort_index()

    lss = df[[time_attributes[1], time_attributes[2]]].pivot_table(index=time_attributes[1], columns=time_attributes[2], fill_value=0, aggfunc=len)
    # the subgroup may not contain certain states that are available in the overall dataset
    # we add columns and rows for states that are not available in the subgroup
    # we then later make sure that the column total is 1, to avoid divisions by zero
    if lss.shape != (s, s):
        if lss.shape[1] != s:
            add_states = list(set(states) - set(lss.columns.tolist()))
            add_data = pd.DataFrame(np.zeros(shape=(len(lss), len(add_states))), columns=add_states, index=lss.index.values)
            lss = pd.concat([lss, add_data], axis=1)
        if lss.shape[0] != s:
            add_states = list(set(states) - set(lss.index.tolist()))
            add_data = pd.DataFrame(np.zeros(shape=(len(add_states), s)), columns=states, index=add_states)
            lss = pd.concat([lss, add_data], axis=0)
    
    lss = lss.sort_index()
    lss.reindex(sorted(lss.columns), axis=1)

    ls = lss.sum(axis=1)
    ls_long = np.repeat(ls.values, s).reshape((s,s))
    if 0 in ls_long:
        ls_long[ls_long == 0] = 1

    tA = lss.values / ls_long
    tpi = ls1.values / ls1.sum()

    return ls1, ls, lss, tA, tpi

def manhattan_distance(taA=None, taB=None, lsB=None, weighted=True):

    g = taB # subgroup
    e = taA # dataset   

    if(weighted):
        s = len(lsB)
        w = np.repeat(lsB, s)
        d = np.matmul(w, np.abs(g-e).reshape(s*s, ))
    else:
        d = np.sum(np.abs(g-e))   

    return d

'''
def sample_dataset(df=None, size=None, time_attributes=None, general_params=None, M=None):

    states = general_params['states']
    wds = []

    for m in np.arange(M):

        # sample subset
        pos_idx = df.index.values
        idx = np.random.choice(pos_idx, size=size, replace=False)
        subset = df.iloc[idx]

        # calculate parameters
        ls1_r, ls_r, lss_r, tA_r = t_count_matrix(df=subset, time_attributes=time_attributes, states=states)
        w_d = manhattan_distance(taA=general_params['tA'], taB=tA_r, lsB=ls_r, weighted=True)
        wds.append(w_d)

    # calculate mu
    mu = np.mean(wds)
    sigma = np.std(wds)
    
    return mu, sigma
'''

def log_likelihood(states=None, model_ls1=None, model_tA=None, data_ls1=None, data_lss=None #,df=None, time_attributes=None, id_attribute=None
                    ):

    pi = model_ls1.values / model_ls1.sum()
    s = len(states)

    # for markov chains it can be done like this
    # because of computer rounding, a probability can be 0
    # however, it is not possible to take the log of a 0 probability
    # we therefore set those values to 1E-13
    if 0.0 in pi:
        pi[pi == 0.] = 0.0000000000001
    ii = np.matmul(data_ls1.values, np.log(pi))
    if 0.0 in model_tA:
        model_tA[model_tA == 0.] = 0.0000000000001
    aa = np.matmul(data_lss.values.reshape(s*s,), np.log(model_tA).reshape(s*s,))
    ll = ii + aa

    return ll 