import numpy as np
import itertools as it

import dataset as dt

def create_starting_descriptions(df=None, cols=None, 
                                 bin_atts=None, nom_atts=None, 
                                 num_atts=None, dt_atts=None,
                                 nr_quantiles=None):

    cq_bin = refine_binary_attributes(seed=None, df=df, subgroup=None, binary_attributes=bin_atts)
    cq_bin_nom, nominal_values = refine_nominal_attributes(cq=cq_bin, seed=None, df=df, subgroup=None, nominal_attributes=nom_atts, nominal_values=None)
    cq_bin_nom_num = refine_numerical_attributes(cq=cq_bin_nom, seed=None, df=df, subgroup=None, 
                                                 numerical_attributes=num_atts, nr_quantiles=nr_quantiles)
    cq_bin_nom_num_dt = refine_datetime_attributes(cq=cq_bin_nom_num, seed=None, df=df, subgroup=None, 
                                                   datetime_attributes=dt_atts, nr_quantiles=nr_quantiles)

    return cq_bin_nom_num_dt, nominal_values

def refine_seed(seed=None, subgroup=None, bin_atts=None, num_atts=None, nom_atts=None, dt_atts=None, nr_quantiles=None, nominal_values=None):

    cq_bin = refine_binary_attributes(seed=seed, df=None, subgroup=subgroup, binary_attributes=bin_atts)
    cq_bin_nom = refine_nominal_attributes(cq=cq_bin, seed=seed, df=None, subgroup=subgroup, nominal_attributes=nom_atts, nominal_values=nominal_values)
    cq_bin_nom_num = refine_numerical_attributes(cq=cq_bin_nom, seed=seed, df=None, subgroup=subgroup, 
                                                 numerical_attributes=num_atts, nr_quantiles=nr_quantiles)
    cq_bin_nom_num_dt = refine_datetime_attributes(cq=cq_bin_nom_num, seed=seed, df=None, subgroup=subgroup, 
                                                   datetime_attributes=dt_atts, nr_quantiles=nr_quantiles)
 
    return cq_bin_nom_num_dt

def refine_datetime_attributes(cq=None, seed=None, df=None, subgroup=None, datetime_attributes=None, nr_quantiles=None):

    refined_cq = cq

    quantiles = np.linspace(0, 1, nr_quantiles+1)[1:-1] # for 4 quantiles, this results in 0.25, 0.5, 0.75

    # first candidate queue
    if seed is None:
        for attribute in datetime_attributes:
            values = df[attribute]

            min_value = values.quantile(0.0)
            max_value = values.quantile(1.0)

            for i in range(nr_quantiles-1):
                value = values.quantile(quantiles[i], interpolation='linear')

                refined_cq.append({'description' : {attribute : (min_value, value)}})
                refined_cq.append({'description' : {attribute : (value, max_value)}})
    
    # refinements for existing candidate queue
    else:    
        description = seed['description']        
        for attribute in datetime_attributes:

            values = subgroup[attribute]
                        
            min_value = values.quantile(0.0)
            max_value = values.quantile(1.0)
                
            for i in range(nr_quantiles-1):

                value = values.quantile(quantiles[i], interpolation='linear')

                temp_desc = description.copy()
                temp_desc[attribute] = (min_value, value)
                refined_cq.append({'description' : temp_desc})

                temp_desc_2 = description.copy()
                temp_desc_2[attribute] = (value, max_value)
                refined_cq.append({'description' : temp_desc_2})     

    return  refined_cq 

