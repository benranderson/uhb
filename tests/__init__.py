
def tol_check(result, expected, tol=0.001):
    return abs(result - expected) <= tol * expected
