
import numpy as np
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
    if SUBFOLDER == 'tca':
        ws_prob = [0.06442809, 0.0709227,  0.07472189, 0.07591763, 0.0747455,  0.07155162,
                   0.06675382, 0.06080169, 0.05413969, 0.04717648, 0.04026251, 0.03367663,
                   0.02762128, 0.02222493, 0.01755019, 0.01360521, 0.01035688, 0.00774379,
                   0.00568809, 0.0041053 ]

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
