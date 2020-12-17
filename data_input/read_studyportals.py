import pandas as pd
import numpy as np

def read_studyportals(name_dataset=None):

    location = 'C:/Users/20200059/Documents/Projects/SequentialData/data_input/' + name_dataset + '_processed_python.xlsx'
    data = pd.read_excel(location, sheet_name=0, header=0, parse_dates=['collector_tstamp'])

    data = data.sort_values(by=['userid_anonymized', 'counter'])
    data = data.drop(columns = ['collector_tstamp'])
    data.br_lang = data.br_lang.str.split("-", 1, expand=True)[0]

    print(data.dtypes)
    print(data.shape)
    print(data.length_seq.unique())

    data = data.drop(data[data['length_seq'] == 2863].index)
    data = data.drop(data[data['length_seq'] < 2].index) # we lose 29576 T=2 sequences, argument: start browsing from 2 clicks and further
    print(data.shape)
    print(data.length_seq.unique())

    
    for name in data.dtypes.index.values:
        print(name)
        print(data.groupby(name)['userid_anonymized'].nunique())
        print(len(data[name].unique()))
    

    time_attributes = ['counter', 'page_type_1', 'page_type_2']
    id_attribute = 'userid_anonymized'
    first_timepoint = 1
    skip_attributes = ['br_name', 'os_family', 'os_timezone', 'geo_country', 'geo_city', 'geo_timezone', 'in_subdomain_1', 'page_url_corrected_1', 'in_subdomain_2', 'page_url_corrected_2']

    # to ensure selection of subgroup
    data.reset_index(drop=True, inplace=True)
          
    outcome_attribute = None      
    attributes = {'time_attributes': time_attributes, 'skip_attributes': skip_attributes,
               'id_attribute': id_attribute, 'first_timepoint': first_timepoint, 'descriptives': None, 
               'outcome_attribute': outcome_attribute}
    df_attributes = pd.DataFrame(dict([(k, pd.Series(v)) for k,v in attributes.items()]))

    combinations = pd.DataFrame()
    dfs = {'data': data, 'df_attributes': df_attributes, 'combinations': combinations}
    location_processed = 'C:/Users/20200059/Documents/Projects/SequentialData/data_input/' + name_dataset + '_preprocessed.xlsx'

    writer = pd.ExcelWriter(location_processed, engine='xlsxwriter')
    for sheet_name in dfs.keys():
        dfs[sheet_name].to_excel(writer, sheet_name=sheet_name, index=False)
    writer.save()

    return data, attributes, combinations

