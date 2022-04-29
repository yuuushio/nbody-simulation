import numpy as np
import pygame

class Vector:
    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z

    def get_vector(self):
        return [self.x, self.y, self.z]

    def __add__(self, other):
        if type(other) == Vector:
            return Vector(self.x+other.x, self.y+other.y, self.z+other.z)
        return Vector(self.x+other, self.y+other, self.z+other)

    def __sub__(self, other):
        if type(other) == Vector:
            return Vector(self.x-other.x, self.y-other.y, self.z-other.z)
        return Vector(self.x-other, self.y-other, self.z-other)
    
    def __mul__(self, other):
        if type(other) == Vector:
            return Vector(self.x*other.x, self.y*other.y, self.z*other.z)
        return Vector(self.x*other, self.y*other, self.z*other)

    def __truediv__(self, other):
        if type(other) == Vector:
            return Vector(self.x/other.x, self.y/other.y, self.z/other.z)
        return Vector(self.x/other, self.y/other, self.z/other)

class Builder:
    def __init__(self):
        # default values
        self.positon_vector = [0, 0, 0]
        self.velocity_vector = [0, 0, 0]
        self.accel_vector = [0, 0, 0]
        self.m = 1
        self.r = 5
        self.colour = (255, 0, 0)
    
    def pos_vec(self, vec: Vector):
        self.positon_vector = vec
        # Return self so we can chain the construction
        return self
    
    def vel_vector(self, vec: Vector):
        self.velocity_vector = vec
        return self

    def mass(self, m):
        self.m = m
        return self
    
    def draw_radius(self, r):
        self.r = r
        return self

    def col(self, c):
        self.colour = c
        return self

    def build(self):
        self.body = Body()
        self.body.position = self.positon_vector
        self.body.velocity = self.velocity_vector
        self.body.mass = self.m
        self.body.radius = self.r
        self.body.colour = self.colour
        self.body.acceleration = self.accel_vector
        return self.body

class Body:
    def __init__(self):
        pass

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, pos_vec):
        self._position = pos_vec

    @property
    def velocity(self):
        return self._vel

    @velocity.setter
    def velocity(self, vel_vec):
        self._vel = vel_vec

    @property
    def mass(self):
        return self._mass

    @mass.setter
    def mass(self, m):
        self._mass = m

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, r):
        self._radius = r

    @property
    def colour(self):
        return self._colour

    @colour.setter
    def colour(self, c):
        self._colour = c

    @property
    def acceleration(self):
        return self._accel

    @acceleration.setter
    def acceleration(self, accel_vec):
        self._accel = accel_vec

    # Return string representation of the object for printing purposes
    def __repr__(self):
        return f"{self.position} {self.velocity} {self.mass}"

    # Where inner is the j'th body in the inner for loop
    def delta_position(self, inner):
        if type(inner) != Body: raise TypeError
        return inner.position - self.position

    # Returns the true distance as a combination of position between
    # calling body and inner body
    def distance(self, inner): 
        if type(inner) != Body: raise TypeError
        delta_pos = self.delta_position(inner)
        # Better to multiply than to use power
        delta_pos_sq = delta_pos * delta_pos
        return np.sqrt(delta_pos_sq[0] + delta_pos_sq[1] + delta_pos_sq[2])

    # Returns the force vector - force acting on x,y,z
    def force(self, inner):
        if type(inner) != Body: raise TypeError
        dp = self.delta_position(inner) # Returns delta vector
        dist = self.distance(inner)
        magnitude = (self.mass*inner.mass)/np.power(dist, 2)
        unit_vector = dp/dist
        force_vec = unit_vector*magnitude
        return force_vec

    def update_acceleration(self, inner):
        if type(inner) != Body: raise TypeError
        a_vec = self.force(inner)/self.mass
        self.acceleration += a_vec

    # Draws the body using its current position and attributes
    def draw(self, screen):
        pygame.draw.circle(screen, self.colour, self.position, self.radius)

    # Updates velocity and moves the body 
    def update(self, dt):
        self.update_velocity(dt)
        self.position += (self.velocity*dt)

    # Updates velocity using the net acceration and dt
    def update_velocity(self, dt):
        self.velocity += self.acceleration*dt

def create_bodies():
    body_a = Builder().pos_vec(Vector(w//2,h//2)).vel_vector(Vector(0,0)).mass(100000).build()
    
    body_b = Builder().pos_vec(Vector(w//2+200,h//2)).vel_vector(Vector(0,25)).mass(1).build()
    body_c = Builder().pos_vec(Vector(w//2-300,h//2)).vel_vector(Vector(0,15)).mass(1).build()
    body_d = Builder().pos_vec(Vector(w//2-380,h//2)).vel_vector(Vector(0,15)).mass(1).build()
    body_e = Builder().pos_vec(Vector(w//2+400,h//2)).vel_vector(Vector(0,17)).mass(2).build()
    return [body_a,body_b,body_c,body_d,body_e]


def main():
    w = 1920
    h = 1080
    fps = 60


if __name__ == "__main__":
    main()

