#!/usr/bin/env python3

import math

def centerpoint(position, size):
    from classes import Point
    x = size[0] / 2 + position[0]
    y = size[1] / 2 + position[1]
    return Point(x, y)

def endpoint(position, size):
    from classes import Point
    x = size[0] + position[0]
    y = size[1] + position[1]
    return Point(x, y)

