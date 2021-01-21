import numpy as np
import pandas as pd
import itertools as it

import beam_search_orders as bso
import summaries_orders as suo
import distribution_false_discoveries_orders as dfdo

def analysis_rw_dataset(dataset=None, calculate_distribution=None, use_distribution=None, attributes=None, 
                        nr_quantiles=None, quality_measure=None, w=None, d=None, q=None, m=None, Z=None, 
                        constraint_subgroup_coverage=None, constraint_subgroup_size=None,
                        ref=None, start_at_order=None, stop_at_order=None, save_location=None):   
    
    if use_distribution:
  
        if calculate_distribution:

            distributions = {}

            # find distribution
            # to find the distribution q = 1
            distribution = dfdo.parallelization_over_iterations(m=m, dataset=dataset, attributes=attributes,
                                                                    constraint_subgroup_coverage=constraint_subgroup_coverage, constraint_subgroup_size=constraint_subgroup_size,
                                                                    nr_quantiles=nr_quantiles, quality_measure=quality_measure, w=w, d=d,
                                                                    ref=ref, start_at_order=start_at_order, stop_at_order=stop_at_order)
            print(distribution)
            distributions[quality_measure] = distribution

            # save
            pd_distributions = pd.DataFrame(distributions)
            pd_distributions_info = pd.DataFrame({'m': [m], 'nr_quantiles': [nr_quantiles], 'w': [w], 'd': [d], 'q': [q]})
            dfs = {'pd_distributions': pd_distributions, 'pd_distributions_info': pd_distributions_info}

            writer = pd.ExcelWriter(save_location + '_distributions.xlsx', engine='xlsxwriter')
            for sheet_name in dfs.keys():
                dfs[sheet_name].to_excel(writer, sheet_name=sheet_name, index=False)
            writer.save()

        else:

            # load
            sheets = pd.read_excel(save_location + '_distributions.xlsx', sheet_name=['pd_distributions', 'pd_distributions_info'], header=0)
            distributions = sheets['pd_distributions']

        # use distribution in the beam search    
        result_rw_analysis, considered_subgroups, general_params = bso.beam_search(dataset=dataset, distribution=distributions[quality_measure], attributes=attributes,
                                                                               nr_quantiles=nr_quantiles, quality_measure=quality_measure, w=w, d=d, q=q, Z=Z, 
                                                                               ref=ref, start_at_order=start_at_order, stop_at_order=stop_at_order,
                                                                               constraint_subgroup_coverage=constraint_subgroup_coverage, constraint_subgroup_size=constraint_subgroup_size)
        print(considered_subgroups)

    else:

        # do not use the distribution    
        result_rw_analysis, considered_subgroups, general_params = bso.beam_search(dataset=dataset, distribution=None, attributes=attributes,
                                                                               nr_quantiles=nr_quantiles, quality_measure=quality_measure, w=w, d=d, q=q, Z=None, 
                                                                               ref=ref, start_at_order=start_at_order, stop_at_order=stop_at_order,
                                                                               constraint_subgroup_coverage=constraint_subgroup_coverage, constraint_subgroup_size=constraint_subgroup_size)
        print(considered_subgroups)

    return result_rw_analysis, considered_subgroups, general_params

def load(name_dataset=None):

    location = 'C:/Users/20200059/Documents/Projects/Dialect/Diabetes ZGT data/' + name_dataset + '_preprocessed.xlsx'
    sheets = pd.read_excel(location, sheet_name=['data', 'summary', 'columns_and_missings', 'df_attributes', 'combinations'], index_col=0)

    #location = 'C:/Users/20200059/Documents/Projects/SequentialData/data_input/' + name_dataset + '_preprocessed.xlsx'
    #sheets = pd.read_excel(location, sheet_name=['data', 'summary', 'columns_and_missings', 'unique_per_seq_length', 'df_attributes', 'combinations'], index_col=0)

    #location = 'C:/Users/20200059/Documents/Projects/SequentialData/data_input/' + name_dataset + '_preprocessed.xlsx'
    #sheets = pd.read_excel(location, sheet_name=['data', 'summary', 'columns_and_missings', 'df_attributes', 'combinations'], index_col=0)

    data = sheets['data']
    df_attributes = sheets['df_attributes']
    combinations = sheets['combinations']

    time_attributes = [value for value in df_attributes['time_attributes'].values if str(value) != 'nan'] 
    skip_attributes = [value for value in df_attributes['skip_attributes'].values if str(value) != 'nan']
    id_attribute = df_attributes['id_attribute'][0]
    first_timepoint = df_attributes['first_timepoint'][0]
    #descriptives = [value for value in df_attributes['descriptives'] .values if str(value) != 'nan']   

    outcome_attribute = None 
    attributes = {'time_attributes': time_attributes, 'skip_attributes': skip_attributes,
                  'id_attribute': id_attribute, 'first_timepoint': first_timepoint, 
                  'outcome_attribute': outcome_attribute}

    return data, attributes, combinations




