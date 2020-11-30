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

def constraint_subgroup_size(subgroup=None, attributes=None, general_params=None):

    constraint_check = True
    
    # constraint on subgroup size
    # length of dataset can be different than number of cases
    # if len(subgroup)/general_params['data_size'] > 0.1:
    if len(subgroup[attributes['id_attribute']].unique()) / general_params['data_size']['nr_sequences'] < 0.1:
        constraint_check = False

    return constraint_check

def redundant_subgroup_coverage(level=None, seed=None, idx_sg_new=None):

    if level == 1:
        return True
    
    if len(seed['qualities']['idx_sg']) >= len(idx_sg_new):
        overlap = [item in idx_sg_new for item in seed['qualities']['idx_sg']]
        perc_overlap = sum(overlap) / len(seed['qualities']['idx_sg'])
        #if perc_overlap != 1.0:
            #print(perc_overlap)
        #if seed['qualities']['idx_sg'] == idx_sg_new:
        if perc_overlap > 0.99:
            #print('yes')
            return False
        else: 
            return True
    else:
        return True

# this function is currently not in use
def qm_constraints(desc_qm=None, sort_measure=None, constraints=None, qm_old=None):

    constraints_aslist = list(constraints.items())

    for constraint in constraints_aslist:
        #if constraint[0] == 'q_min' and desc_qm['qualities'][sort_measure] < constraint[1]:
        #    return False

        if constraint[0] == 'pn_min' and desc_qm['qualities']['sg_prop'] < constraint[1]:
            return False

        #if desc_qm['qualities'][sort_measure] == 0: 
        #    return False

        #else:
        #    proportion_increase = (desc_qm['qualities'][sort_measure] - qm_old) / qm_old
        #    if constraint[0] == 'q_incr' and proportion_increase < constraint[1]: 
        #        return False

    return True