# N-Body Simulation

N-Body Simulation is a common astrophysics simulation, used to model orbiting bodies within a solar system and galaxy. The simulation is done with the integration of Newton's gravitational force equation - calculating the gravitational force between two bodies, which is then used to calculate the new velocity and position using a timestep, `dt`. This is the common brute-force method with time complexity of `O(n^2)`; it's is good for understanding the concept, and forms a basis for more efficient, practical models. The results of the simulation are animated and can be visualized in real-time via a graphical interface, which itself is implemented using PyGame.

### Update - `nbody_eff.py` (24/05/2022)
`nbody_eff` is a more efficient version of the original `nbody` (which is now renamed to `nbody_old`). It can easily handle (along with the animation) more than 3000 body objects; whereas, the original version would end up lagging (regarding the animation/visualization) significantly when dealing with more than 300 bodies. 

The original version consisted of the conventional, double for-loop - where, for each body, it would calculate its new velocity and position as a result of forces exerted by other bodies. As you can probably tell, running this double for-loop, over a large number of bodies, each animation tick, would seriously slow down the processing. In the new version, however, the body/object data is transformed into matricies, so as to make use of numpy's broadcasting and vectorized operations, which would allow us to perform the mathematical calculations significantly faster.

*The original version is still there to see the differences in the implemenation and the performance improvements.*

## Dependencies
- `numpy`
- `pygame`

## Usage

First, make the `run.sh` file executable using `chmod +x run.sh` command. Then, run the file which executes the python program.

```bash
./run.sh
```

Alternatively, run the `nbody_eff.py` file directly by specifying your own command line arguments in the following format:
```bash
python nbody_eff.py <w> <r> <dt> <squeeze> <file>
```
Where:
- `w`: width of the graphical interface.
- `h`: height of the graphical interface.
- `dt`: time-step for the simulation.
- `squeeze`: Integer. Determines how spread out the bodies will be in the graphical interface. Default is 2. Higher the number = closer the bodies.
- `file`: path of the file. See `solarSystem.txt` for example format.

Example:

```bash
python nbody.py 1920 1080 dt 1 data/solarSystem.txt
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




