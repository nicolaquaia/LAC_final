import numpy as np

#Our values
R_X=89.16
r_hub = 2.8
B = 3 
rho = 1.225

V_rated_Y = 11.122788574520852
R_Y = 92.52423873190985


TSR_opt = 7.2631578947368425
omega_max = TSR_opt * V_rated_Y / R_Y * 60 / (2*np.pi)

print(omega_max)
