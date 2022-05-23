import numpy as np
import pandas as pd
import pygame
import sys


class Parser:

    def __init__(self, file):
        self.file = file

    def get_data(self):
        full_df = pd.read_csv(self.file,
                              header=None,
                              delimiter=" ",
                              names=list(range(6)))
        universe_radius = full_df[0][0]

        full_df = full_df.drop([len(full_df.columns) - 1], axis=1).drop([0])

        return full_df, universe_radius


class Calculator:

    def __init__(self, file, step):
        self.parser = Parser(file)
        self.initialize_data()
        self.g_constant = 6.67e-11
        self.timestep = step

    def initialize_data(self):
        self.full_df, self.universe_radius = self.parser.get_data()
        print("# of bodies", len(self.full_df))
        self.mass_m = self.full_df.iloc[:, [0]].to_numpy()
        self.pos_m = self.full_df.iloc[:, [1, 2]].to_numpy()
        self.vel_m = self.full_df.iloc[:, [3, 4]].to_numpy()

    def unv_r(self):
        return self.universe_radius

    def num_bodies(self):
        return len(self.full_df)

    def delta_position(self, i):
        # np.delete used to skip calculation when we're comparing a body/index
        # with itself (i.e., continue: when i == j)
        return np.delete(self.pos_m, i, 0) - self.pos_m[i]

    def distance_matrix(self, i):
        delta_pos_matrix = self.delta_position(i)

        # reshape the sum of squares into a column vector for broadcasting purposes
        sq_sum = np.sum(np.square(delta_pos_matrix), axis=1).reshape(
            (len(delta_pos_matrix), 1))

        # This matrix would contain distance values that are 0's
        dist_matrix = np.sqrt(sq_sum)

        # We can't have 0 distance values because that would result in
        # division by 0 when we calculate magnitude.
        # Thus we change any values that are 0, to 1 - using fancy indexing
        dist_matrix[dist_matrix == 0] = 1

        # Return both for force calculations to avoid having to call delta_position again
        return dist_matrix, delta_pos_matrix

    def force_matrix(self, i):
        dist_m, delta_pos = self.distance_matrix(i)

        # Multiply the current body's mass with all other masses except its own
        # - the scalar mass of the single body is broadcasted to all other masses
        m_times_m = np.delete(self.mass_m, i, 0) * self.mass_m[i]

        # Calculate the magnitude using G
        magnitude_matrix = (self.g_constant * m_times_m) / np.square(dist_m)

        # Matrix of force exerted by each body on x,y
        force_m = (delta_pos / dist_m) * magnitude_matrix

        return force_m

    # Calculate the net acceleration acting on i
    def acceleation(self, i):
        # a = f/m
        # sum f/m exerted by all bodies
        return np.sum(self.force_matrix(i) / self.mass_m[i], axis=0)

    def update_velocity(self, i):
        self.vel_m[i] += self.acceleation(i) * self.timestep

    def new_position(self, i):
        # Update velocity, then update i'th body's position
        self.update_velocity(i)
        self.pos_m[i] += self.vel_m[i] * self.timestep
        return self.pos_m[i]


class Simulation:

    def __init__(self, w, h, step, squeeze):
        # Ideally provided in command line arguments, therefore no need to
        # add them as a property
        self.w = w
        self.h = h
        self.timestep = step

        # Set default fps to 60
        self.fps = 120

        self.calc = Calculator(sys.argv[5], step)

        # Set a default universe radius-can be changed when parsing file
        self.universe_radius = self.calc.unv_r()
        self.draw_radius = 10

        # Higher the number the more squeezed the universe will appear in the screen
        self.squeeze = squeeze
        # object color
        self.colour = (201, 203, 255)

    @property
    def max_draw_radius(self):
        return self.draw_radius

    @max_draw_radius.setter
    def max_draw_radius(self, r):
        self.draw_radius = r

    def draw(self, pos_li):
        # Calculate scale to fit x,y coordinates within screen resolution
        x_max = self.universe_radius
        x_min = -self.universe_radius
        y_max = self.universe_radius
        y_min = -self.universe_radius
        x_scale = 1 / (x_max - x_min)
        y_scale = 1 / (y_max - x_min)

        bounding_factor = min(self.w, self.h) // self.squeeze

        # + w/h // 2 - bounding_factor//2 is the formula used to center the universe in the main
        # window/resoultion
        xs = ((x_scale * (pos_li[0] - x_min)) *
              bounding_factor) + self.w // 2 - bounding_factor // 2
        ys = ((y_scale * (pos_li[1] - y_min)) *
              bounding_factor) + self.h // 2 - bounding_factor // 2

        return (xs, ys)

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

            for i in range(self.calc.num_bodies()):
                scaled_coordinates = self.draw(self.calc.new_position(i))
                pygame.draw.circle(screen, self.colour, scaled_coordinates, 1)

            pygame.display.flip()


def main():
    # Choose a certain max draw radius
    radius_cap = 6

    # <w> <h> <step> <squeeze>
    sim = Simulation(int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]),
                     int(sys.argv[4]))

    # Max radius you want the pygame draw object (circle) to have (in pixels)
    sim.draw_radius = radius_cap
    sim.simulate()

    # TODO: add a cmd line argument that lets you set a multipler for the draw radius


if __name__ == "__main__":
    main()
