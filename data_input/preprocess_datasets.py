import numpy as np
import pandas as pd

import read_callcenter_example as rce
import read_studyportals as rsp
import read_logs as rl
import read_movies as rm
import read_dna as rdna
import read_wikispeedia as rw
import read_dialect_glucose as rdg

# callcenter example
# from fluxicon
#data, time_attributes, skip_attributes, id_attribute, first_timepoint, descriptives = rce.read_callcenter_example(name_dataset='callcenter_example')

# studyportals
#data, attributes, combinations = rsp.read_studyportals(name_dataset='studyportals')

# logs
#data, attributes, combinations = rl.read_logs(name_dataset='logs')

# movies
#data, attributes, combinations = rm.read_movies(name_dataset='movies')

# dna
#data, attributes, combinations = rdna.read_dna(name_dataset='dna')

# wikispeedia
data, attributes, combinations = rw.read_wikispeedia(name_dataset='wikispeedia')

# dialect
#data, attributes, combinations = rdg.read_dialect_glucose(name_dataset='C:/Users/20200059/Documents/Projects/Dialect/Diabetes ZGT data/TIRpatientendata', type_states=1)
#data, attributes, combinations = rdg.read_dialect_glucose(name_dataset='C:/Users/20200059/Documents/Projects/Dialect/Diabetes ZGT data/TIRpatientendata', type_states=2)

print('attributes', attributes)
print('data', data.head(10))
print('combinations', combinations)

