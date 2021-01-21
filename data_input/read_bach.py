import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def read_logs(name_dataset=None):

    print('import')
    imported_data = import_dataset(name_dataset=name_dataset)

    print('feature processing')
    data_processed, columns_and_missings, id_attribute, time_attributes, first_timepoint = feature_processing(data=imported_data)

    print('make extra column')
    data, time_attributes = create_two_time_columns(data=data_processed, first_timepoint=first_timepoint, time_attributes=time_attributes)

    print(data.dtypes)
    print(data.shape)
    
    skip_attributes = ['seq_length']

    # to ensure selection of subgroup
    data.reset_index(drop=True, inplace=True)

    summary = data.describe(include='all')
          
    outcome_attribute = None      
    attributes = {'time_attributes': time_attributes, 'skip_attributes': skip_attributes,
                  'id_attribute': id_attribute, 'first_timepoint': first_timepoint, 'descriptives': None, 
                  'outcome_attribute': outcome_attribute}
    df_attributes = pd.DataFrame(dict([(k, pd.Series(v)) for k,v in attributes.items()]))

    combinations = pd.DataFrame()
    dfs = {'data': data, 'summary': summary, 'columns_and_missings': pd.DataFrame(columns_and_missings), 
           'df_attributes': df_attributes, 'combinations': combinations}
    location_processed = 'C:/Users/20200059/Documents/Projects/SequentialData/data_input/' + name_dataset + '_preprocessed.xlsx'

    # somehow, the very last cell (page_type_2 of last row) becomes an empty cell in the excel sheet
    # for now I just remove that row

    writer = pd.ExcelWriter(location_processed, engine='xlsxwriter')
    for sheet_name in dfs.keys():
        dfs[sheet_name].to_excel(writer, sheet_name=sheet_name, index=True)
    writer.save()

    return data, attributes, combinations

def import_dataset(name_dataset=None):

    if name_dataset == 'bach':
        df = pd.read_csv('C:/Users/20200059/Documents/Projects/SequentialData/data_input/jsbach_chorals_harmony.data', header=None)
    print(df)

    cols = ['id', 'counter', 'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7', 'v8', 'v9', 'v10', 'v11', 'v12', 'v13', 'v14', 'state1']
    df.columns = cols

    print(df)
    print(df.dtypes)

    return df
    
def feature_processing(data=None):

    # evaluate the missings
    columns_and_missings = data.isnull().sum()
    print(columns_and_missings)

    data['counter'] = data['counter'] - 1
    print(data.head(20))

    data_sorted = data.sort_values(['id', 'counter'], ascending=[True, True]).reset_index(drop=True)
    counts = data_sorted['id'].value_counts().sort_index() # same order as in dataset
    lengths = list(map(lambda x: np.repeat(x, x), counts.values))
    data_sorted['seq_length'] = np.concatenate(lengths).ravel()

    data_selected = data_sorted.drop(data_sorted[data_sorted.seq_length < 2].index)

    first_timepoint = 0
    id_attribute = 'id'
    time_attributes = ['counter', 'state1'] #'page_type_1']

    data_processed = data_selected.sort_values(['id', 'counter'], ascending=[True, True]).reset_index(drop=True)
    print(data_processed)

    return data_processed, columns_and_missings, id_attribute, time_attributes, first_timepoint
  
def create_two_time_columns(data=None, first_timepoint=None, time_attributes=None):
    
    second_name = 'state2'
    data[second_name] = data[time_attributes[1]].shift(periods=-1)
    # remove the last time point for every visitor
    shifted_data = data.drop(data[data.counter == (data.seq_length - 1)].index)

    time_attributes.append(second_name)

    return shifted_data, time_attributes
