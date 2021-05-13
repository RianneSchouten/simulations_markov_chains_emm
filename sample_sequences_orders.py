import numpy as np
import pandas as pd
import itertools as it
import string

def define_attributes(dataset=None, time_attributes=None):

    cols = dataset.columns.values.tolist()
    
    id_attribute = 'n'
    first_timepoint = 0
    skip_attributes = []

    for col in cols:
        if col not in id_attribute and col not in time_attributes and 'x' not in col:
            skip_attributes.append(col)

    outcome_attribute = None
    descriptives = None
    
    attributes = {'time_attributes': time_attributes, 'skip_attributes': skip_attributes,
                  'id_attribute': id_attribute, 'first_timepoint': first_timepoint, 'descriptives': descriptives, 
                  'outcome_attribute': outcome_attribute}

    return attributes

def sample_dataset(N=None, T=None, S=None, ncovs=None, 
                   p=None, true_desc_length=None, global_model_order=None, 
                   subgroup_order=None):
    
    states, dataset_probs, subgroup_probs = sample_parameters(N=N, S=S, ncovs=ncovs, 
                                                              global_model_order=global_model_order,
                                                              subgroup_order=subgroup_order)

    timepoint_names = ['s' + str(k) for k in np.arange(T+1)]

    covs, indicator_subgroup = sample_covs(N=N, ncovs=ncovs, p=p, true_desc_length=true_desc_length)
    df = covs.copy()
    df['n'] = np.arange(N)
    df['g'] = indicator_subgroup

    df_sg = df[df.g == 1].copy().reset_index(drop=True) # sg
    N1 = len(df_sg)
    df_d = df[df.g == 0].copy().reset_index(drop=True) # non sg
    N2 = len(df_d)

    df_sg = sample_extra_timepoints(df_sg=df_sg, probs=subgroup_probs, N=N1, order=subgroup_order, states=states, timepoint_names=timepoint_names, S=S, T=T)
    df_d = sample_extra_timepoints(df_sg=df_d, probs=dataset_probs, N=N2, order=global_model_order, states=states, timepoint_names=timepoint_names, S=S, T=T)
    df = pd.concat([df_sg, df_d]).sort_values(by=['n'])
    
    # reshape dataset
    time_attributes = ['transition', 'source', 'target']
    dataset = from_p_to_2_columns(df=df, time_attributes=time_attributes, T=T)

    return dataset, states, time_attributes

def sample_extra_timepoints(df_sg=None, probs=None, N=None, order=None, states=None, timepoint_names=None, S=None, T=None):

    if order == 0:

        # sample first timepoint from pi
        first_timepoints = np.random.choice(a=states, size=N, p=probs['probs_0'].values.flatten())
        df_first_timepoints = pd.DataFrame(first_timepoints, columns=['s0'])
        
        # get probs of interest
        name_A = 'probs_' + str(1)
        probs = probs[name_A]
        probs_norm = probs / np.repeat(probs.sum(axis=1).values, S).reshape(S**(order+1), S)

        # subgroup timepoint k+2:T
        for t in np.arange(order+1, T):
            new_column = 's' + str(t)            
            df_first_timepoints[new_column] = list(map(lambda x: np.random.choice(a=states, size=1, p=probs_norm.loc[[tuple(df_first_timepoints.loc[x, timepoint_names[t-1:t]])], :].values[0])[0],
                                                                 np.arange(N)))
        
    else:
        
        # first timepoints
        # first order timepoints
        
        # check if the sequences are long enough for the desired order
        # this will not happen for our current simulation setting where T = 10 and subgroup_order = 4
        # or when T = 2 and subgruop_order = 0 (in reality, this is 1).
        if T <= order:
            name_A = 'probs_' + str(T - 1)
            order = T - 1
            print('adapted order to', order)
        else: 
            name_A = 'probs_' + str(order)
        
        # set the right list of states
        expended_states = list(it.product(states, repeat=order+1))

        idx_first_timepoints = np.random.choice(a=np.arange(S**(order+1)), size=N, p=probs[name_A].values.flatten())
        first_timepoints = [expended_states[i] for i in idx_first_timepoints]
        df_first_timepoints = pd.DataFrame(first_timepoints, columns=timepoint_names[0:(order+1)])

        # normalize probs for sampling each subsequent timepoint
        probs = probs[name_A]
        probs_norm = probs / np.repeat(probs.sum(axis=1).values, S).reshape(S**order, S)

        for t in np.arange(order+1, T): #to T gives T-1 transitions
            new_column = 's' + str(t)
            df_first_timepoints[new_column] = list(map(lambda x: np.random.choice(a=states, size=1, p=probs_norm.loc[[tuple(df_first_timepoints.loc[x, timepoint_names[t-order:t]])], :].values[0])[0],
                                                                 np.arange(N)))
    
    sampled_timepoint_data = df_sg.join(df_first_timepoints, )

    return sampled_timepoint_data

