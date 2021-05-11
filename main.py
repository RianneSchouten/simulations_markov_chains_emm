#import os
#import beam_search as bs
#import experiment as ex
import experiment_orders as exo

def main(subgroup_orders=None,
         nr_quantiles=None, quality_measures=None, 
         w=10, d=5, q=50, refs=None, start_at_order=None,
         save_location=None, stop_at_order=None,
         constraint_subgroup_size=None, constraint_subgroup_coverage=None,
         nreps=None, seed=None, ncovs=None,
         N=None, T=None, S=None, wcs_params=None):

    result_experiment = exo.experiment(nreps=nreps, seed=seed, ncovs=ncovs, N=N, T=T, S=S, 
                                       subgroup_orders=subgroup_orders, refs=refs,
                                       nr_quantiles=nr_quantiles, quality_measures=quality_measures, 
                                       w=w, d=d, q=q, start_at_order=start_at_order, stop_at_order=stop_at_order,
                                       constraint_subgroup_size=0.1, constraint_subgroup_coverage=0.9, 
                                       wcs_params=wcs_params, save_location=save_location)

    
    if save_location is not None:
        save_location_added = save_location + '_' + str(seed) + '_' + str(nreps) + 'nreps' + '_' + str(N) + '_' + str(T) + '_' + str(S) + '_' + str(ncovs) + str('.xlsx')
        result_experiment.to_excel(save_location_added)  
    
    print(result_experiment) 

   
if __name__ == '__main__':

    # we rewrite the code a bit to give it more overview
    # and to add possibilities for higher order global models, a different parameters for start_at_order (s)
    # and different subgroup size with a different true subgroup description
        

    '''
    # run with redundancy techniques to see if that makes a difference
    # turns out the redundancy techniques do not make a difference for the synthetic data study
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
    #  EXPERIMENT RUN BEFORE REVISION
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
### main for first order markov chains
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




