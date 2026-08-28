# import pygame
import numba as nb
import numpy as np
import cupy as cp
import time

# @nb.njit()
def calculate_ys(m, start_x, b):
    l = []
    for i in range(10000):
        l.append(m*start_x + b)
        start_x += 1/m
    return l


m = 1/4
x = 10
b = 5
# t = time.time()
ls = calculate_ys(m, x, 5)
# t_end = time.time()
# print(t_end-t)
