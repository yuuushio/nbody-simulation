import numpy as np

# [ m   x   y   vx  vy]
li_a = [5.97400e+24,  1.49600e+11, 0.00000e+00, 0.00000e+00, 2.98000e+04] 
li_b = [6.41900e+23,  2.27900e+11,  0.00000e+00,  0.00000e+00,  2.41000e+04]
li_c = [3.30200e+23,  5.79000e+10,  0.00000e+00,  0.00000e+00,  4.79000e+04] 
li_d = [1.98900e+30,  0.00000e+00,  0.00000e+00,  0.00000e+00,  0.00000e+00]  
li_e = [4.86900e+24,  1.08200e+11,  0.00000e+00,  0.00000e+00,  3.50000e+04]  

bodies = [li_a,li_b,li_c,li_d,li_e]
x_vals  = np.array([b[1] for b in bodies])
y_vals  = np.array([b[2] for b in bodies])

normalized_x = []
normalized_y = []

scale = max(x_vals.max() - x_vals.min(), y_vals.max() - y_vals.min())

for x in x_vals:
    x -= (x_vals.max()+x_vals.min())/2
    x = x/scale
    x += (1920//2)
    normalized_x.append(x)
    print(x)

for y in y_vals:
    y -= (y_vals.max()+y_vals.min())/2
    y /= scale
    y += 0.5
    normalized_y.append(y)

for i in range(len(x_vals)):
    print(x_vals[i], round(normalized_x[i]*1920, 4))

print("===============")
for i in range(len(y_vals)):
    print(y_vals[i], normalized_y[i])

#print(scale)

