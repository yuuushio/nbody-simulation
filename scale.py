import numpy as np
import math

x_min = 0
y_min = 0

x_max = 0
y_max = 0

x_scale = 0
y_scale = 0

width = height = 512


def scale_x(x):
    return x_scale * (x - x_min)

def scale_y(y):
    return y_scale * (y_max - y)

def user_x(x):
    return x_min + x / x_scale

def user_y(y):
    return y_max - y / y_scale

# w = width of the IMAGE - can ignore this method
def factor_x(w):
    return w*width / abs(x_max - x_min)

def factor_y(h):
    return h*height / abs(y_max-y_min)
####################################################

def draw(x, y):
    pass

# x,y are the center's x-y coordinates of the body
def picture(x, y):
    xs = x_scale * (x - x_min)
    ys = height - y_scale * (y-y_min)
    draw(round(xs - 0.5, 2), round(ys - 0.5, 2))

def set_transform():
    x_scale = width / (x_max - x_min) # = 1
    y_scale = height / (y_max - y_min) # == 1
    # basically x_scale == width
    # and y_scale == height

def set_x_scale(min, max):
    x_min = min
    x_max = max

    set_transform()
    
def set_y_scale(min, max):
    y_min = min
    y_max = max

    set_transform()

def init():
    radius = 2.50e+11
    set_x_scale(-radius, radius)
    set_y_scale(-radius, radius)
