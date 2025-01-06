
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from our_values import *
from lacbox.io import load_stats, load_oper, ReadHAWC2


def extract_bd_master(file_path,
                      start_line = 125, end_line = 151):
    number = []
    x = []
    y = []
    z = []
    twist = []

    # Open the file and extract relevant lines
    with open(file_path, 'r') as file:
        lines = file.readlines()[start_line - 1:end_line]
        for line in lines:
            # Split the line into components
            parts = line.strip().split()
            number.append(int(parts[1]))
            x.append(float(parts[2]))
            y.append(float(parts[3]))
            z.append(float(parts[4]))
            twist.append(float(parts[5]))

    # Create a DataFrame
    data = {
        'number': np.array(number),
        'x': np.array(x),
        'y': np.array(y),
        'z': np.array(z),
        'twist': np.array(twist),
    }

    return data


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



# hawc2s values

def load_ctrl_tuning(file_path):
    with open(file_path, 'r') as file:
        file_content = file.read()

    # Split the file content into lines
    lines = file_content.splitlines()

    # Initialize the dictionary with predefined keys
    data_dict = {
        "K_opt": None,
        "I": None,
        "Kp_torque": None,
        "Ki_torque": None,
        "Kp_pitch": None,
        "Ki_pitch": None,
        "KK1": None,
        "KK2": None,
        "dQ_dtheta_0": None
    }

    # Manually assign values based on line positions
    data_dict["K_opt"] = float(lines[1].split('=')[1].split()[0])
    data_dict["I"] = float(lines[3].split('=')[1].split()[0])
    data_dict["Kp_torque"] = float(lines[4].split('=')[1].split()[0])
    data_dict["Ki_torque"] = float(lines[5].split('=')[1].split()[0])
    data_dict["Kp_pitch"] = float(lines[7].split('=')[1].split()[0])
    data_dict["Ki_pitch"] = float(lines[8].split('=')[1].split()[0])
    data_dict["KK1"] = float(lines[9].split('=')[1].split()[0])
    data_dict["KK2"] = float(lines[9].split('=')[2].split()[0])
    data_dict["dQ_dtheta_0"] = float(lines[9].split('=')[3].split()[0])

    #data_dict["dQ_dtheta_0"] = np.rad2deg(data_dict["dQ_dtheta_0"])*1e3



    fit = pd.read_csv(file_path, sep='\\s+', skiprows=17, header=None)
    fit.columns = ['theta', 'dq_dtheta', 'fit_theta', 'dq_domega', 'fit_omega']

    return data_dict, fit

def fit_curve_KK(fit_redesign, hawc2s_data):

    theta = fit_redesign['theta']
    dQdtheta = fit_redesign['dq_dtheta']  # Replace with your actual y data
    c = hawc2s_data["dQ_dtheta_0"]

    # Fit the model to the data
    def model(x, K1, K2):
        return c * (1 + x/K1 + (x**2)/K2)

    initial_guess = [1, 1]  # Initial guess for K1 and K2
    params, covariance = curve_fit(model, theta, dQdtheta, p0=initial_guess)

    # Extract the optimal values of K1 and K2
    KK1, KK2 = params
    dQdtheta_fit =  model(theta, KK1, KK2)

    return KK1, KK2, dQdtheta_fit

def compute_ctrl_tuning(hawc2s_data, fit_redesign):

    eta = 1
    I_r = 1         # rotor inertia, what is the value?
    I_g = 1         # equivalent generator inertia, what is the value?
    n_g = 1         # gear box ratio
    I = I_r + n_g**2 * I_g
    I = hawc2s_data['I']

    # region 2: optinmal CP tracking
    K_opt = eta * RHO * np.pi * R_Y**5 * CP_MAX / (2 * TSR_OPT**3)

    # region 2.5: rotor speed regulation
    omega_speed_torque = 0.05*2*np.pi
    zeta_speed_torque = 0.7
    Kp_torque = 2 * eta * zeta_speed_torque * omega_speed_torque * I
    Ki_torque = eta * I * omega_speed_torque**2

    # region 3:
    omega_speed_pitch = 0.06*2*np.pi
    zeta_speed_pitch = 0.7
    KK1, KK2, dQdtheta_fit = fit_curve_KK(fit_redesign, hawc2s_data)
    dQ_dtheta_0 = np.rad2deg(hawc2s_data['dQ_dtheta_0'])*1e3     # ???

    dQ_dtheta = dQ_dtheta_0
    dQg_domega = POWER_MAX / ((OMEGA_MAX*2*np.pi/60)**2)

    Kp_pitch = (2 * zeta_speed_pitch * omega_speed_pitch * I + 1/eta *dQg_domega) / (-dQ_dtheta)
    Ki_pitch = (omega_speed_pitch**2 * I) / (- dQ_dtheta)
    
    # K_P_P = -(2*(I)*omega_P*zeta+Power/rot_speed**2)/dqdtheta
    
    dQ_dtheta_0  = np.deg2rad(dQ_dtheta_0/1e3)
    th_data = {
            "K_opt": K_opt,
            "I": I,
            "Kp_torque": Kp_torque,
            "Ki_torque": Ki_torque,
            "Kp_pitch": Kp_pitch,
            "Ki_pitch": Ki_pitch,
            "KK1": KK1,
            "KK2": KK2,
            "dQ_dtheta_0": dQ_dtheta_0
        }
    
    return th_data


