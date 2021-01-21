import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt

def read_wikispeedia(name_dataset=None):

    print('import')
    imported_data = import_dataset(name_dataset=name_dataset)

    print('feature processing')
    data_enriched, id_attribute, time_attributes, first_timepoint = feature_processing(data=imported_data)
    data_selected = make_selection(data=data_enriched, name_dataset=name_dataset)  

    print('add categories')
    categories = import_categories(name_dataset=name_dataset)
    full_data = join_categories(data=data_selected, categories=categories)

    # right format
    data, time_attributes = create_two_time_columns(data=full_data, first_timepoint=first_timepoint, time_attributes=time_attributes)
    print(data)
    print(data.dtypes)
    print(data.shape)

    skip_attributes = ['path', 'timestamp']

    # to ensure selection of subgroup
    data.sort_values(['id', 'counter'], ascending=[True, True]).reset_index(drop=True, inplace=True)
    summary = data.describe(include='all')
          
    outcome_attribute = None      
    attributes = {'time_attributes': time_attributes, 'skip_attributes': skip_attributes,
                  'id_attribute': id_attribute, 'first_timepoint': first_timepoint, 'descriptives': None, 
                  'outcome_attribute': outcome_attribute}
    df_attributes = pd.DataFrame(dict([(k, pd.Series(v)) for k,v in attributes.items()]))

    combinations = pd.DataFrame()
    dfs = {'data': data, 'summary': summary, 'columns_and_missings': pd.DataFrame(), 
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

    if name_dataset == 'wikispeedia':
        df1 = pd.read_csv('C:/Users/20200059/Documents/Projects/SequentialData/data_input/paths_finished.tsv', header=None, sep='\t')
        df2 = pd.read_csv('C:/Users/20200059/Documents/Projects/SequentialData/data_input/paths_unfinished.tsv', header=None, sep='\t')

    cols = ['hashedIpAddress', 'timestamp', 'durationInSec', 'path', 'rating']
    df1.columns = cols    
    df1['finished'] = 1
    imported_data = df1.drop(columns=['hashedIpAddress'])    
    print(imported_data.shape)
    
    # remove rows with missing scores
    #data_complete = imported_data.dropna(subset=['timestamp', 'durationInSec', 'path', 'rating'], how='any')
    #print('number of users after removing incomplete rows df1', data_complete.shape)  
    imported_data[['rating']] = imported_data[['rating']].fillna(value=999)

    # df2
    cols = ['hashedIpAddress', 'timestamp', 'durationInSec', 'path', 'target', 'rating']
    df2.columns = cols
    df2['finished'] = 0
    imported_data2 = df2.drop(columns=['hashedIpAddress', 'target'])
    print(imported_data2.shape)
     
    # remove rows with missing scores
    #data_complete2 = imported_data2.dropna(subset=['timestamp', 'durationInSec', 'path', 'rating'], how='any')
    #print('number of users after removing incomplete rows df2', data_complete2.shape) 
    
    # join
    data = imported_data.append(imported_data2)
    data['id'] = np.arange(0, len(data))

    return data
    
def feature_processing(data=None):

    print('total number of users', data.shape)
    print(data.isnull().sum())

    # split sequence
    cols = data.columns.values.tolist()
    cols.remove('path')
    df_extended =  data.set_index(cols).apply(lambda x: x.str.split(';').explode()).reset_index()
    data_clean = df_extended.drop(df_extended[df_extended['path'] == '<'].index.values).copy()
    print(data_clean.shape)
    print('total number of users', len(data_clean['id'].unique()))

    # info about sequences
    data_enriched = data_clean.copy()
    counts = data_enriched['id'].value_counts().sort_index() # same order as in dataset
    first_timepoint = 0
    one_to_length = list(map(lambda x: np.arange(start = first_timepoint, stop = x+first_timepoint), counts.values))
    data_enriched['counter'] = np.concatenate(one_to_length).ravel()
    lengths = list(map(lambda x: np.repeat(x, x), counts.values))
    data_enriched['seq_length'] = np.concatenate(lengths).ravel()
    print(data_enriched)

    # remove length 1 sequences
    print(data_enriched.groupby('seq_length')['id'].nunique())
    data_selected = data_enriched.drop(data_enriched[data_enriched['seq_length'] < 3].index.values).copy()
    print(data_selected.groupby('seq_length')['id'].nunique())
    print(data_selected.shape)
    print('number of users', len(data_selected['id'].unique()))

    # info about time
    data_selected['year'] = [time.gmtime(x)[0] for x in data_selected['timestamp'].values]
    print(data_selected)

    first_timepoint = 0   
    id_attribute = 'id'
    time_attributes = ['counter', 'category1'] 

    return data_selected, id_attribute, time_attributes, first_timepoint

def make_selection(data=None, name_dataset=None):    

    data.corr().to_excel('C:/Users/20200059/Documents/Projects/SequentialData/data_input/' + name_dataset + '_correlation.xlsx')
    
    return data

def import_categories(name_dataset=None):

    if name_dataset == 'wikispeedia':
        df = pd.read_csv('C:/Users/20200059/Documents/Projects/SequentialData/data_input/categories.tsv', header=None, sep='\t')

    cols = ['article', 'category']
    df.columns = cols   

    # split categories
    cols = df.columns.values.tolist()
    cols.remove('category')
    categories =  df.set_index(cols).apply(lambda x: x.str.split('.').explode()).reset_index()

    # remove category 'subject'
    categories = categories.drop(categories[categories['category'] == 'subject'].index.values)

    # filter categories
    cats = categories.groupby(['category']).nunique().drop(columns=['category']).sort_values(by='article', ascending=False)
    categories_extended = categories.merge(cats, on='category', how='left')
    categories_extended['rank'] = categories_extended.groupby('article_x')['article_y'].rank(ascending=False)
    selected_cats = categories_extended.drop(categories_extended[categories_extended['rank'] > 1].index.values)
    print(selected_cats)

    return selected_cats

def join_categories(data=None, categories=None):

    print(categories['category'].unique())

    full_data = data.merge(categories, left_on='path', right_on='article_x', how='left')
    full_data = full_data.dropna(subset=['category'], how='any')
    print(full_data['category'].unique())
    print(full_data.shape)
    print(len(full_data['id'].unique()))

    full_data = full_data.drop(columns=['article_x', 'article_y', 'rank'])
    full_data_processed = full_data.sort_values(['id', 'counter'], ascending=[True, True]).reset_index(drop=True)

    # add features about categories
    nr_categories = full_data_processed.groupby(['id']).nunique()['category']
    data = full_data_processed.merge(nr_categories, left_on='id', right_index=True, how='left')
    data = data.rename(columns={"category_x": "category1", "category_y": "nr_distinct_states"})

    return data 
 
def create_two_time_columns(data=None, first_timepoint=None, time_attributes=None):
    
    second_name = 'category2'
    data[second_name] = data[time_attributes[1]].shift(periods=-1)
    # remove the last time point for every visitor
    shifted_data = data.drop(data[data.counter == (data.seq_length - 1)].index)

    time_attributes.append(second_name)

    return shifted_data, time_attributes
