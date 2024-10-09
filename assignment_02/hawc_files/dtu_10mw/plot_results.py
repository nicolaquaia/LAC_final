from lacbox.io import load_pwr, load_ind, load_inds
from lacbox.test import test_data_path
import matplotlib.pyplot as plt

# Path for the file
ind_path = './res_hawc2s/dtu_10mw_hawc2s_1wsp_u8000.ind'
# Load the data
ind_data = load_ind(ind_path)
# Print the names in the dict
ind_data.keys()

#dict_keys(['s_m', 'a', 'ap', 'flow_angle_rad', 'aoa_rad', 'flow_speed_ms', 'Fx_Nm', 'Fy_Nm', 'M_Nmm', 'UX0_m', 'UY0_m', 'UZ0_m', 'twist_rad', 'X_AC0_m', 'Y_AC0_m', 'Z_AC0_m', 'Cl', 'Cd', 'Cm', 'CLp0_rad', 'CDp0_rad', 'CMp0_rad', 'F0', 'F_rad', 'CL_FS0', 'CLFS_rad', 'V_a_ms', 'V_t_ms', 'torsion_rad', 'vx_ms', 'vy_ms', 'chord_m', 'CT', 'CP', 'angle_rad', 'v_1', 'v_2', 'v_3'])

fig, axs = plt.subplots(4, 2)

# flow_angle_rad
axs[0, 0].plot(ind_data["s_m"], ind_data["flow_angle_rad"])
axs[0, 0].set_ylabel("fl. angl. [rad]")

# aoa_rad
axs[0, 1].plot(ind_data["s_m"], ind_data["aoa_rad"])
axs[0, 1].set_ylabel("aoa [rad]")

# Cl
axs[1, 0].plot(ind_data["s_m"], ind_data["Cl"])
axs[1, 0].set_ylabel("$C_l$ [-]")

# Cd
axs[1, 1].plot(ind_data["s_m"], ind_data["Cd"])
axs[1, 1].set_ylabel("$Cd$ [-]")

# CT
axs[2, 1].plot(ind_data["s_m"], ind_data["CT"])
axs[2, 1].set_ylabel("$CT$ [-]")

# CP
axs[2, 0].plot(ind_data["s_m"], ind_data["CP"])
axs[2, 0].set_ylabel("$CP$ [-]")

# a
axs[3, 0].plot(ind_data["s_m"], ind_data["a"])
axs[3, 0].set_ylabel("ax.-ind. ($a$) [-]")

# ap
axs[3, 1].plot(ind_data["s_m"], ind_data["ap"])
axs[3, 1].set_ylabel("tan.-ind. ($a_p$) [-]")

"""
# a
axs[0, 0].plot(ind_data["s_m"], ind_data["a"])
axs[0, 0].set_ylabel("ax.-ind. ($a$) [-]")
# ap
axs[0, 1].plot(ind_data["s_m"], ind_data["ap"])
axs[0, 1].set_ylabel("tan.-ind. ($a_p$) [-]")
# Cl
axs[1, 0].plot(ind_data["s_m"], ind_data["Cl"])
axs[1, 0].set_ylabel("$C_l$ [-]")
# Cd
axs[1, 1].plot(ind_data["s_m"], ind_data["Cd"])
axs[1, 1].set_ylabel("$C_d$ [-]")
# CP
axs[2, 0].plot(ind_data["s_m"], ind_data["CP"])
axs[2, 0].set_ylabel("Blade-span ($s$) [m]")
axs[2, 0].set_ylabel("local-$C_P$ [-]")
# CP
axs[2, 1].plot(ind_data["s_m"], ind_data["CT"])
axs[2, 1].set_ylabel("Blade-span ($s$) [m]")
axs[2, 1].set_ylabel("local-$C_T$ [-]")
"""


fig.suptitle("Parameters in Function of the Chord Length in m for a Tip-speed ratio of 5.53")
fig.tight_layout()
plt.savefig("plot_1wsp.pdf")
plt.show()
