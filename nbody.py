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
        magnitude = (6.67e-11*self.mass*inner.mass)/np.power(dist, 2)
        unit_vector = dp/dist
        force_vec = unit_vector*magnitude
        return force_vec

    def update_acceleration(self, inner):
        if type(inner) != Body: raise TypeError
        a_vec = self.force(inner)/self.mass
        self.acceleration += a_vec

    # Draws the body using its current position and attributes
    def draw(self, screen, vec: Vector):
        pygame.draw.circle(screen, self.colour, (vec.x, vec.y), self.radius)

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


def create_bodies(w, h):
    #body_a = Builder().pos_vec(Vector(w//2,h//2)).vel_vector(Vector(0,0)).mass(100000).build()
    #body_b = Builder().pos_vec(Vector(w//2+200,h//2)).vel_vector(Vector(0,25)).mass(1).build()
    #body_c = Builder().pos_vec(Vector(w//2-300,h//2)).vel_vector(Vector(0,15)).mass(1).build()
    #body_d = Builder().pos_vec(Vector(w//2-380,h//2)).vel_vector(Vector(0,15)).mass(1).build()
    #body_e = Builder().pos_vec(Vector(w//2+400,h//2)).vel_vector(Vector(0,17)).mass(2).build()
    body_a = Builder().pos_vec(Vector(1.49600e+11,0.00000e+00)).vel_vector(Vector(0.00000e+00,2.98000e+04)).mass(5.97400e+24).build()
    body_b = Builder().pos_vec(Vector(2.27900e+11,0.00000e+00)).vel_vector(Vector(0.00000e+00,2.41000e+04)).mass(6.41900e+23).build()
    body_c = Builder().pos_vec(Vector(5.79000e+10,0.00000e+00)).vel_vector(Vector(0.00000e+00,4.79000e+04)).mass(3.30200e+23).build()
    
    body_d = Builder().pos_vec(Vector(0.00000e+00,0.00000e+00)).vel_vector(Vector(0.00000e+00,0.00000e+00)).mass(1.98900e+30).draw_radius(20).build()
    body_e = Builder().pos_vec(Vector(1.08200e+11,0.00000e+00)).vel_vector(Vector(0.00000e+00,3.50000e+04)).mass(4.86900e+24).build()
 
    return [body_a,body_b,body_c,body_d,body_e]

def get_x_y(bodies):
	x = np.array([b.position.x for b in bodies])
	y = np.array([b.position.y for b in bodies])
	return x,y

def scale(x_vals, y_vals):
    normalized_vectors = []
    scale = max(x_vals.max()-x_vals.min(), y_vals.max()-y_vals.min())
    for i in range(len(x_vals)):
        # use constant variable for each max to make it faster later
        x = x_vals[i]
        y = y_vals[i]
        #x -= (x_vals.max()+x_vals.min())/2 
        #y -= (y_vals.max()+y_vals.min())/2 
        x = x/scale
        y = y/scale
        x *= 300
        y *= 300
        x += 1920//2
        y += 1080//2
        normalized_vectors.append(Vector(x,y))
        for v in normalized_vectors: print(v)
    return normalized_vectors

def main():
    w = 1920
    h = 1080
    fps = 60
    bodies = read_file("test.txt")
    pygame.init()
    screen = pygame.display.set_mode((w,h))
    pygame.display.set_caption("nbody")
    clock = pygame.time.Clock()
    dt = 30000
    run = True
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
        x,y = get_x_y(bodies)
        nv = scale(x,y)
        for i in range(len(bodies)):
            bodies[i].draw(screen, nv[i])

        pygame.display.flip()


if __name__ == "__main__":
    main()

