import numpy as np 
import pandas as pd
import itertools as it
from joblib import Parallel, delayed

import sample_sequences_orders as sso
import beam_search as bs
import summaries as su

def experiment(nreps=None, seed=None, ncovs=None, subgroup_orders=None,
               transition=None, N=None, T=None, S=None, 
               nr_quantiles=None, constraints=None,
               quality_measures=None, w=None, d=None, q=None,
               save_location=None):

    parameter_set = list(it.product(N, T, S, ncovs, subgroup_orders)) 
    nexp = len(parameter_set)

    np.random.seed(seed)
    for exp in np.arange(nexp):   
        print('experiment', exp+1, 'of', nexp)

        params = parameter_set[exp]
        print('parameters:', params)

        ranks_one_parameter_run = parallelization(nreps=nreps, params=params, quality_measures=quality_measures, 
                                                  nr_quantiles=nr_quantiles, w=w, d=d, q=q)

        print(ranks_one_parameter_run)

    return ranks_one_parameter_run

def parallelization(nreps=None, params=None, quality_measures=None, nr_quantiles=None, w=None, d=None, q=None):

    inputs = range(nreps)
    #num_cores = multiprocessing.cpu_count() - 2

    print('iterations...')

    ranks_one_parameter_run = Parallel(n_jobs=-2)(delayed(one_parameter_run)(i,
                                                                             params,
                                                                             quality_measures,
                                                                             nr_quantiles,
                                                                             w, d, q) for i in inputs)

    return ranks_one_parameter_run

def one_parameter_run(i=None, params=None, quality_measures=None, nr_quantiles=None, w=None, d=None, q=None):

    print(i)
    
    result_ranks_one_rep = one_repetition(N=params[0], T=params[1], S=params[2], 
                                          ncovs=params[3], subgroup_order=params[4],
                                          nr_quantiles=nr_quantiles,
                                          quality_measures=quality_measures, w=w, d=d, q=q)
  
    return result_ranks_one_rep

def one_repetition(N=None, T=None, S=None, ncovs=None, subgroup_order=None,
                   nr_quantiles=None, 
                   quality_measures=None, w=None, d=None, q=None,
                   save_location=None):

    tA, tB, dataset, Adist, pidist = sso.sample_dataset(N=N, T=T, S=S, ncovs=ncovs, subgroup_order=subgroup_order)
    print(dataset.dtypes)
    print(dataset.shape)
    
    attributes = sso.define_attributes(dataset=dataset)  

    '''
    result_ranks_one_rep = {'Adist': Adist, 'pidist': pidist}
    for quality_measure in quality_measures:
        #print('quality_measure', quality_measure)
        result_emm, considered_subgroups, general_params = bs.beam_search(dataset=dataset, distribution=None, attributes=attributes, 
                                                                          nr_quantiles=nr_quantiles, save_location=None,
                                                                          quality_measure=quality_measure, w=w, d=d, q=q)

        # here, as part of the experiment, the rank of the true subgroup is evaluated
        result_rank = su.rank_result_emm(result_emm=result_emm, quality_measure=quality_measure)
        result_ranks_one_rep.update(result_rank)
    
    #result_ranks_one_rep.update({'nconsd': np.mean(all_nconsd)})
    '''
    result_ranks_one_rep = 10

    return result_ranks_one_rep

result_experiment = experiment(nreps=1, seed=20200102, ncovs=[3], 
                               N=[5], T=[5], S=[2], 
                               nr_quantiles=8, subgroup_orders = [2, 3],
                               quality_measures=['deltatv', 'omegatv', 'phiwd', 'phikl', 'phiarl', 'phiwarl', 'phibic'],
                               w=25, d=2, q=25,
                               save_location='./data_output/')