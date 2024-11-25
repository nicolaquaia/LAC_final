from lacbox.io import load_pwr, load_ind, load_inds
from lacbox.test import test_data_path
import matplotlib.pyplot as plt
from pathlib import Path

base_path = Path(__file__).parent
pwr_path = base_path / "res_hawc2s/dtu_10mw_hawc2s_7wsp.pwr"

# Load the data
pwr_data = load_pwr(pwr_path)
# Print the names in the dict
print(pwr_data.keys())

TSR =  [6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0]

print(pwr_data["Cp"])


plt.figure(1)
plt.plot(TSR, pwr_data["Cp"], label='Cp')
plt.plot(TSR, pwr_data["Ct"], label='Ct')
plt.xlabel("TSR")
plt.ylabel("Coefficient")
plt.legend()
plt.savefig("coefficient_vs_TSR.png")
plt.show()

