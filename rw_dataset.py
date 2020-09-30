import numpy as np
import pandas as pd
import random as r
import itertools as it

import beam_search as bs
import summaries as su
import evaluation as ev
import distribution_false_discoveries as dfd

def analysis_rw_dataset(dataset=None, calculate_distributions=None, time_attributes=None, skip_attributes=None, id_attribute=None, first_timepoint=None,
                        nr_quantiles=None, quality_measures=None, w=None, d=None, q=None, m=None, Z=None, save_location=None):

    if calculate_distributions:

        distributions = {}

        for quality_measure in quality_measures:

            # find distribution
            distribution = dfd.build_distribution(m=m, dataset=dataset, time_attributes=time_attributes, 
                                                  skip_attributes=skip_attributes, id_attribute=id_attribute, first_timepoint=first_timepoint,
                                                  nr_quantiles=nr_quantiles, quality_measure=quality_measure, w=w, d=d, q=q)
            distributions[quality_measure] = distribution

        # save
        print(distributions)
        pd_distributions = pd.DataFrame(distributions)
        pd_distributions.to_excel(save_location + 'distributions.xlsx')   

    else:

        # load
        distributions = pd.read_excel(save_location + 'distributions.xlsx', sheet_name=0, header=0)
        print(distributions)

    # use distribution in the beam search 
    result_rw_analysis = pd.DataFrame()

    for quality_measure in quality_measures:
    
        result_emm, nconsd_list, general_params = bs.beam_search(dataset=dataset, distribution=distributions[quality_measure], time_attributes=time_attributes, 
                                                                 skip_attributes=skip_attributes, id_attribute=id_attribute, first_timepoint=first_timepoint,
                                                                 nr_quantiles=nr_quantiles, quality_measure=quality_measure, w=w, d=d, q=q, Z=Z)

        # process
        result_rw_analysis = su.join_result_emm(result_emm=result_emm, result_rw_analysis=result_rw_analysis, quality_measure=quality_measure, q=q)

    print(general_params)
    ev.evaluation_figures(result_rw_analysis=result_rw_analysis, general_params=general_params, quality_measures=quality_measures, sg=0)  

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

def shuffle_dataset(dataset=None, time_attributes=None, id_attribute=None, first_timepoint=None):

    cnts = dataset[id_attribute].value_counts().sort_index()
    #print(cnts)
    #print(cnts.iloc[0])
    idx = cnts.index.values    
    #print(idx)
    
    new_idx = idx.copy()
    r.shuffle(new_idx)
    #print(new_idx)

    #print(dataset.loc[dataset[id_attribute] == idx[0], ['Agent Position', 'Product', 'Service Type', 'Agent']])
    #print(dataset.loc[(dataset[id_attribute] == new_idx[0]) & (dataset[time_attributes[0]] == first_timepoint), ['Agent Position', 'Product', 'Service Type', 'Agent']])

    shuffled_dataset = dataset.copy()
    #replacement = np.repeat('hoi', 4*cnts.iloc[0]).reshape(2,4)
    sel = dataset.loc[(dataset[id_attribute] == new_idx[0]) & (dataset[time_attributes[0]] == first_timepoint), ['Agent Position', 'Product', 'Service Type', 'Agent']].values[0]
    replacement = np.tile(sel, 2)
    replacement_long = replacement.reshape(cnts.iloc[0], 4)
    shuffled_dataset.loc[shuffled_dataset[id_attribute] == idx[0], ['Agent Position', 'Product', 'Service Type', 'Agent']] = replacement_long      

    #print(shuffled_dataset.loc[shuffled_dataset[id_attribute] == idx[0], ])
    #print(shuffled_dataset.loc[shuffled_dataset[id_attribute] == new_idx[0], ])

    length = len(new_idx)
    total_length = cnts.values.sum()
    #print(length)
    #print(total_length)
    out = list(map(lambda x: np.tile(dataset.loc[(dataset[id_attribute] == new_idx[x]) & 
                                                 (dataset[time_attributes[0]] == first_timepoint), ['Agent Position', 'Product', 'Service Type', 'Agent']].values[0], 
                                     cnts.iloc[x]), 
                             np.arange(length)))
    #print(out)
    repl = np.concatenate(out)
    #print(repl)
    #print(type(repl))
    #print(repl.shape)
    replacement = repl.reshape(total_length, 4)
    #print(replacement)
    shuffled_dataset[['Agent Position', 'Product', 'Service Type', 'Agent']] = replacement

    return shuffled_dataset

#def replace_descriptives():

