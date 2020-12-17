import numpy as np
import pandas as pd
import itertools as it

import mc_functions_orders as fo

def params_markov_chain_general(df=None, attributes=None, order=None, start_at_order=None, data_size=None, quality_measure=None):

    # the first time attribute is the counter or time index, the second and third are the two time points for a 1st order chain
    time_attributes = attributes['time_attributes']
    first_timepoint = attributes['first_timepoint']
    states = np.unique(np.concatenate((df[time_attributes[1]].unique(), df[time_attributes[2]].unique())))
    
    # prepare empty transition matrices for higher order chains
    states, empty_dfs, col_list = order_and_prepare_states(states=states, time_attributes=time_attributes, start_at_order=start_at_order)

    # comment out line 19 to test whether entire dataset follows order 1
    # furthermore, comment out line 40 and 41, and uncomment lines 36,37
    # and comment out all lines after line 25 in beam_search_orders
    # and from line 89 in experiment_orders 
    #order = start_at_order

    # calculate the frequency matrix
    freqs, df_additions, new_order = higher_order_count_matrix(df=df, time_attributes=time_attributes, states=states, first_timepoint=first_timepoint,
                                                    id_attribute=attributes['id_attribute'], order=order, col_list=col_list, empty_dfs=empty_dfs)
    
    # calculate the frequency matrices for the first k timepoints
    initial_freqs = initial_count_matrix(df=df_additions, time_attributes=time_attributes, states=states, first_timepoint=first_timepoint,
                                         id_attribute=attributes['id_attribute'], order=new_order, col_list=col_list, empty_dfs=empty_dfs)
    
    # calculate the probability transition matrices by normalizing the frequency matrices
    probs = calculate_model_probs(freqs=freqs, s=len(states), order=new_order)
    
    # calculate the likelihood fit of the entire data plus the order of the markov chain using bic or aic
    # this function can be used to check the order of the dataset
    #score, lld, found_order = fo.calculate_best_fitting_order(probs=probs, freqs=freqs, initial_freqs=initial_freqs, start_at_order=order, 
    #                                                         s=len(states), quality_measure=quality_measure, data_size=data_size)
    # instead, we calculate the lld and score given an order of 1
    lld, lld_list = fo.calculate_log_likelihood(probs=probs, freqs=freqs, initial_freqs=initial_freqs, ll_list=None, order=order, s=len(states), print_this=False)
    score = fo.calculate_score(ll=lld, quality_measure=quality_measure, order=order, s=len(states), data_size=data_size, print_this=False)
    found_order = np.nan
    
    #print(found_order)
    #print(score)
    #print(lld)

    params = {'freqs': freqs, 'initial_freqs': initial_freqs, 'probs': probs, 'empty_dfs': empty_dfs, 'col_list': col_list, 
              'score': score, 'lld': lld, 'found_order': found_order, 'states': states}

    return params

