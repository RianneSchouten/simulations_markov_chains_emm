import numpy as np

def redundant_description(desc=None, cq_satisfied=None):

    redundancy_check = True

    # check for redundant descriptions (the exact same description but in another order)
    # the comparison has to be done with the candidate queue of the current iteration only
    # this queue is saved in cq_satisfied
    for seed in cq_satisfied:
        if desc['description'] == seed['description']:
            redundancy_check = False
            break

    return redundancy_check

def constraint_subgroup_size(subgroup=None, attributes=None, general_params=None, constraint_subgroup_size=None):

    constraint_check = True
    
    # constraint on subgroup size
    # length of dataset can be different than number of cases
    # if len(subgroup)/general_params['data_size'] > 0.1:
    if len(subgroup[attributes['id_attribute']].unique()) / general_params['data_size']['nr_sequences'] < constraint_subgroup_size:
        print('constraint on subgroup size')
        constraint_check = False


    return constraint_check

def redundant_subgroup_coverage(level=None, idx_sg_old=None, idx_sg_new=None, constraint_subgroup_coverage=None):

    if len(idx_sg_old) >= len(idx_sg_new):
        #overlap = [item in idx_sg_new for item in idx_sg_old] # this is not necessary beacuse idx_sg_new is always a subset of idx_sg_old because of the way the refinements are set up
        perc_overlap = len(idx_sg_new) / len(idx_sg_old)

        if perc_overlap > constraint_subgroup_coverage:
            print('constraint on redundant subgroup coverage')
            return False
        else: 
            return True
    else:
        return True

