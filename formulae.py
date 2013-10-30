#!/usr/bin/env python3

import math

def distance(point1, point2):
    assert len(point1) == len(point2), \
            "points given to distance must be of the same dimensionality"
    return math.sqrt(sum([ (a1 - a2) ** 2 for a1, a2 in zip(point1, point2) ]))

def angle(point1, point2):
    assert len(point1) == len(point2), \
            "points given to distance must be of the same dimensionality"
    x1, y1 = point1
    x2, y2 = point2
    dx = x2 - x1
    dy = y2 - y1
    rads = math.atan2(-dy, dx)
    rads %= 2 * math.pi
    deg = math.degrees(rads)
    return deg

def directionOfAngle(degs=None, rads=None, north=0):
    from classes import Cardinal
    assert degs is not rads, 'specify either degrees or radians'
    if rads is not None:
        degs = math.degrees(rads)
    degs %= 360.0
    if 45.0 < degs <= 135.0: # e.g. 90
        direction = Cardinal(0, north=north)
    elif 135.0 < degs <= 225.0: # e.g. 180
        direction = Cardinal(3, north=north)
    elif 225.0 < degs <= 315.0: # e.g. 270
        direction = Cardinal(2, north=north)
    elif 315.0 < degs or degs <= 45.0: # e.g. 0
        direction = Cardinal(1, north=north)
    return direction

def centerpoint(position, size):
    x = size[0] / 2 + position[0]
    y = size[1] / 2 + position[1]
    return (x, y)

def endpoint(position, size):
    x = size[0] + position[0]
    y = size[1] + position[1]
    return (x, y)

