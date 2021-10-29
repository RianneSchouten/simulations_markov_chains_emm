import numpy as np 
import pandas as pd
import itertools as it
#import time
from joblib import Parallel, delayed
#import multiprocessing

import sample_sequences as ss
import beam_search as bs
import summaries as su

def experiment(nreps=None, seed=None, ncovs=None,
               transition=None, N=None, T=None, S=None, 
               nr_quantiles=None, constraints=None,
               quality_measures=None, w=None, d=None, q=None,
               save_location=None):

    parameter_set = list(it.product(N, T, S, ncovs, [True, False], [True, False])) # the [True, False] is for with/without difference in tA and with/without dif in pi
    #parameter_set = list(it.product(N, T, S, ncovs, [True], [False]))
    nexp = len(parameter_set)

    np.random.seed(seed)
    for exp in np.arange(nexp):   
        print('experiment', exp+1, 'of', nexp)

        params = parameter_set[exp]
        print('parameters:', params)

        ranks_one_parameter_run = parallelization(nreps=nreps, params=params, quality_measures=quality_measures, 
                                                  nr_quantiles=nr_quantiles, w=w, d=d, q=q)

        # concatenate all results per parameter combination
        params_pd = pd.DataFrame(np.tile(params, nreps).reshape(nreps, len(params)), columns = ['N', 'T', 'S', 'ncovs', 'distAyn', 'distPiyn'])
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
                                        ncovs=params[3], distAyn=params[4], distPiyn=params[5],
                                        nr_quantiles=nr_quantiles,
                                        quality_measures=quality_measures, w=w, d=d, q=q)
  
    return result_ranks_one_rep

def one_repetition(N=None, T=None, S=None, ncovs=None,
                   distAyn=None, distPiyn=None, nr_quantiles=None, 
                   quality_measures=None, w=None, d=None, q=None,
                   save_location=None):

    tA, tB, dataset, Adist, pidist = ss.sample_dataset(N=N, T=T, S=S, ncovs=ncovs, distAyn=distAyn, distPiyn=distPiyn)
    attributes = ss.define_attributes(dataset=dataset)
    #print(dataset.dtypes)
    #print(dataset.shape)

    '''
    df_attributes = pd.DataFrame(dict([(k, pd.Series(v)) for k,v in attributes.items()]))
    dfs = {'data': dataset, 'df_attributes': df_attributes}
    location_processed = 'data_input/' + 'ss' + '_preprocessed.xlsx'

    if (distAyn == 1) & (pidist == 0):
        writer = pd.ExcelWriter(location_processed, engine='xlsxwriter')
        for sheet_name in dfs.keys():
            dfs[sheet_name].to_excel(writer, sheet_name=sheet_name, index=False)
        writer.save()
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
    
    return result_ranks_one_rep
