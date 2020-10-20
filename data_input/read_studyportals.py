import pandas as pd
import numpy as np

def read_studyportals(name_dataset=None):

    location = 'data_input/' + name_dataset + '.xlsx'
    data = pd.read_excel(location, sheet_name=0, header=0, parse_dates=['collector_tstamp'])

    data = data.sort_values(by=['userid_anonymized', 'counter'])
    data = data.drop(columns = ['collector_tstamp'])

    time_attributes = ['counter', 'page_url_corrected_1', 'page_url_corrected_2']
    id_attribute = 'userid_anonymized'
    first_timepoint = 1
    skip_attributes = ['br_name', 'os_family', 'os_timezone', 'in_subdomain_1', 'page_type_1', 'in_subdomain_2', 'page_type_2']

    cols = data.dtypes
    cols = cols.drop(time_attributes)
    cols = cols.drop(id_attribute)
    cols = cols.drop(skip_attributes)
    descriptives = cols.index.values

    return data, time_attributes, skip_attributes, id_attribute, first_timepoint, descriptives

