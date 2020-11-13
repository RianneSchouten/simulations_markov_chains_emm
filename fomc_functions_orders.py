import numpy as np
import pandas as pd

def calculate_quality_values(general_params=None, subgroup_params=None, quality_measure=None, start_at_order=None):

    quality_values = {}

    print('start qms')
    qm, llsg, best_order = search_quality_values(general_params=general_params, subgroup_params=subgroup_params, 
                                               quality_measure=quality_measure, start_at_order=start_at_order)

    #name_quality_measure_pi = quality_measure + '_pi'
    #name_quality_measure_A = quality_measure + '_A'
    #quality_values[name_quality_measure_pi] = np.round(qm_pi, 4)
    #quality_values[name_quality_measure_A] = np.round(qm_A, 4)
    quality_values[quality_measure] = np.round(qm, 2)
    quality_values['best_order'] = best_order
    quality_values['llsg'] = np.round(llsg, 2)
    #quality_values['probs'] = probs

    return quality_values

def search_quality_values(general_params=None, subgroup_params=None, quality_measure=None, start_at_order=None):

    # do the procedure for finding the o-th order markov chain with the highest quality value
    o = start_at_order

    # calculate reference likelihood
    llpisg = calculate_log_likelihood(probs=general_params['probs'], freqs=subgroup_params['freqs'], initial_freqs=subgroup_params['initial_freqs'], s=len(general_params['states']), max_o=1) 
    subgroup_params.update({'llpisg': llpisg})

    if quality_measure in ['deltatv', 'omegatv']:
        value_o, llsg_o = from_probs_to_quality_value(general_params=general_params, subgroup_params=subgroup_params, quality_measure=quality_measure, max_o=1)
        qm = value_o
        llsg = llsg_o
        order = 1

    else:
        
        value_o, llsg_o = from_probs_to_quality_value(general_params=general_params, subgroup_params=subgroup_params, quality_measure=quality_measure, max_o=o)

        if o == 1:
            qm = value_o
            order = o
            llsg = llsg_o

        o -= 1
        while o > 0:

            value_o_minus_1, llsg_o_minus_1 = from_probs_to_quality_value(general_params=general_params, subgroup_params=subgroup_params, quality_measure=quality_measure, max_o=o)

            if np.isnan(value_o) and o != 1: # comparison cannot be made, go to next level
                o -= 1
                value_o = value_o_minus_1         
            elif value_o > value_o_minus_1:
                qm = value_o
                llsg = llsg_o
                order = o+1
                o = 0
            elif o == 1:
                qm = value_o_minus_1
                llsg = llsg_o_minus_1
                order = o
                o = 0
            else: 
                o -= 1
                value_o = value_o_minus_1

        # do something to find qm_pi
        # use probs based on initial_freqs['freq_0'] for the first timepoint
        # and probs_1 for the other timepoints
        value_pi, llsg_pi = from_probs_to_quality_value(general_params=general_params, subgroup_params=subgroup_params, quality_measure=quality_measure, max_o=0)
        if value_pi >= qm:
            order = 0
            qm = value_pi
            llsg = llsg_pi

    return qm, llsg, order

def from_probs_to_quality_value(general_params=None, subgroup_params=None, quality_measure=None, max_o=None):

    # subgroup    
    llsg = calculate_log_likelihood(probs=subgroup_params['probs'], freqs=subgroup_params['freqs'], initial_freqs=subgroup_params['initial_freqs'], s=len(general_params['states']), max_o=max_o)
    value = calculate_quality_measure(quality_measure=quality_measure, llsg=llsg, subgroup_params=subgroup_params, general_params=general_params, o=max_o)

    return value, llsg

