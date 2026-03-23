import math

def factorial(x):
    if isinstance(x, float):
        if abs(x - round(x)) < 1e-10:
            x = int(round(x))

    return math.factorial(x)


def cbrt(x):
    return x ** (1/3)
    

def sin(x, angle_mode):
    if angle_mode == 'DEG':
        x = math.radians(x)
    return _clean(math.sin(x))


def cos(x, angle_mode):
    if angle_mode == 'DEG':
        x = math.radians(x)
    return _clean(math.cos(x))
    

def tan(x, angle_mode):
    if angle_mode == 'DEG':
        x = math.radians(x)
    c = math.cos(x)
    if abs(c) < 1e-12:
        raise ValueError('Error')
    return _clean(math.tan(x))


def cot(x, angle_mode):
    if angle_mode == 'DEG':
        x = math.radians(x)
    s = math.sin(x)
    if abs(s) < 1e-12:
        raise ValueError('Error')
    return _clean(math.cos(x)/s)
    

def arcsin(x, angle_mode):
    result = math.asin(x)
    if angle_mode == 'DEG':
        result = math.degrees(result)
    return _clean(result)    


def arccos(x, angle_mode):
    result = math.acos(x)
    if angle_mode == 'DEG':
        result = math.degrees(result)
    return _clean(result)    


def arctan(x, angle_mode):
    result = math.atan(x)
    if angle_mode == 'DEG':
        result = math.degrees(result)
    return _clean(result)


def arccot(x, angle_mode):
    result = math.atan2(1, x)
    if angle_mode == 'DEG':
        result = math.degrees(result)
    return _clean(result)


def _clean(x):
    if abs(x) < 1e-10:
        return 0
    elif abs(x - round(x) < 1e-10):
        return int(round(x))
    return round(x, 12)