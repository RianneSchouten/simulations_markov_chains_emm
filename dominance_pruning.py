import numpy as np
import pandas as pd
import itertools as it

#import select_subgroup as ss
#import collect_qualities as qu
import constraints as cs

import dataset as dt
import qualities_orders as qmo

def apply_dominance_pruning(result_set=None, dataset=None, 
                            bin_atts=None, num_atts=None, nom_atts=None, dt_atts=None,
                            start_at_order=None, ref=None, stop_at_order=None, 
                            constraint_subgroup_size=None, attributes=None, general_params=None, qm=None, beam_search_params=None):

    print('start pruning')
    pruned_descriptions = get_new_descritions(result_set=result_set)
    pruned_subgroups, n_small_groups = get_new_qualities(pruned_descriptions=pruned_descriptions, dataset=dataset, 
                                                                        bin_atts=bin_atts, nom_atts=nom_atts, num_atts=num_atts,
                                                                        dt_atts=dt_atts, start_at_order=start_at_order, ref=ref, stop_at_order=stop_at_order,
                                                                        constraint_subgroup_size=constraint_subgroup_size, attributes=attributes, 
                                                                        general_params=general_params, qm=qm, beam_search_params=beam_search_params)

    return pruned_subgroups, len(pruned_descriptions), n_small_groups

def get_new_descritions(result_set=None):

    pruned_descriptions = []
    for existing_subgroup in result_set:

        old_desc = existing_subgroup['description']
        items_old_desc = old_desc.items()

        for r in np.arange(1, len(list(items_old_desc))):
            combs = list(it.combinations(items_old_desc, r=r))
            combs_r = [{'description': dict(desc)} for desc in combs]
            pruned_descriptions.append(combs_r)

    pruned_descriptions = [item for sublist in pruned_descriptions for item in sublist]

    return pruned_descriptions

def get_new_qualities(pruned_descriptions=None, dataset=None, 
                      bin_atts=None, num_atts=None, nom_atts=None, dt_atts=None,
                      start_at_order=None, ref=None, stop_at_order=None,
                      constraint_subgroup_size=None,
                      attributes=None, general_params=None, qm=None, beam_search_params=None):

    pruned_subgroups = []
    n_small_groups = 0
    for desc in pruned_descriptions:

        #print(desc)

        #subgroup, idx_sg, subgroup_compl, idx_compl = ss.select_subgroup(description=desc['description'], df=dataset, descriptives=descriptives)
        subgroup, idx_sg, subgroup_compl, idx_compl = dt.select_subgroup(description=desc['description'], df=dataset,
                                                                         bin_atts=bin_atts, nom_atts=nom_atts, num_atts=num_atts,
                                                                         dt_atts=dt_atts)

        constraint_check_size = cs.constraint_subgroup_size(subgroup=subgroup, attributes=attributes, general_params=general_params, constraint_subgroup_size=constraint_subgroup_size)
                    
        if not constraint_check_size:
            n_small_groups += 1
        else:

            #subgroup_params, is_replaced = qu.calculate_subgroup_parameters(subgroup=subgroup, attributes=attributes)
            subgroup_params = qmo.calculate_subgroup_parameters(df=dataset, subgroup=subgroup, subgroup_compl=subgroup_compl, idx_sg=idx_sg,
                                                                attributes=attributes, quality_measure=qm, start_at_order=start_at_order,
                                                                general_params=general_params, ref=ref)

            desc_qm = qmo.add_qm(desc=desc, idx_sg=idx_sg, general_params=general_params, 
                                 subgroup_params=subgroup_params, quality_measure=qm, 
                                 ref=ref, start_at_order=subgroup_params['new_order'], stop_at_order=stop_at_order,
                                 print_this=False)

            #print(desc_qm.keys())
            pruned_subgroups.append(desc_qm)   

    return pruned_subgroups, n_small_groups