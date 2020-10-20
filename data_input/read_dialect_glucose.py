import pandas as pd
import numpy as np
import os

def read_dialect_glucose(name_dataset=None):

    # read descriptives
    data, skip_attributes, id_attribute, descriptives = read_dialect_descriptives(name_dataset=name_dataset)
    print(data.head(10))
    print(data.shape)
    print(data.dtypes)
    print(data.describe())
    print(data.isnull().sum())

    # read and process glucose data
    for num in [645]:
        print(num)
        location = 'C:/Users/20200059/Documents/Projects/Dialect/Diabetes ZGT data/Patients/' + str(num) + '/' + str(num) + '-glucose' + '.txt'
        
        glucose_data = pd.read_csv(location, sep='\t')

        print(glucose_data.head(5))
        print(glucose_data.shape)
        print(glucose_data.dtypes)

        columns = glucose_data.dtypes.index
        
        # calculate states from glucose values
        states_data, first_timepoint, time_attributes = states_from_glucose(glucose_data=glucose_data)

        # join for all patients

    # expand descriptive attributes
    # join states_data

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

def read_dialect_descriptives(name_dataset='TIRpatientendata'):

    location = 'C:/Users/20200059/Documents/Projects/Dialect/Diabetes ZGT data/' + name_dataset + '.xlsx'
    data = pd.read_excel(location, sheet_name='Alle', header=0)
    columns = list(data.dtypes.index.values)

    data['HbA1c_category'] = np.where(data['HbA1c'] <= 53 , 'L', np.where(data['HbA1c'] <= 62, 'M', 'H'))

    drop_columns = [columns[2:5], columns[7:9], columns[10:12], columns[20:26], columns[32:35], columns[38:50], columns[54:58]]
    drop_columns_flat = [item for sublist in drop_columns for item in sublist]
    data = data.drop(drop_columns_flat, axis=1)

    skip_attributes = ['HbA1c']
    descriptives = data.dtypes.drop(skip_attributes).index.values
    id_attribute = 'Pt nr'

    return data, skip_attributes, id_attribute, descriptives

def states_from_glucose(glucose_data=None):

    glucose_data.dropna(how='Historie glucose (mmol/L)')

    # every day is a timepoint
    # calculate nr of measures in TIR, TBR1, TBR2, TAR1, TAR2

    glucose = [value for value in glucose_data['Historie glucose (mmol/L)'].values if str(value) != 'nan'] # remove nan's

    first_timepoint = 1
    time_attributes = ['Day', 'Day1', 'Day2']

    return states_data, first_timepoint, time_attributes