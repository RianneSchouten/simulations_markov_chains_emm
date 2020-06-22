import numpy as np

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