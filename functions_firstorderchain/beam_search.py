import numpy as np
import pandas as pd

import dataset as dt
import refinements as rf
import qualities as qm
import constraints as cs
import summaries as su

def beam_search(dataset=None, distribution=None, attributes=None, nr_quantiles=None, quality_measure=None, 
                w=None, d=None, q=None, Z=None,
                save_location=None):

    df, cols, bin_atts, nom_atts, num_atts, dt_atts = dt.read_data(dataset=dataset, attributes=attributes)
    #print(df.head(5))
    #print(df.shape)
    #print(cols)
    #print(bin_atts)
    #print(nom_atts)
    #print(num_atts)
    #print(dt_atts)
    #print(df.describe(include='all'))

    # Calculate general parameters
    general_params = qm.calculate_general_parameters(df=df, distribution=distribution, cols=cols, attributes=attributes)
    #print(general_params)

    candidate_queue  = rf.create_starting_descriptions(df=df, cols=cols, 
                                                       bin_atts=bin_atts, nom_atts=nom_atts, 
                                                       num_atts=num_atts, dt_atts=dt_atts,
                                                       nr_quantiles=nr_quantiles)

    #print('candidate queue:', candidate_queue)
    
    result_set = []
    considered_subgroups = {}
    #nconsd = 0
    for d_i in range(1, d+1):
        
        n_consd = 0
        n_redundant_descs = 0
        n_small_groups = 0
        n_redundant_coverage = 0
        
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

                #print(desc['description'])
                n_consd += 1
   
                redundancy_check_description = cs.redundant_description(desc=desc, cq_satisfied=cq_satisfied)    

                if not redundancy_check_description:
                    n_redundant_descs += 1
                else:
                    subgroup, idx_sg = dt.select_subgroup(description=desc['description'], df=df,
                                                          bin_atts=bin_atts, nom_atts=nom_atts, num_atts=num_atts,
                                                          dt_atts=dt_atts)
                    
                    constraint_check_size = cs.constraint_subgroup_size(subgroup=subgroup, attributes=attributes, general_params=general_params)
                    
                    if not constraint_check_size:
                        n_small_groups += 1
                    else:
                        redundancy_check_coverage = cs.redundant_subgroup_coverage(level=d_i, seed=seed, idx_sg_new=idx_sg)
                    
                        if not redundancy_check_coverage:
                            n_redundant_coverage += 1
                        else:                        
                            # calculate quality measure
                            subgroup_params = qm.calculate_subgroup_parameters(df=df, subgroup=subgroup, idx_sg=idx_sg,
                                                                           attributes=attributes,
                                                                           general_params=general_params)

                            desc_qm = qm.add_qm(desc=desc, idx_sg=idx_sg, general_params=general_params, 
                                            subgroup_params=subgroup_params, quality_measure=quality_measure)

                            cq_satisfied.append(desc_qm)                  

        considered_subgroups['level_' + str(d_i)] = {'n_consd': n_consd, 'n_redundant_descs': n_redundant_descs, 
                                                     'n_small_groups': n_small_groups, 'n_redundant_coverage': n_redundant_coverage}

        result_set, candidate_queue = su.prepare_resultlist_cq(result_set=result_set, cq_satisfied=cq_satisfied, 
                                                               quality_measure=quality_measure, q=q, w=w)
        #print(candidate_queue)
    
    # result set is a dictionary
    # result emm is a dataframe with the descriptive attributes on the columns, and q*2 rows
    result_emm = su.resultlist_emm(result_set=result_set, distribution=distribution, general_params=general_params,
                                   quality_measure=quality_measure, Z=Z)
    #print(result_emm)
    
    if save_location is not None:
        result_emm.to_excel(save_location)
    
    # nconsd_list contains the number of candidate descriptions that are considered at least level
    #print(nconsd_list)
   
    return result_emm, considered_subgroups, general_params