def ideal_curve(flex_path, res_step_path):
    data = load_oper(flex_path)

    wind_speed =data['ws_ms']#[i for i in range(len(data['ws_ms']))]

    h2res = ReadHAWC2(res_step_path)

    # find time for every wind speed
    idx_array = []
    for ws in wind_speed:
        idx = np.argmin(h2res.data[:,14] < ws)
        idx_array.append(idx)

    idx_array = np.array(idx_array)
    idx_array[6] = idx_array[6]-4000
    idx_array[20] = idx_array[20]-4000
    idx_array[25] = idx_array[25]-4000
    for i in range(8,17):
        idx_array[i] = idx_array[17]
    
    return idx_array


def compute_overshoot_settling(array, idx_start, mean, tolerance=0.01):
    
    idx_lim = idx_start + 3800
    array_reduced = array[idx_start:idx_lim]
    overshoot = np.max(abs(array_reduced))/mean*100
    
    ratio = array_reduced / mean
    more = ratio < 1+tolerance
    less = ratio > 1-tolerance
    combined = more & less
    reversed_idx = np.argmax(combined[::-1] == False)
    settling_idx =  len(ratio) - reversed_idx

    settling_idx += idx_start

    return overshoot, settling_idx


def load_calculation(STATS_PATH, SUBFOLDER, CHAN_DESCS, chan_ids):
    '''
    function that extract operational data and load from the csv file
    in the output dictionary you can chose:
      chan_id for the channels
          min / mean / max for the different data set
              minimum / average / maximum for the different arrays
              scatter for all values in the data set
    '''

    value_list = ['min', 'mean', 'max']
    data = {}

    df, _ = load_stats(STATS_PATH, subfolder=SUBFOLDER, statstype='turb')

    for _, chan_id in enumerate(chan_ids):

        # isolate the channel data
        chan_df = df.filter_channel(chan_id, CHAN_DESCS)

        # extract hawc2 wind and channel to plot from the HAWC2 stats
        h2_wind = chan_df['wsp']

        data_channel = {}

        for value in value_list:
            HAWC2val = chan_df[value]

            h2_wind, HAWC2val = np.array(h2_wind), np.array(HAWC2val) # wind speed, loads
            i_h2 = np.argsort(h2_wind) # sorts indexies so the wind speed array is in ascending order

            groups = [i_h2[i:i + 6] for i in range(0, len(i_h2), 6)]
            nws = len(groups)
            ws_array = np.zeros(nws)
            average_array = np.zeros(nws)
            max_array = np.zeros(nws)
            min_array = np.zeros(nws)

            for idx, group in enumerate(groups): # index, group
                ws_array[idx] = h2_wind[groups[idx]][0]
                average_array[idx] = np.mean(HAWC2val[groups[idx]])
                max_array[idx] = np.max(HAWC2val[groups[idx]])
                min_array[idx] = np.min(HAWC2val[groups[idx]])
            
            data_value = {
                'scatter_wind': h2_wind[i_h2],
                'scatter_load': HAWC2val[i_h2],
                'ws': ws_array,
                'ave': average_array,
                'max': max_array,
                'min': min_array,
            }

            data_channel[value] = data_value
        
        data[chan_id] = data_channel

    return data


def DEL_calculation(STATS_PATH, SUBFOLDER, CHAN_DESCS, wohler_4, wohler_10,
                    n_seed=6, n_t=20*365*24*60*60 , n_life=1e7, n_eq = 10*60):
    
    '''
    function that extract DEL from the csv file
    in the output dictionary you can chose:
      chan_id for the channels
        scatter for all values in the data set
        Equivalent load and relative confident interval
        life equivalent load
    '''

    AEP_data = AEP_calculation(STATS_PATH, SUBFOLDER, CHAN_DESCS)
    ws_prob = AEP_data['prob']
    chan_ids = wohler_4 + wohler_10

    data = {}

    # load the HAWC2 data from the stats file. Isolate the simulations with no tilt.
    df, _ = load_stats(STATS_PATH, subfolder=SUBFOLDER, statstype='turb')

    # loop over each channels
    for iplot, chan_id in enumerate(chan_ids):

        # isolate the channel data
        chan_df = df.filter_channel(chan_id, CHAN_DESCS)

        # extract hawc2 wind and channel to plot from the HAWC2 stats
        h2_wind = chan_df['wsp']

        if chan_id in wohler_4:
            HAWC2val = chan_df['del4']
            wohler_exp = 4
        elif chan_id in wohler_10:
            HAWC2val = chan_df['del10']
            wohler_exp = 10
        else:
            continue        # goes to the next element in the loop

        h2_wind, HAWC2val = np.array(h2_wind), np.array(HAWC2val)
        i_h2 = np.argsort(h2_wind)

        # compute 10-min DELs combined within each wind-speed bin: 
        groups = [i_h2[i:i + 6] for i in range(0, len(i_h2), 6)]
        nws = len(groups)
        ws_array = np.zeros(nws)
        R_eq_array = np.zeros(nws)
        ci_array = np.zeros(nws)
        for idx, group in enumerate(groups):
            ws_array[idx] = h2_wind[groups[idx]][0]
            R_eq_array[idx] = (sum(HAWC2val[groups[idx]]**wohler_exp)/n_seed)**(1/wohler_exp) # takes an average load from the 6 cases

            ci_array[idx] = 1.96 * np.std(HAWC2val[groups[idx]], ddof=1) / np.sqrt(6)

        # compute equivalent lifetime load     
        R_eql = (sum(ws_prob * R_eq_array**wohler_exp) * n_t / n_life) ** (1 / wohler_exp)

        data_channel = {
            'wohler_exp': wohler_exp,
            'scatter_wind': h2_wind[i_h2],
            'scatter_load': HAWC2val[i_h2],
            'ws': ws_array,
            'R_eq': R_eq_array,
            'R_eq_err': ci_array,
            'R_eql': R_eql
        }

        data[chan_id] = data_channel

    data_general = {
        'channels': wohler_4 + wohler_10
    }
    data['general'] = data_general

    return data


