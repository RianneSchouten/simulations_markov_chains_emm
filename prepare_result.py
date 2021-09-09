import numpy as np
import pandas as pd

import desc_based_selection as dbs
import cover_based_selection as cbs

def select_result_set(candidate_result_set=None, beam_search_params=None, wcs_params=None, data_size=None, qm=None):

    print('result set selection')
    result_set_ordered = sorted(candidate_result_set, key = lambda i: i['qualities'][qm], reverse=True) 
   
    cq_result_set, rs_n_redun_descs = dbs.remove_redundant_descriptions(descs=result_set_ordered, stop_number=wcs_params['stop_number_description_selection'], 
                                                                        qm=qm, beam_search_params=beam_search_params)
    result_set = cbs.select_using_weighted_coverage(candidates=cq_result_set, stop_number=beam_search_params['q'], 
                                                    qm=qm, data_size=data_size, wcs_params=wcs_params) 

    return result_set, rs_n_redun_descs

def prepare_result_list(result_set=None):

    if len(result_set) == 0:
        
        print('Empty result set')
        result_emm = None
    
    else:        
        
        result_set_selected = result_set.copy()

        if len(result_set_selected) == 0:
            
            print('Empty result set')
            result_emm = None
        
        else: 

            result_emm = pd.DataFrame.from_dict(result_set_selected[0]).T
            result_emm.drop(columns=['idx_sg'], inplace=True)
            for sg in np.arange(1, len(result_set_selected)):
                new_sg = pd.DataFrame.from_dict(result_set_selected[sg]).T
                new_sg.drop(columns=['idx_sg'], inplace=True)
                result_emm = result_emm.append(new_sg)
            result_emm['sg'] = np.repeat(np.arange(len(result_set_selected)), 2) 
            result_emm.sort_index(axis=1, inplace=True)  

    print(result_emm.dtypes)

    return result_emm



