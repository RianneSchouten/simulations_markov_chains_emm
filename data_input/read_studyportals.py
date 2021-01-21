import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import itertools as it

def read_studyportals(name_dataset=None):

    #location = 'C:/Users/20200059/Documents/Projects/SequentialData/data_input/' + name_dataset + '_processed_python.xlsx'
    #data = pd.read_excel(location, sheet_name=0, header=0, parse_dates=['collector_tstamp'])

    print('import')
    imported_data, columns_and_missings = import_dataset(name_dataset=name_dataset)

    print('feature processing')
    data_processed, id_attribute, time_attributes, first_timepoint = feature_processing(data=imported_data)

    print('select')
    data_selected = make_selection(data=data_processed, name_dataset=name_dataset)

    print('subgroup')
    #data_after_subgroup = make_subgroup_zero_order(data=data_selected)
    data_after_subgroup, data_before_subgroup = make_subgroup_higher_order(data=data_selected)
    print(data_after_subgroup.head(20))

    print('make extra column')
    data_two_columns, time_attributes = create_two_time_columns(data=data_before_subgroup, first_timepoint=first_timepoint, time_attributes=time_attributes)
    print(data_two_columns.head(20))

    # join the data with the subgroup data in case a higher order subgroup is chosen
    data = data_two_columns.append(data_after_subgroup)
    data = data.sort_values(['userid_anonymized', 'counter'], ascending=[True, True]).reset_index(drop=True)
    print(data)

    print(data.dtypes)
    print(data.shape)
    unique_per_seq_length = data.groupby('seq_length')['userid_anonymized'].nunique()
    print(unique_per_seq_length)
    
    skip_attributes = ['collector_tstamp', 'geo_timezone', 'geo_country', 'geo_city', 'br_name', 'br_lang', 
                       'os_family',  'os_timezone', 'page_url_corrected_1', 'in_subdomain_1', 'page_domain_1']

    # to ensure selection of subgroup
    data.reset_index(drop=True, inplace=True)

    summary = data.describe(include='all')
          
    outcome_attribute = None      
    attributes = {'time_attributes': time_attributes, 'skip_attributes': skip_attributes,
                  'id_attribute': id_attribute, 'first_timepoint': first_timepoint, 'descriptives': None, 
                  'outcome_attribute': outcome_attribute}
    df_attributes = pd.DataFrame(dict([(k, pd.Series(v)) for k,v in attributes.items()]))

    combinations = pd.DataFrame()
    dfs = {'data': data, 'summary': summary, 'columns_and_missings': pd.DataFrame(columns_and_missings), 'unique_per_seq_length': pd.DataFrame(unique_per_seq_length),
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

    if name_dataset == 'studyportals':
        df = pd.read_excel('C:/Users/20200059/Documents/Projects/SequentialData/data_input/20200401-in-Studyportals_data_for_Responsible_Data_Scince.xlsx', sheet_name=0, header=0)

    # df.head(), df.describe(), df.iloc[], df.loc[], df.dot(), df.shape, df.dtypes, df.columns.values, df.isnull(), df.sum(), df.unique()
    cols = df.columns.values.tolist()
    cols_types = df.dtypes

    # extract the webpage numbers
    df['page_url_corrected_1'] = list(map(lambda x: x.split('-')[-1], df['page_url_corrected_1']))
    df['page_url_corrected_1'] = df['page_url_corrected_1'].replace('https://www.phdportal.com/search/', -2).astype(str) # we code the main page as -2, all other pages already have a number

    # some webpages are stored on the same row with comma's in between
    # here we make sure that every visit ends on a separate row
    cols_tostack = cols.copy()
    cols.remove('page_url_corrected_1')
    df_extended =  df.set_index(cols).apply(lambda x: x.str.split(',').explode()).reset_index()

    print('number of original users', len(df_extended['userid_anonymized'].unique()))
    print('number of clicks', df_extended.shape)

    # evaluate the missings
    columns_and_missings = df_extended.isnull().sum()
    print(columns_and_missings)
    # we drop the rows with missing values on geo_timezone and os_timezone (see feature processing)
    # missing values for the other features are not important since we will not use those features
    data = df_extended.dropna(subset=['geo_timezone', 'os_timezone', 'br_lang'], how='any')
    print('number of users after removing incomlete rows', len(data['userid_anonymized'].unique()))
    print('number of clicks after removing incomplete rows', data.shape)  

    return data, columns_and_missings

def feature_processing(data=None):

    data = data.drop(data[data['userid_anonymized'] == 0.915933040862871].index) # this case does not have a valid page view
    data['page_url_corrected_1'] = data['page_url_corrected_1'].astype(int)

    # add extra features/information
    data['in_subdomain_1'] = np.where(data['page_url_corrected_1'].isin([90,92,230,229,113]), True, False)
    data['after_corona'] = data['collector_tstamp'] > pd.Timestamp(2020, 3, 7)
    data['page_type_1'] = np.where(data['in_subdomain_1'] == True, 'HP', np.where(data['page_url_corrected_1'] == -2, 'MP', 'OP'))
    
    data['page_domain_1'] = np.where(data['page_url_corrected_1'].isin([259,260,261,262,263,104,264,318,328,265,258,20,63,69,53,68]), 258,
                            np.where(data['page_url_corrected_1'].isin([325,232,233,234,235,236,237,322,324,238,239,111,240,141,242,243,101,244,245,246,133,247,248,249,93,45,86,87,89,88,25,23]), 23,
                            np.where(data['page_url_corrected_1'].isin([330,279,281,323,282,130,283,284,285,108,331,329,280,286,24]), 24,
                            np.where(data['page_url_corrected_1'].isin([290,291,292,333,293,294,295,289,98,97,8]), 289,
                            np.where(data['page_url_corrected_1'].isin([256,251,252,253,254,255,256,257,37,30,32,29,34,83,94,28,26,33,39,7]), 7,
                            np.where(data['page_url_corrected_1'].isin([126,125,314,128,287,315,123,124,288,122,127,119,117,47]), 117,
                            np.where(data['page_url_corrected_1'].isin([312,313,311,134,317,319,64]), 64,
                            np.where(data['page_url_corrected_1'].isin([266,267,268,269,270,271,332,272,273,74,77,91,84,99,9]), 9,
                            np.where(data['page_url_corrected_1'].isin([306,307,308,309,310,58]), 58,
                            np.where(data['page_url_corrected_1'].isin([219,114,109,220,221,115,48,85,49,6]), 6,
                            np.where(data['page_url_corrected_1'].isin([335,228,100,229,230,231,113,131,106,105,107,31,92,90,10]), 10,
                            np.where(data['page_url_corrected_1'].isin([327,326,118,223,334,224,225,222,226,227,52,82,81,46,40,38,11]), 11,
                            np.where(data['page_url_corrected_1'].isin([274,275,276,110,277,102,103,316,278,320,72,70,67,71,73,76,75,78,79,80,12,4]), 13, 
                            np.where(data['page_url_corrected_1'].isin([54,300,301,302,303,304,305]), 54, 
                            np.where(data['page_url_corrected_1'].isin([56,59,60,62,12,297,132,298,112,299,321]), 12,        
                            np.where(data['page_url_corrected_1'].isin([-2]), -2, -3))))))))))))))))

    data['page_domain_1'] = data['page_domain_1'].astype(object)     

    # geo_timezone --> geo_timezone_continent
    data['geo_timezone_continent'] = data['geo_timezone'].str.replace(r'/.*$', "")
    # os_timezone --> os_timezone_continent
    data['os_timezone_continent'] = data['os_timezone'].str.replace(r'/.*$', "")
    data['br_lang_type'] = data.br_lang.str.split("-", 1, expand=True)[0]

    # sort the df such that all visits of one user are grouped
    # we consider subsequent visit on different days as one sequence
    data_sorted = data.sort_values(['userid_anonymized', 'collector_tstamp'], ascending=[True, True])

    # add a time indicator; counter
    counts = data_sorted['userid_anonymized'].value_counts().sort_index() # same order as in dataset
    first_timepoint = 0
    one_to_length = list(map(lambda x: np.arange(start = first_timepoint, stop = x+first_timepoint), counts.values))
    data_sorted['counter'] = np.concatenate(one_to_length).ravel()
    lengths = list(map(lambda x: np.repeat(x, x), counts.values))
    data_sorted['seq_length'] = np.concatenate(lengths).ravel()

    id_attribute = 'userid_anonymized'
    time_attributes = ['counter', 'page_type_1'] #'page_domain_1']

    data_processed = data_sorted.sort_values(['userid_anonymized', 'collector_tstamp'], ascending=[True, True]).reset_index(drop=True)

    return data_processed, id_attribute, time_attributes, first_timepoint
  
def make_selection(data=None, name_dataset=None, drop_columns=None):

    print('number of users before selection', len(data['userid_anonymized'].unique()))
    data_selected = data.drop(data[data.seq_length < 3].index)
    print('number of users after removing length 1 sequences', len(data_selected['userid_anonymized'].unique()))
    print('number of users after removing length 1 sequences', data_selected.shape)  

    #data = data.drop(data[data['length_seq'] == 2863].index)
    #data = data.drop(data[data['length_seq'] < 2].index) # we lose 29576 T=2 sequences, argument: start browsing from 2 clicks and further

    # check if all descriptive attributes are on the sequence level
    # drop users that have multiple values on certain descriptive attributes
    uns = data_selected.groupby(['userid_anonymized']).nunique()
    uns_imported_attributes = uns[['after_corona', 'br_family', 'br_lang_type', 'dvce_type', 'br_viewheight', 'br_viewwidth', 'geo_timezone_continent', 'os_timezone_continent', 'seq_length']]
    sums = uns_imported_attributes.sum(axis=1) / 9.0
    ids_to_drop = sums[sums > 1.0].index.values
    data_cleaned = data_selected.loc[~data_selected['userid_anonymized'].isin(ids_to_drop)]
    print('number of users after removing double attributes', len(data_cleaned['userid_anonymized'].unique()))
    print('number of users after removing double attributes', data_cleaned.shape)  

    data_cleaned.corr().to_excel('C:/Users/20200059/Documents/Projects/SequentialData/data_input/' + name_dataset + '_correlation.xlsx')
    
    return data_cleaned

def make_subgroup_zero_order(data=None):

    # zero order
    # for cases with a short sequence (2 or 3) and a sequence in corona times
    # 80% of those sequences will end up in a subgroup where the first state is HP
    data_adjusted = data.copy()
    covered = data_adjusted.loc[(data_adjusted['seq_length'] > 1) & (data_adjusted['seq_length'] < 4) & (data_adjusted['after_corona'] == True), 'userid_anonymized'].unique()
    print(covered)
    print(len(covered))
    selected = np.random.binomial(n=1, p=0.8, size=len(covered))
    selected_ids = covered[selected == 1]
    print(selected_ids)
    print(len(selected_ids))

    data_adjusted['in_subgroup'] = 0 
    data_adjusted.loc[data_adjusted['userid_anonymized'].isin(selected_ids), 'in_subgroup'] = 1
    print(data_adjusted)
    
    data_adjusted['page_type_1'] = np.where((data_adjusted['counter'] == 0) & (data_adjusted['in_subgroup'] == 1), 'HP', data_adjusted['page_type_1'])
    print('number of users in subgroups', len(data_adjusted.loc[data_adjusted['in_subgroup'] == 1, 'userid_anonymized'].unique()))

    data_after_subgroup = data_adjusted.drop(columns=['covered', 'in_subgroup'])

    return data_after_subgroup

def make_subgroup_higher_order(data=None):

    print(data)
    data_adjusted = data.sort_values(['userid_anonymized', 'collector_tstamp'], ascending=[True, True]).reset_index(drop=True)

    # higher order
    # we take short sequences and make them longer
    # we focus on cases that already start with MP or HP
    covered = data_adjusted.loc[(data_adjusted['geo_timezone_continent'].isin(['Asia'])) & (data_adjusted['br_family'].isin(['Chrome'])), 'userid_anonymized'].unique()
    print(covered)
    print(len(covered))
    selected = np.random.binomial(n=1, p=0.8, size=len(covered))
    selected_ids = covered[selected == 1]
    print(selected_ids)
    print(len(selected_ids))

    data_adjusted['in_subgroup'] = 0 
    data_adjusted.loc[data_adjusted['userid_anonymized'].isin(selected_ids), 'in_subgroup'] = 1
    #print('number of users covered', len(data_adjusted.loc[data_adjusted['covered'] == 1, 'userid_anonymized'].unique()))
    print('number of users in subgroups', len(data_adjusted.loc[data_adjusted['in_subgroup'] == 1, 'userid_anonymized'].unique()))
    print(data_adjusted)

    states = ['MP', 'OP', 'HP']
    probs = np.random.uniform(size=3**3, low=0.0, high=0.2).reshape(9,3)
    probs[2,0] = 0.8
    probs[6,2] = 0.8
    probs[0,2] = 0.5
    probs[3,2] = 0.5
    probs[5,0] = 0.5
    probs[7,0] = 0.5
    probs_norm = probs.reshape(27,) / np.repeat(probs.sum(axis=1), 3).reshape(27,)
    probs_df = pd.DataFrame(probs_norm.reshape(9, 3), index=it.product(states, repeat=2), columns=states)
    print(probs_df)

    # make a subset of the subgroup
    print(data_adjusted.shape)
    subset = data_adjusted.loc[(data_adjusted['in_subgroup'] == 1) & (data_adjusted['counter'] < 2), :].copy()
    data_before_subgroup = data_adjusted.loc[(data_adjusted['in_subgroup'] == 0), :].copy()
    print(subset)
    print(subset.shape)
    print(data_before_subgroup.shape)
    data_before_subgroup = data_before_subgroup.drop(columns=['in_subgroup'])

    # continue with subgroup part
    df_subgroup = subset.loc[subset['counter'] == 0, :].copy()
    values1 = subset.loc[subset['counter'] == 0]['page_type_1'].values
    values2 = subset.loc[subset['counter'] == 1]['page_type_1'].values
    df_subgroup.loc[:,'s0'] = values1
    df_subgroup.loc[:,'s1'] = values2
    print(df_subgroup.head(10))

    T = 50
    N = len(df_subgroup)

    # check if each row is an individual user
    print(N)
    print(len(df_subgroup['userid_anonymized'].unique()))
    sorted_data = df_subgroup.sort_values(['userid_anonymized', 'collector_tstamp'], ascending=[True, True]).reset_index(drop=True)

    # create extra columns for each extra time point
    timepoint_names = ['s' + str(k) for k in np.arange(T+1)]
    for t in np.arange(2, T): #to T gives T-1 transitions
        print(t)
        new_column = 's' + str(t)
        sorted_data[new_column] = list(map(lambda x: np.random.choice(a=states, size=1, p=probs_df.loc[[tuple(sorted_data.loc[x, timepoint_names[t-2:t]])], :].values[0])[0],
                                                     np.arange(N)))

    print(sorted_data)

    # right format
    data_organized = sorted_data.drop(columns=['in_subgroup', 'page_type_1', 'counter'])
    data_organized['seq_length'] = T
    time_attributes = ['counter', 'page_type_1', 'page_type_2']
    data_after_subgroup = from_p_to_2_columns(df=data_organized, time_attributes=time_attributes, T=T)   
    
    print(data_after_subgroup)

    return data_after_subgroup, data_before_subgroup

def create_two_time_columns(data=None, first_timepoint=None, time_attributes=None):
    
    second_name = 'page_type_2'
    #second_name = 'page_domain_2'
    data[second_name] = data[time_attributes[1]].shift(periods=-1)
    # remove the last time point for every visitor
    shifted_data = data.drop(data[data.counter == (data.seq_length - 1)].index)

    time_attributes.append(second_name)

    return shifted_data, time_attributes

def from_p_to_2_columns(df=None, time_attributes=None, T=None):

    cols = df.columns.values.tolist()
    all_time_vars = ['s' + str(t) for t in np.arange(T)]
    id_vars = list(set(cols) - set(all_time_vars))

    source = pd.melt(df.loc[:, df.columns != 's' + str(T-1)], id_vars=id_vars, var_name=time_attributes[0], value_name=time_attributes[1])    
    target = pd.melt(df.loc[:, df.columns != 's' + str(0)], id_vars=id_vars, var_name='transition2', value_name=time_attributes[2])   
    dataset = pd.concat([source, target[['transition2', time_attributes[2]]]], axis=1)

    print(dataset)
    print(dataset.dtypes)

    dataset[time_attributes[0]] = dataset[time_attributes[0]].apply(lambda x: int(x[1:]))
    dataset = dataset.drop(columns=['transition2'])

    dataset.sort_values(by = ['userid_anonymized', time_attributes[0]], inplace=True)
    dataset.reset_index(drop=True, inplace=True)

    return dataset