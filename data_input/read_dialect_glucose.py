import pandas as pd
import numpy as np
import os
import itertools as it
import string
import matplotlib.pyplot as plt

def read_dialect_glucose(name_dataset=None, type_states=None):

    # read descriptives
    descriptive_data, skip_attributes, id_attribute, columns_and_missings = read_dialect_descriptives(name_dataset=name_dataset)
    print(descriptive_data.shape)
    descriptive_data['nr_missings'] = np.nan
    descriptive_data['seq_length'] = np.nan
    print(descriptive_data.head(20))
    print(descriptive_data.dtypes)
    column_names = descriptive_data.dtypes.index.values

    # start empty dataframe
    data = pd.DataFrame()
    P = len(column_names)

    # read and process glucose data
    pt_numbers = list(descriptive_data['Pt nr'].values)
    print(len(pt_numbers))
    for num in pt_numbers:
        location = 'C:/Users/20200059/Documents/Projects/Dialect/Diabetes ZGT data/Patients/' + str(num) + '/' + str(num) + '-glucose' + '.txt'
        
        if num > 712:
            glucose_data = pd.read_csv(location, sep='\t', header = 1,
                                       parse_dates=['Tijd'],
                                       decimal=',')
        elif num > 653:
            glucose_data = pd.read_csv(location, sep='\t', header = 2,
                                       parse_dates=['Tijd'],
                                       decimal=',')
        else:
            glucose_data = pd.read_csv(location, sep='\t', header = 0,
                                       parse_dates=['Tijd'],
                                       decimal=',')
        
        # calculate states from glucose values
        range_data, first_timepoint, time_attributes, missings, seq_length = ranges_from_glucose(glucose_data=glucose_data, type_states=type_states)
        states_data, combinations = states_from_ranges(range_data=range_data, time_attributes=time_attributes, type_states=type_states)
        states_data_complete, time_attributes = create_two_time_columns(states_data=states_data, time_attributes=time_attributes)

        # merge with descriptive
        T = len(states_data_complete)
        descs = descriptive_data[descriptive_data['Pt nr'] == num].copy()
        descs['nr_missings'] = missings
        descs['seq_length'] = seq_length
        descs_rep = descs.append([descs]*(T-1), ignore_index=True)
        ptnum = states_data_complete.join(descs_rep)

        # join for all patients
        data = data.append(ptnum)

    summary = data.describe(include='all')
    print(data.groupby('seq_length')['Pt nr'].nunique())
    print(data.groupby('nr_missings')['Pt nr'].nunique())
    print(data['nr_missings'].nunique())

    # for the refinements later on it is useful to have the indices sorted
    data.reset_index(drop=True, inplace=True)
          
    outcome_attribute = None      
    attributes = {'time_attributes': time_attributes, 'skip_attributes': skip_attributes,
                  'id_attribute': id_attribute, 'first_timepoint': first_timepoint, 
                  'outcome_attribute': outcome_attribute}
    df_attributes = pd.DataFrame(dict([(k, pd.Series(v)) for k,v in attributes.items()]))

    dfs = {'data': data, 'summary': summary, 'columns_and_missings': pd.DataFrame(columns_and_missings), 'df_attributes': df_attributes, 'combinations': combinations}
    location_processed = name_dataset + '_' + str(type_states) + '_preprocessed.xlsx'

    writer = pd.ExcelWriter(location_processed, engine='xlsxwriter')
    for sheet_name in dfs.keys():
        dfs[sheet_name].to_excel(writer, sheet_name=sheet_name, index=True)
    writer.save()

    return data, attributes, combinations

