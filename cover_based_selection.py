import numpy as np
import pandas as pd

def select_using_weighted_coverage(candidates=None, stop_number=None, qm=None, data_size=None, wcs_params=None):

    #print('len candidates', len(candidates))
    # if the number of candidates is smaller than the desired number, we can just select all candidates
    if len(candidates) > stop_number:

        all_idx = pd.DataFrame(pd.Series(np.zeros(data_size)), columns=[['count']])
        temp_qm = 'temp_' + qm

        # list has to be sorted
        # already sorted during description-based selection    
        # first pop sg_idx from first candidate, leftover is the candidate without sg_idx

        #sel_idx = candidates[0]['qualities'].pop('sg_idx')
        sel_idx = candidates[0]['qualities']['idx_sg']
        sel = [candidates[0]]
        left_over_candidates = candidates.copy()
        left_over_candidates.remove(left_over_candidates[0])

        #print('desc', sel[0]['description'])

        i = 1
    
        while i < stop_number:
       
            candidates_with_updated_qms = []
            # update weights of cases covered by already selected descriptions (sel_idx)
            all_idx.loc[sel_idx,['count']] = all_idx.loc[sel_idx,['count']] + 1

            for candidate in left_over_candidates:

                # select rows in current candidate and calculate weight for candidate
                sg_idx = candidate['qualities']['idx_sg']
                all_weights = np.power(wcs_params['gamma'], all_idx.loc[sg_idx, ['count']].values)
                weight = np.sum(all_weights) / len(sg_idx)

                # calculate new quality for candidate
                candidate['qualities'][temp_qm] = candidate['qualities'][qm] * weight
                candidates_with_updated_qms.append(candidate)

            # re-sort candidates
            candidates_sorted = sorted(candidates_with_updated_qms, key = lambda i: i['qualities'][temp_qm], reverse=True)
            # select first candidate and update other lists
            #sel_idx = candidates_sorted[0]['qualities'].pop('sg_idx')
            sel_idx = candidates_sorted[0]['qualities']['idx_sg']
            sel.append(candidates_sorted[0])
            left_over_candidates.remove(candidates_sorted[0])

            #print('desc', sel[i]['description'])

            i += 1

    else:

        sel = candidates

    #print('len sel', len(sel))

    return sel