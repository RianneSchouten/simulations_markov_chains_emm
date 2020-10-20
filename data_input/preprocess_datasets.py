import numpy as np
import pandas as pd

import read_callcenter_example as rce
import read_studyportals as rsp
import read_dialect_glucose as rdg

# callcenter example
# from fluxicon
#data, time_attributes, skip_attributes, id_attribute, first_timepoint, descriptives = rce.read_callcenter_example(name_dataset='callcenter_example')

# studyportals
#data, time_attributes, skip_attributes, id_attribute, first_timepoint, descriptives = rsp.read_studyportals(name_dataset='studyportals')

# dialect
data, time_attributes, skip_attributes, id_attribute, first_timepoint, descriptives = rdg.read_dialect_glucose(name_dataset='TIRpatientendata')

print('descriptives', descriptives)
print('length descriptives', len(descriptives))
print('number of states', len(data[time_attributes[1]].unique()))
print('length data', len(data))
print('time_attributes', time_attributes)
print('skip_attributes', skip_attributes)
print('id_attribute', id_attribute)
print('first_timepoint', first_timepoint)
print('data', data.head(10))

