import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as grd
import itertools as it
import matplotlib.colors as colors

import emm_rw_dataset_orders as rwdto
import dataset as dt
import qualities_orders as qmo

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

    desc_dict = desc_series.apply(eval).to_dict()
    subgroup, idx_sg, subgroup_compl, idx_compl = dt.select_subgroup(description=desc_dict, df=df, 
                                                                     bin_atts=bin_atts, num_atts=num_atts, nom_atts=nom_atts,
                                                                     dt_atts=dt_atts)

    subgroup_params = qmo.calculate_subgroup_parameters(df=df, subgroup=subgroup, subgroup_compl=None, idx_sg=idx_sg,
                                                        attributes=attributes, quality_measure=quality_measure, start_at_order=best_order,
                                                        general_params=general_params)

    return subgroup_params, idx_sg

def make_one_pic(data=None, x_names=None, y_names=None, order=None, dif=None, title=None, name_fig=None):

    if order == 1:
        height = 6
        width_ratio = [14,1]
        aspect = 1.
        ysize = 15
        titlesize = 18
    
    if order == 2:
        height = 16
        width_ratio = [28,1]
        aspect = 0.5
        ysize = 22
        titlesize = 20

    if dif:
        min_value = -0.5
        max_value = 0.5
        cmap = 'bwr' 
    else:
        min_value = 0
        max_value = 1
        cmap = 'Purples'

    fig = plt.figure(figsize=(8, height), dpi=300, facecolor='w', edgecolor='k')
    gs = grd.GridSpec(1, 2, width_ratios=width_ratio)

    # image plot
    ax0 = plt.subplot(gs[0])
    p = ax0.imshow(data, aspect=aspect, vmin=min_value, vmax=max_value, cmap=plt.get_cmap(cmap))
    ax0.set_xticklabels(x_names, rotation=45)
    ax0.set_yticks(np.arange(len(y_names)))
    ax0.set_yticklabels(y_names)
    for tick in ax0.xaxis.get_major_ticks():
        tick.label.set_fontsize(15)
    for tick in ax0.yaxis.get_major_ticks():
        tick.label.set_fontsize(ysize)
    plt.title(title, fontsize=titlesize)

    colorAx = plt.subplot(gs[1])
    cb = plt.colorbar(p, cax=colorAx)
    cb.set_clim(min_value, max_value)
        
    fig.savefig(name_fig, bbox_inches='tight')


### DIALECT dataset 2, long sequences, section 6.1 in revised manuscript

result_rw_analysis, rw_analysis_info, considered_subgroups, general_params_pd = load(name_dataset='TIRpatientendata_2_20210514_resultset')
results = result_rw_analysis.copy()

dataset, attributes, combinations = rwdto.load(name_dataset='TIRpatientendata_2')  
df, cols, bin_atts, nom_atts, num_atts, dt_atts, idx = dt.read_data(dataset=dataset, attributes=attributes)
quality_measure = 'phiaic'
general_params = qmo.calculate_general_parameters(df=df, cols=cols, attributes=attributes, order=2, 
                                                  start_at_order=2, stop_at_order=1, quality_measure=quality_measure)

# figure general params, order = 2
data = general_params['probs']['prob_2']
new_order_states = ['BR2', 'BR1', 'IR', 'AR1', 'AR2']
x_names = [('start')] + list(new_order_states)
new_index = list(it.product(new_order_states, repeat=2))
data_new_columns = data[new_order_states]
data_new_values = data_new_columns.reindex(new_index)

'''
fig = make_one_pic(data=data_new_values, x_names=x_names, y_names=new_index, order=2, dif = False,
                   title='Parameters entire dataset', name_fig='figures/Figures_revised_manuscript/visualization_dialect_long_general.png')
'''

# figure sg 0
sgn = 0
print(sgn)
sg = results.loc[results.sg == sgn, ]
desc_series = sg.iloc[0, ].dropna().drop(['sg'])
print(desc_series)
quals = sg.iloc[1, ].dropna()
order = int(quals.loc['best_order'])

subgroup_params_0, idx = recalculate_parameters(quality_measure=quality_measure, best_order=order,
                                                    df=dataset, cols=cols, attributes=attributes, 
                                                    quals=quals, general_params=general_params,
                                                    desc_series=desc_series,
                                                    bin_atts=bin_atts, num_atts=num_atts, nom_atts=nom_atts, dt_atts=dt_atts)

