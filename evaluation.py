import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as grd

def visualize_probs(tA=None, tpi=None, title=None, name_fig=None):

    fig = plt.figure()

    # create a 2 X 2 grid 
    gs = grd.GridSpec(2, 2, height_ratios=[1,7], width_ratios=[7,1], wspace=0.1)

    # image plot
    ax0 = plt.subplot(gs[0])
    ax0.imshow(np.atleast_2d(tpi), aspect='auto', vmin=0, vmax=1)
    ax0.set_yticks([])
    plt.title(title)

    ax2 = plt.subplot(gs[2])
    p = ax2.imshow(tA, aspect='auto', vmin=0, vmax=1)

    colorAx = plt.subplot(gs[3])
    cb = plt.colorbar(p, cax = colorAx)
    cb.set_label('probability')

    fig.savefig(name_fig, bbox_inches='tight')
      
    return fig

def evaluation_figures(result_rw_analysis=None, general_params=None, quality_measures=None, sg=None, log_transform=None):

    if log_transform:
        tA = np.log(general_params['tA'])
        tpi = np.log(general_params['tpi'])
    else:
        tA = general_params['tA']
        tpi = general_params['tpi']
    
    fig = visualize_probs(tA=tA, tpi=tpi, title='General parameters', name_fig='figures/visualization_general.png')

    for quality_measure in quality_measures:

        sg1tA = result_rw_analysis.loc[(result_rw_analysis.qm==quality_measure) & 
                                       (result_rw_analysis.sg==sg), 'tA'].values[1]
        sg1tpi = result_rw_analysis.loc[(result_rw_analysis.qm==quality_measure) & 
                                       (result_rw_analysis.sg==sg), 'tpi'].values[1]
        
        title = 'Subgroup_' + str(sg) + '_' + quality_measure
        name_fig = 'figures/visualization_' + str(sg) + '_' + quality_measure

        if log_transform:
            sg1tA = np.log(sg1tA)
            sg1tpi = np.log(sg1tpi)

        fig = visualize_probs(tA=sg1tA, tpi=sg1tpi, title=title, name_fig=name_fig)
