#!/usr/bin/env python3

import math

def distance(point1, point2):
    assert len(point1) == len(point2), \
            "points given to distance must be of the same dimensionality"
    return math.sqrt(sum([ (a1 - a2) ** 2 for a1, a2 in zip(point1, point2) ]))

def angle(point1, point2):
    assert len(point1) == len(point2), \
            "points given to distance must be of the same dimensionality"
    pass #TODO