def calculate_quality_measure(quality_measure=None, llsg=None, subgroup_params=None, general_params=None, o=None):

    seq_plus_transitions_sg = subgroup_params['sg_size']['seq_plus_transitions']
    seq_plus_transitions_d = general_params['data_size']['seq_plus_transitions']
    s = len(general_params['states'])
    llpisg = subgroup_params['llpisg']

    phiwd = llsg - llpisg
    phiwd2 = 2*llsg - 2*llpisg
    phikl = phiwd / seq_plus_transitions_sg

    if o == 0:
        K = (s-1) + ((s**1) * (s-1)) # we add extra s-1 parameters for the initial probs
    else:
        K = ((s**o) * (s-1))
    L = s*(s-1)

    sg_penalty = K * np.log(seq_plus_transitions_sg)
    d_penalty = L * np.log(seq_plus_transitions_sg)
    bicsg = 2*llsg - sg_penalty
    bicd = 2*llpisg - d_penalty
    phibic = bicsg - bicd

    sg_penalty = 2*K 
    aicsg = 2*llsg - sg_penalty
    aicd = 2*llpisg - 2*L
    phiaic = aicsg - aicd

    # it can be that the number of K or L is too large compared to the subgroup
    # this is problematic for the aicc (for the other quality measures, the qm value will only become increadibly small)
    # while constructing q and w, np.nan values will be placed at the end
    if K >= (seq_plus_transitions_sg - 1):
        phiaicc = np.nan
    else:
        sg_smallsample_penalty = (2*(K**2) + 2*K) / (seq_plus_transitions_sg - K - 1)
        aicsg_smallsample = 2*llsg - sg_penalty - sg_smallsample_penalty
        aicd_smallsample = 2*llpisg - 2*L - (2*(L**2) + 2*L) / (seq_plus_transitions_sg - L - 1)
        phiaicc = aicsg_smallsample - aicd_smallsample

    phiarl = np.abs((llpisg / seq_plus_transitions_sg) - (general_params['lld'] / seq_plus_transitions_d))
    phiwarl = np.abs(seq_plus_transitions_sg*((llpisg / seq_plus_transitions_sg) - (general_params['lld'] / seq_plus_transitions_d)))

    deltatv, omegatv = h_distance_transition_matrix(general_params=general_params, subgroup_params=subgroup_params)

    value = eval(quality_measure)

    return value

def calculate_log_likelihood(probs=None, freqs=None, initial_freqs=None, max_o=None, s=None):

    # for markov chains it can be done like this
    # because of computer rounding, a probability can be 0
    # however, it is not possible to take the log of a 0 probability
    # we therefore set those values to 1E-13
    # the function np.log in python uses the natural logarithm ln
    # which is what we need for the log likelihood (bishop)
    ll = []

    if max_o > 0: 
    
        for o in np.arange(0, max_o):

            # for the first max_o timepoints, the initial freqs are used
            # these only count the sequences
            # the probs are based on the start_at_order frequencies normalized till o
            prob = probs['prob_' + str(o)]
            data = initial_freqs['freq_' + str(o)]

            if 0.0 in prob:
                prob[prob == 0.] = 0.0000000000001
        
            likelihood = np.dot(data.values.reshape(s**(o+1),), np.log(prob).reshape(s**(o+1),))
            ll.append(likelihood)

        # and for the rest of the sequence
        # in freqs, depending on the order, only the transitions that can be made are calculated
        o = max_o
        prob = probs['prob_' + str(o)]
        data = freqs['freq_' + str(o)]

        if 0.0 in prob:
            prob[prob == 0.] = 0.0000000000001
    
        likelihood = np.dot(data.values.reshape(s**(o+1),), np.log(prob).reshape(s**(o+1),))
        ll.append(likelihood)

    if max_o == 0:

        # timepoint 0
        o = 0
        data = initial_freqs['freq_' + str(o)]
        prob = (data / data.sum()).values
        if 0.0 in prob:
            prob[prob == 0.] = 0.0000000000001
    
        likelihood = np.dot(data.values.reshape(s**(o+1),), np.log(prob).reshape(s**(o+1),))
        ll.append(likelihood)

        # other timepoints
        o = 1
        prob = probs['prob_' + str(o)]
        data = freqs['freq_' + str(o)]

        if 0.0 in prob:
            prob[prob == 0.] = 0.0000000000001
    
        likelihood = np.dot(data.values.reshape(s**(o+1),), np.log(prob).reshape(s**(o+1),))
        ll.append(likelihood)

    llt = sum(ll)

    return llt

def h_distance_transition_matrix(general_params=None, subgroup_params=None):

    ls = subgroup_params['freqs']['freq_0']

    deltatv = manhattan_distance(taA=general_params['probs']['prob_1'], taB=subgroup_params['probs']['prob_1'], lsB=ls, weighted=False)
    omegatv = manhattan_distance(taA=general_params['probs']['prob_1'], taB=subgroup_params['probs']['prob_1'], lsB=ls, weighted=True)

    return deltatv, omegatv

def manhattan_distance(taA=None, taB=None, lsB=None, weighted=True):

    g = taB # subgroup
    e = taA # dataset   

    if weighted:
        s = len(lsB)
        w = np.repeat(lsB.values, s)
        d = np.matmul(w, np.abs(g-e).reshape(s*s, ))
    else:
        d = np.sum(np.abs(g-e)) 

    return d
