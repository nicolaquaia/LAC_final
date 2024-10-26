# %% Import modules
import matplotlib.pyplot as plt
import numpy as np
from aero_design_functions import get_design_functions_1MW, single_point_design


# Function for the absolute thickness vs span for the 35 m blade
def thickness(r, chord_root):
    """Absolute thickness [m] as a function of blade span [m] for 35-m blade"""
    p_edge = [
        9.35996e-8,
        -1.2911e-5,
        7.15038e-4,
        -2.03735e-2,
        3.17726e-1,
        -2.65357,
        10.2616,
    ]  # polynomial coefficients
    t_poly = np.polyval(p_edge, r)  # evaluate polynomial
    t = np.minimum(t_poly, chord_root)  # clip at max thickness
    return t


# %% Inputs
R = 35  # Rotor radius [m]
tsr = 9.0  # Tip-Speed-Ratio [-]
r_hub = 1.0  # Hub radius [m]
r = np.linspace(r_hub, R - 0.1, 40)  # Rotor span [m]
chord_max = 3.0  # Maximum chord size [m]
chord_root = 2.7  # Chord size at the root [m]
t = thickness(r, chord_root)  # Absolute thickness [m]
B = 3  # Number of blades [#]
# Aero dynamic polar design functions and the values (t/c vs. cl, cd, aoa)
cl_scale = 1.0  # Change this value to scale the cl-values
cl_des, cd_des, aoa_des, tc_vals, cl_vals, cd_vals, aoa_vals = get_design_functions_1MW(
    cl_scale
)


# %% Solving for the a single design
chord, tc, twist, cl, cd, aoa, a, CLT, CLP, CT, CP = single_point_design(
    r, t, tsr, R, cl_des, cd_des, aoa_des, chord_root, chord_max, B
)


# modifications

# change thickness
t = t* 0.9
cl_des1, cd_des1, aoa_des1, tc_vals1, cl_vals1, cd_vals1, aoa_vals1 = get_design_functions_1MW(
    cl_scale
    )
chord1, tc1, twist1, cl1, cd1, aoa1, a1, CLT1, CLP1, CT1, CP1 = single_point_design(
    r, t, tsr, R, cl_des1, cd_des1, aoa_des1, chord_root, chord_max, B
    )

# change Cl scale
cl_des2, cd_des2, aoa_des2, tc_vals2, cl_vals2, cd_vals2, aoa_vals2 = get_design_functions_1MW(
    cl_scale=1.1
    )
chord2, tc2, twist2, cl2, cd2, aoa2, a2, CLT2, CLP2, CT2, CP2 = single_point_design(
    r, t, tsr, R, cl_des2, cd_des2, aoa_des2, chord_root, chord_max, B
    )

# change TSR
tsr = 8
cl_des3, cd_des3, aoa_des3, tc_vals3, cl_vals3, cd_vals3, aoa_vals3 = get_design_functions_1MW(
    cl_scale=1
    )
chord3, tc3, twist3, cl3, cd3, aoa3, a3, CLT3, CLP3, CT3, CP3 = single_point_design(
    r, t, tsr, R, cl_des3, cd_des3, aoa_des3, chord_root, chord_max, B
    )


# %% Plotting design functions
tc_plot = np.linspace(0, 100, 100)
fig1, axs1 = plt.subplots(3, 1, num=1)

axs1[0].plot(tc_plot, cl_des(tc_plot), "k", label='original')
axs1[0].plot(tc_vals, cl_vals, "ok")
axs1[0].plot(tc_plot, cl_des1(tc_plot), "r", label='reduced thickness')
axs1[0].plot(tc_vals, cl_vals1, "or")
axs1[0].plot(tc_plot, cl_des2(tc_plot), "g", label='increased lift')
axs1[0].plot(tc_vals, cl_vals2, "og")
axs1[0].plot(tc_plot, cl_des3(tc_plot), "y", label='decreased TSR')
axs1[0].plot(tc_vals, cl_vals3, "oy")
axs1[0].set_ylabel("$C_l$ [-]")
axs1[0].set_xlim(0, 100)

axs1[1].plot(tc_plot, cd_des(tc_plot), "k")
axs1[1].plot(tc_vals, cd_vals, "ok")
axs1[1].plot(tc_plot, cd_des1(tc_plot), "r")
axs1[1].plot(tc_vals, cd_vals1, "or")
axs1[1].plot(tc_plot, cd_des2(tc_plot), "g")
axs1[1].plot(tc_vals, cd_vals2, "og")
axs1[1].plot(tc_plot, cd_des3(tc_plot), "y")
axs1[1].plot(tc_vals, cd_vals3, "oy")
axs1[1].set_ylabel("$C_d$ [-]")
axs1[1].set_xlim(0, 100)

axs1[2].plot(tc_plot, aoa_des(tc_plot), "k")
axs1[2].plot(tc_vals, aoa_vals, "ok")
axs1[2].plot(tc_plot, aoa_des1(tc_plot), "r")
axs1[2].plot(tc_vals, aoa_vals1, "or")
axs1[2].plot(tc_plot, aoa_des2(tc_plot), "g")
axs1[2].plot(tc_vals, aoa_vals2, "og")
axs1[2].plot(tc_plot, aoa_des3(tc_plot), "y")
axs1[2].plot(tc_vals, aoa_vals3, "oy")
axs1[2].set_ylabel(r"$\alpha$ [-]")
axs1[2].set_xlabel(r"$t/c$ [deg]")
axs1[2].set_xlim(0, 100)


