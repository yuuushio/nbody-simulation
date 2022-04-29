import numpy as np
import pygame

class Body:
    def __init__(self,x,y,mass,vel_x,vel_y,z=0,vel_z=0):
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
    return (mass_product/dist_sq)

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
            if i != j:
                distance, delta_d = calc_distance(body_list[j], body_list[i])
                print(distance, delta_d)
                magnitude = calc_magnitude(body_list[j], body_list[i], distance)
                unit_v = unit_vec(delta_d, distance)
                a_x += (unit_v[0]*magnitude)/body_list[i].mass
                a_y += (unit_v[1]*magnitude)/body_list[i].mass
                a_z += (unit_v[2]*magnitude)/body_list[i].mass
        print("aceleration",a_x, a_y)
        body_list[i].vel_x += a_x*dt
        body_list[i].vel_y += a_y*dt
        body_list[i].vel_z += a_z*dt
        print(body_list[i].vel_x, body_list[i].vel_y, body_list[i].vel_z)
        body_list[i].x += body_list[i].vel_x*dt
        body_list[i].y += body_list[i].vel_y*dt
        body_list[i].z += body_list[i].vel_z*dt
        print(body_list[i].x, body_list[i].y, body_list[i].z)
        print("---")

def main():
    w = 1920
    h = 1080
    fps = 60
    white = (255,255,255)
    black = (0,0,0)
    red = (255,0,0)
    green = (0,255,0)
    blue = (0,0,255)

    b_a = Body(w//2, h//2, 100000, 0, 0)
    b_b = Body(w//2+200, h//2, 1, 0, 25)
    b_c = Body(w//2-300, h//2, 1, 0, 15)
    b_d = Body(w//2-380, h//2, 1, 0, 15)
    b_e = Body(w//2+400, h//2, 2, 0, 17)
    body_list = [b_a,b_b,b_c,b_d,b_e]
    pygame.init()
    screen = pygame.display.set_mode((w,h))
    pygame.display.set_caption("nbody")
    clock = pygame.time.Clock()

    running = True
    #for i in range(3):
    #    step(body_list, (0.05*speed))
    #    print("==============")
    while running:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
        screen.fill(black)
        step(body_list, 0.1)
        for b in body_list:
            pygame.draw.circle(screen, red, (int(b.x), (b.y)), 10)
        pygame.display.flip()
    #for i in range(100):
    


if __name__ == "__main__":
    main()
