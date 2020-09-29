import numpy as np
import pandas as pd
import dataset as dt
import rw_dataset as rwdt
import beam_search as bs

def main(name_dataset=None, nr_quantiles=None, quality_measures=None, 
         w=10, d=5, q=50, seed=None, save_location=None):
         
     data, time_attributes, skip_attributes, id_attribute, first_timepoint = rwdt.import_and_process(name_dataset=name_dataset)
     
     result_rw_analysis = rwdt.analysis_rw_dataset(dataset=data, time_attributes=time_attributes, 
                                                   skip_attributes=skip_attributes, id_attribute=id_attribute, first_timepoint=first_timepoint,
                                                   nr_quantiles=nr_quantiles, quality_measures=quality_measures, w=w, d=d, q=q)

     if save_location is not None:
        save_location_added = save_location + name_dataset + '_' + str(seed) + str('.xlsx')
        result_rw_analysis.to_excel(save_location_added)  

     print(result_rw_analysis)

if __name__ == '__main__':

    main(name_dataset = 'callcenter_example',
         nr_quantiles=4, quality_measures=['deltatv', 'omegatv', 'phiwd', 'phikl', 'phiarl', 'phiwarl', 'phibic'],
         w=10, d=5, q=15, seed=20200929,
         save_location='./data_output/')