data = subgroup_params_0['probs']['prob_1']
new_order_states = ['BR2', 'BR1', 'IR', 'AR1', 'AR2']
x_names = [('start')] + list(new_order_states)
new_columns = data[new_order_states]
data_new_values = new_columns.reindex(new_order_states).copy()
fig = make_one_pic(data=data_new_values, x_names=x_names, y_names=new_order_states, order=1, dif = False,
                   title='Parameter estimates subgroup 1', name_fig='figures/Figures_revised_manuscript/visualization_dialect_long_sg1.png')

# figure subgroup 1, calculate difference with subgroup 0
sgn = 1
print(sgn)
sg = results.loc[results.sg == sgn, ]
desc_series = sg.iloc[0, ].dropna().drop(['sg'])
print(desc_series)
quals = sg.iloc[1, ].dropna()
order = int(quals.loc['best_order'])
print(order)

subgroup_params_1, idx = recalculate_parameters(quality_measure=quality_measure, best_order=order,
                                                  df=dataset, cols=cols, attributes=attributes, 
                                                  quals=quals, general_params=general_params,
                                                  desc_series=desc_series,
                                                  bin_atts=bin_atts, num_atts=num_atts, nom_atts=nom_atts, dt_atts=dt_atts)


data = subgroup_params_1['probs']['prob_1']
data_dif_10 = data - subgroup_params_0['probs']['prob_1']
new_order_states = ['BR2', 'BR1', 'IR', 'AR1', 'AR2']
x_names = [('start')] + list(new_order_states)
new_columns = data_dif_10[new_order_states]
data_new_values_10 = new_columns.reindex(new_order_states).copy()

'''
fig = make_one_pic(data=data_new_values_10, x_names=x_names, y_names=new_order_states, order=1, dif = True,
                   title='Difference between SG 2 and SG 1', name_fig='figures/Figures_revised_manuscript/visualization_dialect_long_difference_sg2_sg1.png')
'''

# figure subgroup 5, calculate difference with general params
sgn = 5
print(sgn)
sg = results.loc[results.sg == sgn, ]
desc_series = sg.iloc[0, ].dropna().drop(['sg'])
print(desc_series)
quals = sg.iloc[1, ].dropna()
order = int(quals.loc['best_order'])
print(order)

subgroup_params_5, idx = recalculate_parameters(quality_measure=quality_measure, best_order=order,
                                                df=dataset, cols=cols, attributes=attributes, 
                                                quals=quals, general_params=general_params,
                                                desc_series=desc_series,
                                                bin_atts=bin_atts, num_atts=num_atts, nom_atts=nom_atts, dt_atts=dt_atts)


data = subgroup_params_5['probs']['prob_2']
data_dif_5 = subgroup_params_5['probs']['prob_2'] - general_params['probs']['prob_2']
new_order_states = ['BR2', 'BR1', 'IR', 'AR1', 'AR2']
x_names = [('start')] + list(new_order_states)
new_index = list(it.product(new_order_states, repeat=2))
data_new_columns_5 = data_dif_5[new_order_states]
data_new_values_5 = data_new_columns_5.reindex(new_index)

'''
fig = make_one_pic(data=data_new_values_5, x_names=x_names, y_names=new_index, order=2, dif = False,
                   title='Parameters 5', name_fig='figures/Figures_revised_manuscript/visualization_dialect_long_subgroup5.png')
'''
'''
fig = make_one_pic(data=data_new_values_5, x_names=x_names, y_names=new_index, order=2, dif = True,
                   title='Difference SG 6 and global model', name_fig='figures/Figures_revised_manuscript/visualization_dialect_long_difference_sg6_global_model.png')
'''

# subgroup 1 and 5 in one figure
fig = plt.figure(figsize=(18, 16), dpi=300, facecolor='w', edgecolor='k')
gs = grd.GridSpec(1, 3, width_ratios=[18, 14, 0.1])

# first
ax0 =  plt.subplot(gs[0])
p0 = ax0.imshow(data_new_values_10, aspect=1, vmin=-0.5, vmax=0.5, cmap=plt.get_cmap('bwr'))
ax0.set_xticklabels(x_names, rotation=45)
ax0.set_yticklabels(x_names)
for tick in ax0.xaxis.get_major_ticks():
    tick.label.set_fontsize(15)
