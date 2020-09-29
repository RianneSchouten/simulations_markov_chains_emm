import numpy as np
from scipy import stats
#import time

import measures as me

def add_qm(desc=None, idx_sg=None, general_params=None, subgroup_params=None, quality_measure=None):

    qm_all = calculate_qm(general_params=general_params, 
                          subgroup_params=subgroup_params,
                          quality_measure=quality_measure)     
        
    # add new measures to the qualities part
    desc_added = desc
    desc_added['qualities'] = qm_all
       
    return desc_added

def calculate_qm(general_params=None, subgroup_params=None, quality_measure=None):

    qm_all = {}
   
    deltatv, omegatv = h_distance_transition_matrix(general_params=general_params, subgroup_params=subgroup_params)
    llsg, llpisg, phiwd, phikl, phiarl, phiwarl, phibic = \
        h_log_likelihood(general_params=general_params, subgroup_params=subgroup_params)

    qm_all[quality_measure] = round(eval(quality_measure), 4)    

    #qm_all['deltatv'] = round(d_unw, 4)
    #qm_all['omegatv'] = round(d_w, 4)
    #qm_all['sampledwtv'] = round(d_s, 4)

    #rel_size_sg = subgroup_params['sg_size']/general_params['data_size']
    #rel_size_compl = (general_params['data_size']-subgroup_params['sg_size'])/general_params['data_size']
    #entropy = -rel_size_sg*np.log(rel_size_sg) - rel_size_compl*np.log(rel_size_compl)

    #qm_all['entropydtv'] = round(entropy*d_unw, 4)

    #qm_all['llsg'] = round(llsg, 4)
    #qm_all['llpisg'] = round(llpisg, 4)
    
    #qm_all['phiwd'] = round(phiwd, 4)
    #qm_all['phikl'] = round(phikl, 4)
    #qm_all['entropydifll'] = round(entropy*difll, 4)

    #qm_all['phibic'] = round(phibic, 4)
    #qm_all['BICmismatch'] = round(BICmismatch, 4)

    #qm_all['phiarl'] = round(phiarl, 4)
    #qm_all['phiwarl'] = round(phiwarl, 4)
    #qm_all['entropyrll'] = round(entropy*relativell, 4)
    
    qm_all['sg_prop'] = round(subgroup_params['sg_size']/general_params['data_size'], 4)
    qm_all['tA'] = np.around(subgroup_params['tA'], decimals=4)
    qm_all['tpi'] = np.around(subgroup_params['tpi'], decimals=4)

    return qm_all

def calculate_general_parameters(df=None, cols=None, time_attributes=None, id_attribute=None, first_timepoint=None):

    data_size = len(df)
    # the first time attribute is the counter or time index, the second and third are the two time points for a 1st order chain
    states = np.unique(np.concatenate((df[time_attributes[1]].unique(), df[time_attributes[2]].unique())))

    ls1, ls, lss, tA, tpi = me.t_count_matrix(df=df, time_attributes=time_attributes, states=states, first_timepoint=first_timepoint)
    ll_d = me.log_likelihood(states=states, model_ls1=ls1, model_tA=tA, data_ls1=ls1, data_lss=lss)

    general_params = {'ls1': ls1, 'ls': ls, 'lss': lss, 'tA': tA, 'tpi': tpi, 'll_d': ll_d, 'states': states, 'data_size': data_size}  

    return general_params

def calculate_subgroup_parameters(df=None, subgroup=None, idx_sg=None, time_attributes=None, general_params=None, 
                                  id_attribute=None, first_timepoint=None):

    sg_size = len(subgroup)
    ls1, ls, lss, tA, tpi = me.t_count_matrix(df=subgroup, time_attributes=time_attributes, states=general_params['states'], 
                                         first_timepoint=first_timepoint)

    ll_sg = me.log_likelihood(states=general_params['states'], model_ls1=ls1, model_tA=tA, data_ls1=ls1, data_lss=lss)
    ll_pi_sg = me.log_likelihood(states=general_params['states'], model_ls1=general_params['ls1'], model_tA=general_params['tA'], data_ls1=ls1, data_lss=lss)
    ll_sg_d = me.log_likelihood(states=general_params['states'], model_ls1=ls1, model_tA=tA, data_ls1=general_params['ls1'], data_lss=general_params['lss'])

    #mu, sigma = me.sample_dataset(df=df, size=sg_size, time_attributes=time_attributes, general_params=general_params, M=50)
    #if sigma == 0.0: sigma = 1.0
        
    subgroup_params = {'ls1': ls1, 'ls': ls, 'lss': lss, 'tA': tA, 'tpi': tpi, #'mu': mu, 'sigma': sigma, 
                       'll_sg': ll_sg, 'll_pi_sg': ll_pi_sg, 'll_sg_d': ll_sg_d, 'sg_size': sg_size}

    return subgroup_params

def h_distance_transition_matrix(general_params=None, subgroup_params=None):

    deltatv = me.manhattan_distance(taA=general_params['tA'], taB=subgroup_params['tA'], lsB=subgroup_params['ls'], weighted=False)
    omegatv = me.manhattan_distance(taA=general_params['tA'], taB=subgroup_params['tA'], lsB=subgroup_params['ls'], weighted=True)

    #d_sg = me.manhattan_distance(taA=general_params['tA'], taB=subgroup_params['tA'], lsB=subgroup_params['ls'], weighted=True)
    #d_s = (np.abs(d_sg - subgroup_params['mu'])) / subgroup_params['sigma']

    return deltatv, omegatv

def h_log_likelihood(general_params=None, subgroup_params=None):

    llsg = subgroup_params['ll_sg']
    llpisg = subgroup_params['ll_pi_sg']
    phiwd = subgroup_params['ll_sg'] - subgroup_params['ll_pi_sg']
    phikl = phiwd / subgroup_params['sg_size']
    phiarl = np.abs((subgroup_params['ll_pi_sg'] / subgroup_params['sg_size']) - (general_params['ll_d'] / general_params['data_size']))
    phiwarl = np.abs(subgroup_params['sg_size']*((subgroup_params['ll_pi_sg'] / subgroup_params['sg_size']) - (general_params['ll_d'] / general_params['data_size'])))

    p = len(general_params['states'])^2 - 1 # equivalent to m(m-1) for the probs + (m-1) for the initial probs = m^2 - m + m - 1 
    BIC = 2*subgroup_params['ll_sg'] - (p * np.log(subgroup_params['sg_size']))
    phibic = BIC - (2*subgroup_params['ll_pi_sg'] - (p * np.log(general_params['data_size'])))
    #BICmismatch = BICdif + ((general_params['ll_d'] - (p * np.log(general_params['data_size']))) - (subgroup_params['ll_sg_d'] - (p * np.log(subgroup_params['sg_size']))))

    return llsg, llpisg, phiwd, phikl, phiarl, phiwarl, phibic#, BICmismatch

