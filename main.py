#import os
import beam_search as bs
import experiment as ex

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

    main(nr_quantiles=4, 
         quality_measures=['deltatv', 'omegatv', 'phiwd', 'phikl', 'phiarl', 'phiwarl', 'phibic'],
         w=10, d=5, q=25,
         save_location='./data_output/experiment_initialprobs',
         nreps=50, seed=20200619, ncovs=[2, 5, 10, 25],
         N=[100, 1000], T=[2, 5, 25], S=[2, 5, 25])







