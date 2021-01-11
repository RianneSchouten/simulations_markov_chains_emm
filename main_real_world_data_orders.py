import numpy as np
import pandas as pd
import dataset as dt
import emm_rw_dataset_orders as rwdto

def main(name_dataset=None, calculate_distributions=None, nr_quantiles=None, quality_measures=None, 
         w=None, d=None, q=None, m=None, Z=None, seed=None, 
         ref=None, start_at_order=None, save_location=None):
         
    data, attributes, combinations = rwdto.load(name_dataset=name_dataset)  

    print('attributes', attributes)
    print('data', data.tail(20))
    print(data.isnull().sum().sum())
    print(data.shape)
   
    if save_location is not None:
        save_location_total = save_location + name_dataset + '_' + str(seed)
     
    result_rw_analysis, considered_subgroups, general_params = rwdto.analysis_rw_dataset(dataset=data, calculate_distributions=calculate_distributions, attributes=attributes, 
                                                  nr_quantiles=nr_quantiles, quality_measures=quality_measures, w=w, d=d, q=q, m=m, Z=Z,
                                                  ref=ref, start_at_order=start_at_order, save_location=save_location_total)

    # save
    rw_analysis_info = pd.DataFrame({'m': [m], 'nr_quantiles': [nr_quantiles], 'w': [w], 'd': [d], 'q': [q], 'Z': [Z]})
    general_params_pd = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in general_params.items() ]))
    dfs = {'result_rw_analysis': result_rw_analysis, 'rw_analysis_info': rw_analysis_info, 'considered_subgroups': pd.DataFrame(considered_subgroups), 'general_params_pd': general_params_pd}

    writer = pd.ExcelWriter(save_location_total + '_resultset.xlsx', engine='xlsxwriter')
    for sheet_name in dfs.keys():
        dfs[sheet_name].to_excel(writer, sheet_name=sheet_name, index=False)
    writer.save()

    print(result_rw_analysis)

if __name__ == '__main__':

    main(#name_dataset='TIRpatientendata_1',  
         name_dataset='studyportals',
         calculate_distributions=False,
         nr_quantiles=4, quality_measures=['phiaic'],
         w=15, d=3, q=10, m=2, Z=0.01, seed=20201214,
         ref='dataset', start_at_order=4,
         save_location='./data_output/')

