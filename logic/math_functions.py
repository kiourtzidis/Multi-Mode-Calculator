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
    return round(math.sin(x), 12)


def cos(x, angle_mode):
    if angle_mode == 'DEG':
        x = math.radians(x)
    return round(math.cos(x), 12)
    

def tan(x, angle_mode):
    if angle_mode == 'DEG':
        x = math.radians(x)
    return round(math.tan(x), 12)
    

def arcsin(x, angle_mode):
    result = math.asin(x)
    if angle_mode == 'DEG':
        result = math.degrees(result)
    return round(result, 12)    


def arccos(x, angle_mode):
    result = math.acos(x)
    if angle_mode == 'DEG':
        result = math.degrees(result)
    return round(result, 12)    


def arctan(x, angle_mode):
    result = math.atan(x)
    if angle_mode == 'DEG':
        result = math.degrees(result)
    return round(result, 12)