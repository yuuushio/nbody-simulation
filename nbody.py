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

def pi_macro():
    return 3.141592653589793

def solar_mass():
    return (4*pi_macro()*pi_macro())

def n_day():
    return 365.25

def g_const():
    return (6.67e-11)

def calc_distance(b_a, b_b):
    dx = b_a.x - b_b.x
    dy = b_a.y - b_b.y
    dz = b_a.z - b_b.z
    return np.sqrt(np.power(dx, 2) + np.power(dy, 2) + np.power(dz, 2))

def calc_magnitude(a, b, distance):
    mass_product = a.mass*b.mass
    dist_sq = np.power(distance, 2)
    return g_const()*(mass_product/dist_sq)

# Advances the simulation with time difference (dt)
def step(body_list, dt):
    for i in range(len(body_list)):
        for j in range(len(body_list)):
            distance = calc_distance(body_list[i], body_list[j])
            magnitude = calc_magnitude(body_list[i], body_list[j], distance)

def main():
    body_list = []


if __name__ == "__main__":
    main()
