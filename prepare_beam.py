import numpy as np
import pandas as pd

import desc_based_selection as dbs
import cover_based_selection as cbs

def collect_beam_and_candidate_result_set(candidate_result_set=None, cq_satisfied=None, qm=None, beam_search_params=None, data_size=None, wcs_params=None):

    n_redun_descs = None
    if len(cq_satisfied) > 0:

        if wcs_params['run']:

            # follow procedure using 1 quality measure
            # we apply description based selection and cover based selection to prevent issues with redundancy
            candidate_result_set, candidate_queue, n_redun_descs = prepare_beam_and_candidate_result_set_redundancy_techniques(candidate_result_set=candidate_result_set, 
                                                                                                                               cq_satisfied=cq_satisfied, 
                                                                                                                               qm=qm, beam_search_params=beam_search_params,
                                                                                                                               data_size=data_size, wcs_params=wcs_params)

        else:

            candidate_result_set, candidate_queue = prepare_beam_and_candidate_result_set_simple(candidate_result_set=candidate_result_set, 
                                                                                                 cq_satisfied=cq_satisfied, 
                                                                                                 qm=qm, beam_search_params=beam_search_params)
    
    else:

        candidate_queue = []

    return candidate_result_set, candidate_queue, n_redun_descs

def prepare_beam_and_candidate_result_set_simple(candidate_result_set=None, cq_satisfied=None, qm=None, beam_search_params=None):

    # beam
    beam = sorted(cq_satisfied, key = lambda i: i['qualities'][qm], reverse=True) 
    candidate_queue = beam[0:beam_search_params['w']]
    #print(len(candidate_queue))
    #for candidate in candidate_queue:
    #    print(candidate['description'])
    #    print(candidate['qualities']['phiwd'])

    # result set
    candidate_result_set.append(candidate_queue) # creates a nested list
    #print(len(candidate_result_set))
    candidate_result_set_unpacked = [item for sublist in candidate_result_set for item in sublist] # unlist alle elements
    candidate_result_set_ordered = sorted(candidate_result_set_unpacked, key = lambda i: i['qualities'][qm], reverse=True) # sort each description according to the sort var
    #for candidate in candidate_result_set_ordered:
    #    print(candidate['description'])
    rs_candidates = candidate_result_set_ordered[0:beam_search_params['q']] 
    #print(len(rs_candidates))
    

    return [rs_candidates], candidate_queue

def prepare_beam_and_candidate_result_set_redundancy_techniques(candidate_result_set=None, cq_satisfied=None, qm=None, beam_search_params=None, data_size=None, wcs_params=None):

    # sort cq_satisfied on quality value
    cq_sorted = sorted(cq_satisfied, key = lambda i: i['qualities'][qm], reverse=True) 
    
    # apply description-based selection
    # difficult to know when to stop
    # only from 2nd level and onwards
    print('description-based selection')
    candidates, n_redun_descs = dbs.remove_redundant_descriptions(descs=cq_sorted, stop_number=wcs_params['stop_number_description_selection'], 
                                                                  qm=qm, beam_search_params=beam_search_params)

    # apply cover-based selection
    print('cover-based selection')
    candidate_queue = cbs.select_using_weighted_coverage(candidates=candidates, stop_number=beam_search_params['w'], 
                                                         qm=qm, data_size=data_size, wcs_params=wcs_params)
                                             
    # we have the same procedure for the result set
    # but we only do it at the end of the entire beam search
    # in every level of the beam search we only select the first q of the beam
    selected_for_result_list = candidate_queue[0:beam_search_params['q']] # q has to be smaller than w
    candidate_result_set.append(selected_for_result_list) # creates a nested list
    rs_candidates = [item for sublist in candidate_result_set for item in sublist] # unlist alle elements
    
    return [rs_candidates], candidate_queue, n_redun_descs