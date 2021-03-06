#!/usr/bin/env python3

import numpy as np
from math import cos, sin, atan2

def pixels_to_meters(pixels):
    return 0.01 * float(pixels)

def meters_to_pixels(meters):
    return float(meters) / 0.01

def map_val(val,in_start,in_end,out_start,out_end):
    slope = (out_end - out_start)/(in_end - in_start)
    return out_start + slope*(val-in_start)

def min_dist_point_to_line(P,A,B):
    '''This function computes the shortest distance between a point and a line segment
        params:
            P (2x1 numpy.array): Point of interest
            A (2x1 numpy.array): First vertex of line segment
            B (2x1 numpy.array): Second vertex of line segment
    '''
    # Direction vector
    M = B - A
    # Running parameter at the orthogonal intersection
    t0 = np.dot(M,P-A) / np.dot(M,M)
    # Intersection point
    C = A + t0 * M
    # Compute distance based on where the point lies
    if t0 <= 0: # left of the segment
        dist = np.linalg.norm(P-A)
    elif t0 >= 1: # right of the segment
        dist = np.linalg.norm(P-B)
    else: # Over the segment
        dist = np.linalg.norm(P-C)
    return dist,C

def rotate_2d(vertices,angle):
    rot_mat = np.array([[cos(angle),-sin(angle)],[sin(angle),cos(angle)]])
    r,c = vertices.shape
    for idx in range(0,c):
        res = np.matmul(rot_mat,vertices[:,idx].reshape(2,1))
        vertices[0,idx] = res[0]
        vertices[1,idx] = res[1]
    return vertices

def edge_angle(V0,V1,V2):
    '''
    The edge angle is found using unit vectors. This function is passed a set of three vertices where V0 is the shared point of the two vectors.
    Args:
        V0 (1x2 numpy array): Shared point of the two vectors
        V1 (1x2 numpy array): Vector 1 endpoint
        V2 (1x2 numpy array): Vector 2 endpoint
    '''
    # This function finds the signed shortest distance between two vectors
    V1[0] = V1[0] - V0[0]
    V1[1] = V1[1] - V0[1]
    V2[0] = V2[0] - V0[0]
    V2[1] = V2[1] - V0[1]

    # Dot product of the vectors
    cosine_theta = V1[0]*V2[0] + V1[1]*V2[1]
    # Cross product of the vectors
    sin_theta = V1[0]*V2[1] - V1[1]*V2[0]
    # find the angle using the relationships sin(theta)== tan(theta) = sin(theta)/cos(theta)
    edge_angle = atan2(sin_theta,cosine_theta)
    return edge_angle