for tick in ax0.yaxis.get_major_ticks():
    tick.label.set_fontsize(18)
plt.title('Difference between SG 2 and SG 1', fontsize=18)

# second
ax1 =  plt.subplot(gs[1])
p1 = ax1.imshow(data_new_values_5, aspect=0.5, vmin=-0.5, vmax=0.5, cmap=plt.get_cmap('bwr'))
ax1.set_xticklabels(x_names, rotation=45)
ax1.set_yticks(np.arange(len(new_index)))
ax1.set_yticklabels(new_index)
for tick in ax1.xaxis.get_major_ticks():
    tick.label.set_fontsize(15)
for tick in ax1.yaxis.get_major_ticks():
    tick.label.set_fontsize(18)
plt.title('Difference SG 6 and global model', fontsize=20)

# colorbar
cbaxes = fig.add_axes([0.82, 0.185, 0.02, 0.62])  
#colorAx = plt.subplot(gs[2])
cb = plt.colorbar(p1, cax=cbaxes)
cb.set_clim(-0.5,0.5)
cb.ax.tick_params(labelsize=15)
#colorAx.yaxis.set_ticks_position('right')

fig.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.8, hspace=None)
fig.savefig('figures/Figures_revised_manuscript/visualization_dialect_long_difference_sg2_sg6_oneplot.png', bbox_inches='tight')

### Dataset 1, Experiment 2, Sect. 6.1
result_rw_analysis, rw_analysis_info, considered_subgroups, general_params_pd = load(name_dataset='TIRpatientendata_1_20210514_resultset')
results = result_rw_analysis.copy()

dataset, attributes, combinations = rwdto.load(name_dataset='TIRpatientendata_1')  
df, cols, bin_atts, nom_atts, num_atts, dt_atts, idx = dt.read_data(dataset=dataset, attributes=attributes)
quality_measure = 'phiaic'
general_params = qmo.calculate_general_parameters(df=df, cols=cols, attributes=attributes, order=1, 
                                                  start_at_order=1, stop_at_order=1, quality_measure=quality_measure)

# figure general params, order = 1
data = general_params['probs']['prob_1']
new_order_states = ['AA', 'AB', 'AC', 'AE', 'AF', 'AG', 'AH']
x_names = [('start')] + list(new_order_states)
new_columns = data[new_order_states]
data_new_values = new_columns.reindex(new_order_states).copy()

'''
fig = make_one_pic(data=data_new_values, x_names=x_names, y_names=new_order_states, order=1, dif = False,
                   title='Parameters entire dataset', name_fig='figures/Figures_revised_manuscript/visualization_dialect_short_general.png')
'''

# figure sg 0, save parameters as well
sgn = 0
print(sgn)
sg = results.loc[results.sg == sgn, ]
desc_series = sg.iloc[0, ].dropna().drop(['sg'])
print(desc_series)
quals = sg.iloc[1, ].dropna()
order = int(quals.loc['best_order'])

subgroup_params_0, idx = recalculate_parameters(quality_measure=quality_measure, best_order=order,
                                                    df=dataset, cols=cols, attributes=attributes, 
                                                    quals=quals, general_params=general_params,
                                                    desc_series=desc_series,
                                                    bin_atts=bin_atts, num_atts=num_atts, nom_atts=nom_atts, dt_atts=dt_atts)

data = subgroup_params_0['probs']['prob_1']
data_dif_0 = subgroup_params_0['probs']['prob_1'] - general_params['probs']['prob_1']
new_order_states = ['AA', 'AB', 'AC', 'AE', 'AF', 'AG', 'AH']
x_names = [('start')] + list(new_order_states)
new_columns = data_dif_0[new_order_states]
data_new_values_0 = new_columns.reindex(new_order_states).copy()

'''
fig = make_one_pic(data=data_new_values_0, x_names=x_names, y_names=new_order_states, order=1, dif = True,
                   title='Difference SG 1 and global model', name_fig='figures/Figures_revised_manuscript/visualization_dialect_short_difference_sg1_global_model.png')
'''

# figure sg 1, save parameters as well
sgn = 1
print(sgn)
sg = results.loc[results.sg == sgn, ]
desc_series = sg.iloc[0, ].dropna().drop(['sg'])
print(desc_series)
quals = sg.iloc[1, ].dropna()
order = int(quals.loc['best_order'])

