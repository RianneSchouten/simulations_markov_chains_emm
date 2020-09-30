import numpy as np
import pandas as pd
import dataset as dt
import rw_dataset as rwdt
import beam_search as bs

def main(name_dataset=None, calculate_distributions=None, nr_quantiles=None, quality_measures=None, 
         w=None, d=None, q=None, m=None, Z=None, seed=None, save_location=None):
         
     data, time_attributes, skip_attributes, id_attribute, first_timepoint = rwdt.import_and_process(name_dataset=name_dataset)
     print(data.head(10))
     
     result_rw_analysis = rwdt.analysis_rw_dataset(dataset=data, calculate_distributions=calculate_distributions, time_attributes=time_attributes, 
                                                   skip_attributes=skip_attributes, id_attribute=id_attribute, first_timepoint=first_timepoint,
                                                   nr_quantiles=nr_quantiles, quality_measures=quality_measures, w=w, d=d, q=q, m=m, Z=Z,
                                                   save_location=save_location)

     if save_location is not None:
        save_location_added = save_location + name_dataset + '_' + str(seed) + str('.xlsx')
        result_rw_analysis.to_excel(save_location_added)  

     print(result_rw_analysis)

if __name__ == '__main__':

    main(name_dataset = 'callcenter_example', calculate_distributions=True,
         nr_quantiles=8, quality_measures=['phibic', 'phiwd', 'deltatv', 'omegatv'],
         w=10, d=5, q=15, m=100, Z=1.96, seed=20200930,
         save_location='./data_output/')

