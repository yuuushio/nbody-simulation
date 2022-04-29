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
    delta_d = [dx, dy, dz]
    return np.sqrt(np.power(dx, 2) + np.power(dy, 2) + np.power(dz, 2)), delta_d

def calc_magnitude(a, b, distance):
    mass_product = a.mass*b.mass
    dist_sq = np.power(distance, 2)
    return g_const()*(mass_product/dist_sq)

def unit_vec(delta_d, dist):
    uv = [delta_d[0]/dist, delta_d[1]/dist, delta_d[2]/dist]
    return uv

# Advances the simulation with time difference (dt)
def step(body_list, dt):
    for i in range(len(body_list)):
        a_x = 0
        a_y = 0
        a_z = 0
        for j in range(len(body_list)):
            if i ==j: continue
            distance, delta_d = calc_distance(body_list[i], body_list[j])
            magnitude = calc_magnitude(body_list[i], body_list[j], distance)
            unit_v = unit_vec(delta_d, distance)
            a_x += (unit_v[0]*magnitude)/body_list[i].mass
            a_y += (unit_v[1]*magnitude)/body_list[i].mass
            a_z += (unit_v[2]*magnitude)/body_list[i].mass
        body_list[i].vel_x += a_x*dt
        body_list[i].vel_y += a_y*dt
        body_list[i].vel_z += a_z*dt
        body_list[i].x += body_list[i].vel_x*dt
        body_list[i].y += body_list[i].vel_y*dt
        body_list[i].z += body_list[i].vel_z*dt

def main():
    body_list = []


if __name__ == "__main__":
    main()
