import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as grd
import itertools as it
import matplotlib.colors as colors

import emm_rw_dataset_orders as rwdto
import dataset as dt
import qualities_orders as qmo
import mc_functions_orders as fo

def load(name_dataset=None):

    location = 'C:/Users/20200059/Documents/Github/simulations_beam_search_markov_chain/data_output/results_revised_manuscript/' + name_dataset + '.xlsx'
    sheets = pd.read_excel(location, sheet_name=['result_rw_analysis', 'rw_analysis_info', 'considered_subgroups', 'general_params_pd'])

    result_rw_analysis = sheets['result_rw_analysis']
    rw_analysis_info = sheets['rw_analysis_info']
    considered_subgroups = sheets['considered_subgroups']
    general_params_pd = sheets['general_params_pd']

    return result_rw_analysis, rw_analysis_info, considered_subgroups, general_params_pd

def recalculate_parameters(quality_measure=None, best_order=None,
                           df=None, cols=None, attributes=None, 
                           quals=None, general_params=None,
                           desc_series=None,
                           bin_atts=None, num_atts=None, nom_atts=None, dt_atts=None):

    #lswithstrings = quals.loc['idx_sg'].strip()[1:-1].split(',')
    #idx = list(map(int, lswithstrings[0:-1]))
    #subgroup = df.loc[idx]

    #desc_series = sg.iloc[0, ].dropna().drop(['sg'])
    desc_dict = desc_series.apply(eval).to_dict()
    subgroup, idx_sg, subgroup_compl, idx_compl = dt.select_subgroup(description=desc_dict, df=df, 
                                                                     bin_atts=bin_atts, num_atts=num_atts, nom_atts=nom_atts,
                                                                     dt_atts=dt_atts)

    subgroup_params = qmo.calculate_subgroup_parameters(df=df, subgroup=subgroup, subgroup_compl=None, idx_sg=idx_sg,
                                                        attributes=attributes, quality_measure=quality_measure, start_at_order=best_order,
                                                        general_params=general_params, ref='dataset')

    return subgroup_params, idx_sg
              
def visualize_probs(tA=None, tpi=None, dif=None, states=None, order=None, title=None, name_fig=None, data_set=None):

    if order == 1 and data_set == 1:
        x_names = [('start')] + list(states)
        y_names = [('start')] + list(states)
        #x_names[0] = r'$\delta$TIR' #,$\uparrow$TBR'
    elif order == 1 and data_set == 2:
        new_order_states = ['BR2', 'BR1', 'IR', 'AR1', 'AR2']
        x_names = [('start')] + list(new_order_states)
        y_names = x_names.copy()
        new_columns = tA[new_order_states]
        tA = new_columns.reindex(new_order_states).copy()
    elif order == 2:
        new_order_states = ['BR2', 'BR1', 'IR', 'AR1', 'AR2']
        x_names = [('start')] + list(new_order_states)
        new_index = list(it.product(new_order_states, repeat=2))
        tA_new_columns = tA[new_order_states]
        new_values = tA_new_columns.reindex(new_index)
    elif order == 3:
        new_order_states = ['BR2', 'BR1', 'IR', 'AR1', 'AR2']
        x_names = [('start')] + list(new_order_states)
        new_index = list(it.product(new_order_states, repeat=3))
        tA_new_columns = tA[new_order_states]
        new_values = tA_new_columns.reindex(new_index)

    if dif:
        min_value = -0.5
        max_value = 0.5
        cmap = 'bwr' 
    else:
        min_value = 0
        max_value = 1
        cmap = 'Purples'

    # create a 1 X 2 grid 
    if order == 1:

        fig = plt.figure(figsize=(8, 6), dpi=300, facecolor='w', edgecolor='k')
        gs = grd.GridSpec(1, 2, width_ratios=[14,1], wspace=0.1)

        # image plot
        ax0 = plt.subplot(gs[0])
        p = ax0.imshow(tA, aspect=1, vmin=min_value, vmax=max_value, cmap=plt.get_cmap(cmap))
        ax0.set_xticklabels(x_names, rotation=45)
        ax0.set_yticklabels(y_names)
        plt.title(title)

        colorAx = plt.subplot(gs[1])
        cb = plt.colorbar(p, cax=colorAx)
        cb.set_clim(min_value, max_value)
        
        fig.savefig(name_fig, bbox_inches='tight')

    elif order == 2:

        fig = plt.figure(figsize=(8, 16), dpi=300, facecolor='w', edgecolor='k')
        gs = grd.GridSpec(1, 2, width_ratios=[28,1])

        # image plot
        ax0 = plt.subplot(gs[0])
        p = ax0.imshow(new_values, aspect=0.5, vmin=min_value, vmax=max_value, cmap=plt.get_cmap(cmap))
        ax0.set_xticklabels(x_names, rotation=45)
        ax0.set_yticks(np.arange(len(new_values)))
        ax0.set_yticklabels(new_index)
        plt.title(title)

        colorAx = plt.subplot(gs[1])
        cb = plt.colorbar(p, cax=colorAx)
        cb.set_clim(min_value, max_value)
        
        fig.savefig(name_fig, bbox_inches='tight')

    elif order == 3:

        fig = plt.figure(figsize=(8, 24), dpi=300, facecolor='w', edgecolor='k')
        gs = grd.GridSpec(1, 2, width_ratios=[28,1])

        # image plot
        ax0 = plt.subplot(gs[0])
        p = ax0.imshow(new_values, aspect=0.33, vmin=min_value, vmax=max_value, cmap=plt.get_cmap(cmap))
        ax0.set_xticklabels(x_names, rotation=45)
        ax0.set_yticks(np.arange(len(new_values)))
        ax0.set_yticklabels(new_index)
        plt.title(title)

        colorAx = plt.subplot(gs[1])
        cb = plt.colorbar(p, cax=colorAx)
        cb.set_clim(min_value, max_value)
        
        fig.savefig(name_fig, bbox_inches='tight')

    return fig

