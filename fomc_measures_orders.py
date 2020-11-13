import numpy as np
import pandas as pd
import itertools as it

import fomc_functions_orders as fomcfo

def params_markov_chain_general(df=None, attributes=None, order=None):

    # the first time attribute is the counter or time index, the second and third are the two time points for a 1st order chain
    time_attributes = attributes['time_attributes']
    first_timepoint = attributes['first_timepoint']
    states = np.unique(np.concatenate((df[time_attributes[1]].unique(), df[time_attributes[2]].unique())))
    states = np.sort(states)

    freqs, df_additions, col_list, new_order = higher_order_count_matrix(df=df, time_attributes=time_attributes, states=states, first_timepoint=first_timepoint,
                                                                         id_attribute=attributes['id_attribute'], order=order)
    initial_freqs = initial_count_matrix(df=df_additions, time_attributes=time_attributes, states=states, first_timepoint=first_timepoint,
                                         id_attribute=attributes['id_attribute'], order=new_order, col_list=col_list)
    
    probs = calculate_model_probs(freqs=freqs, s=len(states), max_o=1)

    lld = fomcfo.calculate_log_likelihood(probs=probs, freqs=freqs, initial_freqs=initial_freqs, max_o=1, s=len(states))

    params = {'freqs': freqs, 'initial_freqs': initial_freqs, 'probs': probs, 'lld': lld, 'states': states, 'new_order': new_order}

    return params

def params_markov_chain_subgroup(df=None, subgroup=None, general_params=None, attributes=None, order=None):

    time_attributes = attributes['time_attributes']
    first_timepoint = attributes['first_timepoint']

    print('start freqs')
    freqs, sg_additions, col_list, new_order = higher_order_count_matrix(df=subgroup, time_attributes=time_attributes, states=general_params['states'], first_timepoint=first_timepoint,
                                                                         id_attribute=attributes['id_attribute'], order=order)

    print('start initial freqs')
    initial_freqs = initial_count_matrix(df=sg_additions, time_attributes=time_attributes, states=general_params['states'], first_timepoint=first_timepoint,
                                         id_attribute=attributes['id_attribute'], order=new_order, col_list=col_list)

    print('start probs')
    probs = calculate_model_probs(freqs=freqs, s=len(general_params['states']), max_o=new_order)

    params = {'freqs': freqs, 'initial_freqs': initial_freqs, 'probs': probs, 'new_order': new_order}

    return params

def higher_order_count_matrix(df=None, time_attributes=None, states=None, first_timepoint=None, id_attribute=None, order=None):

    s = len(states)
    freqs = {}

    # parameters given argument order
    if order == 1:
        lss = df[[time_attributes[1], time_attributes[2]]].pivot_table(index=time_attributes[1], columns=time_attributes[2], fill_value=0, aggfunc=len)
        col_list = []
        new_order = order
    else:
        print('start freqs 2')
        ids = df[id_attribute].unique()
        col_list = [time_attributes[1], time_attributes[2]]
    
        # extra check if the length of the sequences is not enough to calculate a certain order
        maxs = df.loc[:, [id_attribute, time_attributes[0]]].pivot_table(index=[id_attribute], values=[time_attributes[0]], aggfunc=np.max)
        min_T = min(maxs.iloc[:, -1])
        if min_T + 1 < order:
            order = min_T + 1
            #print('new order', order)
        new_order = order
        print('start loop')
        if order > 1:
            for o in np.arange(2, order+1):

                # add some stop if you cannot go to a higher order depending on the length of the sequence
    
                shift_col = time_attributes[2] + str(o + 1)
                col_list = col_list + [shift_col]
    
                out = list(map(lambda x: df.loc[(df[id_attribute] == x), time_attributes[2]].shift(periods=-(o-1)), \
                                             ids))                         
                df[shift_col] = np.concatenate(out)

                #df['selection' + str(o)] = df['selection' + str(o-1)]
                #df.loc[df['timepoint1'] == max_timepoint_state1 - o + 2, 'selection' + str(o)] = 0

        print('start calculating lss')
        lss = df.loc[:, col_list].pivot_table(index=col_list[0:-1], columns=col_list[-1], fill_value=0, aggfunc=len)

    print('start adapting lss')
    if lss.shape != (s**order, s):
        if lss.shape[1] != s:
            print('add columns')
            add_states = list(set(states) - set(lss.columns.tolist()))
            add_data = pd.DataFrame(np.zeros(shape=(len(lss), len(add_states))), columns=add_states, index=lss.index.values)
            lss = pd.concat([lss, add_data], axis=1)
        if lss.shape[0] != s**order:
            print('add rows')
            indices = lss.index.values
            if order == 1:
                all_possible_indices = states
            else:
                print('calculate new indices')
                all_possible_indices = list(it.product(states, repeat = order))
            print('add states')
            add_states = list(set(all_possible_indices) - set(indices))      
            print('add data')
            add_data = pd.DataFrame(np.zeros(shape=(len(add_states), s)), columns=states, index=add_states)
            print('concat lss')
            lss = pd.concat([lss, add_data], axis=0)

    print('sort index')
    lss.sort_index(axis=1, inplace=True)
    lss.sort_index(axis=0, inplace=True)

    freqs['freq_' + str(order)] = lss

    # calculate the other frequency matrices as well to make life easier later on
    print('start normalized versions')
    o = order - 1
    while o > 0:
        ls = lss.sum(axis=1)
        new_lss =  pd.DataFrame(ls.values.reshape(s**o, s), index=list(it.product(states, repeat = o)), columns=states)
        freqs['freq_' + str(o)] = new_lss
        lss = new_lss.copy()
        o -= 1 

    # for normalized initial probs
    freqs['freq_0'] = pd.DataFrame(lss.sum(axis=1))

    return freqs, df, col_list, new_order