def params_markov_chain_subgroup(subgroup=None, subgroup_compl=None, general_params=None, attributes=None, quality_measure=None, start_at_order=None, ref=None):

    time_attributes = attributes['time_attributes']
    first_timepoint = attributes['first_timepoint']
    params = {}
   
    if quality_measure in ['deltatv', 'omegatv', 'phiwrl']:

        freqs1_alltimepoints, df_alltimepoints, new_order = higher_order_count_matrix(df=subgroup, time_attributes=time_attributes, states=general_params['states'], 
                                                                           first_timepoint=first_timepoint, id_attribute=attributes['id_attribute'], order=1, 
                                                                           col_list=general_params['col_list'], empty_dfs=general_params['empty_dfs'])
        initial_freqs = initial_count_matrix(df=df_alltimepoints, time_attributes=time_attributes, states=general_params['states'], first_timepoint=first_timepoint,
                                             id_attribute=attributes['id_attribute'], order=1, col_list=general_params['col_list'], empty_dfs=general_params['empty_dfs'])
        probs1_alltimepoints = calculate_model_probs(freqs=freqs1_alltimepoints, s=len(general_params['states']), order=1)
        params.update({'freqs1_alltimepoints': freqs1_alltimepoints, 'probs1_alltimepoints': probs1_alltimepoints, 'initial_freqs': initial_freqs})

    else:

        freqs, sg_additions, new_order = higher_order_count_matrix(df=subgroup, time_attributes=time_attributes, states=general_params['states'], first_timepoint=first_timepoint,
                                                    id_attribute=attributes['id_attribute'], order=start_at_order, col_list=general_params['col_list'], empty_dfs=general_params['empty_dfs'])

        initial_freqs = initial_count_matrix(df=sg_additions, time_attributes=time_attributes, states=general_params['states'], first_timepoint=first_timepoint,
                                         id_attribute=attributes['id_attribute'], order=new_order, col_list=general_params['col_list'], empty_dfs=general_params['empty_dfs'])

        probs = calculate_model_probs(freqs=freqs, s=len(general_params['states']), order=new_order)
        params.update({'freqs': freqs, 'initial_freqs': initial_freqs, 'probs': probs, 'new_order': new_order})

    # same for complement
    # complement always has order 1
    # not necessary if we compare with the dataset
    if ref != 'dataset':
        freqs_compl, sg_compl_additions, new_order = higher_order_count_matrix(df=subgroup_compl, time_attributes=time_attributes, states=general_params['states'], first_timepoint=first_timepoint,
                                                                id_attribute=attributes['id_attribute'], order=1, col_list=general_params['col_list'], empty_dfs=general_params['empty_dfs'])

        initial_freqs_compl = initial_count_matrix(df=sg_compl_additions, time_attributes=time_attributes, states=general_params['states'], first_timepoint=first_timepoint,
                                               id_attribute=attributes['id_attribute'], order=1, col_list=general_params['col_list'], empty_dfs=general_params['empty_dfs'])

        probs_compl = calculate_model_probs(freqs=freqs_compl, s=len(general_params['states']), order=1)
        params.update({'freqs_compl': freqs_compl, 'initial_freqs_compl': initial_freqs_compl, 'probs_compl': probs_compl, 'new_order': new_order})

    return params

def order_and_prepare_states(states=None, time_attributes=None, start_at_order=None):

    states = np.sort(states)
    empty_dfs = {}
    col_list = [time_attributes[1], time_attributes[2]]

    for o in np.arange(1, start_at_order+1):

        if o < 2:
            
            all_possible_indices = states
            empty_lss = pd.DataFrame(index=states)
            empty_dfs['empty_lss_' + str(0)] = empty_lss
            empty_dfs['empty_lss_' + str(o)] = empty_lss

        else:

            all_possible_indices = list(it.product(states, repeat = o))

            shift_col = time_attributes[2] + str(o + 1)
            col_list = col_list + [shift_col]

            idx = pd.MultiIndex.from_tuples(all_possible_indices, names=col_list[0:o])

            empty_lss = pd.DataFrame(index=idx)
            empty_dfs['empty_lss_' + str(o)] = empty_lss            

    return states, empty_dfs, col_list

