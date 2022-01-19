# simulations_beam_search_markov_chain

This repository contains the code for the experiments in the manuscript [Mining Sequences with Exceptional Transition Behaviour of Varying Order using Quality Measures based on Information-Theoretic Scoring Functions](https://rianneschouten.github.io/pdfs/MiningExceptionalSequences_DAMI_2021.pdf)', published in the journal Data Mining and Knowledge Discovery (DAMI).

The files are the result of a long development period, and you will therefore also find files and results for the Work In Progress paper `Mining exceptional sequences using log likelihood based quality measures' presented at the PhD Forum at ECML-PKDD 2020, and for a draft version of the manuscript mentioned above.

The scripts for the extended beam_search algorithm, the synthetic data exeperiments, and the analysis of real-world data can all directly be found in the repository.

Start with:

- main.py if you want to check the experiments with synthetic data
- main_real_world_data_orders if you want to check the experiments with real-world data

There are 4 folders:

- data_output: contains the results of both the experiments with synthetic data and with real-world data
- data_input: contains the scripts for reading the real-world data and the data for one real-world dataset
- figures: contains the visualizations for the several papers. The script in Figures_revised_manuscript contains the figures for the latest version (May 2021). Note that that script is used to create the figures for the synthetic data experiment. The figures for real-world data experiments are created with figures_dialect_version2.py (in the main repository)
- earlier_versions: contains scripts used for earlier versions of the manuscript, such as functions_firstorderchain, which contains the scripts that are used to run simulations with first order markov chains. These scripts were mainly used for the WIP paper mentioned above.

Let me know if things are unclear and reach out to me if you have any questions.

Bests,
