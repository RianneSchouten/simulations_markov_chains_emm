import numpy as np
import pandas as pd
import itertools as it
import string

import fomc_functions as fomcf

def define_attributes(dataset=None):

    cols = dataset.columns.values.tolist()
    
    first_timepoint = 's0'
    time_attributes = ['timepoint1']
    id_attribute = 'n'
    skip_attributes = []

    for col in cols:
        if 'state' in col:
            time_attributes.append(col)
    for col in cols:
        if col not in id_attribute and col not in time_attributes and 'x' not in col:
            skip_attributes.append(col)

    outcome_attribute = None
    descriptives = None
    
    attributes = {'time_attributes': time_attributes, 'skip_attributes': skip_attributes,
                  'id_attribute': id_attribute, 'first_timepoint': first_timepoint, 'descriptives': descriptives, 
                  'outcome_attribute': outcome_attribute}

    return attributes

def sample_dataset(N=None, T=None, S=None, ncovs=None, subgroup_order = None, distAyn=None, distPiyn=None):
    
    states, dataset_probs, subgroup_probs, covs = sample_parameters(N=N, S=S, ncovs=ncovs, 
                                                            subgroup_order=subgroup_order)

    df = covs.copy()
    df['n'] = np.arange(N)
    df['g'] = np.where((df.x0 == 1) & (df.x1 == 1), 1, 0)

    df_g1 = df[df.g == 1].copy() # sg
    N1 = len(df_g1)
    df_g0 = df[df.g == 0].copy() # non sg
    N2 = len(df_g0)

    # timepoint s0

    subgroup_probs['probs_0'].index.values

    df_g1['s0'] = np.random.choice(a=states, size=N1, p=subgroup_probs['probs_0']['pi'].values)
    df_g0['s0'] = np.random.choice(a=states, size=N2, p=dataset_probs['probs_0']['pi'].values)

    print(df_g1)

    # timepoint s1
    print(df_g1['s0'].values)
    old_data = [(state,) for state in df_g1['s0']]
    print(old_data)
    print(old_data[0])
    print(subgroup_probs['probs_1'].loc[old_data[0], ])
    df_g1['s1'] = list(map(lambda x: np.random.choice(a=states, size=1, p=subgroup_probs['probs_1'].loc[x])[0], old_data))
    print(df_g1['s1'])

    old_data = [(state,) for state in df_g0['s0']]
    print(old_data)
    df_g0['s1'] = list(map(lambda x: np.random.choice(a=states, size=1, p=dataset_probs['probs_1'].loc[x])[0], old_data))
    print(df_g0['s1'])

    for t in np.arange(1, T):
        old_column = 's' + str(t-1)
        new_column = 's' + str(t)

        df_g1[new_column] = list(map(lambda x: np.random.choice(a=states, size=1, p=subgroup_probs['probs_' + str].loc[x])[0], df_g1[old_column]))
        df_g0[new_column] = list(map(lambda x: np.random.choice(a=states, size=1, p=tB.loc[x])[0], df_g0[old_column]))
    
    df = pd.concat([df_g1, df_g0])
    
    # reshape dataset
    cols = df.columns.values.tolist()
    all_time_vars = ['s' + str(t) for t in np.arange(T)]
    id_vars = list(set(cols) - set(all_time_vars))
    df_minT = pd.melt(df.loc[:, df.columns != 's' + str(T-1)], id_vars=id_vars, var_name='timepoint1', value_name='state1')
    df_min0 = pd.melt(df.loc[:, df.columns != 's' + str(0)], id_vars=id_vars, var_name='timepoint2', value_name='state2')
    
    dataset = pd.concat([df_minT, df_min0[['timepoint2', 'state2']]], axis=1)
    dataset.sort_values(by = ['n', 'timepoint1'], inplace=True)
    dataset.reset_index(drop=True, inplace=True)

    return tA, tB, dataset, Adist, pidist

def sample_parameters(N=None, S=None, ncovs=None, subgroup_order=None):

    letters_tuples = list(it.product(string.ascii_uppercase, string.ascii_uppercase))
    letters = []
    for tuple in letters_tuples:
        letters.append(''.join(tuple))
    states = letters[0:S]

    # sample dataset parameters
    dataset_probs = sample_order_probs(states=states, subgroup_order=1)
    # sample parameters for the subgroup
    subgroup_probs = sample_order_probs(states=states, subgroup_order=subgroup_order)

    # sample covariates
    covs = pd.DataFrame()
    for cov in np.arange(ncovs):
        covs['x' + str(cov)] = np.random.binomial(n=1, p=0.5, size=N)
    
    return states, dataset_probs, subgroup_probs, covs

def sample_order_probs(states=None, subgroup_order=None):

    probs = {}
    S = len(states)

    # start with 0 order
    p = np.random.uniform(size=S, low=0.0, high=1.0)
    p_norm = p / np.repeat(p.sum(axis=0), S)
    index_states = [(st,) for st in states]
    probs['probs_' + str(0)] = pd.DataFrame(p_norm, index=index_states, columns=['pi'])

    for o in np.arange(1, subgroup_order+2):

        # do something
        p = np.random.uniform(size=S, low=0.0, high=1.0)
        p_norm = p / np.repeat(p.sum(axis=0), S)
    
        p_norm_cor = np.outer(probs['probs_' + str(o-1)].values.flatten(), p_norm)
        probs['probs_' + str(o)] = pd.DataFrame(p_norm_cor, index=it.product(states, repeat=o), columns=states)

    print(probs)

    return probs
