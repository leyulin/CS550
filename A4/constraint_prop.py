'''
Created on Apr 11, 2020

@author1: leyu_lin(Jack)
@author2: Parth_Thummar

Constraint propagation
'''


def AC3(csp, queue=None, removals=None):
    """AC3 constraint propagation

    """
    # Hints:
    # Remember that:
    #    csp.variables is a list of variables
    #    csp.neighbors[x] is the neighbors of variable x

    if queue is None:
        queue = [(a, b) for a in csp.curr_domains for b in csp.neighbors[a]]

    #  call support pruning before pure
    csp.support_pruning()

    def arcs_build(a):
        for x in csp.neighbors[a]:
            if (x, a) not in queue:
                queue.append((x, a))

    # go over queue get consistent arcs
    while queue:
        a, b = queue.pop()
        if consistent_arcs(csp, a, b, removals):
            if csp.curr_domains[a] is 0:
                return False
            arcs_build(a)
    return True


# check consistency consistent arcs
# go over each values in domain  if been modified
# prune values if is not satisfy constraints in domains
def consistent_arcs(csp, a, b, removals):
    consistency = False
    # check values in a that satisfy in b if not prune it
    for val in csp.curr_domains[a]:
        if all([not csp.constraints(a, val, b, x) for x in
                csp.curr_domains[b]]):
            csp.prune(a, val, removals)
            consistency = True
    return consistency