def refine_numerical_attributes(cq=None, seed=None, df=None, subgroup=None, numerical_attributes=None, nr_quantiles=None):

    refined_cq = cq

    quantiles = np.linspace(0, 1, nr_quantiles+1)[1:-1] # for 4 quantiles, this results in 0.25, 0.5, 0.75
    
    # first candidate queue
    if seed is None:
        for attribute in numerical_attributes:
            
            values = df[attribute]

            if df[attribute].isnull().any():
                refined_cq.append({'description' : {attribute : np.nan}})
                values = values[~np.isnan(values)]  

            # continue with quantile split
            min_value = values.quantile(0.0) 
            max_value = values.quantile(1.0)
              
            for i in range(nr_quantiles-1):
                value = values.quantile(quantiles[i], interpolation='linear')

                refined_cq.append({'description' : {attribute : (min_value, value)}})
                refined_cq.append({'description' : {attribute : (value, max_value)}})       

    # refinements for existing candidate queue
    else:    
        description = seed['description']        
        for attribute in numerical_attributes:
            
            values = subgroup[attribute]
            if subgroup[attribute].isnull().any():
                temp_desc = description.copy()
                temp_desc[attribute] = np.nan
                refined_cq.append({'description' : temp_desc})
                values = values[~np.isnan(values)]  
            
            # continue with quantile split
            # only if there are real numbers left in the subgroup
            elif not len(values)==0:

                min_value = values.quantile(0.0) 
                max_value = values.quantile(1.0)
                
                for i in range(nr_quantiles-1):

                    value = values.quantile(quantiles[i], interpolation='linear')

                    temp_desc = description.copy()
                    temp_desc[attribute] = (min_value, value)
                    refined_cq.append({'description' : temp_desc})

                    temp_desc_2 = description.copy()
                    temp_desc_2[attribute] = (value, max_value)
                    refined_cq.append({'description' : temp_desc_2})     

    return  refined_cq

def refine_nominal_attributes(cq=None, seed=None, df=None, subgroup=None, nominal_attributes=None, nominal_values=None):

    refined_cq = cq

    # first candidate queue
    if seed is None:

        nominal_values = {}

        for attribute in nominal_attributes:
            
            values = df[attribute].unique()
            nominal_values.update({attribute: values})

            for i in range(len(values)):

                value = values[i]
                refined_cq.append({'description' : {attribute : [(1.0, value)]}}) # 1.0 indicates == this nominal value
                refined_cq.append({'description' : {attribute : [(0.0, value)]}}) # 0.0 indicates != this nominal value

        return refined_cq, nominal_values

    # refinements for existing candidate queue
    else:
        
        description = seed['description']

        for attribute in nominal_attributes:

            values = nominal_values[attribute]

            for i in range(len(values)):

                value = values[i]
                tup1 = (1.0, value)
                tup0 = (0.0, value)

                temp_desc = description.copy()
                if attribute in list(temp_desc.keys()):
                    temp_tuple_list = temp_desc[attribute].copy()
                    if tup1 not in temp_tuple_list:
                        temp_tuple_list.append(tup1)
                        temp_desc[attribute] = temp_tuple_list
                        refined_cq.append({'description' : temp_desc})
                else:
                    temp_desc[attribute] = [tup1] # every one-tuple description also has a list, to be able to add other tuples later on      
                    refined_cq.append({'description' : temp_desc})

                temp_desc = description.copy()
                if attribute in list(temp_desc.keys()):
                    temp_tuple_list = temp_desc[attribute].copy()
                    if tup0 not in temp_tuple_list:
                        temp_tuple_list.append(tup0)
                        temp_desc[attribute] = temp_tuple_list
                        refined_cq.append({'description' : temp_desc})
                else:
                    temp_desc[attribute] = [tup0]     
                    refined_cq.append({'description' : temp_desc})

        return refined_cq

def refine_binary_attributes(seed=None, df=None, subgroup=None, binary_attributes=None):

    refined_cq = []

    # first candidate queue
    if seed is None:

        for attribute in binary_attributes:
            
            values = df[attribute].unique()
            refined_cq.append({'description' : {attribute : values[0]}})
            refined_cq.append({'description' : {attribute : values[1]}})

    # refinements for a seed
    else:
        
        description = seed['description']

        for attribute in binary_attributes:
            if not attribute in list(description.keys()):
                
                values = subgroup[attribute].unique()
                for i in range(len(values)):

                    value = values[i]
                    temp_desc = description.copy()
                    temp_desc[attribute] = value
                    refined_cq.append({'description' : temp_desc})

    return  refined_cq     