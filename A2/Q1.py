'''
"""
Created on Feb 24, 2020

@author1: leyu_lin(Jack)
@author2: Parth_Thummar
'''

def polyval(fpoly, x):
    # reverse use slicing
    rev_fpoly = fpoly[::-1]
    value = 0
    for b, a in enumerate(rev_fpoly):
        value += a * x ** b
    return value

def derivative(fpoly):
    rev_fpoly = fpoly[::-1]
    poly_der = []
    for b, a in enumerate(rev_fpoly):
        if b > 0:
            poly_der.append(a * b)
    poly_der = poly_der[::-1]
    return poly_der

def NewtonRaphson(fpoly, a, tolerance=.00001):
    # evaluate util close to f(a) = 0 get root
    root_tolerance = polyval(fpoly, a)
    poly_der = derivative(fpoly)
    while abs(root_tolerance) > tolerance:
        # new_a = a - f(a) / der_f(a)
        # evaluate f(a) at x = new_a
        new_a = a - polyval(fpoly, a) / polyval(poly_der, a)
        root_tolerance = polyval(fpoly, new_a)
    return a


# root is 0.2250 and -2.0216
print('root is {:.4f}'.format(NewtonRaphson([7, 3, -5, 32, -7], 5)))
print('root is {:.4f}'.format(NewtonRaphson([7, 3, -5, 32, -7], -50)))
