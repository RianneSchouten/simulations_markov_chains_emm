import numpy as np
import pandas as pd
import itertools as it

import beam_search as bs
import summaries as su
import evaluation as ev
import distribution_false_discoveries as dfd

def analysis_rw_dataset(dataset=None, calculate_distributions=None, time_attributes=None, skip_attributes=None, id_attribute=None, first_timepoint=None,
                        descriptives=None, nr_quantiles=None, quality_measures=None, w=None, d=None, q=None, m=None, Z=None, save_location=None):   
    
    if calculate_distributions:

        distributions = {}

        for quality_measure in quality_measures:

            # find distribution
            distribution = dfd.build_distribution(m=m, dataset=dataset, time_attributes=time_attributes, descriptives=descriptives,
                                                  skip_attributes=skip_attributes, id_attribute=id_attribute, first_timepoint=first_timepoint,
                                                  nr_quantiles=nr_quantiles, quality_measure=quality_measure, w=w, d=d, q=q)
            distributions[quality_measure] = distribution

        # save
        pd_distributions = pd.DataFrame(distributions)
        pd_distributions.to_excel(save_location + '_distributions.xlsx')   

    else:

        # load
        distributions = pd.read_excel(save_location + '_distributions.xlsx', sheet_name=0, header=0)

    # use distribution in the beam search 
    result_rw_analysis = pd.DataFrame()

    for quality_measure in quality_measures:
    
        result_emm, nconsd_list, general_params = bs.beam_search(dataset=dataset, distribution=distributions[quality_measure], time_attributes=time_attributes, 
                                                                 skip_attributes=skip_attributes, id_attribute=id_attribute, first_timepoint=first_timepoint,
                                                                 nr_quantiles=nr_quantiles, quality_measure=quality_measure, w=w, d=d, q=1, Z=Z)

        # process
        result_rw_analysis = su.join_result_emm(result_emm=result_emm, result_rw_analysis=result_rw_analysis, quality_measure=quality_measure, q=q)

    ev.evaluation_figures(result_rw_analysis=result_rw_analysis, general_params=general_params, quality_measures=quality_measures, sg=0)  

    return result_rw_analysis

def load(name_dataset=None):

    location = 'data_input/' + name_dataset + '_preprocessed.xlsx'
    sheets = pd.read_excel(location, sheet_name=['data', 'df_attributes'])
    print(sheets)

    data = sheets['data']
    df_attributes = sheets['df_attributes']

    time_attributes = [value for value in df_attributes['time_attributes'].values if str(value) != 'nan'] 
    skip_attributes = [value for value in df_attributes['skip_attributes'].values if str(value) != 'nan']
    id_attribute = df_attributes['id_attribute'][0]
    first_timepoint = df_attributes['first_timepoint'][0]
    descriptives = [value for value in df_attributes['descriptives'] .values if str(value) != 'nan']   

    return data, time_attributes, skip_attributes, id_attribute, first_timepoint, descriptives