subgroup_params_1, idx = recalculate_parameters(quality_measure=quality_measure, best_order=order,
                                                    df=dataset, cols=cols, attributes=attributes, 
                                                    quals=quals, general_params=general_params,
                                                    desc_series=desc_series,
                                                    bin_atts=bin_atts, num_atts=num_atts, nom_atts=nom_atts, dt_atts=dt_atts)

data = subgroup_params_1['probs']['prob_1']
data_dif_1 = subgroup_params_1['probs']['prob_1'] - general_params['probs']['prob_1']
new_order_states = ['AA', 'AB', 'AC', 'AE', 'AF', 'AG', 'AH']
x_names = [('start')] + list(new_order_states)
new_columns = data_dif_1[new_order_states]
data_new_values_1 = new_columns.reindex(new_order_states).copy()

'''
fig = make_one_pic(data=data_new_values_1, x_names=x_names, y_names=new_order_states, order=1, dif = True,
                   title='Difference SG 2 and global model', name_fig='figures/Figures_revised_manuscript/visualization_dialect_short_difference_sg2_global_model.png')
'''

# figure sg 13, save parameters as well
sgn = 13
print(sgn)
sg = results.loc[results.sg == sgn, ]
desc_series = sg.iloc[0, ].dropna().drop(['sg'])
print(desc_series)
quals = sg.iloc[1, ].dropna()
order = int(quals.loc['best_order'])

subgroup_params_13, idx = recalculate_parameters(quality_measure=quality_measure, best_order=order,
                                                    df=dataset, cols=cols, attributes=attributes, 
                                                    quals=quals, general_params=general_params,
                                                    desc_series=desc_series,
                                                    bin_atts=bin_atts, num_atts=num_atts, nom_atts=nom_atts, dt_atts=dt_atts)

data = subgroup_params_13['probs']['prob_1']
data_dif_13 = subgroup_params_13['probs']['prob_1'] - general_params['probs']['prob_1']
new_order_states = ['AA', 'AB', 'AC', 'AE', 'AF', 'AG', 'AH']
x_names = [('start')] + list(new_order_states)
new_columns = data_dif_13[new_order_states]
data_new_values_13 = new_columns.reindex(new_order_states).copy()

'''
fig = make_one_pic(data=data_new_values_13, x_names=x_names, y_names=new_order_states, order=1, dif = True,
                   title='Difference SG 14 and global model', name_fig='figures/Figures_revised_manuscript/visualization_dialect_short_difference_sg14_global_model.png')
'''

# sg 0 and 13 in one plot
fig = plt.figure(figsize=(18, 16), dpi=300, facecolor='w', edgecolor='k')
gs = grd.GridSpec(1, 3, width_ratios=[14, 14, 1])

# first
ax0 =  plt.subplot(gs[0])
p0 = ax0.imshow(data_new_values_0, aspect=1, vmin=-0.5, vmax=0.5, cmap=plt.get_cmap('bwr'))
ax0.set_xticklabels(x_names, rotation=45)
ax0.set_yticklabels(x_names)
for tick in ax0.xaxis.get_major_ticks():
    tick.label.set_fontsize(15)
for tick in ax0.yaxis.get_major_ticks():
    tick.label.set_fontsize(18)
plt.title('Difference SG 1 and global model', fontsize=18)

# second
ax1 =  plt.subplot(gs[1])
p1 = ax1.imshow(data_new_values_13, aspect=1, vmin=-0.5, vmax=0.5, cmap=plt.get_cmap('bwr'))
ax1.set_xticklabels(x_names, rotation=45)
ax1.set_yticklabels(x_names)
for tick in ax1.xaxis.get_major_ticks():
    tick.label.set_fontsize(15)
for tick in ax1.yaxis.get_major_ticks():
    tick.label.set_fontsize(18)
plt.title('Difference SG 14 and global model', fontsize=18)

# colorbar
#colorAx = plt.subplot(gs[2])
cbaxes = fig.add_axes([0.88, 0.308, 0.02, 0.37])  
cb = plt.colorbar(p1, cax=cbaxes)
cb.set_clim(-0.5,0.5)
cb.ax.tick_params(labelsize=15)
#colorAx.yaxis.set_ticks_position('left')

fig.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.3, hspace=None)
fig.savefig('figures/Figures_revised_manuscript/visualization_dialect_short_difference_sg1_sg14_oneplot.png', bbox_inches='tight')