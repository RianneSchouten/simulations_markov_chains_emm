import numpy as np
import pandas as pd

def params_first_order_markov_chain_general(df=None, attributes=None):

    # the first time attribute is the counter or time index, the second and third are the two time points for a 1st order chain
    time_attributes = attributes['time_attributes']
    first_timepoint = attributes['first_timepoint']
    states = np.unique(np.concatenate((df[time_attributes[1]].unique(), df[time_attributes[2]].unique())))
    states = np.sort(states)

    ls1, ls, lss = t_count_matrix(df=df, time_attributes=time_attributes, states=states, first_timepoint=first_timepoint)
    tA, tpi = calculate_model_params(ls1=ls1, ls=ls, lss=lss, states=states)

    model_ls1 = tpi.copy()
    model_tA = tA.copy()
    ll_d = log_likelihood(states=states, model_ls1=model_ls1, model_tA=model_tA, data_ls1=ls1, data_lss=lss)

    params = {'ls1': ls1, 'ls': ls, 'lss': lss, 'tA': tA, 'tpi': tpi, 'll_d': ll_d, 'states': states}

    return params

def params_first_order_markov_chain_subgroup(df=None, subgroup=None, general_params=None, attributes=None):

    time_attributes = attributes['time_attributes']
    first_timepoint = attributes['first_timepoint']

    ls1, ls, lss = t_count_matrix(df=subgroup, time_attributes=time_attributes, states=general_params['states'], 
                                  first_timepoint=first_timepoint)
    tA, tpi = calculate_model_params(ls1=ls1, ls=ls, lss=lss, states=general_params['states'])

    model_ls1 = tpi.copy()
    model_tA = tA.copy()

    ll_sg = log_likelihood(states=general_params['states'], model_ls1=model_ls1, model_tA=model_tA, data_ls1=ls1, data_lss=lss)
    ll_pi_sg = log_likelihood(states=general_params['states'], model_ls1=general_params['tpi'].copy(), model_tA=general_params['tA'].copy(), data_ls1=ls1, data_lss=lss)
    ll_sg_d = log_likelihood(states=general_params['states'], model_ls1=model_ls1, model_tA=model_tA, data_ls1=general_params['ls1'], data_lss=general_params['lss'])

    params = {'ls1': ls1, 'ls': ls, 'lss': lss, 'tA': tA, 'tpi': tpi, 
              'll_sg': ll_sg, 'll_pi_sg': ll_pi_sg, 'll_sg_d': ll_sg_d} 

    return params

def t_count_matrix(df=None, time_attributes=None, states=None, first_timepoint=None):

    s = len(states)

    ls1 = df[df[time_attributes[0]] == first_timepoint][time_attributes[1]].value_counts()
    if (ls1.sum() == 0):
        print('ls1', ls1)
        print(df)

    add_states = list(set(states) - set(ls1.index.tolist()))
    ls1 = ls1.append(pd.Series(np.repeat(0, len(add_states)), index=add_states)).sort_index(axis=0)

    lss = df[[time_attributes[1], time_attributes[2]]].pivot_table(index=time_attributes[1], columns=time_attributes[2], fill_value=0, aggfunc=len)
    
    # it could happen that the subgroup does not have certain states that are available in the overall dataset
    # we therefore add columns and rows for states that are not available in the subgroup
    # later, we make sure that the column total is 1, to avoid divisions by zero
    if lss.shape != (s, s):
        if lss.shape[1] != s:
            add_states = list(set(states) - set(lss.columns.tolist()))
            add_data = pd.DataFrame(np.zeros(shape=(len(lss), len(add_states))), columns=add_states, index=lss.index.values)
            lss = pd.concat([lss, add_data], axis=1)
        if lss.shape[0] != s:
            add_states = list(set(states) - set(lss.index.tolist()))
            add_data = pd.DataFrame(np.zeros(shape=(len(add_states), s)), columns=states, index=add_states)
            lss = pd.concat([lss, add_data], axis=0)
            
    lss.sort_index(axis=1, inplace=True)
    lss.sort_index(axis=0, inplace=True)

    ls = lss.sum(axis=1) # apply to columns will give one sum value per row

    return ls1, ls, lss

def calculate_model_params(ls1=None, ls=None, lss=None, states=None):

    s = len(states)

    # for the calculation of proportions, we add 1 to every cell with 0
    ls_long = np.repeat(ls.values, s).reshape((s,s))
    if 0 in ls_long:
        ls_long[ls_long == 0] = 1

    tA = lss.values / ls_long

    tpi = ls1.values / ls1.sum()

    return tA, tpi

def log_likelihood(states=None, model_ls1=None, model_tA=None, data_ls1=None, data_lss=None):

    s = len(states)
    pi = model_ls1
    A = model_tA

    # for markov chains it can be done like this
    # because of computer rounding, a probability can be 0
    # however, it is not possible to take the log of a 0 probability
    # we therefore set those values to 1E-13
    # the function np.log in python uses the natural logarithm ln
    # which is what we need for the log likelihood (bishop)
    if 0.0 in pi:
        pi[pi == 0.] = 0.0000000000001
    ii = np.matmul(data_ls1.values, np.log(pi))
    
    if 0.0 in A:
        A[A == 0.] = 0.0000000000001
    aa = np.matmul(data_lss.values.reshape(s*s,), np.log(A).reshape(s*s,))
    
    ll = ii + aa

    return ll 