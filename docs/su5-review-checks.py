#!/usr/bin/env python3
"""Exact representation-factor diagnostics, independent of the submitted Lean code.

Polynomials in four arbitrary Cartan coordinates, with h5 = -h1-h2-h3-h4.
The weights of wedge^2(5), conjugate(5), and adjoint(5) determine their traces.
This checks algebraic group factors, not a chiral path integral or RG construction.
The conventional one-loop formula used below is stated in Tachikawa, section 3.1:
https://www-hep.phys.s.u-tokyo.ac.jp/~yujitach/tmp/dummies/dummiessu8.html
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import json

def add(*polys):
    result = {}
    for p in polys:
        for monomial, coefficient in p.items():
            result[monomial] = result.get(monomial, 0) + coefficient
    return {m: c for m, c in result.items() if c}

def scale(p, c):
    return {m: c*v for m, v in p.items() if c*v}

def multiply(p, q):
    result = {}
    for a, c in p.items():
        for b, d in q.items():
            m = tuple(x+y for x, y in zip(a,b))
            result[m] = result.get(m,0) + c*d
    return {m:c for m,c in result.items() if c}

def power(p, n):
    result = {(0,0,0,0):1}
    for _ in range(n):
        result = multiply(result, p)
    return result

def trace(weights, degree):
    return add(*(power(w, degree) for w in weights))

fund = [{tuple(int(i==j) for j in range(4)):1} for i in range(4)]
fund.append(scale(add(*fund),-1))
ten = [add(fund[i], fund[j]) for i,j in combinations(range(5),2)]
anti = [scale(w,-1) for w in fund]
adjoint = [add(fund[i],scale(fund[j],-1)) for i in range(5) for j in range(5) if i!=j]
checks = {
    'quadratic_wedge2_equals_3_fundamental': trace(ten,2)==scale(trace(fund,2),3),
    'quadratic_antifundamental_equals_fundamental': trace(anti,2)==trace(fund,2),
    'quadratic_adjoint_equals_10_fundamental': trace(adjoint,2)==scale(trace(fund,2),10),
    'cubic_wedge2_plus_antifundamental_vanishes': add(trace(ten,3),trace(anti,3))=={},
}
assert all(checks.values())
t_fund = F(1,2)
t_ten = 3*t_fund
c_adj = 10*t_fund
gauge = F(11,3)*c_adj
screening = F(2,3)*3*(t_ten+t_fund)
b0 = gauge-screening
assert (gauge,screening,b0)==(F(55,3),F(4),F(43,3))
result = {
    'method':'Exact polynomial expansion on an arbitrary traceless diagonal Hermitian generator of su(5).',
    'checks':checks,
    'conventional_normalization':{'T_fundamental':str(t_fund),'T_antisymmetric_10':str(t_ten),'C_adjoint':str(c_adj)},
    'three_generations_of_left_handed_10_plus_5bar':{'gauge':str(gauge),'screening':str(screening),'b0':str(b0)},
    'one_loop_formula_source':'https://www-hep.phys.s.u-tokyo.ac.jp/~yujitach/tmp/dummies/dummiessu8.html',
    'scope':'Independent representation-factor and coefficient arithmetic check; not an independent loop integration, proof of chiral gauge-measure invariance, or validation of the submitted running parameter.',
}
Path(__file__).with_name('su5-review-checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
