# simulations_markov_chains_emm

The simulations start with main.py, with output stored in data_output. The synthetic data is generated in simulate_sequence.py.
The beam_search occurs in the file of the same name, with the quality measures calculated in measures.py (characteristics of the data) and qualities.py (the real quality value).

The processing of real-world datasets happens in data_input. Analyzing this data then starts in main_real_world_data.py.
For every dataset, a distribution_false_discoveries is built first, stored in data_output and can be used in later runs.

The file run.txt can be used to run the simulation on a server.
