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

def sample_dataset(N=None, T=None, S=None, ncovs=None, distAyn=None, distPiyn=None):
    
    states, tA, tB, covs, Adist, pidist = sample_parameters(N=N, S=S, ncovs=ncovs, distAyn=distAyn, distPiyn=distPiyn)

    df = covs.copy()
    df['n'] = np.arange(N)
    df['g'] = np.where((df.x0 == 1) & (df.x1 == 1), 1, 0)

    df_g1 = df[df.g == 1].copy()
    N1 = len(df_g1)
    df_g0 = df[df.g == 0].copy()
    N2 = len(df_g0)

    df_g1['s0'] = np.random.choice(a=states, size=N1, p=tA.loc['pi'])
    df_g0['s0'] = np.random.choice(a=states, size=N2, p=tB.loc['pi'])

    for t in np.arange(1, T):
        old_column = 's' + str(t-1)
        new_column = 's' + str(t)

        df_g1[new_column] = list(map(lambda x: np.random.choice(a=states, size=1, p=tA.loc[x])[0], df_g1[old_column]))
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

def sample_parameters(N=None, S=None, ncovs=None, distAyn=None, distPiyn=None):

    letters_tuples = list(it.product(string.ascii_uppercase, string.ascii_uppercase))
    letters = []
    for tuple in letters_tuples:
        letters.append(''.join(tuple))
    states = letters[0:S]

    if distAyn:
        # sample two transition matrices
        tA_values = np.random.uniform(size=S*S, low=0.0, high=1.0)
        tA = pd.DataFrame(data=tA_values.reshape((S, S)), index=states, columns=states)
        tA = tA / np.repeat(tA.sum(axis=1), S).values.reshape((S, S))
    
        tB_values = np.random.uniform(size=S*S, low=0.0, high=1.0)
        tB = pd.DataFrame(data=tB_values.reshape((S, S)), index=states, columns=states)
        tB = tB / np.repeat(tB.sum(axis=1), S).values.reshape((S, S))

        Adist = fomcf.manhattan_distance(taA=tA.values.reshape(S*S,1), taB=tB.values.reshape(S*S,1), weighted=False)

    else:
        # sample one transition matrix
        tA_values = np.random.uniform(size=S*S, low=0.0, high=1.0)
        tA = pd.DataFrame(data=tA_values.reshape((S, S)), index=states, columns=states)
        tA = tA / np.repeat(tA.sum(axis=1), S).values.reshape((S, S))
        tB = tA.copy()

        Adist = 0

    if distPiyn:

        init_prob_A = np.random.uniform(size=S, low=0.0, high=1.0)
        init_prob_A = init_prob_A / np.sum(init_prob_A)
        tA = tA.append(pd.DataFrame(init_prob_A, columns=['pi'], index=states).T)

        init_prob_B = np.random.uniform(size=S, low=0.0, high=1.0)
        init_prob_B = init_prob_B / np.sum(init_prob_B)
        tB = tB.append(pd.DataFrame(init_prob_B, columns=['pi'], index=states).T)

        pidist = fomcf.manhattan_distance(taA=init_prob_A, taB=init_prob_B, weighted=False)

    else:
        init_prob_A = np.random.uniform(size=S, low=0.0, high=1.0)
        init_prob_A = init_prob_A / np.sum(init_prob_A)
        tA = tA.append(pd.DataFrame(init_prob_A, columns=['pi'], index=states).T)
        tB = tB.append(pd.DataFrame(init_prob_A, columns=['pi'], index=states).T)

        pidist = 0

    # sample covariates
    covs = pd.DataFrame()
    for cov in np.arange(ncovs):
        covs['x' + str(cov)] = np.random.binomial(n=1, p=0.5, size=N)
    
    return states, tA, tB, covs, Adist, pidist


