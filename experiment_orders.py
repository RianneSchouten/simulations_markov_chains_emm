import numpy as np 
import pandas as pd
import itertools as it
from joblib import Parallel, delayed

import sample_sequences_orders as sso
import beam_search_orders as bso
import summaries_orders as suo

def experiment(subgroup_orders=None,
               quality_measures=None, 
               markov_model_params=None,
               beam_search_params=None,
               simulation_params=None,
               constraints=None,
               wcs_params=None):

    parameter_set = list(it.product(simulation_params['N'], simulation_params['T'], simulation_params['S'], simulation_params['ncovs'], 
                                    simulation_params['p'], simulation_params['true_desc_length'], simulation_params['global_model_order'], 
                                    markov_model_params['start_at_order'], subgroup_orders)) 
    nexp = len(parameter_set)

    for exp in np.arange(nexp):   
        print('experiment', exp+1, 'of', nexp)

        params = parameter_set[exp]
        print('parameters:', params)

        ranks_one_parameter_run = parallelization(nreps=simulation_params['nreps'], params=params, quality_measures=quality_measures, 
                                                  beam_search_params=beam_search_params, markov_model_params=markov_model_params, 
                                                  constraints=constraints, wcs_params=wcs_params)

        # concatenate all results per parameter combination
        params_pd = pd.DataFrame(np.tile(params, simulation_params['nreps']).reshape(simulation_params['nreps'], len(params)), 
                                 columns = ['N', 'T', 'S', 'ncovs', 'p', 'true_desc_length', 'global_model_order', 'start_at_order', 'subgroup_orders'])
        ranks_pd = pd.DataFrame(ranks_one_parameter_run)
        results_one_parameter_pd = pd.concat((params_pd, ranks_pd), axis=1)
        results_one_parameter_pd.insert(len(params), 'nreps', pd.DataFrame(np.arange(1, simulation_params['nreps']+1)))   

        # save with the parameter combination
        if exp == 0:
            result_experiment = results_one_parameter_pd
        else:
            result_experiment = result_experiment.append(results_one_parameter_pd)
        result_experiment.reset_index(drop=True)

    return result_experiment

def parallelization(nreps=None, params=None, quality_measures=None, beam_search_params=None, markov_model_params=None, constraints=None, wcs_params=None):

    inputs = range(nreps)
    #num_cores = multiprocessing.cpu_count() - 2

    print('iterations...')

    ranks_one_parameter_run = Parallel(n_jobs=-2)(delayed(one_parameter_run)(i,
                                                                             params,
                                                                             quality_measures,
                                                                             beam_search_params, 
                                                                             markov_model_params, 
                                                                             constraints,
                                                                             wcs_params) for i in inputs)

    return ranks_one_parameter_run

def one_parameter_run(i=None, params=None, quality_measures=None, beam_search_params=None, markov_model_params=None, constraints=None, wcs_params=None):

    print(i)
    
    result_ranks_one_rep = one_repetition(params=params, 
                                          beam_search_params=beam_search_params, markov_model_params=markov_model_params,      
                                          constraints=constraints, wcs_params=wcs_params, 
                                          quality_measures=quality_measures)
  
    return result_ranks_one_rep

def one_repetition(params=None, quality_measures=None, beam_search_params=None, 
                   markov_model_params=None, constraints=None, wcs_params=None):

    #print('params', params)
    dataset, states, time_attributes = sso.sample_dataset(N=params[0], T=params[1], S=params[2], ncovs=params[3], 
                                                          p=params[4], true_desc_length=params[5], global_model_order=params[6],
                                                          subgroup_order=params[8])   

    attributes = sso.define_attributes(dataset=dataset, time_attributes=time_attributes)  

    #print(attributes)
    #print(states)
    #print(dataset.head(20))

    result_ranks_one_rep = {}
    for quality_measure in quality_measures:
        #print('quality_measure', quality_measure)
        result_emm, considered_subgroups, general_params = bso.beam_search(dataset=dataset, attributes=attributes, start_at_order=params[7],
                                                                           beam_search_params=beam_search_params, stop_at_order=markov_model_params['stop_at_order'],
                                                                           quality_measure=quality_measure, constraints=constraints, wcs_params=wcs_params)
        
        # here, as part of the experiment, the rank of the true subgroup is evaluated
        result_rank = suo.rank_result_emm(result_emm=result_emm, quality_measure=quality_measure, true_desc_length=params[5])
        result_ranks_one_rep.update(result_rank)
        result_ranks_one_rep.update({quality_measure + '_found_order': general_params['found_order']})

    #print(result_ranks_one_rep)

    return result_ranks_one_rep

