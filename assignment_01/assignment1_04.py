"""Script/module for scaling the HAWC2 ST-data

The file can be run directly which shows an example of how to scale the ST-data
The file can also be imported as a module where the `scale_ST_data` can be used in another script/notebook
"""


def scale_ST_data(baseline_st_data, scale_factor):
    """Applying scaling for a baseline HAWC2 ST-file.

    Parameters
    ----------
    baseline_st_data : dict
        Dict containing the baseline ST-data. The ST-data can be loaded with `lacbox.load_st`
    scale_factor : float
        Scaling factor to apply for the ST-data. If scaling factor is using rotor span it can be computed as: `scale_factor = R_new/R_old`

    Returns
    -------
    dict
        The scaled ST-data. Can be written to file with `lacbox.save_st`
    """
    st_data = dict()
    st_data["s"] = baseline_st_data["s"] * scale_factor
    st_data["m"] = baseline_st_data["m"] * scale_factor**2
    st_data["x_cg"] = baseline_st_data["x_cg"] * scale_factor
    st_data["y_cg"] = baseline_st_data["y_cg"] * scale_factor
    st_data["ri_x"] = baseline_st_data["ri_x"] * scale_factor
    st_data["ri_y"] = baseline_st_data["ri_y"] * scale_factor
    st_data["x_sh"] = baseline_st_data["x_sh"] * scale_factor
    st_data["y_sh"] = baseline_st_data["y_sh"] * scale_factor
    st_data["E"] = baseline_st_data["E"]
    st_data["G"] = baseline_st_data["G"]
    st_data["I_x"] = baseline_st_data["I_x"] * scale_factor**4
    st_data["I_y"] = baseline_st_data["I_y"] * scale_factor**4
    st_data["I_p"] = baseline_st_data["I_p"] * scale_factor**4
    st_data["k_x"] = baseline_st_data["k_x"]
    st_data["k_y"] = baseline_st_data["k_y"]
    st_data["A"] = baseline_st_data["A"] * scale_factor**2
    st_data["pitch"] = baseline_st_data["pitch"]
    st_data["x_e"] = baseline_st_data["x_e"] * scale_factor
    st_data["y_e"] = baseline_st_data["y_e"] * scale_factor
    return st_data

"""def annotate_points(ax, x_data, y_data, label):
    # Annotate first point
    ax.annotate(f'({x_data[0]:.2f}, {y_data[0]:.2f})', 
                xy=(x_data[0], y_data[0]), xycoords='data',
                xytext=(5, -5), textcoords='offset points', 
                arrowprops=dict(arrowstyle="->", lw=0.5))
    
    # Annotate last point
    ax.annotate(f'({x_data[-1]:.2f}, {y_data[-1]:.2f})', 
                xy=(x_data[-1], y_data[-1]), xycoords='data',
                xytext=(-40, 5), textcoords='offset points', 
                arrowprops=dict(arrowstyle="->", lw=0.5))
"""

"""def display_lines(ax, x_data, y_data, label):
    # First point
    ax.axvline(x_data[0], color='gray', linestyle='--', linewidth=0.8)
    ax.axhline(y_data[0], color='gray', linestyle='--', linewidth=0.8)
    ax.text(x_data[0], ax.get_ylim()[0], f'{x_data[0]:.2f}', ha='center', va='bottom', fontsize=8)
    ax.text(ax.get_xlim()[0], y_data[0], f'{y_data[0]:.2f}', ha='right', va='center', fontsize=8)
    
    # Last point
    ax.axvline(x_data[-1], color='gray', linestyle='--', linewidth=0.8)
    ax.axhline(y_data[-1], color='gray', linestyle='--', linewidth=0.8)
    ax.text(x_data[-1], ax.get_ylim()[0], f'{x_data[-1]:.2f}', ha='center', va='bottom', fontsize=8)
    ax.text(ax.get_xlim()[0], y_data[-1], f'{y_data[-1]:.2f}', ha='right', va='center', fontsize=8)
"""

