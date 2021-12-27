#!/usr/bin/env python3

import random
import numpy as np

def shuffle(tab):
    for e in reversed(range(0,len(tab)-1)):
        index = round(random.random()*(e-1))
        temp  = tab[e]
        tab[e] = tab[index]
        tab[index] = temp

def make_permutation():
    perm = []
    for i in range(0,256):
        perm.append(i)
    shuffle(perm)
    for i in range(0,256):
        perm.append(perm[i])
    return perm

def get_constant_vector(v):
    # v is the value from the permutation table
    h = v & 3
    if(h == 0):
        return np.array([[1.0], [1.0]])
    elif(h == 1):
        return np.array([[-1.0], [1.0]])
    elif(h == 2):
        return np.array([[-1.0], [-1.0]])
    else:
        return np.array([[1.0], [-1.0]])

def fade(t):
    return ((6*t - 15)*t + 10)*t*t*t

def lerp(t, a1, a2):
    return a1 + t*(a2-a1)

def perlin_2d(x, y, perm):
    X = int(x) & 255
    Y = int(y) & 255
    xf = x-int(x)
    yf = y-int(y)

    topRight = np.array([[xf-1.0], [yf-1.0]])
    topLeft = np.array([[xf], [yf-1.0]])
    bottomRight = np.array([[xf-1.0], [yf]])
    bottomLeft = np.array([[xf], [yf]])

    # Select a value in the array for each of the 4 corners
    valueTopRight = perm[perm[X+1]+Y+1]
    valueTopLeft = perm[perm[X]+Y+1]
    valueBottomRight = perm[perm[X+1]+Y]
    valueBottomLeft = perm[perm[X]+Y]

    dotTopRight = np.sum(topRight*get_constant_vector(valueTopRight))
    dotTopLeft = np.sum(topLeft*get_constant_vector(valueTopLeft))
    dotBottomRight = np.sum(bottomRight*get_constant_vector(valueBottomRight))
    dotBottomLeft = np.sum(bottomLeft*get_constant_vector(valueBottomLeft))

    u = fade(xf)
    v = fade(yf)

    return lerp(u,lerp(v, dotBottomLeft, dotTopLeft),lerp(v, dotBottomRight, dotTopRight))

def generate_perlin_noise(r,c,out_range=(0,1)):
    '''
        Generates a 2D grid using perlin noise.
        Each value is in the range [0,1]
        
        Params:
            r int: Number of rows.
            c int: Number of columns.
            out_range (int,int): Tuple of ints to specify the range of the noise values. [0,1] by default.
        Returns:
            grid (numpy.ndarray): rxc numpy array of floats in the specified param out_range.
    '''
    grid = np.zeros([r,c])
    perm = make_permutation()
    for y in range(0,c):
        for x in range(0,r):
            # Noise2D generally returns a value in the range [-1.0, 1.0]
            n = perlin_2d(x*0.1, y*0.1,perm)
            # Transform the range to [0.0, 1.0], supposing that the range of Noise2D is [-1.0, 1.0]
            n += 1.0
            n /= 2.0
            grid[x][y] += n
    return grid