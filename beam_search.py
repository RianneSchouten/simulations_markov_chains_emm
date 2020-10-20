import numpy as np
import pandas as pd
#import time

import dataset as dt
import refinements as rf
import qualities as qm
import constraints as cs
import summaries as su

def beam_search(dataset=None, distribution=None, time_attributes=None, skip_attributes=None, id_attribute=None,
                first_timepoint=None, nr_quantiles=None, quality_measure=None, 
                w=None, d=None, q=None, Z=None,
                save_location=None):

    df, cols, bin_atts, nom_atts, num_atts, dt_atts = dt.read_data(dataset=dataset, skip_attributes=skip_attributes,
                                                                   id_attribute=id_attribute, time_attributes=time_attributes)
    #print(df.head(5))
    #print(df.shape)
    #print(cols)
    print(bin_atts)
    print(nom_atts)
    print(num_atts)
    print(dt_atts)
    #print(df.describe(include='all'))

    # Calculate general parameters
    general_params = qm.calculate_general_parameters(df=df, distribution=distribution, cols=cols, time_attributes=time_attributes, 
                                                     id_attribute=id_attribute, first_timepoint=first_timepoint)
    #print(general_params)

    candidate_queue  = rf.create_starting_descriptions(df=df, cols=cols, 
                                                       bin_atts=bin_atts, nom_atts=nom_atts, 
                                                       num_atts=num_atts, dt_atts=dt_atts,
                                                       nr_quantiles=nr_quantiles)

    #print('candidate queue:', candidate_queue)
    
    result_set = []
    nconsd_list = []
    #nconsd = 0
    for d_i in range(1, d+1):
        nconsd = 0
        #print('level:', d_i)

        cq_satisfied = []
        for seed in candidate_queue:

            subgroup, idx_sg = dt.select_subgroup(description=seed['description'], df=df, 
                                                  bin_atts=bin_atts, num_atts=num_atts, nom_atts=nom_atts,
                                                  dt_atts=dt_atts)
            if d_i == 1:
                seed_set = []
                seed_set.append(seed)
            else:                
                seed_set = rf.refine_seed(seed=seed, subgroup=subgroup, bin_atts=bin_atts, nom_atts=nom_atts,
                                          num_atts=num_atts, dt_atts=dt_atts, nr_quantiles=nr_quantiles)

            for desc in seed_set:

                # check for redundant descriptions
                # the comparison has to be done with the candidate queue of the current iteration only
                # this queue is saved in cq_satisfied
                redundancy_check = True
                for seed in cq_satisfied:
                    if desc['description'] == seed['description']:
                        redundancy_check = False
                        break

                if redundancy_check: 

                    subgroup, idx_sg = dt.select_subgroup(description=desc['description'], df=df,
                                                          bin_atts=bin_atts, nom_atts=nom_atts, num_atts=num_atts,
                                                          dt_atts=dt_atts)
                    # constraint on subgroup size
                    if len(subgroup)/general_params['data_size'] > 0.1:

                        # calculate quality measure
                        subgroup_params = qm.calculate_subgroup_parameters(df=df, subgroup=subgroup, idx_sg=idx_sg,
                                                                           id_attribute=id_attribute, time_attributes=time_attributes, 
                                                                           first_timepoint=first_timepoint,
                                                                           general_params=general_params)

                        desc_qm = qm.add_qm(desc=desc, idx_sg=idx_sg, general_params=general_params, 
                                            subgroup_params=subgroup_params, quality_measure=quality_measure)

                        if distribution is not None:
                            # check whether the qm is significant
                            check, checked_desc_qm = qm.check_significance(general_params=general_params, desc_qm=desc_qm, quality_measure=quality_measure, Z=Z)
                            if check:
                                cq_satisfied.append(checked_desc_qm)
                        else:
                            cq_satisfied.append(desc_qm)
                        nconsd += 1

        nconsd_list.append(nconsd)
        result_set, candidate_queue = su.prepare_resultlist_cq(result_set=result_set, cq_satisfied=cq_satisfied, 
                                                               quality_measure=quality_measure, q=q, w=w)
 
    # result set is a dictionary
    # result emm is a dataframe with the descriptive attributes on the columns, and q*2 rows
    result_emm = su.resultlist_emm(result_set=result_set)
    #print(result_emm)
    
    if save_location is not None:
        result_emm.to_excel(save_location)
    
    # nconsd_list contains the number of candidate descriptions that are considered at least level
    #print(nconsd_list)
   
    return result_emm, nconsd_list, general_params