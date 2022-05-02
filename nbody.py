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

    def __repr__(self):
        return f"{self.x}, {self.y}"

    def __str__(self):
        return f"{self.x}, {self.y}"

class Builder:
    def __init__(self):
        # default values
        self.positon_vector = Vector(0,0,0)
        self.velocity_vector = Vector(0,0,0)
        self.accel_vector = Vector(0,0,0)
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
        delta_pos_sq_vec = delta_pos_sq.get_vector()
        return np.sqrt(delta_pos_sq_vec[0] + delta_pos_sq_vec[1] + delta_pos_sq_vec[2])

    # Returns the force vector - force acting on x,y,z
    def force(self, inner):
        if type(inner) != Body: raise TypeError
        dp = self.delta_position(inner) # Returns delta vector
        dist = self.distance(inner)
        if dist == 0: dist = 1
        magnitude = (6.67e-11*self.mass*inner.mass)/np.power(dist, 2)
        unit_vector = dp/dist
        force_vec = unit_vector*magnitude
        return force_vec

    def update_acceleration(self, inner):
        if type(inner) != Body: raise TypeError
        a_vec = self.force(inner)/self.mass
        self.acceleration += a_vec

    # Draws the body using its current position and attributes
    def draw(self, screen, radius, w, h):
        x_max = radius
        x_min = -radius
        y_max = radius
        y_min = -radius

        x_scale = 1/(x_max-x_min)
        y_scale = 1/(y_max-x_min)
        bounding_factor = min(w,h)//2
        xs = ((x_scale*(self.position.x-x_min))*bounding_factor)+w//2-bounding_factor//2
        ys = ((y_scale*(self.position.y-y_min))*bounding_factor)+h//2-bounding_factor//2

        pygame.draw.circle(screen, self.colour, (xs, ys), self.radius)

    # Updates velocity and moves the body 
    def update(self, dt):
        self.update_velocity(dt)
        self.position += (self.velocity*dt)

    # Updates velocity using the net acceration and dt
    def update_velocity(self, dt):
        self.velocity += self.acceleration*dt
        # Reset acceleration
        self.acceleration = Vector(0,0,0)

def read_file(file):
    with open(file) as f:
        data = f.read()

    # List of strings; each string contains the body's attributes
    string_bodies = [b for b in data.split("\n")]
    bodies = []
    # Get individual attribute
    for b in string_bodies:
        atb = b.split(",") # Short for "attributes"
        if len(atb) >= 5:
            pv = Vector(float(atb[0]),float(atb[1]),float(atb[2]))
            vv = Vector(float(atb[3]),float(atb[4]),float(atb[5]))
            body = Builder().pos_vec(pv).vel_vector(vv).mass(float(atb[6])).build()
            bodies.append(body)
    return bodies

def main():
    w = 200
    h = 200
    fps = 60
    bodies = read_file("test.txt")
    pygame.init()
    screen = pygame.display.set_mode((w,h))
    pygame.display.set_caption("nbody")
    clock = pygame.time.Clock()
    dt = 20000
    run = True
    radius = 2.50e+11
    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: run = False

        screen.fill((0,0,0))

        for outer_b in bodies:
            for inner in bodies:
                if inner is not outer_b:
                    outer_b.update_acceleration(inner)
            outer_b.update(dt)
            outer_b.draw(screen, radius, w, h)

        pygame.display.flip()


if __name__ == "__main__":
    main()

