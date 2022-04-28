import numpy as np

class Body:
    def __init__(self,x,y,z,vel_x,vel_y,vel_z,mass):
        self.x = x
        self.y = y
        self.z = z
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.vel_z = vel_z
        self.mass = mass
