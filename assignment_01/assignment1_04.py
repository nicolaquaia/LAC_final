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


if __name__ == "__main__":
    # %% Import modules
    import matplotlib.pyplot as plt
    from lacbox.io import load_st,save_st, load_oper
    from pathlib import Path
    from Our_values import*
    from lacbox.test import test_data_path
    import copy


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
    # I_x
    ax = axs[1]
    ax.plot(st_data["s"], st_data["I_x"], label="scaled")
    ax.plot(st_data_DTU10MW["s"], st_data_DTU10MW["I_x"], label="DTU 10MW")
    ax.set_ylabel("$I_x$ [m$^4$]")
    ax.grid()
    ax.legend()
    # I_y
    ax = axs[2]
    ax.plot(st_data["s"], st_data["I_y"], label="scaled")
    ax.plot(st_data_DTU10MW["s"], st_data_DTU10MW["I_y"], label="DTU 10MW")
    ax.set_ylabel("$I_y$ [m$^4$]")
    ax.set_xlabel("Curve length $r$ [m]")
    ax.grid()

    fig.tight_layout()
    plt.close()
    #plt.show()

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



    #print(rigid_data.keys())

    # plotting omega and pitch as function of ws
    fig1, axs1 = plt.subplots(1, 2, num=2, clear=True, figsize=(18,8))

    axs1[0].plot(rigid_data['ws_ms'], rigid_data['rotor_speed_rpm'], label='redesign')
    axs1[0].plot(rigid_DTU_10_data['ws_ms'], rigid_DTU_10_data['rotor_speed_rpm'], label='DTU_10')
    axs1[0].plot(flex_data['ws_ms'], flex_data['rotor_speed_rpm'], label='flex redesign')
    axs1[0].set_xlabel("wind speed [m/s]")
    axs1[0].set_ylabel("Rotor speed [rpm]")
    axs1[0].legend()
    axs1[0].grid(True)

    axs1[1].plot(rigid_data['ws_ms'], rigid_data['pitch_deg'], label='redesign')
    axs1[1].plot(rigid_DTU_10_data['ws_ms'], rigid_DTU_10_data['pitch_deg'], label='DTU_10')
    axs1[1].plot(flex_data['ws_ms'], flex_data['pitch_deg'], label='flex redesign')
    axs1[1].set_xlabel("wind speed [m/s]")
    axs1[1].set_ylabel("pitch [deg]")
    axs1[1].legend()
    axs1[1].grid(True)

    # Adjust layout and show the figure
    plt.tight_layout()
    #plt.show()

    # plotting P and T as function of ws
    # Side-by-side plots of the aerodynamic power (left plot) and its coefficient (right plot), and the thrust (left plot) and its coefficient (right plot) versus wind speed
    fig1, axs1 = plt.subplots(1, 2, num=2, clear=True, figsize=(18,8))

    axs1[0].plot(rigid_data['ws_ms'], rigid_data['power_kw'], label='redesign')
    axs1[0].plot(rigid_DTU_10_data['ws_ms'], rigid_DTU_10_data['power_kw'], label='DTU_10')
    axs1[0].plot(flex_data['ws_ms'], flex_data['power_kw'], label='flex redesign')
    axs1[0].set_ylabel("Power [kW]")
    axs1[0].set_xlabel("Wind speed [m/s]")
    axs1[0].legend()
    axs1[0].grid(True)

    axs1[1].plot(rigid_data['ws_ms'], rigid_data['thrust_kn'], label='redesign')
    axs1[1].plot(rigid_DTU_10_data['ws_ms'], rigid_DTU_10_data['thrust_kn'], label='DTU_10')
    axs1[1].plot(flex_data['ws_ms'], flex_data['thrust_kn'], label='flex redesign')
    axs1[1].set_xlabel("wind speed [m/s]")
    axs1[1].set_ylabel("thrust [kN]")
    axs1[1].legend()
    axs1[1].grid(True)

    # Adjust layout and show the figure
    plt.tight_layout()
    #plt.show()


    # plotting CP and CT as function of ws

    rho = 1.225
    CP_rigid = rigid_data['power_kw'] / (0.5 * rho * rigid_data['ws_ms']**3 * np.pi*R_Y**2)*1e3
    CP_flex = flex_data['power_kw'] / (0.5 * rho * flex_data['ws_ms']**3 * np.pi*R_Y**2)*1e3
    CP_DTU_10 = rigid_DTU_10_data['power_kw'] / (0.5 * rho * rigid_DTU_10_data['ws_ms']**3 * np.pi*R_X**2)*1e3

    CT_rigid = rigid_data['thrust_kn'] / (0.5 * rho * rigid_data['ws_ms']**2 * np.pi*R_Y**2)*1e3
    CT_flex = flex_data['thrust_kn'] / (0.5 * rho * flex_data['ws_ms']**2 * np.pi*R_Y**2)*1e3
    CT_DTU_10 = rigid_DTU_10_data['thrust_kn'] / (0.5 * rho * rigid_DTU_10_data['ws_ms']**2 * np.pi*R_X**2)*1e3
    
    fig1, axs1 = plt.subplots(1, 2, num=2, clear=True, figsize=(18,8))

    axs1[0].plot(rigid_data['ws_ms'], CP_rigid, label='redesign')
    axs1[0].plot(rigid_DTU_10_data['ws_ms'], CP_DTU_10, label='DTU_10')
    axs1[0].plot(flex_data['ws_ms'], CP_flex, label='flex redesign')
    axs1[0].set_ylabel("Power coefficient")
    axs1[0].set_xlabel("Wind speed [m/s]")
    axs1[0].legend()
    axs1[0].grid(True)
    #axs1[0].set_ylim(8000,10000)
    #axs1[0].set_xlim(10,12)

    axs1[1].plot(rigid_data['ws_ms'], CT_rigid, label='redesign')
    axs1[1].plot(rigid_DTU_10_data['ws_ms'], CT_DTU_10, label='DTU_10')
    axs1[1].plot(flex_data['ws_ms'], CT_flex, label='flex redesign')
    axs1[1].set_xlabel("wind speed [m/s]")
    axs1[1].set_ylabel("Thrust coefficient")
    axs1[1].legend()
    axs1[1].grid(True)

    # Adjust layout and show the figure
    plt.tight_layout()
    plt.show()
