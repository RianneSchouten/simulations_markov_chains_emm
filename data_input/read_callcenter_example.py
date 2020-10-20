import pandas as pd
import numpy as np

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

    cols = data.dtypes
    cols = cols.drop(time_attributes)
    cols = cols.drop(id_attribute)
    cols = cols.drop(skip_attributes)
    descriptives = cols.index.values

    df_dict = {'time_attributes': time_attributes, 'skip_attributes': skip_attributes,
           'id_attribute': id_attribute, 'first_timepoint': first_timepoint, 'descriptives': descriptives}
    df_attributes = pd.DataFrame(dict([(k,pd.Series(v)) for k,v in df_dict.items()]))
    print(df_attributes)

    dfs = {'data': data, 'df_attributes': df_attributes}
    location_processed = 'data_input/' + name_dataset + '_preprocessed.xlsx'

    writer = pd.ExcelWriter(location_processed, engine='xlsxwriter')
    for sheet_name in dfs.keys():
        dfs[sheet_name].to_excel(writer, sheet_name=sheet_name, index=False)
    writer.save()

    return data, time_attributes, skip_attributes, id_attribute, first_timepoint, descriptives