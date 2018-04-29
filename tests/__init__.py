
tol = 0.001

def tol_check(result, expected):
    return abs(result - expected) <= tol * expected