def initial_count_matrix(df=None, time_attributes=None, states=None, first_timepoint=None, id_attribute=None, order=None, col_list=None):

    initial_freqs = {}
    s = len(states)

    # calculate initial freqs for timepoint 0
    ls1 = df[df[time_attributes[0]] == first_timepoint][time_attributes[1]].value_counts()
    if (ls1.sum() == 0):
        print('ls1 sum 0', ls1)
        print(df)
    add_states = list(set(states) - set(ls1.index.tolist()))
    ls1 = ls1.append(pd.Series(np.repeat(0, len(add_states)), index=add_states)).sort_index(axis=0)
    initial_freqs['freq_' + str(0)] = ls1

    if order > 1:

        ids = df[id_attribute].unique()
    
        # we start at o = 1 because we have to calculate the initial freqs for the first timepoint
        for o in np.arange(1, order):
            
            lss = df.loc[df[time_attributes[0]] < (first_timepoint + o), col_list[0:(o+1)]].pivot_table(index=col_list[0:o], columns=col_list[o], fill_value=0, aggfunc=len)
            
            if lss.shape != (s**o, s):
                if lss.shape[1] != s:
                    add_states = list(set(states) - set(lss.columns.tolist()))
                    add_data = pd.DataFrame(np.zeros(shape=(len(lss), len(add_states))), columns=add_states, index=lss.index.values)
                    lss = pd.concat([lss, add_data], axis=1)
                if lss.shape[0] != s**o:
                    indices = lss.index.values
                    if o == 1:
                        all_possible_indices = states
                    else:
                        all_possible_indices = list(it.product(states, repeat = o))
                    add_states = list(set(all_possible_indices) - set(indices))      
                    add_data = pd.DataFrame(np.zeros(shape=(len(add_states), s)), columns=states, index=add_states)
                    lss = pd.concat([lss, add_data], axis=0)

            lss.sort_index(axis=1, inplace=True)
            lss.sort_index(axis=0, inplace=True)    
            
            initial_freqs['freq_' + str(o)] = lss  

    return initial_freqs

def calculate_model_probs(freqs=None, s=None, max_o=None):

    probs = {}

    # and for tpi the normalized values
    lss = freqs['freq_' + str(0)]
    tpi = (lss / lss.sum()).values
    probs['prob_' + str(0)] = tpi

    for o in np.arange(1, max_o+1):
         
        lss = freqs['freq_' + str(o)]
        ls = lss.sum(axis=1) # apply to columns will give one sum value per row

        # for the calculation of proportions, we add 1 to every cell with 0
        ls_long = np.repeat(ls.values, s).reshape((s**o, s))
        if 0.0 in ls_long:
            ls_long[ls_long == 0.0] = 1.0

        tA = lss.values / ls_long
        probs['prob_' + str(o)] = tA

    return probs



