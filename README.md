# simulations_beam_search_markov_chain

This repository contains the code for the experiments in the manuscript `Mining sequences with exceptional transition behaviour of varying order using quality measures based on information-theoretic scoring functions', submitted to the journal Data Mining and Knowledge Discovery (DMKD) on January 31st 2021. 

The files are the result of a long development period, and you will therefore also find files and results for the Work In Progress paper `mining exceptional sequences using log likelihood based quality measures' presented at the PhD Forum at ECML-PKDD 2020, and for a draft version of the manuscript mentioned above.

The scripts for the extended beam_search algorithm, the synthetic data exeperiments, and the analysis of real-world data can all directly be found in the repository. Start with:

- main.py if you want to check the experiments with synthetic data
- main_real_world_data_orders if you want to check the experiments with real-world data

There are 4 folders:

- data_output: contains the results of both the experiments with synthetic data and with real-world data
- data_input: contains the scripts for reading the real-world data (but not the data itself)
- figures: contains the visualizations for the several papers. Note that Figures.R is used to create the figures for the synthetic data experiment. The figures for real-world data experiments are created with figures_dialect.py, figures.py and figures_functios.py (in the main repository)
- functions_firstorderchain: contains the old scripts that are used to run simulations with first order markov chains. These scripts were mainly used for the WIP paper mentioned above.

Let me know if things are unclear and reach out to me if you have any questions.

Bests,
