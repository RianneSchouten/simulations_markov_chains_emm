import numpy as np
import pandas as pd

def calculate_quality_values(general_params=None, subgroup_params=None, quality_measure=None, ref=None, start_at_order=None, print_this=None):

    quality_values = {}

    qm, score, llsg, sg_order = search_quality_values(general_params=general_params, subgroup_params=subgroup_params, print_this=print_this,
                                                      quality_measure=quality_measure, ref=ref, start_at_order=start_at_order)

    quality_values[quality_measure] = np.round(qm, 2)
    quality_values['best_order'] = sg_order
    quality_values['llsg'] = np.round(llsg, 2)
    quality_values['score'] = score

    return quality_values

def search_quality_values(general_params=None, subgroup_params=None, quality_measure=None, ref=None, start_at_order=None, print_this=None):

    if quality_measure in ['deltatv', 'omegatv']:

        deltatv, omegatv = h_distance_transition_matrix(general_params=general_params, subgroup_params=subgroup_params)
        qm = eval(quality_measure)
        score = np.nan
        llsg = np.nan
        sg_order = 1
        return qm, score, llsg, sg_order

    else:

        score, llsg, sg_order = calculate_best_fitting_order(probs=subgroup_params['probs'], freqs=subgroup_params['freqs'], initial_freqs=subgroup_params['initial_freqs'],
                                                             start_at_order=start_at_order, s=len(general_params['states']), print_this=print_this,
                                                             quality_measure=quality_measure, data_size=subgroup_params['sg_size'])
        
        if quality_measure == 'phiwarl':
            qm = np.abs(subgroup_params['sg_size']['seq_plus_transitions'] * (score - (2*general_params['lld'] / general_params['data_size']['seq_plus_transitions'])))
            return qm, score, llsg, sg_order

        else:
            # calculate reference likelihood
            refll, refscore = calculate_reference_score(ref=ref, general_params=general_params, subgroup_params=subgroup_params, 
                                                        quality_measure=quality_measure, print_this=print_this)
               
            if print_this:
                print('reference')
                print(refll)
                print(refscore)

            if ref in ['dataset', 'complement']:
                qm = score - refscore
            elif ref == 'addition':
                qm = score + refscore        

            return qm, score, llsg, sg_order

def calculate_reference_score(ref=None, general_params=None, subgroup_params=None, quality_measure=None, print_this=None):

    if ref == 'dataset':
        # sg on dataset params
        ll, ll_list = calculate_log_likelihood(probs=general_params['probs'], freqs=subgroup_params['freqs'], print_this=print_this,
                                               initial_freqs=subgroup_params['initial_freqs'], ll_list=None, order=1, s=len(general_params['states']))
        score = calculate_score(ll=ll, quality_measure=quality_measure, order=1, s=len(general_params['states']), 
                                data_size=subgroup_params['sg_size'], print_this=print_this)
        return ll, score
    
    elif ref == 'complement':
        # sg on complement
        ll, ll_list = calculate_log_likelihood(probs=subgroup_params['probs_compl'], freqs=subgroup_params['freqs'], 
                                               initial_freqs=subgroup_params['initial_freqs'], ll_list=None, order=1, s=len(general_params['states']))
        score = calculate_score(ll=ll, quality_measure=quality_measure, order=1, s=len(general_params['states']), data_size=subgroup_params['sg_size'])
        return ll, score

    elif ref == 'addition':
        ll, ll_list = calculate_log_likelihood(probs=subgroup_params['probs_compl'], freqs=subgroup_params['freqs_compl'], 
                                               initial_freqs=subgroup_params['initial_freqs_compl'], ll_list=None, order=1, s=len(general_params['states']))
        score = calculate_score(ll=ll, quality_measure=quality_measure, order=1, s=len(general_params['states']), data_size=subgroup_params['sg_size_compl'])
        return ll, score

def calculate_best_fitting_order(probs=None, freqs=None, initial_freqs=None, start_at_order=None, s=None, quality_measure=None, data_size=None, print_this=None):

    o = start_at_order
    #print(o)

    ll, ll_list = calculate_log_likelihood(probs=probs, freqs=freqs, initial_freqs=initial_freqs, ll_list=None, order=o, s=s, print_this=print_this)
    score = calculate_score(ll=ll, quality_measure=quality_measure, order=o, s=s, data_size=data_size, print_this=print_this)

    o -= 1
    # if testing for a subgroup with order = 0, then set last_order to 0
    last_order = 1
    while o > (last_order-1):

        ll_lower_order, ll_list = calculate_log_likelihood(probs=probs, freqs=freqs, initial_freqs=initial_freqs, ll_list=ll_list, order=o, s=s, print_this=print_this)
        score_lower_order = calculate_score(ll=ll_lower_order, quality_measure=quality_measure, order=o, s=s, data_size=data_size, print_this=print_this)
        if print_this:
            print(start_at_order)
            print(ll)
            print(score)
            print(o)
            print(ll_lower_order)
            print(score_lower_order)

        if np.isnan(score_lower_order) and o != last_order: # comparison cannot be made, go to next level
            o -= 1
            score = score_lower_order       
        elif score > score_lower_order:
            return score, ll, o+1     
        else: 
            o -= 1
            score = score_lower_order
            ll = ll_lower_order

    return score, ll, o+1

