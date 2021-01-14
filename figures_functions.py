import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as grd

import qualities_orders as qmo

def load(name_dataset=None):

    location = 'C:/Users/20200059/Documents/Github/simulations_beam_search_markov_chain/data_output/' + name_dataset + '.xlsx'
    sheets = pd.read_excel(location, sheet_name=['result_rw_analysis', 'rw_analysis_info', 'considered_subgroups', 'general_params_pd'])

    result_rw_analysis = sheets['result_rw_analysis']
    rw_analysis_info = sheets['rw_analysis_info']
    considered_subgroups = sheets['considered_subgroups']
    general_params_pd = sheets['general_params_pd']

    return result_rw_analysis, rw_analysis_info, considered_subgroups, general_params_pd

def recalculate_parameters(quality_measure=None, best_order=None,
                           df=None, cols=None, attributes=None, 
                           quals=None, general_params=None):

    lswithstrings = quals.loc['idx_sg'].strip()[1:-1].split(',')
    idx = list(map(int, lswithstrings[0:-1]))
    subgroup = df.loc[idx]

    subgroup_params = qmo.calculate_subgroup_parameters(df=df, subgroup=subgroup, subgroup_compl=None, idx_sg=idx,
                                                        attributes=attributes, quality_measure=quality_measure, start_at_order=best_order,
                                                        general_params=general_params, ref='dataset')

    return subgroup_params, idx
              
def visualize_probs(tA=None, tpi=None, states=None, order=None, y_names=None, title=None, name_fig=None):

    fig = plt.figure()

    tA[tA == 0.0000000000001] = 0
    tpi[tpi == 0.0000000000001] = 0

    tpi_reshape = np.array(tpi.values).reshape(1,len(tpi.values))

    states = list(states)
    x_names = ['start'] + states
    y_names = list(y_names) #[('start')] + list(y_names)

    # create a 2 X 2 grid 
    if order == 1:
        gs = grd.GridSpec(2, 2, height_ratios=[1,7], width_ratios=[7,1], wspace=0.1)

        # image plot
        ax0 = plt.subplot(gs[0])
        ax0.imshow(tpi_reshape, aspect='auto', vmin=0, vmax=1)
        ax0.set_yticks([])
        ax0.set_xticks([])
        plt.title(title)

        ax2 = plt.subplot(gs[2])
        p = ax2.imshow(tA, aspect='auto', vmin=0, vmax=1)
        ax2.set_xticklabels(x_names)
        ax2.set_yticklabels(y_names)

        colorAx = plt.subplot(gs[3])
        cb = plt.colorbar(p, cax = colorAx)
        cb.set_label('probability')

        fig.savefig(name_fig, bbox_inches='tight')
    else:
        gs = grd.GridSpec(1, 2, width_ratios=[7,1], wspace=0.1)

        # image plot

        plt.title(title)

        ax2 = plt.subplot(gs[0])
        p = ax2.imshow(tA, aspect='auto', vmin=0, vmax=1)
        ax2.set_xticklabels(x_names)
        ax2.set_yticks(np.arange(len(tA)))
        ax2.set_yticklabels(y_names)
        plt.title(title)

        colorAx = plt.subplot(gs[1])
        cb = plt.colorbar(p, cax = colorAx)
        cb.set_label('probability')

        fig.savefig(name_fig, bbox_inches='tight')
      
    return fig