def display_lines(ax, x_data, y_data, label, stagger_offset=0.1):
    # Adjust text positions to avoid overlapping
    ylim = ax.get_ylim()
    xlim = ax.get_xlim()
    
    # First point
    ax.axhline(y_data[0], color='red', linestyle='--', linewidth=0.8)
    
    # Display x and y values with slight offsets
    ax.text(xlim[0] - stagger_offset * (4), y_data[0], f'{y_data[0]:.2f}', 
            ha='right', va='center', fontsize=8)
    
    # Last point
    ax.axvline(x_data[-1], color='green', linestyle='--', linewidth=0.8)
    
    # Display x and y values with slight offsets
    ax.text(x_data[-1], ylim[0] - stagger_offset * (ylim[1] - ylim[0]), f'{x_data[-1]:.2f}', 
            ha='center', va='top', fontsize=8, rotation=0)
    
if __name__ == "__main__":
    # %% Import modules
    import matplotlib.pyplot as plt
    from lacbox.io import load_st,save_st, load_oper
    from pathlib import Path
    from Our_values import*
    from lacbox.test import test_data_path
    import copy
    import matplotlib.ticker as ticker

    plt.rcParams.update({'font.family': 'serif', 'font.size': 12})
    # %% Inputs
    # Baseline ST-data (DTU 10MW)
    script_dir = Path(__file__).parent
    path_st_file_DTU10MW = script_dir / "hawc_files/our_design/data/DTU_10MW_RWT_Blade_st.dat"

    print(f"Constructed path: {path_st_file_DTU10MW}")
    print(f"File exists: {path_st_file_DTU10MW.exists()}")

    st_data_DTU10MW = load_st(path_st_file_DTU10MW, 0, 0)  # Baseline data

    # Scaling factor
    R_old = R_X
    R_new = R_Y # !! Use your own values !!
    scale_factor = R_new / R_old
    print(scale_factor, scale_factor**2,scale_factor**3,scale_factor**4)

    # %% Scaling ST-data
    st_data = scale_ST_data(st_data_DTU10MW, scale_factor)
    #print(st_data)
    #print(st_data_DTU10MW)

    # %% Plotting scaled and baseline data
    # Plotting m, I_x, I_y, I_p, S_chord, S_thickness
    fig, axs = plt.subplots(3, 1, figsize=(7, 6))
    # m_d
    ax = axs[0]
    ax.plot(st_data["s"], st_data["m"], label="scaled")
    ax.plot(st_data_DTU10MW["s"], st_data_DTU10MW["m"], label="DTU 10MW")
    ax.set_ylabel("$m$ [kg/m]")
    ax.grid()
    # Annotate first and last points for both curves
    #annotate_points(ax, st_data["s"], st_data["m"], "scaled")
    #annotate_points(ax, st_data_DTU10MW["s"], st_data_DTU10MW["m"], "DTU 10MW")

    # Display lines for both curves
    display_lines(ax, st_data["s"], st_data["m"], "scaled", stagger_offset=0.03)
    display_lines(ax, st_data_DTU10MW["s"], st_data_DTU10MW["m"], "DTU 10MW", stagger_offset=0.1)


    # I_x
    ax = axs[1]
    ax.plot(st_data["s"], st_data["I_x"], label="scaled")
    ax.plot(st_data_DTU10MW["s"], st_data_DTU10MW["I_x"], label="DTU 10MW")
    ax.set_ylabel("$I_x$ [m$^4$]")
    ax.set_ylim([0, 5.99])
    ax.grid()
    ax.legend()
    # Annotate first and last points for both curves
    #annotate_points(ax, st_data["s"], st_data["I_x"], "scaled")
    #annotate_points(ax, st_data_DTU10MW["s"], st_data_DTU10MW["I_x"], "DTU 10MW")

    # Display lines for both curves
    display_lines(ax, st_data["s"], st_data["I_x"], "scaled", stagger_offset=0.03)
    display_lines(ax, st_data_DTU10MW["s"], st_data_DTU10MW["I_x"], "DTU 10MW", stagger_offset=0.1)

    # I_y
    ax = axs[2]
    ax.plot(st_data["s"], st_data["I_y"], label="scaled")
    ax.plot(st_data_DTU10MW["s"], st_data_DTU10MW["I_y"], label="DTU 10MW")
    ax.set_ylabel("$I_y$ [m$^4$]")
    ax.set_xlabel("Curve length $r$ [m]")
    ax.grid()
    
    # Annotate first and last points for both curves
    #annotate_points(ax, st_data["s"], st_data["I_y"], "scaled")
    #annotate_points(ax, st_data_DTU10MW["s"], st_data_DTU10MW["I_y"], "DTU 10MW")

    # Display lines for both curves
    display_lines(ax, st_data["s"], st_data["I_y"], "scaled", stagger_offset=0.03)
    display_lines(ax, st_data_DTU10MW["s"], st_data_DTU10MW["I_y"], "DTU 10MW", stagger_offset=0.1)

    fig.tight_layout()
    plt.savefig("4-Mass and inertia redesign.pdf")
    plt.show()

    # create rigid data
    st_data_rigid = st_data.copy()
    st_data_rigid["E"] = st_data["E"]*1e7
    st_data_rigid["G"] = st_data["G"]*1e9

    # Saving the upscaled data
    out_dir = Path(__file__).parent
    path_out = script_dir / "hawc_files/our_design/data/Group1_RWT_Blade_st.dat"
    save_st(path_out, [st_data, st_data_rigid])


    # Side-by-side plots of the rotor speed (left plot) and pitch angles (right plot) versus wind speed
    script_dir = Path(__file__).parent
    rigid_path = script_dir / 'hawc_files/our_design/data/Group1_redesign_rigid.opt'
    rigid_data = load_oper(rigid_path)

    print(f"Constructed path: {rigid_path}")
    print(f"File exists: {rigid_path.exists()}")

    script_dir = Path(__file__).parent
    rigid_DTU_10_path = script_dir / 'hawc_files/our_design/data/dtu_10mw_rigid.opt'
    rigid_DTU_10_data = load_oper(rigid_DTU_10_path)

    print(f"Constructed path: {rigid_DTU_10_path}")
    print(f"File exists: {rigid_DTU_10_path.exists()}")


    script_dir = Path(__file__).parent
    flex_path = script_dir / 'hawc_files/our_design/data/Group1_redesign_flex.opt'
    flex_data = load_oper(flex_path)



    print(rigid_data.keys())


    fig1, axs1 = plt.subplots(1, 2, num=2, clear=True, figsize=(10,4))

    axs1[0].plot(rigid_data['ws_ms'], rigid_data['rotor_speed_rpm'], label='rigid redesign')
    axs1[0].plot(rigid_DTU_10_data['ws_ms'], rigid_DTU_10_data['rotor_speed_rpm'], label='DTU 10 MW')
    axs1[0].plot(flex_data['ws_ms'], flex_data['rotor_speed_rpm'], label='flex redesign')
    axs1[0].set_xlabel("wind speed [m/s]")
    axs1[0].set_ylabel("Rotor speed [rpm]")
    axs1[0].legend()
    axs1[0].grid(True)

    axs1[1].plot(rigid_data['ws_ms'], rigid_data['pitch_deg'], label='rigid redesign')
    axs1[1].plot(rigid_DTU_10_data['ws_ms'], rigid_DTU_10_data['pitch_deg'], label='DTU 10 MW')
    axs1[1].plot(flex_data['ws_ms'], flex_data['pitch_deg'], label='flex redesign')
    axs1[1].set_xlabel("wind speed [m/s]")
    axs1[1].set_ylabel("pitch [deg]")
    axs1[1].legend()
    axs1[1].grid(True)

    # Adjust layout and show the figure
    plt.tight_layout()
    plt.savefig("4-pitch and rot speed.pdf")
    plt.show()


    # Side-by-side plots of the aerodynamic power (left plot) and its coefficient (right plot), and the thrust (left plot) and its coefficient (right plot) versus wind speed
    fig1, axs1 = plt.subplots(1, 2, num=2, clear=True, figsize=(10,4))

    axs1[0].plot(rigid_data['ws_ms'], rigid_data['power_kw']/1000, label='rigid redesign')
    axs1[0].plot(rigid_DTU_10_data['ws_ms'], rigid_DTU_10_data['power_kw']/1000, label='DTU 10 MW')
    axs1[0].plot(flex_data['ws_ms'], flex_data['power_kw']/1000, label='flex redesign')
    axs1[0].set_ylabel("Power [MW]")
    axs1[0].set_xlabel("Wind speed [m/s]")
    axs1[0].legend()
    axs1[0].grid(True)

    axs1[1].plot(rigid_data['ws_ms'], rigid_data['thrust_kn']/1000, label='rigid redesign')
    axs1[1].plot(rigid_DTU_10_data['ws_ms'], rigid_DTU_10_data['thrust_kn']/1000, label='DTU 10 MW')
    axs1[1].plot(flex_data['ws_ms'], flex_data['thrust_kn']/1000, label='flex redesign')
    axs1[1].set_xlabel("wind speed [m/s]")
    axs1[1].set_ylabel("thrust [MN]")
    axs1[1].legend()
    axs1[1].grid(True)

    # Adjust layout and show the figure
    plt.tight_layout()
    plt.savefig("4-Power and Thrust.pdf")
    plt.show()

    fig1, axs1 = plt.subplots(1, 2, num=2, clear=True, figsize=(10,4))

    axs1[0].yaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))
    axs1[0].ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    axs1[0].plot(rigid_data['ws_ms'], rigid_data['power_kw']/(rigid_data['ws_ms']**3*1/2*np.pi*R_Y**2*1.225), label='rigid redesign')
    axs1[0].plot(rigid_DTU_10_data['ws_ms'], rigid_DTU_10_data['power_kw']/(rigid_DTU_10_data['ws_ms']**3*1/2*np.pi*R_X**2*1.225), label='DTU 10 MW')
    axs1[0].plot(flex_data['ws_ms'], flex_data['power_kw']/(flex_data['ws_ms']**3*1/2*np.pi*R_Y**2*1.225), label='flex redesign')
    axs1[0].set_ylabel("CP")
    axs1[0].set_xlabel("Wind speed [m/s]")
    axs1[0].legend()
    axs1[0].grid(True)
    #axs1[0].set_ylim(8000,10000)
    #axs1[0].set_xlim(10,12)

    axs1[1].yaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))
    axs1[1].ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    axs1[1].plot(rigid_data['ws_ms'], rigid_data['thrust_kn']/(rigid_data['ws_ms']**2*1/2*np.pi*R_Y**2*1.225), label='rigid redesign')
    axs1[1].plot(rigid_DTU_10_data['ws_ms'], rigid_DTU_10_data['thrust_kn']/(rigid_DTU_10_data['ws_ms']**2*1/2*np.pi*R_X**2*1.225), label='DTU 10 MW')
    axs1[1].plot(flex_data['ws_ms'], flex_data['thrust_kn']/(flex_data['ws_ms']**2*1/2*np.pi*R_Y**2*1.225), label='flex redesign')
    axs1[1].set_xlabel("wind speed [m/s]")
    axs1[1].set_ylabel("CT")
    axs1[1].legend()
    axs1[1].grid(True)

    # Adjust layout and show the figure
    plt.tight_layout()
    plt.savefig("4-Power and Thrust coefficients.pdf")
    plt.show()

# %%
