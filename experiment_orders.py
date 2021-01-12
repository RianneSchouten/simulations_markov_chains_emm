import numpy as np 
import pandas as pd
import itertools as it
from joblib import Parallel, delayed

import sample_sequences_orders as sso
import beam_search_orders as bso
import summaries_orders as suo

def experiment(nreps=None, seed=None, ncovs=None, subgroup_orders=None,
               N=None, T=None, S=None, refs=None,
               nr_quantiles=None, start_at_order=None,
               quality_measures=None, w=None, d=None, q=None,
               constraint_subgroup_size=None, constraint_subgroup_coverage=None,
               stop_at_order=None,
               save_location=None):

    parameter_set = list(it.product(N, T, S, ncovs, subgroup_orders, refs)) 
    nexp = len(parameter_set)

    np.random.seed(seed)
    for exp in np.arange(nexp):   
        print('experiment', exp+1, 'of', nexp)

        params = parameter_set[exp]
        print('parameters:', params)

        ranks_one_parameter_run = parallelization(nreps=nreps, params=params, quality_measures=quality_measures, 
                                                  nr_quantiles=nr_quantiles, w=w, d=d, q=q, start_at_order=start_at_order,
                                                  stop_at_order=stop_at_order, constraint_subgroup_size=constraint_subgroup_size, 
                                                  constraint_subgroup_coverage=constraint_subgroup_coverage)

        # concatenate all results per parameter combination
        params_pd = pd.DataFrame(np.tile(params, nreps).reshape(nreps, len(params)), columns = ['N', 'T', 'S', 'ncovs', 'subgroup_orders', 'refs'])
        ranks_pd = pd.DataFrame(ranks_one_parameter_run)
        results_one_parameter_pd = pd.concat((params_pd, ranks_pd), axis=1)
        results_one_parameter_pd.insert(len(params), 'nreps', pd.DataFrame(np.arange(1, nreps+1)))   

        # save with the parameter combination
        if exp == 0:
            result_experiment = results_one_parameter_pd
        else:
            result_experiment = result_experiment.append(results_one_parameter_pd)
        result_experiment.reset_index(drop=True)

    return result_experiment

def parallelization(nreps=None, params=None, quality_measures=None, nr_quantiles=None, w=None, d=None, q=None, start_at_order=None, stop_at_order=None,
                    constraint_subgroup_size=None, constraint_subgroup_coverage=None):

    inputs = range(nreps)
    #num_cores = multiprocessing.cpu_count() - 2

    print('iterations...')

    ranks_one_parameter_run = Parallel(n_jobs=-2)(delayed(one_parameter_run)(i,
                                                                             params,
                                                                             quality_measures,
                                                                             nr_quantiles,
                                                                             w, d, q,
                                                                             start_at_order,
                                                                             stop_at_order,
                                                                             constraint_subgroup_size,
                                                                             constraint_subgroup_coverage) for i in inputs)

    return ranks_one_parameter_run

def one_parameter_run(i=None, params=None, quality_measures=None, nr_quantiles=None, w=None, d=None, q=None, start_at_order=None, stop_at_order=None,
                      constraint_subgroup_size=None, constraint_subgroup_coverage=None):

    print(i)
    
    result_ranks_one_rep = one_repetition(N=params[0], T=params[1], S=params[2], 
                                          ncovs=params[3], subgroup_order=params[4],
                                          nr_quantiles=nr_quantiles, ref=params[5], 
                                          start_at_order=start_at_order, stop_at_order=stop_at_order,
                                          quality_measures=quality_measures, w=w, d=d, q=q,
                                          constraint_subgroup_size=constraint_subgroup_size, constraint_subgroup_coverage=constraint_subgroup_coverage)
  
    return result_ranks_one_rep

def one_repetition(N=None, T=None, S=None, ncovs=None, subgroup_order=None,
                   nr_quantiles=None, ref=None, start_at_order=None,
                   quality_measures=None, w=None, d=None, q=None,
                   constraint_subgroup_size=None, constraint_subgroup_coverage=None,
                   stop_at_order=None,
                   save_location=None):

    dataset, states, time_attributes = sso.sample_dataset(N=N, T=T, S=S, ncovs=ncovs, subgroup_order=subgroup_order)    
    attributes = sso.define_attributes(dataset=dataset, time_attributes=time_attributes)  

    #print(attributes)
    #print(states)
    #print(dataset.head(20))

    result_ranks_one_rep = {}
    for quality_measure in quality_measures:
        #print('quality_measure', quality_measure)
        result_emm, considered_subgroups, general_params = bso.beam_search(dataset=dataset, distribution=None, attributes=attributes, 
                                                                           nr_quantiles=nr_quantiles, save_location=None, ref=ref, start_at_order=start_at_order,
                                                                           stop_at_order=stop_at_order, quality_measure=quality_measure, w=w, d=d, q=q, Z=None,
                                                                           constraint_subgroup_size=constraint_subgroup_size, constraint_subgroup_coverage=constraint_subgroup_coverage)
        # here, as part of the experiment, the rank of the true subgroup is evaluated
        result_rank = suo.rank_result_emm(result_emm=result_emm, quality_measure=quality_measure)
        result_ranks_one_rep.update(result_rank)
        result_ranks_one_rep.update({quality_measure + '_found_order': general_params['found_order']})

    #print(result_ranks_one_rep)

    return result_ranks_one_rep