def sample_parameters(N=None, S=None, ncovs=None, global_model_order=None, subgroup_order=None, p=None):

    letters_tuples = list(it.product(string.ascii_uppercase, string.ascii_uppercase))
    letters = []
    for tuple in letters_tuples:
        letters.append(''.join(tuple))
    states = letters[0:S] 

    # sample dataset parameters
    dataset_probs = sample_order_probs(states=states, order=global_model_order)

    # sample parameters for the subgroup
    subgroup_probs = sample_order_probs(states=states, order=subgroup_order)
    if subgroup_order == 0:
        subgroup_probs['probs_' + str(1)] = dataset_probs['probs_1']
    
    return states, dataset_probs, subgroup_probs

def sample_covs(N=None, ncovs=None, p=None, true_desc_length=None):

    frac = 0.01
    while frac <= 0.1:
        
        # sample covariates
        covs = pd.DataFrame()
        for cov in np.arange(ncovs):
            covs['x' + str(cov)] = np.random.binomial(n=1, p=p, size=N)

        # tell which cases should be in subgroup
        if true_desc_length == 1:        
            indicator_subgroup = np.where((covs.x0 == 1), 1, 0)        
        elif true_desc_length == 2:
            indicator_subgroup = np.where((covs.x0 == 1) & (covs.x1 == 1), 1, 0)
        elif true_desc_length == 3:
            indicator_subgroup = np.where((covs.x0 == 1) & (covs.x1 == 1) & (covs.x2 == 1), 1, 0)

        frac = np.sum(indicator_subgroup) / N
        #print(frac)

    return covs, indicator_subgroup

def sample_order_probs(states=None, order=None):

    probs = {}
    S = len(states)

    # start with 0 order
    p = np.random.uniform(size=S, low=0.0, high=1.0)
    p_norm = p / np.repeat(p.sum(axis=0), S)
    index_states = [(st,) for st in states]
    probs['probs_' + str(0)] = pd.DataFrame(p_norm, index=index_states, columns=['pi'])

    if order > 0:
        for o in np.arange(1, order+1):

            # new probs for next level
            p = np.random.uniform(size=S**(o+1), low=0.0, high=1.0).reshape(S**o, S)
            p_norm = p.reshape(S**(o+1),) / np.repeat(p.sum(axis=1), S).reshape(S**(o+1),)
    
            # we multiply the old probs with the new probs
            # as such, normalization of a higher order matrix will be valid
            # it also means that for the final probability matrix, the values sum to 1 for the total matrix, and not per row
            earlier_probs = np.repeat(probs['probs_' + str(o-1)].values, S).reshape(S**(o+1),)
            p_norm_cor = earlier_probs * p_norm
            probs['probs_' + str(o)] = pd.DataFrame(p_norm_cor.reshape(S**o, S), index=it.product(states, repeat=o), columns=states)

    return probs

def from_p_to_2_columns(df=None, time_attributes=None, T=None):

    cols = df.columns.values.tolist()
    all_time_vars = ['s' + str(t) for t in np.arange(T)]
    id_vars = list(set(cols) - set(all_time_vars))

    source = pd.melt(df.loc[:, df.columns != 's' + str(T-1)], id_vars=id_vars, var_name=time_attributes[0], value_name=time_attributes[1])    
    target = pd.melt(df.loc[:, df.columns != 's' + str(0)], id_vars=id_vars, var_name='transition2', value_name=time_attributes[2])   
    dataset = pd.concat([source, target[['transition2', time_attributes[2]]]], axis=1)

    dataset[time_attributes[0]] = dataset[time_attributes[0]].apply(lambda x: int(x[1:]))
    dataset['transition2'] = dataset['transition2'].apply(lambda x: int(x[1:]))
    dataset.sort_values(by = ['n', time_attributes[0]], inplace=True)
    dataset.reset_index(drop=True, inplace=True)

    return dataset
