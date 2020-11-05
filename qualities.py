import numpy as np
from scipy import stats

import fomc_measures as fomcm
import fomc_functions as fomcf

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

    quality_values = fomcf.calculate_quality_values(general_params=general_params, subgroup_params=subgroup_params, quality_measure=quality_measure)
    #quality_values = cf.calculate_quality_values(general_params=general_params, subgroup_params=subgroup_params, quality_measure=quality_measure)

    qm_all.update(quality_values)
  
    qm_all['sg_prop'] = round(subgroup_params['sg_size']['nr_sequences']/general_params['data_size']['nr_sequences'], 4)
    qm_all['idx_sg'] = subgroup_params['idx_sg']

    return qm_all

def calculate_general_parameters(df=None, distribution=None, cols=None, attributes=None):

    nr_sequences = len(df[attributes['id_attribute']].unique())
    nr_transitions = len(df)
    data_size = {'nr_sequences': nr_sequences, 'nr_transitions': nr_transitions}

    params = fomcm.params_first_order_markov_chain_general(df=df, attributes=attributes)
    #params = cme.params_wra_general(df=df, attributes=attributes)

    if distribution is not None:
        mu = np.mean(distribution)
        sigma = np.std(distribution)
    else:
        mu = np.nan
        sigma = np.nan

    general_params = {'mu': mu, 'sigma': sigma, 'data_size': data_size}
    general_params.update(params)

    return general_params

def calculate_subgroup_parameters(df=None, subgroup=None, idx_sg=None, attributes=None, general_params=None):

    nr_sequences = len(subgroup[attributes['id_attribute']].unique())
    nr_transitions = len(subgroup)
    sg_size = {'nr_sequences': nr_sequences, 'nr_transitions': nr_transitions}

    params = fomcm.params_first_order_markov_chain_subgroup(subgroup=subgroup, general_params=general_params, attributes=attributes)
        
    subgroup_params = {'sg_size': sg_size, 'idx_sg': idx_sg}
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

