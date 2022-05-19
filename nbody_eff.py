import numpy as np
import pandas as pd
import pygame
import sys


class Body:

    def __init__(self):
        pass

    # Draws the body using its current position and attributes
    def draw(self, screen, radius, w, h, squeeze):
        # Calculate scale to fit x,y coordinates within screen resolution
        x_max = radius
        x_min = -radius
        y_max = radius
        y_min = -radius
        x_scale = 1 / (x_max - x_min)
        y_scale = 1 / (y_max - x_min)

        # Size of the universe itself - bound to a certain resolution.
        # Smaller than the specified resolution for visualization purposes.
        # Also determines how "spread" out the bodies are on x,y axes
        bounding_factor = min(w, h) // squeeze

        # + w/h // 2 - bounding_factor//2 is the formula used to center the universe in the main
        # window/resoultion
        xs = ((x_scale * (self.position.x - x_min)) *
              bounding_factor) + w // 2 - bounding_factor // 2
        ys = ((y_scale * (self.position.y - y_min)) *
              bounding_factor) + h // 2 - bounding_factor // 2

        pygame.draw.circle(screen, self.colour, (xs, ys), self.radius)

    # Updates velocity and moves the body
    def update(self, dt):
        self.update_velocity(dt)
        self.position += (self.velocity * dt)

    # Updates velocity using the net acceration and dt
    def update_velocity(self, dt):
        self.velocity += self.acceleration * dt
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
        self.fps = 120

        # Set a default universe radius-can be changed when parsing file
        self.universe_radius = 2.50e+11
        self.draw_radius = 10

        # Higher the number the more squeezed the universe will appear in the screen
        self.squeeze = squeeze

        self.colour = (201, 203, 255)

        pass

    @property
    def max_draw_radius(self):
        return self.draw_radius

    @max_draw_radius.setter
    def max_draw_radius(self, r):
        self.draw_radius = r

    # External method used to calculate and apply radius using the builder, and build the body
    def assign_draw_radius(self, builder_list, mass_list, largest_draw_r):
        return None

    def parse_file(self, file):
        self.full_df = pd.read_csv(file,
                                   header=None,
                                   delimiter=" ",
                                   names=list(range(6)))
        self.universe_radius = self.full_df[0][0]

        self.full_df = self.full_df.drop([len(self.full_df.columns) - 1],
                                         axis=1).drop([0])

        self.mass_m = self.full_df.iloc[:, [0]].to_numpy()
        self.pos_m = self.full_df.iloc[:, [1, 2]].to_numpy()
        self.vel_m = self.full_df.iloc[:, [3, 4]].to_numpy()
        print(self.mass_m[2])

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
        g_constant = 6.67e-11

        # Game loop
        while run:
            clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            screen.fill((22, 19, 32))

            for i in range(len(self.full_df)):
                delta_pos_matrix = np.delete(self.pos_m, i, 0) - self.pos_m[i]

                val_sums = np.sum(np.square(delta_pos_matrix), axis=1).reshape(
                    (len(delta_pos_matrix), 1))

                dist_m = np.sqrt(val_sums)

                dist_m[dist_m == 0] = 1

                a = (np.delete(self.mass_m, i, 0) * self.mass_m[i])
                magnitude_m = (g_constant * a) / np.square(dist_m)

                # matrix of force exerted by each body on body-i
                force_m = (delta_pos_matrix / dist_m) * magnitude_m
                # a = f/m
                accel_on_i = np.sum(force_m / self.mass_m[i], axis=0)
                print(accel_on_i)

                self.vel_m[i] += accel_on_i * self.timestep
                print(self.vel_m[i])
                print("......")
                self.pos_m[i] += self.vel_m[i] * self.timestep

                scale_tup = self.draw(self.pos_m[i])

                pygame.draw.circle(screen, self.colour, scale_tup, 1)

            pygame.display.flip()


def main():
    # Choose a certain max draw radius
    radius_cap = 6

    # <w> <h> <step> <squeeze>
    sim = Simulation(int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]),
                     int(sys.argv[4]))

    # Max radius you want the pygame draw object (circle) to have (in pixels)
    sim.draw_radius = radius_cap
    sim.parse_file(sys.argv[5])
    sim.simulate()

    # TODO: add a cmd line argument that lets you set a multipler for the draw radius


if __name__ == "__main__":
    main()
