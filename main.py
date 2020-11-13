#import os
import beam_search as bs
import experiment as ex
import experiment_orders as exo

'''
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

def main(subgroup_orders=None,
         nr_quantiles=None, quality_measures=None, 
         w=10, d=5, q=50, start_at_order=None,
         save_location=None,
         nreps=None, seed=None, ncovs=None,
         N=None, T=None, S=None):

    result_experiment = exo.experiment(nreps=nreps, seed=seed, ncovs=ncovs, N=N, T=T, S=S, 
                                       subgroup_orders=subgroup_orders,
                                       nr_quantiles=nr_quantiles, quality_measures=quality_measures, 
                                       w=w, d=d, q=q, start_at_order=start_at_order,
                                       save_location=save_location)

    
    if save_location is not None:
        save_location_added = save_location + '_' + str(seed) + '_' + str(nreps) + 'nreps' + '_' + str(N) + '_' + str(T) + '_' + str(S) + '_' + str(ncovs) + str('.xlsx')
        result_experiment.to_excel(save_location_added)  
    
    print(result_experiment) 
    
if __name__ == '__main__':

    main(nr_quantiles=8, subgroup_orders = [0,1,2,3,4],
         quality_measures=['phiwd', 'phibic', 'phiaic', 'phiaicc', 'omegatv', 'phiwarl'],
         w=25, d=3, q=20, start_at_order=4,
         save_location='./data_output/experiment_higherorders',
         nreps=25, seed=20201112, ncovs=[5, 10, 20],
         N=[100], T=[25, 50], S=[5, 10])





