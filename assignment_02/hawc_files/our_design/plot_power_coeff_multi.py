from lacbox.io import load_pwr, load_ind, load_inds
from lacbox.test import test_data_path
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np

base_path = Path(__file__).parent
pwr_path = base_path / "res_hawc2s/Group1_redesign_hawc2s_multiwsp.pwr"

#pwr_path = "C:/Users/nicol/git/LAC_repo/assignment_01/hawc_files/our_design/res_hawc2s/Group1_redesign_hawc2s_multiwsp.pwr"

# Load the data
pwr_data = load_pwr(pwr_path)
# Print the names in the dict
print(pwr_data.keys())

TSR_range = np.arange(4,10,0.5)

print(pwr_data["Cp"])


plt.figure(1)
plt.plot(TSR_range, pwr_data["Cp"], label='Cp')
plt.plot(TSR_range, pwr_data["Ct"], label='Ct')
plt.xlabel("TSR")
plt.ylabel("Coefficient")
plt.legend()
#plt.savefig("coefficient_vs_TSR.png")
plt.show()

