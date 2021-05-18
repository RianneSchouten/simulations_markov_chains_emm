import numpy as np
import pandas as pd

import read_movies as rm
import read_dialect_glucose as rdg

# deselect and run one row to preprocess dataset

# dialect
#data, attributes, combinations = rdg.read_dialect_glucose(name_dataset='C:/Users/20200059/Documents/Projects/Dialect/Diabetes ZGT data/TIRpatientendata', type_states=1) # experiment 6.1.2
#data, attributes, combinations = rdg.read_dialect_glucose(name_dataset='C:/Users/20200059/Documents/Projects/Dialect/Diabetes ZGT data/TIRpatientendata', type_states=2) # experiment 6.1.1

# movies
data, attributes, combinations = rm.read_movies(name_dataset='movies')
print('attributes', attributes)
print('data', data.head(10))
print('combinations', combinations)