def calculate_score(ll=None, quality_measure=None, order=None, s=None, data_size=None, print_this=None):

    if order == 0:
        K = (s-1) + ((s**1) * (s-1)) # we add extra s-1 parameters for the initial probs
    else:
        K = ((s**order) * (s-1))
    
    size = data_size['seq_plus_transitions']

    if quality_measure == 'phiwd':
        score = 2*ll

    elif quality_measure == 'phibic':
        penalty = K * np.log(size)

        if print_this:
            print(K)
            print(penalty)

        score = 2*ll - penalty  

    elif quality_measure == 'phiaic':
        penalty = 2*K
        score = 2*ll - 2*K

    elif quality_measure == 'phiaicc':
        if K >= (size - 1):
            score = np.nan
        else:
            penalty1 = 2*K 
            penalty2 = (2*(K**2) + 2*K) / (size - K - 1)
            score = 2*ll - penalty1 - penalty2
            if print_this:
                print(size)
                print(K)
                print(penalty1)
                print(penalty2)
                print(score)

    elif quality_measure == 'phiwarl':
        score = (2*ll) / size

    elif quality_measure in ['deltatv', 'omegatv']:
        score = np.nan

    return score

def calculate_log_likelihood(probs=None, freqs=None, initial_freqs=None, ll_list=None, order=None, s=None, print_this=None):

    # for markov chains it can be done like this
    # because of computer rounding, a probability can be 0
    # however, it is not possible to take the log of a 0 probability
    # we therefore set those values to 1E-13
    # the function np.log in python uses the natural logarithm ln
    # which is what we need for the log likelihood (bishop)
    
    if order > 0:

        if ll_list is None:
            ll = []
            for o in np.arange(0, order):

                # for the first max_o timepoints, the initial freqs are used
                # these only count the sequences
                # the probs are based on the start_at_order frequencies normalized till o
                prob = probs['prob_' + str(o)]
                data = initial_freqs['freq_' + str(o)]
                prob[prob == 0.0] = 0.0000000000001

                #print(prob)
                #print(data)
            
                likelihood = np.dot(data.values.reshape(s**(o+1),), np.log(prob.values.reshape(s**(o+1),)))
                #likelihood = np.dot(data.values.reshape(total_len,), np.log(prob.values).reshape(total_len,))
                ll.append(likelihood)
        
        else:
            ll = ll_list[0:order]

        if print_this:
            print(ll)
        # and for the rest of the sequence
        # in freqs, depending on the order, only the transitions that can be made are calculated
        o = order
        prob = probs['prob_' + str(o)]
        data = freqs['freq_' + str(o)]
        prob[prob == 0.] = 0.0000000000001        
        
        likelihood = np.dot(data.values.reshape(s**(o+1),), np.log(prob.values.reshape(s**(o+1),)))
        #likelihood = np.dot(data.values.reshape(s**(o+1),), np.log(prob.values.reshape(s**(o+1),)))
        ll.append(likelihood)

    if order == 0:

        ll = [ll_list[1]]

        # timepoint 0
        o = 0
        data = initial_freqs['freq_' + str(o)]
        prob = data.divide(other = data.sum().values[0], axis=0)

        prob[prob == 0.] = 0.0000000000001
        #print(prob)
        #print(data)
   
        likelihood = np.dot(data.values.reshape(s**(o+1),), np.log(prob.values.reshape(s**(o+1),)))
        ll.append(likelihood)

        '''
        # other timepoints
        o = 1
        prob = probs['prob_' + str(o)]
        data = freqs['freq_' + str(o)]

        prob[prob == 0.] = 0.0000000000001
    
        likelihood = np.dot(data.values.reshape(s**(o+1),), np.log(prob.values.reshape(s**(o+1),)))
        ll.append(likelihood)
        '''

    if print_this:
        print(ll)
    llt = sum(ll)

    return llt, ll

def h_distance_transition_matrix(general_params=None, subgroup_params=None):

    ls = subgroup_params['freqs1_alltimepoints']['freq_0'] # normalized freqs first timepoint using all timepoints to estimate 1st order matrix

    deltatv = manhattan_distance(taA=general_params['probs']['prob_1'], taB=subgroup_params['probs1_alltimepoints']['prob_1'], lsB=ls, weighted=False)
    omegatv = manhattan_distance(taA=general_params['probs']['prob_1'], taB=subgroup_params['probs1_alltimepoints']['prob_1'], lsB=ls, weighted=True)

    return deltatv, omegatv

def manhattan_distance(taA=None, taB=None, lsB=None, weighted=True):

    g = taB # subgroup
    e = taA # dataset   
    
    if weighted:
        s = len(lsB)
        w = np.repeat(lsB.values, s)
        d = np.matmul(w, np.abs(g-e).values.reshape(s*s, ))
    else:
        d = np.sum(np.abs(g-e).values) 

    return d