def higher_order_count_matrix(df=None, time_attributes=None, states=None, first_timepoint=None, id_attribute=None, order=None, col_list=None, empty_dfs=None):

    s = len(states)
    freqs = {}

    # parameters given argument order
    # extra check if the length of the sequences is not enough to calculate a certain order
    maxs = df.loc[:, [id_attribute, time_attributes[0]]].pivot_table(index=[id_attribute], values=[time_attributes[0]], aggfunc=np.max)
    min_T = int(min(maxs.iloc[:, -1]) - first_timepoint)
    if min_T + 1 < order:
        order = min_T + 1
        #print('new order', order)
        #print('have to change order')
    new_order = order

    if new_order == 1:
        lss = df[[time_attributes[1], time_attributes[2]]].pivot_table(index=time_attributes[1], columns=time_attributes[2], fill_value=0, aggfunc=len)

    else:
        ids = df[id_attribute].unique()
        for o in np.arange(2, new_order+1):   
            out = list(map(lambda x: df.loc[(df[id_attribute] == x), time_attributes[2]].shift(periods=-(o-1)), ids))                         
            df[col_list[o]] = np.concatenate(out)

        lss = df.loc[:, col_list[0:(o+1)]].pivot_table(index=col_list[0:(o)], columns=col_list[o], fill_value=0, aggfunc=len)

    if lss.shape != (s**new_order, s):

        if lss.shape[1] != s:
            add_states = list(set(states) - set(lss.columns.tolist()))
            for state in add_states:
                lss[state] = np.nan
        
        if lss.shape[0] != s**order:
            
            empty_lss = empty_dfs['empty_lss_' + str(order)]
            lss = empty_lss.merge(lss, left_on=empty_lss.index.values, right_on=lss.index.values, how='left').drop(['key_0'], axis=1).set_index(empty_lss.index).fillna(0)
 
    lss.sort_index(axis=1, inplace=True)
    lss.sort_index(axis=0, inplace=True)

    freqs['freq_' + str(order)] = lss

    # calculate the other frequency matrices as well to make life easier later on
    o = order - 1
    while o > 0:        
        ls = lss.sum(axis=1)
        new_lss = ls.unstack(-1).fillna(value=0)
        new_lss.sort_index(axis=1, inplace=True)
        new_lss.sort_index(axis=0, inplace=True)
        freqs['freq_' + str(o)] = new_lss
        lss = new_lss.copy()
        o -= 1 

    # for normalized initial probs
    freqs['freq_0'] = pd.DataFrame(lss.sum(axis=1))

    return freqs, df, new_order

def initial_count_matrix(df=None, time_attributes=None, states=None, first_timepoint=None, id_attribute=None, order=None, col_list=None, empty_dfs=None):

    initial_freqs = {}
    s = len(states)

    # calculate initial freqs for timepoint 0
    ls1 = df[df[time_attributes[0]] == first_timepoint][time_attributes[1]].value_counts()
    if (ls1.sum() == 0):
        print('ls1 sum 0', ls1)
        print(df)
    add_states = list(set(states) - set(ls1.index.tolist()))
    ls1 = ls1.append(pd.Series(np.repeat(0, len(add_states)), index=add_states)).sort_index(axis=0)
    initial_freqs['freq_' + str(0)] = pd.DataFrame(ls1).sort_index()

    if order > 1:

        ids = df[id_attribute].unique()
    
        # we start at o = 1 because we have to calculate the initial freqs for the first timepoint
        for o in np.arange(1, order):
            
            lss = df.loc[df[time_attributes[0]] < (first_timepoint + o), col_list[0:(o+1)]].pivot_table(index=col_list[0:o], columns=col_list[o], fill_value=0, aggfunc=len)
            
            if lss.shape != (s**o, s):

                if lss.shape[1] != s:
                    add_states = list(set(states) - set(lss.columns.tolist()))
                    for state in add_states:
                        lss[state] = np.nan
        
            if lss.shape[0] != s**o:
            
                empty_lss = empty_dfs['empty_lss_' + str(o)]
                lss = empty_lss.merge(lss, left_on=empty_lss.index.values, right_on=lss.index.values, how='left').drop(['key_0'], axis=1).set_index(empty_lss.index).fillna(0)
     
            lss.sort_index(axis=1, inplace=True)
            lss.sort_index(axis=0, inplace=True)    
            
            initial_freqs['freq_' + str(o)] = lss  

    return initial_freqs

def calculate_model_probs(freqs=None, s=None, order=None):

    probs = {}

    # and for tpi the normalized values
    lss = freqs['freq_' + str(0)]
    tpi = lss.divide(other = lss.sum().values[0], axis=0)
    probs['prob_' + str(0)] = tpi

    for o in np.arange(1, order+1):

        lss = freqs['freq_' + str(o)]
        ls = lss.sum(axis=1) # apply to columns will give one sum value per row

        # for the calculation of probabilities, we add 1 to every cell with 0
        ls[ls == 0.0] = 1.0
        tA = lss.divide(ls, axis=0)
        probs['prob_' + str(o)] = tA

    return probs