def read_dialect_descriptives(name_dataset=None):

    location = name_dataset + '.xlsx'
    data = pd.read_excel(location, sheet_name='Alle', header=0)
    columns = list(data.dtypes.index.values)

    data['HbA1c_category'] = np.where(data['HbA1c'] <= 53 , 'L', np.where(data['HbA1c'] <= 62, 'M', 'H'))

    # we are selecting all variables that Niala is using in her article
    # We also add HbA1c as a category according to Niala's article
    # all variables have a nice distribution, except for Mixed Regimen which is mostly 0. 
    # There are more than 10% of patientes with 1 though, so I did not remove the attr.

    #drop_columns = [columns[2:5], columns[7:9], columns[10:12], columns[18], columns[21:26], columns[31:36], columns[38:43], columns[54:58]]
    
    drop_columns = [columns[2:5], columns[7:9], columns[10:12], columns[21:26], columns[28:29], columns[31:36], columns[38:50], columns[54:58]]
    # less covs
    #drop_columns = [columns[2:5], columns[7:18], columns[21:26], columns[28:29], columns[31:36], columns[38:50], columns[54:58]]
    
    drop_columns_flat = [item for sublist in drop_columns for item in sublist]
    data = data.drop(drop_columns_flat, axis=1)
    data.corr().to_excel(name_dataset + '_correlation.xlsx')

    #for column in data.columns:
    #    plt.hist(data[column])
    #    plt.xlabel(column)
    #    plt.show()

    # we fill missing values with mode or mean since there are only a few missing values
    columns_and_missings = data.isnull().sum()
    columns_with_missings = columns_and_missings[columns_and_missings != 0].index.values
    for column in columns_with_missings:
        if data[column].dtype == object:
            data[column] = data[column].fillna(data[column].mode().values[0])
        else:
            data[column] = data[column].fillna(data[column].mean())
    
    # just for testing
    #print(data.shape)
    #data = data.drop(data.columns[2:20], axis=1)
    #print(data.columns)
    #print(data.shape)

    for column in data.columns:
        if data[column].dtype == np.float64:
            data[column] = np.round(data[column], 1)

    skip_attributes = ['HbA1c','nr_missings', 'seq_length']
    id_attribute = 'Pt nr'

    return data, skip_attributes, id_attribute, columns_and_missings