def combined_visualize_probs(tA_subgroup=None, tA_data=None, dif=None, states=None, order=None, data_set=None,
                             order_data=None, title1=None, title2=None, title3=None, name_fig=None):

    # this will be for data set 1
    if order == 1 and order_data == 1:

        x_names = [('start')] + list(states)
        y_names = [('start')] + list(states)

        fig = plt.figure(figsize=(24, 6), dpi=300, facecolor='w', edgecolor='k')
        gs = grd.GridSpec(1, 5, width_ratios=[14, 14, 1, 14, 1])

        # image plot
        ax0 =  plt.subplot(gs[0])
        p = ax0.imshow(tA_data, aspect='auto', vmin=0.0, vmax=1.0, cmap=plt.get_cmap('Purples'))
        ax0.set_xticklabels(x_names, rotation=45)
        ax0.set_yticklabels(y_names)
        plt.title(title1)

        # second
        ax1 =  plt.subplot(gs[1])
        p1 = ax1.imshow(tA_subgroup, aspect='auto', vmin=0.0, vmax=1.0, cmap=plt.get_cmap('Purples'))
        ax1.set_xticklabels(x_names, rotation=45)
        ax1.set_yticklabels(["","","","","","",""])
        plt.title(title2)

        # colorbar
        colorAx = plt.subplot(gs[2])
        cb = plt.colorbar(p1, cax=colorAx)
        cb.set_clim(0.0, 1.0)
        colorAx.yaxis.set_ticks_position('left')

        # image plot
        ax3 = plt.subplot(gs[3])
        p2 = ax3.imshow(dif, aspect='auto', vmin=-0.5, vmax=0.5, cmap=plt.get_cmap('bwr'))
        ax3.set_xticklabels(x_names, rotation=45)
        ax3.set_yticklabels(y_names)
        plt.title(title3)

        # colorbar
        colorAx = plt.subplot(gs[4])
        cb2 = plt.colorbar(p2, cax=colorAx)
        cb2.set_clim(-0.5, 0.5)
        colorAx.yaxis.set_ticks_position('left')

        fig.savefig(name_fig, bbox_inches='tight')
    
    # this will be for data set 2
    elif order == 1 and order_data == 2:

        x_names = [('start')] + list(states)
        y_names = [('start')] + list(states)

        new_order_states = ['BR2', 'BR1', 'IR', 'AR1', 'AR2']
        x_names = [('start')] + list(new_order_states)
        y_names = x_names.copy()
        tA_new_columns = tA_subgroup[new_order_states]
        new_values_subgroup = tA_new_columns.reindex(new_order_states)

        new_order_states = ['BR2', 'BR1', 'IR', 'AR1', 'AR2']
        tA_data_new_columns = tA_data[new_order_states]
        new_index = list(it.product(new_order_states, repeat=2))
        new_values_data = tA_data_new_columns.reindex(new_index)

        fig = plt.figure(figsize=(18, 16), dpi=300, facecolor='w', edgecolor='k')
        gs = grd.GridSpec(1, 3, width_ratios=[14, 14, 1])

        # image plot
        ax0 =  plt.subplot(gs[0])
        p = ax0.imshow(new_values_data, aspect=0.5, vmin=0.0, vmax=1.0, cmap=plt.get_cmap('Purples'))
        ax0.set_xticklabels(x_names, rotation=45)
        ax0.set_yticks(np.arange(len(new_values_data)))
        ax0.set_yticklabels(new_index)
        plt.title(title1)

        # second
        ax1 =  plt.subplot(gs[1])
        p1 = ax1.imshow(new_values_subgroup, aspect=1, vmin=0.0, vmax=1.0, cmap=plt.get_cmap('Purples'))
        ax1.set_xticklabels(x_names, rotation=45)
        ax1.set_yticklabels(y_names)
        plt.title(title2)

        # colorbar
        colorAx = plt.subplot(gs[2])
        cb = plt.colorbar(p1, cax=colorAx)
        cb.set_clim(0.0, 1.0)
        colorAx.yaxis.set_ticks_position('left')

        fig.savefig(name_fig, bbox_inches='tight')

    elif order == 2 and order_data == 2:

        x_names = [('start')] + list(states)
        y_names = [('start')] + list(states)

        new_order_states = ['BR2', 'BR1', 'IR', 'AR1', 'AR2']
        x_names = [('start')] + list(new_order_states)
        new_index = list(it.product(new_order_states, repeat=2))
        tA_data_new_columns = tA_data[new_order_states]
        new_values_data = tA_data_new_columns.reindex(new_index)
        tA_subgroup_new_columns = tA_subgroup[new_order_states]
        new_values_subgroup = tA_subgroup_new_columns.reindex(new_index)
        dif_new_columns = dif[new_order_states]
        new_values_dif = dif_new_columns.reindex(new_index)

        fig = plt.figure(figsize=(27, 16), dpi=300, facecolor='w', edgecolor='k')
        gs = grd.GridSpec(1, 5, width_ratios=[14, 14, 1, 14, 1], wspace=0.4)

        # image plot
        ax0 =  plt.subplot(gs[0])
        p = ax0.imshow(new_values_data, aspect=0.5, vmin=0.0, vmax=1.0, cmap=plt.get_cmap('Purples'))
        ax0.set_xticklabels(x_names, rotation=45)
        ax0.set_yticks(np.arange(len(new_values_data)))
        ax0.set_yticklabels(new_index)
        plt.title(title1)

        # second
        ax1 =  plt.subplot(gs[1])
        p1 = ax1.imshow(new_values_subgroup, aspect=0.5, vmin=0.0, vmax=1.0, cmap=plt.get_cmap('Purples'))
        ax1.set_xticklabels(x_names, rotation=45)
        ax1.set_yticklabels([""])
        plt.title(title2)

        # colorbar
        colorAx = plt.subplot(gs[2])
        cb = plt.colorbar(p1, cax=colorAx)
        cb.set_clim(0.0, 1.0)
        colorAx.yaxis.set_ticks_position('left')

        # image plot
        ax3 = plt.subplot(gs[3])
        p2 = ax3.imshow(new_values_dif, aspect=0.5, vmin=-0.5, vmax=0.5, cmap=plt.get_cmap('bwr'))
        ax3.set_xticklabels(x_names, rotation=45)
        ax3.set_yticks(np.arange(len(new_values_dif)))
        ax3.set_yticklabels(new_index)
        plt.title(title3)

        # colorbar
        colorAx = plt.subplot(gs[4])
        cb2 = plt.colorbar(p2, cax=colorAx)
        cb2.set_clim(-0.5, 0.5)
        colorAx.yaxis.set_ticks_position('left')

        fig.savefig(name_fig, bbox_inches='tight')

    return fig

