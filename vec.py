#!/usr/bin/env python3

from imports import *
import numpy as np
import math as m

EPSILON = 1e-6

def FEQ(a, b):
    return abs(a - b) < EPSILON

def FLESS(a, b):
    return a - b < -EPSILON

def FLEQ(a, b):
    return a - b < EPSILON

def FGREATER(a, b):
    return b - a < -EPSILON

def FGEQ(a, b):
    return b - a < EPSILON

def length(v):
    # TODO: opt
    return m.sqrt(np.dot(v, v))

def length2(v):
    return np.dot(v, v)

def dist(a, b):
    return length(a - b)

def dist2(a, b):
    return length2(a - b)

def lerp(a, b, t):
    return t * a + (1 - t) * b

def normalize(v):
    return v / length(v)

def prep_rotate_yaw(theta):
    "Rotate clockwise around z axis"
    return np.array([
        [m.cos(theta), -m.sin(theta), 0],
        [m.sin(theta), m.cos(theta), 0],
        [0, 0, 1],
        ])

def prep_rotate_pitch(theta):
    "Rotate clockwise around x axis"
    return np.array([
        [1, 0, 0],
        [0, m.cos(theta), -m.sin(theta)],
        [0, m.sin(theta), m.cos(theta)],
        ])

def prep_rotate_roll(theta):
    "Rotate clockwise around x axis"
    return np.array([
        [m.cos(theta), 0, m.sin(theta)],
        [0, 1, 0],
        [-m.sin(theta), 0, m.cos(theta)],
        ])

# Rotate by yaw, then pitch, then roll
def prep_rotate(yaw, pitch, roll):
    m1 = prep_rotate_yaw(yaw)
    m2 = prep_rotate_pitch(pitch)
    m3 = prep_rotate_roll(roll)
    return np.matmul(np.matmul(m3, m2), m1)

if __name__ == '__main__':
    print("Running tests")
    r0 = prep_rotate_yaw(m.pi / 2)
    r1 = prep_rotate_pitch(m.pi / 2)
    r2 = prep_rotate_roll(m.pi / 2)
    assert(dist(np.matmul(r0, [1, 0, 0]), np.array([0, 1, 0])) < EPSILON)
    assert(dist(np.matmul(r1, [0, 1, 0]), np.array([0, 0, 1])) < EPSILON)
    assert(dist(np.matmul(r2, [0, 0, 1]), np.array([1, 0, 0])) < EPSILON)
    assert(dist(np.matmul(r0, [0, 1, 0]), np.array([-1, 0, 0])) < EPSILON)
    assert(dist(np.matmul(r1, [0, 0, 1]), np.array([0, -1, 0])) < EPSILON)
    assert(dist(np.matmul(r2, [1, 0, 0]), np.array([0, 0, -1])) < EPSILON)
    assert(FEQ(2, 2))
    assert(not FEQ(0, 2 * EPSILON))
    assert(FLESS(2 * -EPSILON, 0))
    assert(not FLESS(0, 0))
    assert(FLEQ(0, 0))
    print("All tests passed")
