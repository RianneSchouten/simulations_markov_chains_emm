#import os
#import beam_search as bs
#import experiment as ex
import experiment_orders as exo

def main(subgroup_orders=None,
         quality_measures=None, 
         markov_model_params=None,
         beam_search_params=None,
         simulation_params=None,
         constraints=None,
         wcs_params=None,
         seed=None,
         save_location=None):

    result_experiment = exo.experiment(subgroup_orders=subgroup_orders,
                                       quality_measures=quality_measures, 
                                       markov_model_params=markov_model_params,
                                       beam_search_params=beam_search_params,
                                       simulation_params=simulation_params,
                                       constraints=constraints,
                                       wcs_params=wcs_params)

    
    if save_location is not None:
        save_location_added = save_location + '_' + str(seed) + '_' + str(list(simulation_params.values())) + str('.xlsx')
        result_experiment.to_excel(save_location_added)  
    
    print(result_experiment) 

   
if __name__ == '__main__':

    '''
    # run with redundancy techniques to see if that makes a difference
    # turns out the redundancy techniques do not make a difference for the synthetic data experiment
    main(nr_quantiles=8, subgroup_orders = [1,2,3,4],
         quality_measures=['phiwd', 'phibic', 'phiaic', 'phiaicc', 'omegatv', 'phiwrl'],
         w=25, d=3, q=20, refs=['dataset'], stop_at_order=1,  
         start_at_order=4, save_location='./data_output/results_revised_manuscript/experiment_higherorders',
         constraint_subgroup_size=0.1, constraint_subgroup_coverage=None,
         nreps=10, seed=20210509, ncovs=[20, 10, 5],
         N=[100], T=[200, 50, 10], S=[10, 5, 2],
         wcs_params={'gamma': 0.9, 'stop_number_description_selection': 50})
    '''
    '''
    # sensitivity analysis: varying global model order, varying start parameter
    main(subgroup_orders = [1,2,3,4],
         quality_measures=['phiwd', 'phibic', 'phiaic', 'phiaicc', 'omegatv', 'phiwrl'],
         markov_model_params={'start_at_order': [2,4], 'stop_at_order':1},
         beam_search_params={'b': 8, 'w': 25, 'd': 3, 'q': 20},
         constraints={'constraint_subgroup_size': 0.1},
         simulation_params={'nreps': 10, 'N': [100], 'ncovs': [20], 'T': [10,200], 'S': [5], 'p': [0.5], 'true_desc_length': [2], 'global_model_order': [1,3]},
         wcs_params={'run': False, 'gamma': 0.9, 'stop_number_description_selection': 50},
         seed=20210512, save_location='./data_output/results_revised_manuscript/experiment_varying_globalmodel_and_start_parameter'
         )

    # sensitivity analysis: varying sample size and varying description lengths
    main(subgroup_orders = [1,2,3,4],
         quality_measures=['phiwd', 'phibic', 'phiaic', 'phiaicc', 'omegatv', 'phiwrl'],
         markov_model_params={'start_at_order': [4], 'stop_at_order':1},
         beam_search_params={'b': 8, 'w': 25, 'd': 3, 'q': 20},
         constraints={'constraint_subgroup_size': 0.1},
         simulation_params={'nreps': 10, 'N': [100], 'ncovs': [20], 'T': [50], 'S': [5], 'p': [0.35,0.5], 'true_desc_length': [1,2], 'global_model_order': [1]},
         wcs_params={'run': False, 'gamma': 0.9, 'stop_number_description_selection': 50},
         seed=20210512, save_location='./data_output/results_revised_manuscript/experiment_varying_sample_size'
         )    '''
    
    '''
    # EXPERIMENTS BEFORE REVISION
    # main analysis
    main(nr_quantiles=8, subgroup_orders = [1,2,3,4],
         quality_measures=['omegatv', 'phiwrl'],
         w=25, d=3, q=20, refs=['dataset'], stop_at_order=1,  
         start_at_order=4, save_location='./data_output/results_manuscript/experiment_higherorders',
         constraint_subgroup_size=0.1, constraint_subgroup_coverage=0.9,
         nreps=30, seed=20210128, ncovs=[20, 10, 5],
         N=[100], T=[200, 50, 10], S=[10, 5, 2])
    '''
    '''
    # simulation with subgroups of order = 0 (i.e. order = I)
    main(nr_quantiles=8, subgroup_orders = [0],
         quality_measures=['phiwd', 'phibic', 'phiaic', 'phiaicc', 'omegatv', 'phiwrl'],
         w=25, d=3, q=20, start_at_order=1, stop_at_order=0, refs=['dataset'],
         save_location='./data_output/results_manuscript/experiment_zero_order_subgroups',
         constraint_subgroup_size=0.1, constraint_subgroup_coverage=0.9,
         nreps=10, seed=20210112, ncovs=[20, 10, 5],
         N=[100, 500, 1000], T=[10, 5, 2], S=[10, 5, 2])
    '''

    '''
    # INITIAL EXPERIMENTS FOR FIRST ORDER MARKOV CHAINS
    # functions are not stored in folder functions_firstorderchain
    def main(experiment=None,
         nr_quantiles=None, quality_measures=None, 
         w=10, d=5, q=50,
         save_location=None,
         nreps=None, seed=None, ncovs=None,
         N=None, T=None, S=None):

    result_experiment = ex.experiment(nreps=nreps, seed=seed, ncovs=ncovs, N=N, T=T, S=S, 
                                      nr_quantiles=nr_quantiles, quality_measures=quality_measures, 
                                      w=w, d=d, q=q,
                                      save_location=save_location)

    if save_location is not None:
        save_location_added = save_location + '_' + str(seed) + '_' + str(nreps) + 'nreps' + '_' + str(N) + '_' + str(T) + '_' + str(S) + '_' + str(ncovs) + str('.xlsx')
        result_experiment.to_excel(save_location_added)  

    print(result_experiment) 
    
    if __name__ == '__main__':

    main(nr_quantiles=8, 
         quality_measures=['deltatv', 'omegatv', 'phiwd', 'phikl', 'phiarl', 'phiwarl'],
         w=25, d=5, q=25,
         save_location='./data_output/experiment_initialprobs',
         nreps=25, seed=20200102, ncovs=[2, 5, 25],
         N=[100], T=[2, 5, 25], S=[2, 5, 25])
    '''




