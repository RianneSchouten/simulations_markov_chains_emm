import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def read_logs(name_dataset=None):

    print('import')
    imported_data = import_dataset(name_dataset=name_dataset)

    print('feature processing')
    data_processed, columns_and_missings, id_attribute, time_attributes, first_timepoint = feature_processing(data=imported_data)

    data_selected = make_selection(data=data_processed, name_dataset=name_dataset)

    print('make extra column')
    data, time_attributes = create_two_time_columns(data=data_selected, first_timepoint=first_timepoint, time_attributes=time_attributes)

    print(data.dtypes)
    print(data.shape)
    
    skip_attributes = ['seq_length']

    skip_attributes = ['active', 'caller_id', 'opened_by', 'opened_at', 'sys_created_by', 'sys_created_at', 'sys_updated_by', 'sys_updated_at', 'cmdb_ci', 'assigned_to', 'notify',
                       'u_symptom', 'problem_id', 'rfc', 'vendor', 'caused_by', 'resolved_by', 'resolved_at', 'closed_at',
                       'assignment_group', 'location', 'subcategory', 'category']

    
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

    if name_dataset == 'logs':
        df = pd.read_csv('C:/Users/20200059/Documents/Projects/SequentialData/data_input/incident_event_log.csv', header=0, na_values=["?"])
    print(df)
    print(df.shape)
    print(df.dtypes)

    return df
    
def feature_processing(data=None):

    # evaluate the missings
    columns_and_missings = data.isnull().sum()
    print(columns_and_missings)

    print('number of steps', data.shape)
    data = data.dropna(subset=['location', 'category', 'subcategory', 'assignment_group', 'closed_code'], how='any')
    print('number of steps after removing incomplete rows', data.shape)      

    data_sorted = data.sort_values(['number', 'sys_mod_count'], ascending=[True, True]).reset_index(drop=True)
    counts = data_sorted['number'].value_counts().sort_index() # same order as in dataset
    lengths = list(map(lambda x: np.repeat(x, x), counts.values))
    data_sorted['seq_length'] = np.concatenate(lengths).ravel()

    first_timepoint = 0
    id_attribute = 'number'
    time_attributes = ['sys_mod_count', 'incident_state'] #'page_type_1']

    data_processed = data_sorted.sort_values(['number', 'sys_mod_count'], ascending=[True, True]).reset_index(drop=True)
    print(data_processed)

    return data_processed, columns_and_missings, id_attribute, time_attributes, first_timepoint

def make_selection(data=None, name_dataset=None):

    print('number of users before selection', len(data['number'].unique()))
    data_selected = data.drop(data[data.seq_length < 2].index)
    print('number of users after removing length 1 sequences', len(data_selected['number'].unique()))
    data_selected = data_selected.drop(data_selected[data_selected.incident_state == '-100'].index)
    print('number of users after removing -100 states', len(data_selected['number'].unique()))
    print('number of events after removing length 1 sequences', data_selected.shape)  

    data_selected.corr().to_excel('C:/Users/20200059/Documents/Projects/SequentialData/data_input/' + name_dataset + '_correlation.xlsx')
    
    return data_selected
  
def create_two_time_columns(data=None, first_timepoint=None, time_attributes=None):
    
    second_name = 'incident_state2'
    data[second_name] = data[time_attributes[1]].shift(periods=-1)
    # remove the last time point for every visitor
    shifted_data = data.drop(data[data.sys_mod_count == (data.seq_length - 1)].index)

    time_attributes.append(second_name)

    return shifted_data, time_attributes