'''
# execute for data 1
result_rw_analysis, rw_analysis_info, considered_subgroups, general_params_pd = load(name_dataset='TIRpatientendata_1_20210114_resultset')
results = result_rw_analysis.copy()

dataset, attributes, combinations = rwdto.load(name_dataset='TIRpatientendata_1')  
df, cols, bin_atts, nom_atts, num_atts, dt_atts, idx = dt.read_data(dataset=dataset, attributes=attributes)
quality_measure = 'phiaic'
general_params = qmo.calculate_general_parameters(df=df, distribution=None, cols=cols, attributes=attributes, order=1, 
                                                  start_at_order=1, quality_measure=quality_measure)

# figure general params
fig = visualize_probs(tA=general_params['probs']['prob_1'], tpi=None, states=general_params['states'],
                      order=1, data_set=1,
                      title='Parameters entire dataset', name_fig='figures/Figures_manuscript/dialect_set1/finished_figures/visualization_general.png')

for sgn in [0,12]:

    sg = results.loc[results.sg == sgn, ]
    desc = sg.iloc[0, ].dropna().drop(['sg']).to_dict()
    print(desc)
    quals = sg.iloc[1, ].dropna()
    order = int(quals.loc['best_order'])

    if order == 0:
        order = 1

    subgroup_params, idx = recalculate_parameters(quality_measure=quality_measure, best_order=order,
                                                     df=dataset, cols=cols, attributes=attributes, 
                                                     quals=quals, general_params=general_params)

    title = 'Parameters subgroup ' + str(sgn+1) 
    name_fig = 'figures/Figures_manuscript/dialect_set1/finished_figures/visualization_' + str(sgn+1) + '_' + quality_measure + '.png'
    prob_name = 'prob_' + str(order)
    state_space = 'empty_lss_' + str(order)
    fig = visualize_probs(tA=subgroup_params['probs'][prob_name], tpi=None, states=general_params['states'], data_set=1,
                          order=order, title=title, name_fig=name_fig)

    dif = subgroup_params['probs'][prob_name] - general_params['probs']['prob_1']
    title = 'Parameter difference of subgroup ' + str(sgn+1) 
    name_fig = 'figures/Figures_manuscript/dialect_set1/finished_figures/visualization_difference' + str(sgn+1) + '_' + quality_measure + '.png'
    fig = visualize_probs(tA=dif, tpi=None, dif=True, states=general_params['states'], data_set=1,
                          order=order, title=title, name_fig=name_fig)

    # combine three figures
    fig = combined_visualize_probs(tA_subgroup=subgroup_params['probs'][prob_name], 
                                   tA_data=general_params['probs']['prob_1'], dif=dif, states=general_params['states'], order=order, 
                                   order_data=1, data_set=1,
                                   title1='Parameters entire dataset (chart 1)', title2='Parameters subgroup ' + str(sgn+1) + ' (chart 2)', 
                                   title3='Difference in parameters subgroup ' + str(sgn+1) + ' (chart 2 - chart 1)', 
                                   name_fig='figures/Figures_manuscript/dialect_set1/finished_figures/visualization_combined_' + str(sgn+1) + '_' + quality_measure + '.png')

'''
# execute for data 2
result_rw_analysis, rw_analysis_info, considered_subgroups, general_params_pd = load(name_dataset='TIRpatientendata_2_20210504_resultset')
results = result_rw_analysis.copy()

