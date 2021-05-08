import numpy as np
from scipy import stats

import mc_measures_orders as mo
import mc_functions_orders as fo

def add_qm(desc=None, idx_sg=None, general_params=None, subgroup_params=None, quality_measure=None, start_at_order=None, stop_at_order=None, ref=None, print_this=None):

    qm_all = calculate_qm(general_params=general_params, 
                          subgroup_params=subgroup_params,
                          quality_measure=quality_measure,
                          ref=ref, print_this=print_this,
                          start_at_order=start_at_order,
                          stop_at_order=stop_at_order)     
        
    # add new measures to the qualities part
    desc_added = desc
    desc_added['qualities'] = qm_all
       
    return desc_added

def calculate_qm(general_params=None, subgroup_params=None, quality_measure=None, start_at_order=None, stop_at_order=None, ref=None, print_this=None):

    qm_all = {}

    quality_values = fo.calculate_quality_values(general_params=general_params, subgroup_params=subgroup_params, print_this=print_this,
                                                 quality_measure=quality_measure, ref=ref, start_at_order=start_at_order, stop_at_order=stop_at_order)

    qm_all.update(quality_values)
  
    qm_all['sg_prop'] = round(subgroup_params['sg_size']['nr_sequences']/general_params['data_size']['nr_sequences'], 4)
    qm_all['idx_sg'] = subgroup_params['idx_sg']    
    #qm_all['prob_0'] = subgroup_params['probs']['prob_0']    
    #qm_all['prob_1'] = subgroup_params['probs']['prob_1']   

    return qm_all

def calculate_general_parameters(df=None, distribution=None, cols=None, attributes=None, order=None, start_at_order=None, 
                                 stop_at_order=None, quality_measure=None):

    nr_sequences = len(df[attributes['id_attribute']].unique())
    nr_transitions = len(df)
    data_size = {'nr_sequences': nr_sequences, 'nr_transitions': nr_transitions, 'seq_plus_transitions': nr_sequences + nr_transitions}

    idx = df.index.values
    params = mo.params_markov_chain_general(df=df, attributes=attributes, order=order, start_at_order=start_at_order, 
                                            stop_at_order=stop_at_order, data_size=data_size, quality_measure=quality_measure)

    if distribution is not None:
        mu = np.nanmean(distribution)
        sigma = np.nanstd(distribution)
    else:
        mu = np.nan
        sigma = np.nan

    general_params = {'mu': mu, 'sigma': sigma, 'data_size': data_size}
    general_params.update(params)

    return general_params

def calculate_subgroup_parameters(df=None, subgroup=None, subgroup_compl=None, idx_sg=None, attributes=None, general_params=None, quality_measure=None, start_at_order=None, ref=None):

    nr_sequences = len(subgroup[attributes['id_attribute']].unique())
    nr_transitions = len(subgroup)
    sg_size = {'nr_sequences': nr_sequences, 'nr_transitions': nr_transitions, 'seq_plus_transitions': nr_sequences + nr_transitions}
    subgroup_params = {'sg_size': sg_size, 'idx_sg': idx_sg}

    params = mo.params_markov_chain_subgroup(subgroup=subgroup, subgroup_compl=subgroup_compl, general_params=general_params, 
                                             attributes=attributes, quality_measure=quality_measure, start_at_order=start_at_order, ref=ref)
        
    subgroup_params.update(params)

    return subgroup_params

def check_significance(result_set_ordered=None, general_params=None, quality_measure=None, Z=None):

    mu = general_params['mu']
    sigma = general_params['sigma']

    result_set_selected = []
    for desc_qm in result_set_ordered:

        # don't take the absolute value
        # we want a high quality value
        z = (desc_qm['qualities'][quality_measure] - mu) / sigma

        if z >= Z:
            desc_qm['qualities']['z'] = z
            result_set_selected.append(desc_qm)

    return result_set_selected

