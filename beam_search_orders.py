import numpy as np
import pandas as pd

import dataset as dt
import refinements as rf
import constraints as cs
#import summaries_orders as suo
import qualities_orders as qmo
import prepare_beam as pb
import prepare_result as pr
import dominance_pruning as dp
                                                                          
def beam_search(dataset=None, attributes=None, quality_measure=None, 
                beam_search_params=None, start_at_order=None, stop_at_order=None,
                constraints=None, wcs_params=None):

    df, cols, bin_atts, nom_atts, num_atts, dt_atts, idx = dt.read_data(dataset=dataset, attributes=attributes)
    #print(df.head(5))
    #print(df.shape)
    #print(cols)
    #print(bin_atts)
    #print(nom_atts)
    #print(num_atts)
    #print(dt_atts)
    #print(df.describe(include='all'))

    # Calculate general parameters
    general_params = qmo.calculate_general_parameters(df=df, cols=cols, attributes=attributes, order=1, 
                                                      start_at_order=start_at_order, 
                                                      stop_at_order=stop_at_order, 
                                                      quality_measure=quality_measure)
    #print(general_params)

    candidate_queue, nominal_values  = rf.create_starting_descriptions(df=df, cols=cols, 
                                                                       bin_atts=bin_atts, nom_atts=nom_atts, 
                                                                       num_atts=num_atts, dt_atts=dt_atts,
                                                                       nr_quantiles=beam_search_params['b'])
    #print('candidate queue:', candidate_queue)
    
    candidate_result_set = []
    considered_subgroups = {}
    #nconsd = 0
    for d_i in range(1, beam_search_params['d']+1):
        
        n_consd = 0
        n_sim_descs = 0
        n_small_groups = 0
        #n_redundant_coverage = 0
        
        #print('level:', d_i)

        cq_satisfied = []
        i = 0
        for seed in candidate_queue:

            #i += 1
            #print(i, ' of ', len(candidate_queue), ' candidates')

            subgroup, idx_sg, subgroup_compl, idx_compl = dt.select_subgroup(description=seed['description'], df=df, 
                                                                             bin_atts=bin_atts, num_atts=num_atts, nom_atts=nom_atts,
                                                                             dt_atts=dt_atts)
            if d_i == 1:
                seed_set = []
                seed_set.append(seed)
            else:                
                seed_set = rf.refine_seed(seed=seed, subgroup=subgroup, bin_atts=bin_atts, nom_atts=nom_atts,
                                          num_atts=num_atts, dt_atts=dt_atts, nr_quantiles=beam_search_params['b'], nominal_values=nominal_values)

            j = 0
            for desc in seed_set:

                #print('desc', desc)

                #j += 1
                #print(j, ' of ', len(seed_set), ' descs')

                print_this = False
                #if desc['description'] == {'x0': [1], 'x1': [1]}:
                #    print(desc['description'])
                #    print_this = True
                n_consd += 1
   
                redundancy_check_description = cs.redundant_description(desc=desc, cq_satisfied=cq_satisfied)    

                if not redundancy_check_description:
                    n_sim_descs += 1
                else:
                    subgroup, idx_sg, subgroup_compl, idx_compl = dt.select_subgroup(description=desc['description'], df=df,
                                                                                     bin_atts=bin_atts, nom_atts=nom_atts, num_atts=num_atts,
                                                                                     dt_atts=dt_atts)
                    
                    constraint_check_size = cs.constraint_subgroup_size(subgroup=subgroup, attributes=attributes, general_params=general_params, 
                                                                        constraint_subgroup_size=constraints['constraint_subgroup_size'])
                    
                    if not constraint_check_size:
                        n_small_groups += 1
                    else:
                        
                        subgroup_params = qmo.calculate_subgroup_parameters(df=df, subgroup=subgroup, subgroup_compl=subgroup_compl, idx_sg=idx_sg,
                                                                            attributes=attributes, quality_measure=quality_measure, start_at_order=start_at_order,
                                                                            general_params=general_params)
                        #print(subgroup_params)

                        # do heuristic search process for initial probs and for higher order
                        desc_qm = qmo.add_qm(desc=desc, idx_sg=idx_sg, general_params=general_params, 
                                             subgroup_params=subgroup_params, quality_measure=quality_measure, 
                                             start_at_order=subgroup_params['new_order'], stop_at_order=stop_at_order,
                                             print_this=print_this)

                        cq_satisfied.append(desc_qm)
                        #print(desc_qm['description'])
                        #print(desc_qm['qualities'][quality_measure])                 

        considered_subgroups['level_' + str(d_i)] = {'n_consd': n_consd, 'n_sim_descs': n_sim_descs, 
                                                     'n_small_groups': n_small_groups}

        # below we prepare the result set and beam (candidate_queue) for the next level
        # there, if required, we apply description based selection and cover based selection to prevent issues with redundancy
        beam_search_params.update({'d_i': d_i})
        candidate_result_set, candidate_queue, n_redun_descs = pb.collect_beam_and_candidate_result_set(candidate_result_set=candidate_result_set, cq_satisfied=cq_satisfied, 
                                                                                                        qm=quality_measure, beam_search_params=beam_search_params, 
                                                                                                        data_size=general_params['data_size']['seq_plus_transitions'], 
                                                                                                        wcs_params=wcs_params)
        considered_subgroups['level_' + str(d_i)]['n_redun_decs'] = n_redun_descs

    if wcs_params['run']:

        result_set, rs_n_redun_descs = pr.select_result_set(candidate_result_set=candidate_result_set[0], qm=quality_measure, 
                                                            beam_search_params=beam_search_params, 
                                                            data_size=general_params['data_size']['seq_plus_transitions'], 
                                                            wcs_params=wcs_params)

        # apply dominance pruning
        result_set_pruned, n_consd, n_small_groups = dp.apply_dominance_pruning(result_set=result_set, dataset=df, 
                                                                                bin_atts=bin_atts, nom_atts=nom_atts, num_atts=num_atts,
                                                                                dt_atts=dt_atts, start_at_order=start_at_order, stop_at_order=stop_at_order, 
                                                                                constraints=constraints, attributes=attributes, 
                                                                                general_params=general_params, qm=quality_measure, beam_search_params=beam_search_params)
        # again apply description and cover based selection
        final_result_set, rs_n_redun_descs = pr.select_result_set(candidate_result_set=result_set_pruned, qm=quality_measure, 
                                                                  beam_search_params=beam_search_params, 
                                                                  data_size=general_params['data_size']['seq_plus_transitions'], wcs_params=wcs_params)

        considered_subgroups['dominance_pruning'] = {'n_consd': n_consd, 'n_sim_descs': None, 
                                                 'n_small_groups': n_small_groups, 
                                                 'n_redun_decs': rs_n_redun_descs}
    
    else:

        final_result_set = candidate_result_set[0]
        #print(len(final_result_set))
    
    # result_set is a list of dictionaries
    # result_emm is a dataframe with the descriptive attributes on the columns, and q*2 rows
    result_emm = pr.prepare_result_list(result_set=final_result_set)

    return result_emm, considered_subgroups, general_params
