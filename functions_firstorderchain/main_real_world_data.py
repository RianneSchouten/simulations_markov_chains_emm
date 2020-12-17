import numpy as np
import pandas as pd
import dataset as dt
import emm_rw_dataset as rwdt
import beam_search as bs

def main(name_dataset=None, calculate_distributions=None, nr_quantiles=None, quality_measures=None, 
         w=None, d=None, q=None, m=None, Z=None, seed=None, save_location=None):
         
    data, attributes = rwdt.load(name_dataset=name_dataset)  

    print('attributes', attributes)
    print('data', data.tail(20))
    print(data.isnull().sum().sum())
    print(data.shape)
   
    if save_location is not None:
        save_location_total = save_location + name_dataset + '_' + str(seed)
     
    result_rw_analysis = rwdt.analysis_rw_dataset(dataset=data, calculate_distributions=calculate_distributions, attributes=attributes, 
                                                  nr_quantiles=nr_quantiles, quality_measures=quality_measures, w=w, d=d, q=q, m=m, Z=Z,
                                                  save_location=save_location_total)

    # save
    rw_analysis_info = pd.DataFrame({'m': [m], 'nr_quantiles': [nr_quantiles], 'w': [w], 'd': [d], 'q': [q], 'Z': [Z]})
    dfs = {'result_rw_analysis': result_rw_analysis, 'rw_analysis_info': rw_analysis_info}

    writer = pd.ExcelWriter(save_location_total + '_resultset.xlsx', engine='xlsxwriter')
    for sheet_name in dfs.keys():
        dfs[sheet_name].to_excel(writer, sheet_name=sheet_name, index=False)
    writer.save()

    print(result_rw_analysis)

if __name__ == '__main__':

    main(name_dataset='TIRpatientendata', calculate_distributions=False,
         nr_quantiles=8, quality_measures=['deltatv', 'omegatv', 'phiwd', 'phikl', 'phiarl', 'phiwarl'],
         w=25, d=3, q=25, m=100, Z=2.1, seed=20201023,
         save_location='./data_output/')

