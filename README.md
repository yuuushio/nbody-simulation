# N-Body Simulation

The N-Body Simulation is a well-known astrophysics model used to simulate the motion of orbiting bodies in a solar system or galaxy. The simulation employs Newton's gravitational force equation to compute the gravitational force between two objects, which is subsequently used to calculate their new velocity and position at a given timestep, dt. Although this brute-force method has a time complexity of `O(n^2)`, it serves as a useful tool for comprehending the underlying concepts and forms a foundation for more efficient and practical models. 

The simulation results are presented through a graphical interface that is implemented using PyGame and can be visualized in real-time.

*The code was, later, greatly improved (details below) to perform the calculations a lot more efficiently using numpy's vectorized matrix operations. The original version is still there to see the differences in the implemenation and the performance improvements.*

## Dependencies
- `numpy`
- `pygame`

## Usage

First, make the `run.sh` file executable using `chmod +x run.sh` command. Then, run the file which executes the python program.

```bash
./run.sh
```

Alternatively, run the `main.py` file directly by specifying your own command line arguments in the following format:
```bash
python main.py <w> <r> <dt> <squeeze> <file>
```
Where:
- `w`: width of the graphical interface.
- `h`: height of the graphical interface.
- `dt`: time-step for the simulation.
- `squeeze`: Integer. Determines how spread out the bodies will be in the graphical interface. Default is 2. Higher the number = closer the bodies.
- `file`: path of the file. See `solarSystem.txt` for example format.

Example:

```bash
python main.py 1920 1080 dt 1 data/solarSystem.txt
```

### Data File-Format
```
<radius>
<mass> <x> <y> <x-velocity> <y-velocity>
.
.
<mass> <x> <y> <x-velocity> <y-velocity>
```

## Demo

Data consisting of 601 bodies, ran on `nbody_eff.py`:

<img src="https://raw.githubusercontent.com/yuuushio/nbody-simulation/main/data/demo/blossom.gif" width=600/>

Data consisting of 1001 bodies, ran on `nbody_eff.py`:

<img src="https://raw.githubusercontent.com/yuuushio/nbody-simulation/main/data/demo/galaxy.gif" width=600/>

The follow data was ran on `nbody_old.py`:

<img src="https://raw.githubusercontent.com/yuuushio/nbody-simulation/main/data/demo/simple-solarsystem.gif" width=600/>

<img src="https://raw.githubusercontent.com/yuuushio/nbody-simulation/main/data/demo/dance.gif" width=600/>

<img src="https://raw.githubusercontent.com/yuuushio/nbody-simulation/main/data/demo/earths.gif" width=600/>

<img src="https://raw.githubusercontent.com/yuuushio/nbody-simulation/main/data/demo/entropy.gif" width=600/>

## Update (24/05/2022)
The `main.py` file has undergone significant refactoring resulting in a more efficient version of the original `nbody` code, which has now been renamed to `nbody_old`. Unlike the original version (which was highly lag prone), the new code can effortlessly handle more than 3000 body objects without experiencing any significant lag during animation/visualization.

The original code used a traditional double for-loop to compute the new position and velocity of each body, accounting for the forces exerted by other bodies. Running this loop for a large number of bodies during each animation tick led to slow processing. On the other hand, the new version transforms the body/object data into matrices, enabling the use of numpy's broadcasting and vectorized operations, resulting in significantly faster mathematical computations.