dataset, attributes, combinations = rwdto.load(name_dataset='TIRpatientendata_2')  
df, cols, bin_atts, nom_atts, num_atts, dt_atts, idx = dt.read_data(dataset=dataset, attributes=attributes)
quality_measure = 'phiaic'
order_data = 2
general_params = qmo.calculate_general_parameters(df=df, distribution=None, cols=cols, attributes=attributes, order=order_data, 
                                                  start_at_order=order_data, quality_measure=quality_measure)

# figure general params
prob = 'prob_' + str(order_data)
fig = visualize_probs(tA=general_params['probs'][prob], tpi=None, states=general_params['states'], data_set=order_data,
                      order=order_data, title='Parameters entire dataset', name_fig='figures/Figures_revised_manuscript/visualization_general.png')

for sgn in [1]:#[0,3]:

    sg = results.loc[results.sg == sgn, ]
    desc_series = sg.iloc[0, ].dropna().drop(['sg'])
    #desc = sg.iloc[0, ].dropna().drop(['sg']).to_dict()
    print(desc_series)
    quals = sg.iloc[1, ].dropna()
    order = int(quals.loc['best_order'])

    if order == 0:
        order = 1

    subgroup_params, idx = recalculate_parameters(quality_measure=quality_measure, best_order=order,
                                                  df=dataset, cols=cols, attributes=attributes, 
                                                  quals=quals, general_params=general_params,
                                                  desc_series=desc_series,
                                                  bin_atts=bin_atts, num_atts=num_atts, nom_atts=nom_atts, dt_atts=dt_atts)

    '''
    subgroup_params, idx = recalculate_parameters(quality_measure=quality_measure, best_order=order,
                                                  df=dataset, cols=cols, attributes=attributes, 
                                                  quals=quals, general_params=general_params)
    '''

    title = 'Parameters subgroup ' + str(sgn+1)
    name_fig = 'figures/Figures_revised_manuscript/visualization_' + str(sgn+1) + '_' + quality_measure + '.png'
    prob_name = 'prob_' + str(order)
    state_space = 'empty_lss_' + str(order)
    fig = visualize_probs(tA=subgroup_params['probs'][prob_name], tpi=None, dif=None,
                          states=general_params['states'], data_set=2,
                          order=order, title=title, name_fig=name_fig)

    if order == 1 and order_data == 2:

        # combine three figures
        fig = combined_visualize_probs(tA_subgroup=subgroup_params['probs'][prob_name], 
                                       tA_data=general_params['probs']['prob_2'], dif=None, states=general_params['states'], order=order, 
                                       order_data=2, data_set=2,
                                       title1='Parameters entire dataset', title2='Parameters subgroup ' + str(sgn+1), 
                                       title3=None, name_fig='figures/Figures_revised_manuscript/visualization_combined_' + str(sgn+1) + '_' + quality_measure + '.png')

    elif order == 2 and order_data == 2:
        
        dif = subgroup_params['probs'][prob_name] - general_params['probs']['prob_2']
        title = 'Parameter difference of subgroup ' + str(sgn+1)
        name_fig = 'figures/Figures_revised_manuscript/visualization_difference_' + str(sgn+1) + '_' + quality_measure + '.png'
        fig = visualize_probs(tA=dif, tpi=None, dif=True, states=general_params['states'], data_set=2,
                              order=order, title=title, name_fig=name_fig)

        # combine three figures
        fig = combined_visualize_probs(tA_subgroup=subgroup_params['probs'][prob_name], 
                                       tA_data=general_params['probs']['prob_2'], dif=dif, states=general_params['states'], order=order, 
                                       order_data=2, data_set=2,
                                       title1='Parameters entire dataset (chart 1)', title2='Parameters subgroup ' + str(sgn+1) + ' (chart 2)', 
                                       title3='Difference in parameters subgroup ' + str(sgn+1) + ' (chart 2 - chart 1)', 
                                       name_fig='figures/Figures_revised_manuscript/visualization_combined_' + str(sgn+1) + '_' + quality_measure + '.png')

