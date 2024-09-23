from lacbox.io import load_pwr, load_ind, load_inds
from lacbox.test import test_data_path
import matplotlib.pyplot as plt
from math import*


# Path for the file
pwr_path = './res_hawc2s/dtu_10mw_hawc2s_7wsp.pwr'
# Load the data
pwr_data = load_pwr(pwr_path)
# Print the names in the dict
pwr_data.keys()


# Path for the file
inds_path = './res_hawc2s/dtu_10mw_hawc2s_7wsp_u800%d.ind'
# Load the data
inds_data = load_inds([inds_path%i for i in range(7)])
# Print the names in the dict
print(inds_data.keys())
# Print shape
inds_data["s_m"].shape

fig, axs = plt.subplots(4, 2, figsize=(6.4, 7))

labels = ["%1.2f"%(pwr_data["Speed_rpm"][i]*88.9/(pwr_data["V_ms"][i]*30/pi)) for i in range (len(pwr_data["V_ms"]))]

# flow_angle_rad
axs[0, 0].plot(inds_data["s_m"], inds_data["flow_angle_rad"], label=labels)
axs[0, 0].set_ylabel("fl. angl. [rad]")

# aoa_rad
axs[0, 1].plot(inds_data["s_m"], inds_data["aoa_rad"], label=labels)
axs[0, 1].set_ylabel("aoa [rad]")

# Cl
axs[1, 0].plot(inds_data["s_m"], inds_data["Cl"], label=labels)
axs[1, 0].set_ylabel("$C_l$ [-]")

# Cd
axs[1, 1].plot(inds_data["s_m"], inds_data["Cd"], label=labels)
axs[1, 1].set_ylabel("$Cd$ [-]")

# CT
axs[2, 1].plot(inds_data["s_m"], inds_data["CT"], label=labels)
axs[2, 1].set_ylabel("$CT$ [-]")

# CP
axs[2, 0].plot(inds_data["s_m"], inds_data["CP"], label=labels)
axs[2, 0].set_ylabel("$CP$ [-]")

# a
axs[3, 0].plot(inds_data["s_m"], inds_data["a"], label=labels)
axs[3, 0].set_ylabel("ax.-ind. ($a$) [-]")

# ap
axs[3, 1].plot(inds_data["s_m"], inds_data["ap"], label=labels)
axs[3, 1].set_ylabel("tan.-ind. ($a_p$) [-]")

"""# a
axs[0, 0].plot(inds_data["s_m"], inds_data["a"], label=labels)
axs[0, 0].set_ylabel("ax. ind. ($a$) [-]")
# ap
axs[0, 1].plot(inds_data["s_m"], inds_data["ap"], label=labels)
axs[0, 1].set_ylabel("tan. ind. ($a_p$) [-]")
# Cl
axs[1, 0].plot(inds_data["s_m"], inds_data["Cl"], label=labels)
axs[1, 0].set_ylabel("$C_l$ [-]")
# Cd
axs[1, 1].plot(inds_data["s_m"], inds_data["Cd"], label=labels)
axs[1, 1].set_ylabel("$C_d$ [-]")
axs[1, 1].legend(title=r"$\omega$ [rpm]", ncol=2)
# CP
axs[2, 0].plot(inds_data["s_m"], inds_data["CP"], label=labels)
axs[2, 0].set_ylabel("Blade-span ($s$) [m]")
axs[2, 0].set_ylabel("local-$C_P$ [-]")
# CP
axs[2, 1].plot(inds_data["s_m"], inds_data["CT"], label=labels)
axs[2, 1].set_ylabel("Blade-span ($s$) [m]")
axs[2, 1].set_ylabel("local-$C_T$ [-]")
"""
plt.legend(title="Tip-speed ratio")


fig.suptitle("Parameters in Function of the Chord Length in m for Several Tip-speed ratios")
fig.tight_layout()
plt.savefig("plot_7wsp.pdf")
plt.show()