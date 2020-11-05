import numpy as np
import pandas as pd
import itertools as it
import emm_rw_dataset as rwdt

df, attributes = rwdt.load(name_dataset='ss')  

print('attributes', attributes)
print('data', df.tail(20))
print(df.isnull().sum().sum())
print(df.shape)

# have to move this to main
df['timepoint1'] = df['timepoint1'].apply(lambda x: int(x[1:]))
df['timepoint2'] = df['timepoint2'].apply(lambda x: int(x[1:]))
df.sort_values(by = ['n', 'timepoint1'], inplace=True)
print(df.head(20))

time_attributes = attributes['time_attributes']
col1 = time_attributes[1]
col2 = time_attributes[2]
id_attribute = attributes['id_attribute']
first_timepoint = 0
max_timepoint_state1 = np.max(df['timepoint1'].unique())
col_list = [col1, col2]

states = np.unique(np.concatenate((df[time_attributes[1]].unique(), df[time_attributes[2]].unique())))
states = np.sort(states)

# order = 1
ls1 = df[df[time_attributes[0]] == first_timepoint][col1].value_counts()
lss = df[[col1, col2]].pivot_table(index=time_attributes[1], columns=col2, fill_value=0, aggfunc=len)

# higher orders
print('start higher orders')
ids = df[id_attribute].unique()
df['selection1'] = np.ones(len(df))
order = 2
s = len(states)
for o in np.arange(2, order+1):
    print('o', o)

    # parameter o+1
    # we start with this one so that we can create all the extra state columns
    
    shift_col = 'state' + str(o + 1)
    col_list = col_list + [shift_col]
    
    out = list(map(lambda x: df.loc[(df[id_attribute] == x), col2].shift(periods=-(o-1)), \
                             ids))                         
    df[shift_col] = np.concatenate(out)

    df['selection' + str(o)] = df['selection' + str(o-1)]
    df.loc[df['timepoint1'] == max_timepoint_state1 - o + 2, 'selection' + str(o)] = 0

    lss = df.loc[df['selection' + str(o)] == 1, col_list].pivot_table(index=col_list[0:-1], columns=col_list[o], fill_value=0, aggfunc=len)
    print(lss)

    if lss.shape != (s**o, s):
        if lss.shape[1] != s:
            add_states = list(set(states) - set(lss.columns.tolist()))
            add_data = pd.DataFrame(np.zeros(shape=(len(lss), len(add_states))), columns=add_states, index=lss.index.values)
            lss = pd.concat([lss, add_data], axis=1)
        if lss.shape[0] != s**o:
            indices = lss.index.values
            print(indices)
            all_possible_indices = list(it.product(states, repeat = o))
            print(all_possible_indices)
            add_states = list(set(all_possible_indices) - set(indices))      
            print(add_states)
            add_data = pd.DataFrame(np.zeros(shape=(len(add_states), s)), columns=states, index=add_states)
            lss = pd.concat([lss, add_data], axis=0)
            lss.sort_index(axis=1, inplace=True)
            lss.sort_index(axis=0, inplace=True)
            print(lss)
            print(lss.shape)

    '''
    # parameter 1:o
    for p in np.arange(1, o):
        print('p', p)
        df_temp = df.loc[df['timepoint1'] <= (first_timepoint + p), ]
        col_list_temp = col_list[0:(p+1)]
        lss = df[col_list_temp].pivot_table(index=col_list_temp[0:-1], columns=col_list_temp[p], fill_value=0, aggfunc=len)
        print(lss)

    # parameter 0
    # the same as for markov order = 1
    ls1 = df.loc[df['timepoint1'] == first_timepoint, col_list[0]].value_counts()
    print(ls1)
    '''

    # given lss
    # calculate log likelihood
    ls = lss.sum(axis=1)
    print(ls.values)
    print(s**o)
    ls_long = np.repeat(ls.values, s).reshape((s**o,s))
    if 0 in ls_long:
        ls_long[ls_long == 0] = 1
    tA = lss.values / ls_long
    print(tA)

'''
if 0.0 in pi:
        pi[pi == 0.] = 0.0000000000001
    ii = np.matmul(data_ls1.values, np.log(pi))
    
    if 0.0 in A:
        A[A == 0.] = 0.0000000000001
    aa = np.matmul(data_lss.values.reshape(s*s,), np.log(A).reshape(s*s,))
    
    ll = ii + aa
'''
