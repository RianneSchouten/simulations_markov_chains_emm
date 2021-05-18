import numpy as np
import pandas as pd
import dataset as dt
import emm_rw_dataset_orders as rwdto

def main(name_dataset=None, seed=None,
         beam_search_params=None, quality_measure=None, constraints=None,
         markov_model_params=None, wcs_params=None, save_location=None):
         
    data, attributes, combinations = rwdto.load(name_dataset=name_dataset)  

    print('data', data.tail(20))
    print('attributes', attributes)
    print(data.dtypes)
    print(data.isnull().sum())
    print(data.shape)
   
    if save_location is not None:
        save_location_total = save_location + name_dataset + '_' + str(seed)
     
    result_rw_analysis, considered_subgroups, general_params = rwdto.analysis_rw_dataset(dataset=data, attributes=attributes, 
                                                                                         beam_search_params=beam_search_params, 
                                                                                         quality_measure=quality_measure, constraints=constraints,
                                                                                         markov_model_params=markov_model_params, wcs_params=wcs_params)

    # save
    beam_search_params.update(constraints)
    beam_search_params.update(wcs_params)
    beam_search_params.update(markov_model_params)
    rw_analysis_info = pd.DataFrame(beam_search_params, index=[0])
    general_params_pd = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in general_params.items() ]))
    dfs = {'result_rw_analysis': result_rw_analysis, 'rw_analysis_info': rw_analysis_info, 'considered_subgroups': pd.DataFrame(considered_subgroups), 'general_params_pd': general_params_pd}

    writer = pd.ExcelWriter(save_location_total + '_resultset.xlsx', engine='xlsxwriter')
    for sheet_name in dfs.keys():
        dfs[sheet_name].to_excel(writer, sheet_name=sheet_name, index=False)
    writer.save()

    print(result_rw_analysis)

if __name__ == '__main__':

   
    main(name_dataset='movies', 
         beam_search_params={'w': 25, 'd': 3, 'q': 20, 'b': 4},
         quality_measure='phiaic', # just one !!
         markov_model_params={'start_at_order': 4, 'stop_at_order': 1},
         constraints={'constraint_subgroup_size': 0.1},
         seed=20210514,
         wcs_params={'run': True, 'gamma': 0.9, 'stop_number_description_selection': 50}, # twice the size of w
         save_location='./data_output/')
    
    '''
     # change to w = 25 (1/4 of 94)
     # change to q = 20
     # q has to be smaller than w

    main(name_dataset='TIRpatientendata_2', 
         beam_search_params={'b': 4, 'w': 25, 'd': 3, 'q': 20}, 
         quality_measure='phiaic', # just one !!
         seed=20210514,
         markov_model_params={'start_at_order':4, 'stop_at_order':1},
         constraints={'constraint_subgroup_size':0.1},         
         wcs_params={'run': True, 'gamma': 0.9, 'stop_number_description_selection': 50}, # twice the size of w
         save_location='./data_output/')

    main(name_dataset='TIRpatientendata_1', 
         beam_search_params={'b': 4, 'w': 25, 'd': 3, 'q': 20}, 
         quality_measure='phiaic', # just one !!
         seed=20210514,
         markov_model_params={'start_at_order':2, 'stop_at_order':1},
         constraints={'constraint_subgroup_size':0.1},         
         wcs_params={'run': True, 'gamma': 0.9, 'stop_number_description_selection': 50}, # twice the size of w
         save_location='./data_output/')
    '''
    '''
    # BEFORE REVISION, VERSION 1 MANUSCRIPT
    main(name_dataset='TIRpatientendata_2', 
         calculate_distribution=False, use_distribution=False,
         nr_quantiles=4, quality_measure='phiaic', # just one !!
         w=20, d=3, q=25, m=None, Z=None, seed=20210114,
         ref='dataset', start_at_order=4,
         constraint_subgroup_size=0.1, constraint_subgroup_coverage=0.9,
         stop_at_order=1, save_location='./data_output/')
    '''

    '''
    main(name_dataset='TIRpatientendata_1', 
         calculate_distribution=False, use_distribution=False,
         nr_quantiles=4, quality_measure='phiaic', # just one !!
         w=20, d=3, q=25, m=None, Z=None, seed=20210114,
         ref='dataset', start_at_order=2,
         constraint_subgroup_size=0.1, constraint_subgroup_coverage=0.9,
         stop_at_order=1, save_location='./data_output/')
    '''
