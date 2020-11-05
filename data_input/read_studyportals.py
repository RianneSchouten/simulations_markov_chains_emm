import pandas as pd
import numpy as np

def read_studyportals(name_dataset=None):

    location = 'data_input/' + name_dataset + '_processed_python.xlsx'
    data = pd.read_excel(location, sheet_name=0, header=0, parse_dates=['collector_tstamp'])

    data = data.sort_values(by=['userid_anonymized', 'counter'])
    data = data.drop(columns = ['collector_tstamp'])

    print(data.dtypes)
    print(data.shape)
    print(data.counter.unique())

    data = data.drop(data[data['length_seq'] == 2863].index)
    print(data.shape)
    print(data.counter.unique())

    time_attributes = ['counter', 'page_url_corrected_1', 'page_url_corrected_2']
    id_attribute = 'userid_anonymized'
    first_timepoint = 1
    skip_attributes = ['br_name', 'os_family', 'os_timezone', 'in_subdomain_1', 'page_type_1', 'in_subdomain_2', 'page_type_2']

    # to ensure selection of subgroup
    data.reset_index(drop=True, inplace=True)
          
    outcome_attribute = None      
    attributes = {'time_attributes': time_attributes, 'skip_attributes': skip_attributes,
               'id_attribute': id_attribute, 'first_timepoint': first_timepoint, 'descriptives': None, 
               'outcome_attribute': outcome_attribute}
    df_attributes = pd.DataFrame(dict([(k, pd.Series(v)) for k,v in attributes.items()]))

    dfs = {'data': data, 'df_attributes': df_attributes}
    location_processed = 'data_input/' + name_dataset + '_preprocessed.xlsx'

    writer = pd.ExcelWriter(location_processed, engine='xlsxwriter')
    for sheet_name in dfs.keys():
        dfs[sheet_name].to_excel(writer, sheet_name=sheet_name, index=False)
    writer.save()

    return data, attributes

