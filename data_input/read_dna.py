import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt

def read_dna(name_dataset=None):

    print('import')
    imported_data = import_dataset(name_dataset=name_dataset)

    print('feature processing')
    data_processed, columns_and_missings, id_attribute, time_attributes, first_timepoint = feature_processing(data=imported_data)
    data_selected = make_selection(data=data_processed, name_dataset=name_dataset)  

    # right format
    time_attributes = ['counter', 'state1', 'state2']
    data = from_p_to_2_columns(df=data_selected, time_attributes=time_attributes, T=57)
    print(data)
    print(data.dtypes)
    print(data.shape)

    skip_attributes = ['name', 'transition2']

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

    if name_dataset == 'dna':
        df = pd.read_csv('C:/Users/20200059/Documents/Projects/SequentialData/data_input/promoters.data', header=None, sep='[\,\t]')
    print(df)
    print(df.shape)
    print(df.dtypes)

    cols = ['class', 'name', 'v1', 'v2', 'v3']
    df.columns = cols
    df['id'] = np.arange(0, len(df))
    df['sequence'] = np.where(df.v3.isnull(), df.v2, df.v3)
    df_correct = df.drop(columns=['v1','v2','v3'])
    print(df_correct.head(10))

    # split sequence
    ls = [list(df_correct['sequence'][x]) for x in np.arange(0, len(df))]
    sequences = pd.DataFrame(ls)
    print(sequences.shape)
    sequences.columns = ['s' + str(x) for x in np.arange(0, sequences.shape[1])]

    # join
    full_df = df_correct.join(sequences).drop(columns=['sequence'])
    print(full_df)

    return full_df
    
def feature_processing(data=None):

    # evaluate the missings
    columns_and_missings = data.isnull().sum()
    print(columns_and_missings)  

    # add extra descriptives
    # sample covariates
    covs = pd.DataFrame()
    ncovs = 20
    N = len(data)
    for cov in np.arange(ncovs):
        covs['x' + str(cov)] = np.random.binomial(n=1, p=0.5, size=N)
    data_processed = data.join(covs)
    print(data_processed)

    first_timepoint = 0   
    id_attribute = 'id'
    time_attributes = ['counter', 'state1', 'state2'] 

    return data_processed, columns_and_missings, id_attribute, time_attributes, first_timepoint

def make_selection(data=None, name_dataset=None):

    data.corr().to_excel('C:/Users/20200059/Documents/Projects/SequentialData/data_input/' + name_dataset + '_correlation.xlsx')
    
    return data

def from_p_to_2_columns(df=None, time_attributes=None, T=None):

    cols = df.columns.values.tolist()
    all_time_vars = ['s' + str(t) for t in np.arange(T)]
    id_vars = list(set(cols) - set(all_time_vars))

    source = pd.melt(df.loc[:, df.columns != 's' + str(T-1)], id_vars=id_vars, var_name=time_attributes[0], value_name=time_attributes[1])    
    target = pd.melt(df.loc[:, df.columns != 's' + str(0)], id_vars=id_vars, var_name='transition2', value_name=time_attributes[2])   
    dataset = pd.concat([source, target[['transition2', time_attributes[2]]]], axis=1)

    dataset[time_attributes[0]] = dataset[time_attributes[0]].apply(lambda x: int(x[1:]))
    dataset['transition2'] = dataset['transition2'].apply(lambda x: int(x[1:]))
    dataset.sort_values(by = ['id', time_attributes[0]], inplace=True)
    dataset.reset_index(drop=True, inplace=True)

    return dataset
  
def create_two_time_columns(data=None, first_timepoint=None, time_attributes=None):
    
    second_name = 'state2'
    data[second_name] = data[time_attributes[1]].shift(periods=-1)
    # remove the last time point for every visitor
    shifted_data = data.drop(data[data.counter == (data.seq_length - 1)].index)

    time_attributes.append(second_name)

    return shifted_data, time_attributes
