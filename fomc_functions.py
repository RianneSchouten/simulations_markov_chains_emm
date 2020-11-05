import numpy as np
import pandas as pd

def calculate_quality_values(general_params=None, subgroup_params=None, quality_measure=None):

    quality_values = {}

    deltatv, omegatv = h_distance_transition_matrix(general_params=general_params, subgroup_params=subgroup_params)
    llsg, llpisg, phiwd, phikl, phiarl, phiwarl = \
        h_log_likelihood(general_params=general_params, subgroup_params=subgroup_params)
    
    quality_values[quality_measure] = round(eval(quality_measure), 4)     

    quality_values['tA'] = np.around(subgroup_params['tA'], decimals=4)
    quality_values['tpi'] = np.around(subgroup_params['tpi'], decimals=4)

    return quality_values

def h_distance_transition_matrix(general_params=None, subgroup_params=None):

    deltatv = manhattan_distance(taA=general_params['tA'], taB=subgroup_params['tA'], lsB=subgroup_params['ls'], weighted=False)
    omegatv = manhattan_distance(taA=general_params['tA'], taB=subgroup_params['tA'], lsB=subgroup_params['ls'], weighted=True)

    #d_sg = me.manhattan_distance(taA=general_params['tA'], taB=subgroup_params['tA'], lsB=subgroup_params['ls'], weighted=True)
    #d_s = (np.abs(d_sg - subgroup_params['mu'])) / subgroup_params['sigma']

    return deltatv, omegatv

def h_log_likelihood(general_params=None, subgroup_params=None):

    seq_plus_transitions_sg = subgroup_params['sg_size']['nr_transitions'] + subgroup_params['sg_size']['nr_sequences']
    seq_plus_transitions_d = general_params['data_size']['nr_transitions'] + general_params['data_size']['nr_sequences']

    llsg = subgroup_params['ll_sg'] # likelihood under sg model
    llpisg = subgroup_params['ll_pi_sg'] # likelihood under data model
    
    phiwd = subgroup_params['ll_sg'] - subgroup_params['ll_pi_sg']
    phikl = phiwd / seq_plus_transitions_sg
    
    phiarl = np.abs((subgroup_params['ll_pi_sg'] / seq_plus_transitions_sg) - (general_params['ll_d'] / seq_plus_transitions_d))
    phiwarl = np.abs(seq_plus_transitions_sg*((subgroup_params['ll_pi_sg'] / seq_plus_transitions_sg) - (general_params['ll_d'] / seq_plus_transitions_d)))

    '''
    p = len(general_params['states'])^2 - 1 # equivalent to m(m-1) for the probs + (m-1) for the initial probs = m^2 - m + m - 1 
    
    # np.log uses the natural logarithm, which is what we need, see bishop
    # we transform the BIC slightly to make it feasible for our quality measure
    # if the likelihood is the same using both sets of parameters, then we prefer the parameters from the data
    # hence we want to penalize the likelihood of the subgroup
    # this value is 1 if the subgroup has the same size as the data
    penalty_size = 1 + ((seq_plus_transitions_d - seq_plus_transitions_sg) / seq_plus_transitions_d)
    BIC_sg = 2*subgroup_params['ll_sg'] - (p * np.log(penalty_size))
    BIC_pi_sg = 2*subgroup_params['ll_pi_sg']
    phibic = BIC_sg - BIC_pi_sg

    AICc_sg = 2*subgroup_params['ll_sg'] - (2*p) - ((2*(p**2) + 2*p) / (seq_plus_transitions_sg - p - 1))
    AICc_pi_sg = 2*subgroup_params['ll_pi_sg'] - (2*p)
    phiaic = AICc_sg - AICc_pi_sg
    '''

    return llsg, llpisg, phiwd, phikl, phiarl, phiwarl#, phibic, phiaic

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
