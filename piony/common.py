#!/usr/bin/env python3
# vim: fileencoding=utf-8

G_DEBUG_ACTIONS = True
G_DEBUG_VISUALS = False  # True


## ----------

def xstr(s):  # Returns empty string even if None
    return '' if s is None else str(s)


def similar(x, y, estimate=0.001):  # Floats robust comparison
    if isinstance(x, list) and isinstance(y, list):
        return all([similar(xi, yi, estimate) for xi, yi in zip(x, y)])
    else:
        return (abs(x-y) < estimate)


# Closest modulus: angle={base+3, base+6} -> base
# Usage: if angle is close to 90: (math.fabs(a - iround(a, 90)) < da/2)
def iround(angle, base):
    return round(float(angle) / base) * base


def lrotate(lst, n):  # Rotate list left:  [1,2,3,4] -> [2,3,4,1]
    n = n % len(lst) if lst else 0
    return lst[n:] + lst[:n]


def char_range(c1, c2):
    for c in range(ord(c1), ord(c2)+1):
        yield chr(c)

## ----------
import math


def degreeNorm(a):  # angle -> [0,360)
    return math.fmod((math.fmod(a, 360) + 360), 360)


def arcContains(a, da, c):  # angle := [a, a+da]
    return (da >= degreeNorm(360 + c - degreeNorm(a)))


def ra2xy(r, angle):  # Polar to cartesian:
    x = r * math.cos(math.radians(angle))
    y = r * math.sin(math.radians(angle))
    return [x, y]


def xy2ra(x, y):  # Cartesian to polar:
    r = math.sqrt(x*x + y*y)
    a = math.degrees(math.acos(x/r)) + (0 if y >= 0 else 180)
    return [r, a]

