import numpy as np
import pandas as pd
import itertools as it

import beam_search_orders as bso
import summaries_orders as suo
import distribution_false_discoveries_orders as dfdo

def analysis_rw_dataset(dataset=None, calculate_distributions=None, attributes=None, 
                        nr_quantiles=None, quality_measures=None, w=None, d=None, q=None, m=None, Z=None, 
                        ref=None, start_at_order=None, save_location=None):   
    
    if calculate_distributions:

        distributions = {}

        for quality_measure in quality_measures:

            # find distribution
            # to find the distribution q = 1
            distribution = dfdo.parallelization_over_iterations(m=m, dataset=dataset, attributes=attributes,
                                                               nr_quantiles=nr_quantiles, quality_measure=quality_measure, w=w, d=d,
                                                               ref=ref, start_at_order=start_at_order)
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
    result_rw_analysis = pd.DataFrame()

    for quality_measure in quality_measures:

        print(quality_measure)
    
        result_emm, considered_subgroups, general_params = bso.beam_search(dataset=dataset, distribution=distributions[quality_measure], attributes=attributes,
                                                                           nr_quantiles=nr_quantiles, quality_measure=quality_measure, w=w, d=d, q=q, Z=Z, 
                                                                           ref=ref, start_at_order=start_at_order)
        print(considered_subgroups)

        # join with other quality measures, if any
        result_rw_analysis = suo.join_result_emm(result_emm=result_emm, result_rw_analysis=result_rw_analysis, quality_measure=quality_measure, q=q)

    return result_rw_analysis, considered_subgroups, general_params

def load(name_dataset=None):

    #location = 'C:/Users/20200059/Documents/Projects/Dialect/Diabetes ZGT data/' + name_dataset + '_preprocessed.xlsx'
    location = 'C:/Users/20200059/Documents/Projects/SequentialData/data_input/' + name_dataset + '_preprocessed.xlsx'
    sheets = pd.read_excel(location, sheet_name=['data', 'df_attributes', 'combinations'])

    data = sheets['data']
    df_attributes = sheets['df_attributes']
    combinations = sheets['combinations']

    time_attributes = [value for value in df_attributes['time_attributes'].values if str(value) != 'nan'] 
    skip_attributes = [value for value in df_attributes['skip_attributes'].values if str(value) != 'nan']
    id_attribute = df_attributes['id_attribute'][0]
    first_timepoint = df_attributes['first_timepoint'][0]
    descriptives = [value for value in df_attributes['descriptives'] .values if str(value) != 'nan']   

    outcome_attribute = None 
    attributes = {'time_attributes': time_attributes, 'skip_attributes': skip_attributes,
                  'id_attribute': id_attribute, 'first_timepoint': first_timepoint, 'descriptives': descriptives,
                  'outcome_attribute': outcome_attribute}

    return data, attributes, combinations



