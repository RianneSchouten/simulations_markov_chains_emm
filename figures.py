import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as grd

import figures_functions as ff
import emm_rw_dataset_orders as rwdto
import dataset as dt
import qualities_orders as qmo
import mc_functions_orders as fo

#result_rw_analysis, rw_analysis_info, considered_subgroups, general_params_pd = ff.load(name_dataset='TIRpatientendata_2_20210114_resultset')
#result_rw_analysis, rw_analysis_info, considered_subgroups, general_params_pd = ff.load(name_dataset='studyportals_20210115_resultset')
#result_rw_analysis, rw_analysis_info, considered_subgroups, general_params_pd = ff.load(name_dataset='logs_20210115_resultset')
#result_rw_analysis, rw_analysis_info, considered_subgroups, general_params_pd = ff.load(name_dataset='bach_20210115_resultset')
#result_rw_analysis, rw_analysis_info, considered_subgroups, general_params_pd = ff.load(name_dataset='movies_20210115_resultset')
#result_rw_analysis, rw_analysis_info, considered_subgroups, general_params_pd = ff.load(name_dataset='dna_20210115_resultset')
#result_rw_analysis, rw_analysis_info, considered_subgroups, general_params_pd = ff.load(name_dataset='wikispeedia_20210121_resultset')
#results = result_rw_analysis.copy()

dataset, attributes, combinations = rwdto.load(name_dataset='wikispeedia')  
df, cols, bin_atts, nom_atts, num_atts, dt_atts, idx = dt.read_data(dataset=dataset, attributes=attributes)
quality_measure = 'phiaic'
general_params = qmo.calculate_general_parameters(df=df, distribution=None, cols=cols, attributes=attributes, order=2, 
                                                  start_at_order=3, quality_measure=quality_measure)
'''
score, lld, found_order = fo.calculate_best_fitting_order(probs=general_params['probs'], freqs=general_params['freqs'], initial_freqs=general_params['initial_freqs'], start_at_order=4, 
                                                          s=len(general_params['states']), quality_measure=quality_measure, data_size=general_params['data_size'])
print(score)
print(lld)
print(found_order)
print(general_params)
'''
# figure general params
fig = ff.visualize_probs(tA=general_params['probs']['prob_1'], tpi=general_params['probs']['prob_0'], states=general_params['states'],
                         order=1, y_names=general_params['empty_dfs']['empty_lss_1'].index.values, 
                         title='General parameters', name_fig='figures/visualization_general.png')

for sgn in np.arange(0, 10):

    sg = results.loc[results.sg == sgn, ]
    desc = sg.iloc[0, ].dropna().drop(['sg']).to_dict()
    quals = sg.iloc[1, ].dropna()
    order = int(quals.loc['best_order'])

    if order == 0:
        order = 1

    subgroup_params, idx = ff.recalculate_parameters(quality_measure=quality_measure, best_order=order,
                                                     df=dataset, cols=cols, attributes=attributes, 
                                                     quals=quals, general_params=general_params)
    #print(subgroup_params)

    title = 'Parameters subgroup ' + str(sgn+1)
    name_fig = 'figures/visualization_' + str(sgn+1) + '_' + quality_measure + '.png'
    prob_name = 'prob_' + str(order)
    state_space = 'empty_lss_' + str(order)
    fig = ff.visualize_probs(tA=subgroup_params['probs'][prob_name], tpi=subgroup_params['probs']['prob_0'], states=general_params['states'],
                             order=order, y_names=general_params['empty_dfs'][state_space].index.values, title=title, name_fig=name_fig)
