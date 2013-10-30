#!/usr/bin/env python3

import math

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
    from classes import Point
    x = size[0] / 2 + position[0]
    y = size[1] / 2 + position[1]
    return (x, y)

def endpoint(position, size):
    from classes import Point
    x = size[0] + position[0]
    y = size[1] + position[1]
    return (x, y)

