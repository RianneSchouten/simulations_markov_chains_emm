import numpy as np
import pandas as pandas
import beam_search as bs
import rw_dataset as rwdt

def build_distribution(m=None, dataset=None, time_attributes=None, skip_attributes=None, id_attribute=None,
                       first_timepoint=None, nr_quantiles=None, quality_measure=None, w=None, d=None, q=None):

    distribution = []
    for k in np.arange(m):
        print('iteration:', k)

        # shuffle dataset
        shuffled_dataset = rwdt.shuffle_dataset(dataset=dataset, time_attributes=time_attributes, id_attribute=id_attribute, first_timepoint=first_timepoint)

        # perform beam search
        result_emm, nconsd_list, general_params = bs.beam_search(dataset=shuffled_dataset, distribution=None, time_attributes=time_attributes, 
                                                                 skip_attributes=skip_attributes, id_attribute=id_attribute, first_timepoint=first_timepoint,
                                                                 nr_quantiles=nr_quantiles, quality_measure=quality_measure, w=w, d=d, q=q)

        # save qm of the first subgroup
        qm_value = result_emm.loc[result_emm.sg == 0, quality_measure].values[1] # 1 is qualities
        distribution.append(qm_value)

    return distribution

