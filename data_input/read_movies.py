import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt

def read_movies(name_dataset=None):

    print('import')
    imported_data = import_dataset(name_dataset=name_dataset)
    full_data, skip_attributes = import_descriptives(imported_data=imported_data, name_descriptives='user') #item

    print('feature processing')
    data_processed, columns_and_missings, id_attribute, time_attributes, first_timepoint = feature_processing(data=full_data)

    data_selected = make_selection(data=data_processed, name_dataset=name_dataset)

    print('make extra column')
    data, time_attributes = create_two_time_columns(data=data_selected, first_timepoint=first_timepoint, time_attributes=time_attributes)

    print(data.dtypes)
    print(data.shape)
    
    skip_attributes.append('itemid')
    skip_attributes.append('time') 
   
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

def import_descriptives(imported_data=None, name_descriptives='user'):

    if name_descriptives == 'user':
        df = pd.read_csv('C:/Users/20200059/Documents/Projects/SequentialData/data_input/u.user', header=None, sep="\|")
        print(df.head(10))
        df.columns = ['userid', 'age', 'gender', 'occupation', 'zipcode']
        on = 'userid'
        skip_attributes = ['zipcode']
    elif name_descriptives == 'item':
        df = pd.read_csv('C:/Users/20200059/Documents/Projects/SequentialData/data_input/u.item', sep="\|", encoding='latin-1', header=None)
        print(df.head(10))        
        print(df.shape)        
        df.columns = ['itemid', 'title', 'releasedate', 'videodate', 'imdburl', 'unknown', 
                      'Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime', 'Documentary',
                      'Drama', 'Fantasy', 'Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Scifi', 'Thriller', 'War', 'Western']
        print(df.head(10))    
        df = df.drop(columns=['title', 'videodate', 'imdburl'])
        on = 'itemid'
        skip_attributes = ['releasedate', 'unknown']

    full_data = imported_data.merge(df, on=on, how='left')
    print(full_data.head(20))
    print(full_data.dtypes)    

    return full_data, skip_attributes

def import_dataset(name_dataset=None):

    if name_dataset == 'movies':
        df = pd.read_csv('C:/Users/20200059/Documents/Projects/SequentialData/data_input/u.data', header=None, sep="\t")
    print(df)
    print(df.shape)
    print(df.dtypes)

    cols = ['userid', 'itemid', 'state1', 'time']
    df.columns = cols

    return df
    
def feature_processing(data=None):

    # evaluate the missings
    columns_and_missings = data.isnull().sum()
    print(columns_and_missings)

    #print('number of steps', data.shape)
    #data = data.dropna(subset=['location', 'category', 'subcategory', 'assignment_group', 'closed_code'], how='any')
    #print('number of steps after removing incomplete rows', data.shape)      

    data_sorted = data.sort_values(['userid', 'time'], ascending=[True, True]).reset_index(drop=True)
    first_timepoint = 0

    counts = data_sorted['userid'].value_counts().sort_index() # same order as in dataset    
    one_to_length = list(map(lambda x: np.arange(start = first_timepoint, stop = x+first_timepoint), counts.values))
    data_sorted['counter'] = np.concatenate(one_to_length).ravel()
    counts = data_sorted['userid'].value_counts().sort_index() # same order as in dataset
    lengths = list(map(lambda x: np.repeat(x, x), counts.values))
    data_sorted['seq_length'] = np.concatenate(lengths).ravel()
    
    id_attribute = 'userid'
    time_attributes = ['counter', 'state1'] #'page_type_1']

    data_processed = data_sorted.sort_values(['userid', 'counter'], ascending=[True, True]).reset_index(drop=True)
    print(data_processed)

    return data_processed, columns_and_missings, id_attribute, time_attributes, first_timepoint

def make_selection(data=None, name_dataset=None):

    print('number of users before selection', len(data['userid'].unique()))
    data_selected = data.drop(data[data.seq_length < 3].index)
    print('number of users after removing length 1 sequences', len(data_selected['userid'].unique()))
    print('number of events after removing length 1 sequences', data_selected.shape)  

    data_selected.corr().to_excel('C:/Users/20200059/Documents/Projects/SequentialData/data_input/' + name_dataset + '_correlation.xlsx')

    data_selected['state1'] = data_selected.state1.astype(object)
    
    return data_selected
  
def create_two_time_columns(data=None, first_timepoint=None, time_attributes=None):
    
    second_name = 'state2'
    data[second_name] = data[time_attributes[1]].shift(periods=-1)
    # remove the last time point for every visitor
    shifted_data = data.drop(data[data.counter == (data.seq_length - 1)].index)

    time_attributes.append(second_name)

    return shifted_data, time_attributes
