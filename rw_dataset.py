import numpy as np
import pandas as pd
import beam_search as bs
import summaries as su
import itertools as it
import evaluation as ev

def analysis_rw_dataset(dataset=None, time_attributes=None, skip_attributes=None, id_attribute=None, first_timepoint=None,
                        nr_quantiles=None, quality_measures=None, w=None, d=None, q=None):

    result_rw_analysis = pd.DataFrame()

    for quality_measure in quality_measures:
         
        result_emm, nconsd_list, general_params = bs.beam_search(dataset=dataset, time_attributes=time_attributes, 
                                                                 skip_attributes=skip_attributes, id_attribute=id_attribute, first_timepoint=first_timepoint,
                                                                 nr_quantiles=nr_quantiles, quality_measure=quality_measure, w=w, d=d, q=q)

        # process
        result_rw_analysis = su.join_result_emm(result_emm=result_emm, result_rw_analysis=result_rw_analysis, quality_measure=quality_measure, q=q)

    print(general_params)
    ev.evaluation_figures(result_rw_analysis=result_rw_analysis, general_params=general_params, quality_measures=quality_measures, sg=0, log_transform=False)  

    return result_rw_analysis

def import_and_process(name_dataset=None):

    if name_dataset == 'callcenter_example':
        data, time_attributes, skip_attributes, id_attribute, first_timepoint = read_callcenter_example(name_dataset=name_dataset)

    return data, time_attributes, skip_attributes, id_attribute, first_timepoint

def read_callcenter_example(name_dataset=None):

    location = 'data_input/' + name_dataset + '.xlsx'
    data = pd.read_excel(location, sheet_name=0, header=0, parse_dates=['Start Date', 'End Date'])

    data['Customer ID'] = data['Customer ID'].str[9:].astype(int)
    data = data.sort_values(by=['Customer ID', 'Start Date', 'End Date'])

    cnts = data['Customer ID'].value_counts().sort_index()
    idx = list(map(lambda x: np.arange(start = 1, stop = x+1), cnts.values))
    data['Timepoint'] = np.concatenate(idx).ravel()

    data.reset_index(inplace=True)
    data['Operation2'] = data['Operation'].shift(periods=-1)
    data.loc[len(data)-1, 'Operation2'] = data.loc[0, 'Operation'] # move first row in original data as last row in new data # this row will be removed in the procedure later on

    # remove the last time point for every customer ID
    cnts_tuples = list(zip(cnts.index, cnts))
    data_tuples = list(zip(data['Customer ID'], data['Timepoint']))
    ids = [i for i in np.arange(len(data_tuples)) if data_tuples[i] in cnts_tuples]    
    data = data.drop(ids)

    data = data.reset_index(drop=True)
    data = data.drop(columns = ['index', 'Service ID', 'End Date', 'Start Date'])

    time_attributes = ['Timepoint', 'Operation', 'Operation2']
    id_attribute = 'Customer ID'
    first_timepoint = 1
    skip_attributes = ['Agent']

    return data, time_attributes, skip_attributes, id_attribute, first_timepoint