def twr_clr_calculation(STATS_PATH, SUBFOLDER, CHAN_DESCS):
    '''
    function that extract tower clearance from the csv file
    gives tower clearance per wind speed
    '''
        
    df, _ = load_stats(STATS_PATH, subfolder=SUBFOLDER, statstype='turb')
    chan_id = 'Twrclr'
    chan_df = df.filter_channel(chan_id, CHAN_DESCS)
    h2_wind = chan_df['wsp']
    HAWC2val = chan_df['min']
    h2_wind, HAWC2val = np.array(h2_wind), np.array(HAWC2val)
    i_h2 = np.argsort(h2_wind)
    groups = [i_h2[i:i + 6] for i in range(0, len(i_h2), 6)]
    nws = len(groups)
    ws_array = np.zeros(nws)
    twr_clr_array = np.zeros(nws)
    for idx, group in enumerate(groups):
        ws_array[idx] = h2_wind[groups[idx]][0]
        twr_clr_array[idx] = np.amin(HAWC2val[groups[idx]])

    result = {
        'ws' : ws_array,                 # wind speeds
        'twr_clr': twr_clr_array,        # Edges of wind-speed bins
    }

    return result


def AEP_calculation(STATS_PATH, SUBFOLDER, CHAN_DESCS, wind_class=3):
    '''
    function that extract probability and AEP from the csv file
    gives probability per bin, power per bin, final AEP value
    '''
        
    df, _ = load_stats(STATS_PATH, subfolder=SUBFOLDER, statstype='turb')
    chan_id = 'ElPow'
    chan_df = df.filter_channel(chan_id, CHAN_DESCS)
    h2_wind = chan_df['wsp']
    HAWC2val = chan_df['mean']
    h2_wind, HAWC2val = np.array(h2_wind), np.array(HAWC2val)
    i_h2 = np.argsort(h2_wind)
    groups = [i_h2[i:i + 6] for i in range(0, len(i_h2), 6)]
    nws = len(groups)
    ws_array = np.zeros(nws)
    power_array = np.zeros(nws)
    for idx, group in enumerate(groups):
        ws_array[idx] = h2_wind[groups[idx]][0]
        power_array[idx] = np.mean(HAWC2val[groups[idx]])

    if wind_class == 3:
        V_ave = 7.5
    if wind_class == 1:
        V_ave = 10

    prob_array = np.zeros(len(ws_array))
    for i, ws in enumerate(ws_array):
        p1 = 1 - np.exp(-np.pi*((ws-0.5)/(2*V_ave))**2)
        p2 = 1 - np.exp(-np.pi*((ws+0.5)/(2*V_ave))**2)
        prob_array[i] = p2 - p1

    T = 365 * 24

    AEP = sum(prob_array * power_array)*T
    
    if len(prob_array)==21:
        AEP1 = sum(prob_array[1:] * power_array[1:])*T
        AEP_bin1 = prob_array[0] * power_array[0]* T/2
        AEP = AEP1 + AEP_bin1


    result = {
        'ws' : ws_array,                 # wind speeds
        'prob' : prob_array,           # Bin probabilities
        'power' : power_array/1e6,      # Power in each bin [MW]
        'AEP' : AEP/1e9                 # annual energy production [GWh]
    }

    return result

def filter_ctrl_output(time, y, div):
    n = len(time)
    delta = int(div/2)

    result = np.zeros(n)
    for i in range(delta,n-delta):
        result[i] = np.mean(y[i-delta:i+delta])

    for i in range(0,delta):
        result[i] = np.mean(y[0:delta])
    for i in range(n-delta, n):
        result[i] = np.mean(y[n-delta:n])

    return result
