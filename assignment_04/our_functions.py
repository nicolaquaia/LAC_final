"""
useful function for assignment 4 but can be expanded
Created on Sat 9/11

@author: Group 1
"""

import numpy as np
from our_values import *
from lacbox.io import load_stats

def DEL_calculation(STATS_PATH, SUBFOLDER, chan_ids, CHAN_DESCS, wohler_4, wohler_10,
                    ws_prob,
                    n_seed=6, n_t=20*365*24*60*60 , n_life=1e7, n_eq = 10*60):
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
        ws_array = np.zeros(20)
        R_eq_array = np.zeros(20)
        for idx, group in enumerate(groups):
            ws_array[idx] = h2_wind[groups[idx]][0]
            R_eq_array[idx] = (sum(HAWC2val[groups[idx]]**wohler_exp)/n_seed)**(1/wohler_exp) # takes an average load from the 6 cases

        # compute equivalent lifetime load
        R_eql = (sum(ws_prob * R_eq_array**wohler_exp) * n_t / n_life) ** (1 / wohler_exp)

        data_channel = {
            'wohler_exp': wohler_exp,
            'scatter_wind': h2_wind,
            'scatter_load': HAWC2val,
            'ws': ws_array,
            'R_eq': R_eq_array,
            'R_eql': R_eql
        }

        data[chan_id] = data_channel
    
    data_general = {
        'channels': wohler_4 + wohler_10
    }
    data['general'] = data_general

    return data


def AEP_calculation(STATS_PATH, SUBFOLDER,CHAN_DESCS):
    df, _ = load_stats(STATS_PATH, subfolder=SUBFOLDER, statstype='turb')
    chan_id = 'ElPow'
    chan_df = df.filter_channel(chan_id, CHAN_DESCS)
    h2_wind = chan_df['wsp']
    HAWC2val = chan_df['mean']
    h2_wind, HAWC2val = np.array(h2_wind), np.array(HAWC2val)
    i_h2 = np.argsort(h2_wind)
    groups = [i_h2[i:i + 6] for i in range(0, len(i_h2), 6)]
    ws_array = np.zeros(20)
    power_array = np.zeros(20)
    for idx, group in enumerate(groups):
        ws_array[idx] = h2_wind[groups[idx]][0]
        power_array[idx] = np.mean(HAWC2val[groups[idx]])

    bins = [(ws - 0.5, ws + 0.5) for ws in ws_array]

    prob_array = np.zeros(len(ws_array))
    for i, ws in enumerate(ws_array):
        a = ((ws - 0.5)**2 * np.pi) / 225
        b = ((ws + 0.5)**2 * np.pi) / 225
        prob_array[i] = np.exp(-a) - np.exp(-b)

    T = 365 * 24
    AEP = sum(prob_array * power_array)*T

    result = {
        'ws' : ws_array,                 # wind speeds
        'bins': bins,                   # Edges of wind-speed bins
        'prob' : prob_array ,           # Bin probabilities
        'power' : power_array/1e6,      # Power in each bin [MW]
        'AEP' : AEP/1e9                 # annual energy production [GWh]
    }

    return result



def filter(time, y, div):
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
