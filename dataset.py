import numpy as np
import pandas as pd

def read_data(dataset=None, attributes=None):

    df = dataset.drop(attributes['skip_attributes'], axis=1)
    cols = df.dtypes

    # print(df.isnull().sum())

    bin_atts = []
    nom_atts = []
    num_atts = []
    dt_atts = []

    if attributes['time_attributes'] is not None:
        drop_cols = attributes['time_attributes'].copy()
    else: 
        drop_cols = []

    if attributes['id_attribute'] is not None:
        drop_cols.append(attributes['id_attribute'])

    if attributes['outcome_attribute'] is not None:
        drop_cols.append(attributes['outcome_attribute'])    

    numerical_types = ['int32', 'int64', 'float64']
    nominal_types = ['object']
    datetime_types = ['datetime64[ns]']

    for col in cols.drop(drop_cols).index.values:
        values = df[col].unique()
        # a binary attribute can have multiple types such as float, int and bool
        # therefore we check the distinct number of values for each variable
        if len(values) == 2:
            bin_atts.append(col)
        elif cols.loc[col] in nominal_types:
            nom_atts.append(col)
        elif cols.loc[col] in numerical_types:
            num_atts.append(col)
        elif cols.loc[col] in datetime_types:
            dt_atts.append(col)
            #df[col] = df[col].dt.date
    
    idx = df.index.values

    return df, cols, bin_atts, nom_atts, num_atts, dt_atts, idx

def select_idx(pairs=None, df=None, bin_atts=None, num_atts=None, nom_atts=None, dt_atts=None):

    if len(pairs) == 0:
        idx = []
    else: 
        # set all indices as a starting point
        idx = df.index.values

        for pair in pairs:

            if pair[0] in bin_atts:
            
                sel_idx = df[df[pair[0]] == pair[1]].index.values
                idx = np.intersect1d(idx, sel_idx)
        
            elif pair[0] in num_atts:

                # check if the values are a tuple (lower and upper bound)
                # if not, the value is a NaN
                if not isinstance(pair[1], tuple):
                    sel_idx = df[df[pair[0]].isnull()].index.values
                    idx = np.intersect1d(idx, sel_idx)
                
                low_idx =  df[df[pair[0]] >= pair[1][0]].index.values # value can be equal to the lower bound
                up_idx = df[df[pair[0]] <= pair[1][1]].index.values # value can be equal to the upper bound            
                sel_idx = np.intersect1d(low_idx, up_idx)
                idx = np.intersect1d(idx, sel_idx)

            elif pair[0] in nom_atts:

                # nominal attributes have a list of tuples as description
                # we have to process each tuple
                for tup in pair[1]:
  
                    # when the first value is a 1, then take all datapoints with the value in position two
                    '''
                    if pair[1][0] == 1.0:
                        sel_idx = df[df[pair[0]] == pair[1][1]].index.values
                        idx = np.intersect1d(idx, sel_idx)
                    # when the first value is a 0, then take all datapoints that do not have the value in position two
                    elif pair[1][0] == 0.0:
                        sel_idx = df[df[pair[0]] != pair[1][1]].index.values
                        idx = np.intersect1d(idx, sel_idx)   
                    '''
                    if tup[0] == 1.0:
                        sel_idx = df[df[pair[0]] == tup[1]].index.values
                        idx = np.intersect1d(idx, sel_idx)
                    # when the first value is a 0, then take all datapoints that do not have the value in position two
                    elif tup[0] == 0.0:
                        sel_idx = df[df[pair[0]] != tup[1]].index.values
                        idx = np.intersect1d(idx, sel_idx)    

            elif pair[0] in dt_atts:

                low_idx =  df[df[pair[0]] >= pair[1][0]].index.values # value can be equal to the lower bound
                up_idx = df[df[pair[0]] <= pair[1][1]].index.values # value can be equal to the upper bound            
                sel_idx = np.intersect1d(low_idx, up_idx)
                idx = np.intersect1d(idx, sel_idx)        

    all_idx = df.index.values
    idx_compl = np.setdiff1d(all_idx, idx)

    return idx, idx_compl

def select_subgroup(description=None, df=None, bin_atts=None, num_atts=None, nom_atts=None, dt_atts=None):

    pairs = list(description.items())
    idx_sg, idx_compl = select_idx(pairs=pairs, df=df, bin_atts=bin_atts, num_atts=num_atts, nom_atts=nom_atts, dt_atts=dt_atts)
    
    # this should be loc!!
    # make sure the dataset is sorted at the beginning of the algorithm
    subgroup = df.loc[idx_sg]
    subgroup_compl = df.loc[idx_compl]

    #print(list(idx_sg))
    #print(list(idx_compl))

    return subgroup, list(idx_sg), subgroup_compl, list(idx_compl)
