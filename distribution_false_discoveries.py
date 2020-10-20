import numpy as np
import pandas as pandas
import random as r

import beam_search as bs
import emm_rw_dataset as rwdt

def build_distribution(m=None, dataset=None, time_attributes=None, skip_attributes=None, id_attribute=None,
                       descriptives=None, first_timepoint=None, nr_quantiles=None, quality_measure=None, w=None, d=None, q=None):

    distribution = []
    for k in np.arange(m):
        print('iteration:', k)

        # shuffle dataset
        shuffled_dataset = shuffle_dataset(dataset=dataset, time_attributes=time_attributes, id_attribute=id_attribute, 
                                           descriptives=descriptives, first_timepoint=first_timepoint)

        # perform beam search
        result_emm, nconsd_list, general_params = bs.beam_search(dataset=shuffled_dataset, distribution=None, time_attributes=time_attributes, 
                                                                 skip_attributes=skip_attributes, id_attribute=id_attribute, first_timepoint=first_timepoint,
                                                                 nr_quantiles=nr_quantiles, quality_measure=quality_measure, w=w, d=d, q=q)

        # save qm of the first subgroup
        qm_value = result_emm.loc[result_emm.sg == 0, quality_measure].values[1] # 1 is qualities
        distribution.append(qm_value)

    return distribution

def shuffle_dataset(dataset=None, time_attributes=None, id_attribute=None, descriptives=None, first_timepoint=None):

    len_descs = len(descriptives)

    cnts = dataset[id_attribute].value_counts().sort_index()
    idx = cnts.index.values   
    
    new_idx = idx.copy()
    r.shuffle(new_idx)

    shuffled_dataset = dataset.copy()

    length = len(new_idx)
    total_length = cnts.values.sum()
    out = list(map(lambda x: np.tile(dataset.loc[(dataset[id_attribute] == new_idx[x]) & 
                                                 (dataset[time_attributes[0]] == first_timepoint), descriptives].values[0], 
                                     cnts.iloc[x]), 
                             np.arange(length)))

    repl = np.concatenate(out)
    replacement = repl.reshape(total_length, len_descs)
    shuffled_dataset[descriptives] = replacement

    return shuffled_dataset

