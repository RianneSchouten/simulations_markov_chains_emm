import numpy as np
import pandas as pandas
import random as r

import beam_search as bs
import emm_rw_dataset as rwdt
from joblib import Parallel, delayed

def parallelization_over_iterations(m=None, dataset=None, attributes=None, nr_quantiles=None, quality_measure=None, w=None, d=None):

    inputs = range(m)
    print('iterations...')

    qm_values = Parallel(n_jobs=-2)(delayed(build_distribution)(i, dataset, attributes, nr_quantiles, quality_measure, w, d) 
                                            for i in inputs)

    return qm_values

def build_distribution(i=None, dataset=None, attributes=None, nr_quantiles=None, quality_measure=None, w=None, d=None):

    print(i)

    shuffled_dataset = shuffle_dataset(dataset=dataset, attributes=attributes)

    # perform beam search
    result_emm, considered_subgroups, general_params = bs.beam_search(dataset=shuffled_dataset, distribution=None, attributes=attributes,
                                                             nr_quantiles=nr_quantiles, quality_measure=quality_measure, w=w, d=d, q=1)

    # save qm of the first subgroup
    qm_value = result_emm.loc[result_emm.sg == 0, quality_measure].values[1] # 1 is qualities

    return qm_value

def shuffle_dataset(dataset=None, attributes=None):

    id_attribute = attributes['id_attribute']
    outcome_attribute = attributes['outcome_attribute']
    time_attributes = attributes['time_attributes']
    first_timepoint = attributes['first_timepoint']

    cols = dataset.columns
    leftout_cols = []
    if outcome_attribute is not None:
        cols = cols.drop(outcome_attribute)
        leftout_cols.append(outcome_attribute)
    if time_attributes is not None:
        cols = cols.drop(time_attributes)
        leftout_cols.append(time_attributes)
    
    #print(cols) # let id_attribute be part of this and shuffle it together with the other descriptive attributes
    #print(leftout_cols)

    cnts = dataset[id_attribute].value_counts().sort_index()
    idx = cnts.index.values
    #print(cnts)   
    
    new_idx = idx.copy()
    r.shuffle(new_idx)
    #print(new_idx)

    shuffled_dataset = dataset.copy()

    length = len(new_idx)
    total_length = cnts.values.sum()
    out = list(map(lambda x: np.tile(dataset.loc[(dataset[id_attribute] == new_idx[x]) & 
                                                 (dataset[time_attributes[0]] == first_timepoint), cols].values[0], 
                                     cnts.iloc[x]), 
                             np.arange(length)))

    #print(len(out))

    repl = np.concatenate(out)
    #print(len(repl))
    #print(repl.shape)

    replacement = repl.reshape(total_length, len(cols))
    #print(replacement.shape)

    shuffled_dataset[cols] = replacement

    #print(dataset.head(20))
    #print(shuffled_dataset.head(20))

    return shuffled_dataset