fig1.tight_layout()
fig1.subplots_adjust(bottom=0.3)
fig1.legend(loc='lower center')

# %% Plot the chord, twist and relative-thickness
fig2, axs2 = plt.subplots(3, 1, num=2, clear=True)

# Chord
axs2[0].plot(r, chord,'k' , label="original")          
axs2[0].plot(r, chord1,'r', label="reduced thickness")
axs2[0].plot(r, chord2,'g', label="increased lift")   
axs2[0].plot(r, chord3,'y', label="decreased TSR")    
axs2[0].set_ylabel("Chord [m]")
axs2[0].set_xlim(0, R)

# Twist
axs2[1].plot(r, twist,'k')
axs2[1].plot(r, twist1,'r')
axs2[1].plot(r, twist2,'g')
axs2[1].plot(r, twist3,'y')
axs2[1].set_ylabel("Twist [deg]")
axs2[1].set_xlim(0, R)

# t/c
axs2[2].plot(r, tc, 'k')
axs2[2].plot(r, tc1,'r')
axs2[2].plot(r, tc2,'g')
axs2[2].plot(r, tc3,'y')
axs2[2].set_ylabel("Rel. thickness [%]")
axs2[2].set_xlabel("Rotor span [m]")
axs2[2].set_xlim(0, R)

fig2.tight_layout()
fig2.subplots_adjust(bottom=0.3)
fig2.legend(loc='lower center')

# %% Plot r vs. t/c, aoa, cl, cd
fig3, axs3 = plt.subplots(2, 2, num=3, clear=True)

# t/c
axs3[0, 0].plot(r, tc, 'k', label="original")         
axs3[0, 0].plot(r, tc1,'r', label="reduced thickness")
axs3[0, 0].plot(r, tc2,'g', label="increased lift")   
axs3[0, 0].plot(r, tc3,'y', label="decreased TSR")    
axs3[0, 0].set_ylabel("t/c [%]")
axs3[0, 0].set_xlim(0, R)

# aoa
axs3[0, 1].plot(r, aoa, 'k')
axs3[0, 1].plot(r, aoa1,'r')
axs3[0, 1].plot(r, aoa2,'g')
axs3[0, 1].plot(r, aoa3,'y')
axs3[0, 1].set_ylabel(r"$\alpha$ [deg]")
axs3[0, 1].set_xlim(0, R)
axs3[0, 1].yaxis.tick_right()
axs3[0, 1].yaxis.set_label_position("right")

# cl
axs3[1, 0].plot(r, cl, 'k')
axs3[1, 0].plot(r, cl1,'r')
axs3[1, 0].plot(r, cl2,'g')
axs3[1, 0].plot(r, cl3,'y')
axs3[1, 0].set_ylabel("$C_l$ [-]")
axs3[1, 0].set_xlabel("Span [m]")
axs3[1, 0].set_xlim(0, R)

# cd
axs3[1, 1].plot(r, cd, 'k')
axs3[1, 1].plot(r, cd1,'r')
axs3[1, 1].plot(r, cd2,'g')
axs3[1, 1].plot(r, cd3,'y')
axs3[1, 1].set_ylabel("$C_d$ [-]")
axs3[1, 1].set_xlabel("Span [m]")
axs3[1, 1].set_xlim(0, R)
axs3[1, 1].yaxis.tick_right()
axs3[1, 1].yaxis.set_label_position("right")

fig3.tight_layout()
fig3.subplots_adjust(bottom=0.3)
fig3.legend(loc='lower center')

# %% Plot r vs. CLT, CLP, a
fig4, axs4 = plt.subplots(3, 1, num=4, clear=True, figsize=(6.5, 5.5))

# Local-Thrust-Coefficient
axs4[0].plot(r, CLT ,'k', label="original")         
axs4[0].plot(r, CLT1,'r', label="reduced thickness")
axs4[0].plot(r, CLT2,'g', label="increased lift")   
axs4[0].plot(r, CLT3,'y', label="decreased TSR")    
axs4[0].axhline(y=8 / 9, ls="--", color="k", lw=1)
axs4[0].set_ylabel("Local thrust ($C_{LT}$) [-]")
axs4[0].set_ylim(0, 1.0)
axs4[0].set_xlim(0, R)

# Local-Power-Coefficient
axs4[1].plot(r, CLP ,'k')
axs4[1].plot(r, CLP1,'r')
axs4[1].plot(r, CLP2,'g')
axs4[1].plot(r, CLP3,'y')
axs4[1].axhline(y=16 / 27, ls="--", color="k", lw=1)
axs4[1].set_ylabel("Local Power ($C_{LP}$) [-]")
axs4[1].set_xlim(0, R)
axs4[1].set_ylim(-0.4, 0.6)

# Axial Induction
axs4[2].plot(r, a ,'k')
axs4[2].plot(r, a1,'r')
axs4[2].plot(r, a2,'g')
axs4[2].plot(r, a3,'y')
axs4[2].axhline(y=1 / 3, ls="--", color="k", lw=1)
axs4[2].set_ylabel("Axial induction ($a$) [-]")
axs4[2].set_xlabel("Rotor span [m]")
axs4[2].set_xlim(0, R)

fig4.suptitle(f"$C_T$={CT:1.3f}, $C_P$={CP:1.3f}, new C_T$={CT1:1.3f}, $C_P$={CP1:1.3f}")
fig4.tight_layout()
fig4.subplots_adjust(bottom=0.3)
fig4.legend(loc='lower center')

plt.show()
