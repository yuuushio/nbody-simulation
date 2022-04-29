class Vector:
    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z

    def get_vector(self):
        return [self.x, self.y, self.z]

    def __add__(self, i, j):
        if type(j) == Vector:
            return Vector(i.x+j.x, i.y+j.y, i.z+j.z)
        return Vector(i.x+j, i.y+j, i.z+j)

    def __sub__(self, i, j):
        if type(j) == Vector:
            return Vector(i.x-j.x, i.y-j.y, i.z-j.z)
        return Vector(i.x-j, i.y-j, i.z-j)
    
    def __mul__(self, i, j):
        if type(j) == Vector:
            return Vector(i.x*j.x, i.y*j.y, i.z*j.z)
        return Vector(i.x*j, i.y*j, i.z*j)

class Body_Builder:
    def __init__(self):
        # default values
        self.positon_vector = [0, 0, 0]
        self.velocity_vector = [0, 0, 0]
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

    # Return string representation of the object for printing purposes
    def __repr__(self):
        return f"{self.position} {self.velocity} {self.mass}"

# Separate calculation algorithms from the body-object class
class Body_Mediator:
    # Class that lets bodies comminicate with each other
    def __init__(self):
        pass
    
    # Returns thee x distance between the calling body and the argument body
    def delta_position(self, inner_body: Body, outer: Body):
        return [inner_body.position - outer.position]


