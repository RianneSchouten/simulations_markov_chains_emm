import numpy as np
import pandas as pd
import itertools as it

import beam_search_orders as bso
import summaries_orders as suo

def analysis_rw_dataset(dataset=None, attributes=None, 
                        beam_search_params=None, quality_measure=None, constraints=None,
                        markov_model_params=None, wcs_params=None):   

    result_rw_analysis, considered_subgroups, general_params = bso.beam_search(dataset=dataset, attributes=attributes, quality_measure=quality_measure, 
                                                                               beam_search_params=beam_search_params, 
                                                                               start_at_order=markov_model_params['start_at_order'], 
                                                                               stop_at_order=markov_model_params['stop_at_order'],
                                                                               constraints=constraints, wcs_params=wcs_params)
    print(considered_subgroups)

    return result_rw_analysis, considered_subgroups, general_params

def load(name_dataset=None):

    print('load data')

    if name_dataset == 'movies':
        location = 'data_input/' + name_dataset + '_preprocessed.xlsx'
        sheets = pd.read_excel(location, sheet_name=['data', 'summary', 'columns_and_missings', 'df_attributes', 'combinations'], index_col=0)
    else:
        location = 'C:/Users/20200059/Documents/Projects/Dialect/Diabetes ZGT data/' + name_dataset + '_preprocessed.xlsx'
        sheets = pd.read_excel(location, sheet_name=['data', 'summary', 'columns_and_missings', 'df_attributes', 'combinations'], index_col=0)

    data = sheets['data']
    df_attributes = sheets['df_attributes']
    combinations = sheets['combinations']

    time_attributes = [value for value in df_attributes['time_attributes'].values if str(value) != 'nan'] 
    skip_attributes = [value for value in df_attributes['skip_attributes'].values if str(value) != 'nan']
    id_attribute = df_attributes['id_attribute'][0]
    first_timepoint = df_attributes['first_timepoint'][0]

    outcome_attribute = None 
    attributes = {'time_attributes': time_attributes, 'skip_attributes': skip_attributes,
                  'id_attribute': id_attribute, 'first_timepoint': first_timepoint, 
                  'outcome_attribute': outcome_attribute}

    return data, attributes, combinations




