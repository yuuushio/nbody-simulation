import numpy as np
import pygame
import sys


class Vector:
    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z

    def get_vector(self):
        return [self.x, self.y, self.z]

    def __add__(self, other):
        if type(other) == Vector:
            return Vector(self.x + other.x, self.y + other.y, self.z + other.z)
        return Vector(self.x + other, self.y + other, self.z + other)

    def __sub__(self, other):
        if type(other) == Vector:
            return Vector(self.x - other.x, self.y - other.y, self.z - other.z)
        return Vector(self.x - other, self.y - other, self.z - other)

    def __mul__(self, other):
        if type(other) == Vector:
            return Vector(self.x * other.x, self.y * other.y, self.z * other.z)
        return Vector(self.x * other, self.y * other, self.z * other)

    # Doesn't handle division by 0
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
        self.positon_vector = Vector(0, 0, 0)
        self.velocity_vector = Vector(0, 0, 0)
        self.accel_vector = Vector(0, 0, 0)
        self.m = 1
        self.r = 5
        self.colour = (201, 203, 255)

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
        if type(inner) != Body:
            raise TypeError
        return inner.position-self.position

    # Returns the true distance as a combination of position between
    # calling body and inner body
    def distance(self, inner):
        if type(inner) != Body:
            raise TypeError
        delta_pos = self.delta_position(inner)
        # Better to multiply than to use power
        delta_pos_sq = delta_pos * delta_pos
        delta_pos_sq_vec = delta_pos_sq.get_vector()
        return np.sqrt(delta_pos_sq_vec[0] + delta_pos_sq_vec[1] + delta_pos_sq_vec[2])

    # Returns the force vector - force acting on x,y,z
    def force(self, inner):
        if type(inner) != Body:
            raise TypeError
        dp = self.delta_position(inner)  # Returns delta vector
        dist = self.distance(inner)
        if dist == 0:
            dist = 1
        magnitude = (6.67e-11 * self.mass * inner.mass)/np.power(dist, 2)
        unit_vector = dp/dist
        force_vec = unit_vector * magnitude
        return force_vec

    def update_acceleration(self, inner):
        if type(inner) != Body:
            raise TypeError
        a_vec = self.force(inner)/self.mass
        self.acceleration += a_vec

    # Draws the body using its current position and attributes
    def draw(self, screen, radius, w, h, squeeze):
        # Calculate scale to fit x,y coordinates within screen resolution
        x_max = radius
        x_min = -radius
        y_max = radius
        y_min = -radius
        x_scale = 1/(x_max - x_min)
        y_scale = 1/(y_max - x_min)

        # Size of the universe itself - bound to a certain resolution.
        # Smaller than the specified resolution for visualization purposes.
        # Also determines how "spread" out the bodies are on x,y axes
        bounding_factor = min(w, h)//squeeze

        # + w/h // 2 - bounding_factor//2 is the formula used to center the universe in the main
        # window/resoultion
        xs = ((x_scale * (self.position.x - x_min)) *
              bounding_factor) + w//2 - bounding_factor//2
        ys = ((y_scale * (self.position.y - y_min)) *
              bounding_factor) + h//2 - bounding_factor//2

        pygame.draw.circle(screen, self.colour, (xs, ys), self.radius)

    # Updates velocity and moves the body
    def update(self, dt):
        self.update_velocity(dt)
        self.position += (self.velocity * dt)

    # Updates velocity using the net acceration and dt
    def update_velocity(self, dt):
        self.velocity += self.acceleration*dt
        # Reset acceleration after each full iteration
        self.acceleration = Vector(0, 0, 0)


class Simulation:
    def __init__(self, w, h, step, squeeze):
        # Ideally provided in command line arguments, therefore no need to
        # add them as a property
        self.w = w
        self.h = h
        self.timestep = step

        # Set default fps to 60
        self.fps = 60

        # Set a default universe radius-can be changed when parsing file
        self.universe_radius = 2.50e+11
        self.bodies = []
        self.draw_radius = 10

        # Higher the number the more squeezed the universe will appear in the screen
        self.squeeze = squeeze
        pass

    @property
    def max_draw_radius(self):
        return self.draw_radius

    @max_draw_radius.setter
    def max_draw_radius(self, r):
        self.draw_radius = r

    # External method used to calculate and apply radius using the builder, and build the body
    def assign_draw_radius(self, builder_list, mass_list, largest_draw_r):
        np_mass_list = np.array(mass_list)
        mass_max = np_mass_list.max()
        bodies_tmp = []
        # Calculate body radius based on/as a percentage of the largest body
        for i in range(len(builder_list)):
            # If % of body vs largest body is less than 3, just assign the body a radius of 3
            if (np_mass_list[i]/mass_max)*largest_draw_r < 4:
                body = builder_list[i].draw_radius(3).build()
                bodies_tmp.append(body)
            else:
                new_r = int((np_mass_list[i]/mass_max)*largest_draw_r)
                # Also assign the body with the highest mass a distinctive colour
                body = builder_list[i].draw_radius(
                    new_r).col((242, 143, 173)).build()
                bodies_tmp.append(body)
        return bodies_tmp

    def parse_file(self, file):
        # New test data in the form of:
        # <num-bodies>
        # <universe-radius>
        # m x y vx vy
        with open(file) as f:
            data = f.read()

        string_bodies = [d for d in data.split("\n")]
        # TODO: if radius isnt provided, use default. impl logic to deal
        # Use radius from file if provided
        self.universe_radius = float(string_bodies[1])
        builder_list = []
        mass_list = []
        for b in string_bodies[2:]:
            # NOTE: fails when there are multiple spaces between the attributes
            atb = b.split(" ")  # Short for "attributes"

            if len(atb) >= 4:
                pv = Vector(float(atb[1]), float(atb[2]))
                vv = Vector(float(atb[3]), float(atb[4]))
                # Append body builder to builder_list
                builder_list.append(Builder().pos_vec(
                    pv).vel_vector(vv).mass(float(atb[0])))
                # Append corressponding mass right after so we can use the same index to reference same entity
                mass_list.append(float(atb[0]))
        self.bodies = self.assign_draw_radius(
            builder_list, mass_list, self.max_draw_radius)

    # Can impl later with z coordinates for value/calculation output purposes

    def simulate(self):
        pygame.init()
        screen = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("nbody")
        clock = pygame.time.Clock()
        run = True

        # Game loop
        while run:
            clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            screen.fill((22, 19, 32))

            for outer_b in self.bodies:
                for inner in self.bodies:
                    if inner is not outer_b:
                        outer_b.update_acceleration(inner)
                outer_b.update(self.timestep)
                outer_b.draw(screen, self.universe_radius,
                             self.w, self.h, self.squeeze)

            pygame.display.flip()


def main():
    # Choose a certain max draw radius
    radius_cap = 6

    # <w> <h> <step> <squeeze>
    sim = Simulation(int(sys.argv[1]), int(
        sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]))

    # Max radius you want the pygame draw object (circle) to have (in pixels)
    sim.draw_radius = radius_cap
    sim.parse_file(sys.argv[5])
    sim.simulate()

    # TODO: add a cmd line argument that lets you set a multipler for the draw radius


if __name__ == "__main__":
    main()
