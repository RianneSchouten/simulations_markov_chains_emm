import numpy as np
import pandas as pd

import read_callcenter_example as rce
import read_studyportals as rsp
import read_dialect_glucose as rdg

# callcenter example
# from fluxicon
#data, time_attributes, skip_attributes, id_attribute, first_timepoint, descriptives = rce.read_callcenter_example(name_dataset='callcenter_example')

# studyportals
#data, attributes = rsp.read_studyportals(name_dataset='studyportals')

# dialect
data, attributes, combinations = rdg.read_dialect_glucose(name_dataset='C:/Users/20200059/Documents/Projects/Dialect/Diabetes ZGT data/TIRpatientendata', type_states=1)
#data, attributes, combinations = rdg.read_dialect_glucose(name_dataset='C:/Users/20200059/Documents/Projects/Dialect/Diabetes ZGT data/TIRpatientendata', type_states=2)

print('attributes', attributes)
print('data', data.head(10))
print('combinations', combinations)