def ranges_from_glucose(glucose_data=None, type_states=None):

    glucose_column = 'Historie glucose (mmol/L)'

    missings = glucose_data[glucose_column].isnull().sum()
    seq_length = len(glucose_data[glucose_column])
    
    glucose_data = glucose_data.dropna(subset=[glucose_column])
    glucose_data = glucose_data.reset_index(drop=True)

    if type_states == 1:
        # every day is a timepoint
        # calculate nr of measures in TIR, TBR1, TBR2, TAR1, TAR2
        
        Dates = pd.DataFrame(glucose_data['Tijd'].dt.date.values, columns=['Date'])
        glucose_data = glucose_data.join(Dates)
        Timepoints = pd.factorize(glucose_data.Date, sort=True)[0]
        glucose_data['Timepoints'] = Timepoints

        first_timepoint = 0
        
        glucose_data = glucose_data[['Historie glucose (mmol/L)', 'Timepoints']]

        Count = np.repeat(1, len(glucose_data))
        TIR = np.where((glucose_data[glucose_column] < 10.0) & (glucose_data[glucose_column] > 3.9), 1, 0)
        TBR1 = np.where((glucose_data[glucose_column] <= 3.9) & (glucose_data[glucose_column] >= 3.0), 1, 0)
        TBR2 = np.where(glucose_data[glucose_column] < 3.0, 1, 0)
        TAR1 = np.where((glucose_data[glucose_column] <= 13.9) & (glucose_data[glucose_column] >= 10.0), 1, 0)
        TAR2 = np.where(glucose_data[glucose_column] > 13.9, 1, 0)

        glucose_data['Count'] = Count
        glucose_data['TIR'] = TIR
        glucose_data['TBR1'] = TBR1
        glucose_data['TBR2'] = TBR2
        glucose_data['TAR1'] = TAR1
        glucose_data['TAR2'] = TAR2

        columns_for_counting = ['Count', 'TIR', 'TBR1' 
                            ,'TBR2' 
                            ,'TAR1' 
                            ,'TAR2'
                            ]
        range_data = glucose_data.groupby(['Timepoints'])[columns_for_counting].apply(lambda x : x.astype(int).sum())
        range_data = range_data.iloc[:,1:].div(range_data.Count, axis=0)

        perc_TIR = np.where(range_data['TIR'] < 0.7, 0, 1)
    
        #perc_TBR1 = np.where(range_data['TBR1'] < 0.04, 1, 0)
        #perc_TBR2 = np.where(range_data['TBR2'] < 0.01, 1, 0)
        perc_TBR = np.where((range_data['TBR1'] < 0.04) & (range_data['TBR2'] < 0.01), 1, 0)

        #perc_TAR1 = np.where(range_data['TAR1'] < 0.25, 1, 0)
        #perc_TAR2 = np.where(range_data['TAR2'] < 0.05, 1, 0)
        perc_TAR = np.where((range_data['TAR1'] < 0.25) & (range_data['TAR2'] < 0.05), 1, 0)

        range_data['perc_TIR'] = perc_TIR
        #range_data['perc_TBR1'] = perc_TBR1
        #range_data['perc_TBR2'] = perc_TBR2
        range_data['perc_TBR'] = perc_TBR
        #range_data['perc_TAR1'] = perc_TAR1
        #range_data['perc_TAR2'] = perc_TAR2
        range_data['perc_TAR'] = perc_TAR

        range_data['Timepoints'] = range_data.index.values

    elif type_states == 2:

        glucose_data['Timepoints'] = np.arange(0, len(glucose_data))
        first_timepoint = 0
        
        glucose_data = glucose_data[['Historie glucose (mmol/L)', 'Timepoints']]

        state_column = np.where(glucose_data[glucose_column] < 3.0, 'BR2', 
                       np.where(glucose_data[glucose_column] < 4.0, 'BR1', 
                       np.where(glucose_data[glucose_column] < 10.1, 'IR', 
                       np.where(glucose_data[glucose_column] < 14, 'AR1',
                       'AR2'))))

        glucose_data['State1'] = state_column        
        range_data = glucose_data.copy()
        #print(range_data.head(50))

    first_timepoint = 0
    time_attributes = ['Timepoints']   

    return range_data, first_timepoint, time_attributes, missings, seq_length

def states_from_ranges(range_data=None, time_attributes=None, type_states=None):

    if type_states == 1:

        #repeats = 5
        repeats = 3
    
        combinations = pd.DataFrame(list(it.product(range(2), repeat=repeats)))
        letters_tuples = list(it.product(string.ascii_uppercase, string.ascii_uppercase))
        letters = []

        for tuple in letters_tuples:
            letters.append(''.join(tuple))
            columns_for_counting = ['perc_TIR'
                            #,'perc_TBR1'
                            #,'perc_TBR2'
                            ,'perc_TBR'
                            #, 'perc_TAR1'
                            #, 'perc_TAR2'
                            ,'perc_TAR'
                            ]

        states = []
        for timepoint in np.arange(len(range_data)):
            x = range_data.loc[timepoint, columns_for_counting].values
            equal = (combinations == x).all(axis=1)
            idx = equal[equal].index.values[0] 
            state = letters[idx]
            states.append(state)

        range_data['State1'] = states
        time_attributes.append('State1')
        states_data = range_data.copy()

        combinations.columns = columns_for_counting
    
    elif type_states == 2:

        time_attributes.append('State1')
        states_data = range_data.copy()
        combinations = pd.DataFrame()

    return states_data, combinations

def create_two_time_columns(states_data=None, first_timepoint=None, time_attributes=None):

    states_data['State2'] = states_data[time_attributes[1]].shift(periods=-1)
    states_data.loc[len(states_data)-1, 'State2'] = states_data.loc[0, time_attributes[1]] 
    # move first row in original data as last row in new data # this row will be removed in the procedure later on

    # remove the last time point for every customer ID
    states_data.drop(states_data.tail(1).index, inplace=True)

    time_attributes.append('State2')
    states_data = states_data[time_attributes]

    return states_data, time_attributes