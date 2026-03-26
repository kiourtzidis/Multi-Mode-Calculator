import math

def factorial(x):
    if isinstance(x, float):
        if abs(x - round(x)) < 1e-10:
            x = int(round(x))

    return math.factorial(x)


def factorize(number):
        
        if number == 0:
            return None
        
        if number == 1:
            return 1
        
        if isinstance(number, float):
            if number.is_integer():
                number = int(number)
            else:
                return None
        
        if number < 0:
            number = abs(number)

        factors = []

        possible_factor = 2
        while number > 1:
            if number % possible_factor == 0:
                factors.append(f'{possible_factor}')
                number //= possible_factor
            else:
                possible_factor += 1

        return '×'.join(factors)


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


def sec(x, angle_mode):
    if angle_mode == 'DEG':
        x = math.radians(x)
    c = math.cos(x)
    if abs(c) < 1e-12:
        raise ValueError('Error')
    return _clean(1/c)


def csc(x, angle_mode):
    if angle_mode == 'DEG':
        x = math.radians(x)
    s = math.sin(x)
    if abs(s) < 1e-12:
        raise ValueError('Error')
    return _clean(1/s)


def cot(x, angle_mode):
    if angle_mode == 'DEG':
        x = math.radians(x)
    s = math.sin(x)
    if abs(s) < 1e-12:
        raise ValueError('Error')
    return _clean(math.cos(x)/s)


def sinh(x, angle_mode):
    return _clean(math.sinh(x))


def cosh(x, angle_mode):
    return _clean(math.cosh(x))


def tanh(x, angle_mode):
    return _clean(math.tanh(x))


def coth(x):
    s = math.sinh(x)
    if abs(s) < 1e-12:
        raise ValueError('Error')
    return _clean(math.cosh(x)/s)


def sech(x):
    return _clean(1/math.cosh(x))


def csch(x):
    s = math.sinh(x)
    if abs(s) < 1e-12:
        raise ValueError('Error')
    return _clean(1/s)
    

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


def arcsec(x, angle_mode):
    if abs(x) < 1:
        raise ValueError('Error')
    result = math.acos(1/x)
    if angle_mode == 'DEG':
        result = math.degrees(result)
    return _clean(result)


def arccsc(x, angle_mode):
    if abs(x) < 1:
        raise ValueError('Error')
    result = math.asin(1/x)
    if angle_mode == 'DEG':
        result = math.degrees(result)
    return _clean(result)


def arccot(x, angle_mode):
    result = math.atan2(1, x)
    if angle_mode == 'DEG':
        result = math.degrees(result)
    return _clean(result)


def arcsinh(x, angle_mode):
    result = math.asinh(x)
    return _clean(result)


def arccosh(x, angle_mode):
    result = math.acosh(x)
    return _clean(result)


def arctanh(x, angle_mode):
    result = math.atanh(x)
    return _clean(result)


def _clean(x):
    if abs(x) < 1e-10:
        return 0
    elif abs(x - round(x)) < 1e-10:
        return int(round(x))
    return round(x, 12)