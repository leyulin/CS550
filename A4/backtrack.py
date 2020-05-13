'''
Created on Apr 11, 2020

@author1: leyu_lin(Jack)
@author2: Parth_Thummar

backtracking search
'''
from csp_lib.backtrack_util import (first_unassigned_variable,
                                    unordered_domain_values,
                                    no_inference)


def backtracking_search(csp,
                        select_unassigned_variable=first_unassigned_variable,
                        order_domain_values=unordered_domain_values,
                        inference=no_inference):
    """backtracking_search
    Given a constraint satisfaction problem (CSP),
    a function handle for selecting variables, 
    a function handle for selecting elements of a domain,
    and a set of inferences, solve the CSP using backtrack search
    """

    # See Figure 6.5] of your book for details

    def backtrack(assignment):
        """Attempt to backtrack search with current assignment
        Returns None if there is no solution.  Otherwise, the
        csp should be in a goal state.
        """
        # check if value assigned
        if len(assignment) == len(csp.variables):
            return assignment

        # check other possible values
        var = select_unassigned_variable(assignment, csp)
        # check values in arcs assign values
        for val in order_domain_values(var, assignment, csp):
            if csp.nconflicts(var, val, assignment) is 0:
                csp.assign(var, val, assignment)
                # called support prune
                removals = csp.suppose(var, val)
                if inference(csp, var, val, assignment, removals):
                    # recursive back track
                    sol = backtrack(assignment)
                    if sol is not None:
                        return sol
                csp.restore(removals)
            csp.unassign(var, assignment)
            return None

    # Call with empty assignments, variables accessed
    # through dynamic scoping (variables in outer
    # scope can be accessed in Python)
    result = backtrack({})
    assert result is None or csp.goal_test(result)
    return result
