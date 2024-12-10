"""
Create turbulent files to sent to Gbar
"""
from pathlib import Path
import random
import numpy as np
from lacbox.htc import _clean_directory
from lacbox.io import load_oper, load_ctrl_txt
from myteampack import MyHTC


def get_initial_rotor_speed(wsp, opt_path):
    """Given a wind speed and path to opt file, find initial rotor speed.

    Args:
        wsp (int, float): Wind speed [m/s].
        opt_path (str, pathlib.Path): Path to opt file.

    Returns:
        int, float: Initial rotor speed interpolated from opt file [rad/s].
    """
    opt_dict = load_oper(opt_path)
    opt_wsps = opt_dict['ws_ms']
    opt_rpm = opt_dict['rotor_speed_rpm']
    omega_rpm = np.interp(wsp, opt_wsps, opt_rpm)
    omega0 = omega_rpm * np.pi / 30  # rpm to rad/s
    return omega0

def make_single_turb(htc, wsp, turbclass, htc_dir='./htc_turb/', res_dir='./res_turb/',
                     subfolder='', opt_path=None, seed=1337, time_start=100, time_stop=700,
                     dy=190, dz=190,
                     P_rated = 10000, min_rot_speed = 0.628, rated_rot_speed = 1.005, max_torque = 15600000, theta_min = 101, 
                     K_opt =  0.152220E+08, KpTrq = 0.846963E+08, KiTrq = 0.190058E+08, constant_power = 0, KpPit = 0.152275E+01,
                    KiPit = 0.293368E+00, K1 = 14.93110, K2 = 464.06438, 
                    **kwargs ):
    """Make a single turbulent-wind file from a master file.
    """
    nx, ny, nz = 1024, 32, 32  # hard-code turbbox size for lac course
    # define the append name based on the subfolder and the wind speed
    wsp_seed_str = ('%.1f' % (wsp)).zfill(4) + ('_%i' % seed)  # e.g., '05.0_1337'
    if subfolder:
        append = f'_turb_{subfolder}_{wsp_seed_str}'  # e.g., '_turb_tca_05.0_1337'
    else:
        append = f'_turb_{wsp_seed_str}'  # e.g.,, '_turb_05.0_1337'
    # get new filename (excl extension) from HTCFile attribute "filename"
    fname = Path(htc.filename).name.replace('.htc', append)
    # delete hawcstab2 block
    del htc.hawcstab2    

    # correct initial rotor speed if opt file is given
    if opt_path is not None:
        omega0 = get_initial_rotor_speed(wsp, opt_path)
        htc._set_initial_rotor_speed(omega0)    

    # set the start and stop time
    htc.set_time(start=time_start, stop=time_stop)  # simulation times

    # calculate turbulence intensity for this turbulence class and wind speed
    if turbclass == 'A' :
        i_ref =  0.16
    if turbclass == 'B' :
        i_ref =  0.14
    else :
        i_ref =  0.12
    tint = i_ref*(0.75*wsp+5.6)/wsp

    # set parameters in wind block
    htc.wind.tint = tint
    htc.wind.turb_format = 1  #mann or flex ?
    htc.wind.tower_shadow_method = 3
    htc.wind.wsp = wsp  # mean wind speed
    htc.wind.shear_format = [3, 0.2]

    # set parameters in mann block
    turb_filesname = [f'./turb/{fname}_turb_{c}.bin' for c in 'uvw']
    no_grid_points = (nx, ny, nz)
    box_dimension = (wsp * (time_stop - time_start), dy, dz)
    htc.add_mann_turbulence(L=29.4, ae23=1, Gamma=3.9,
                            seed=seed, high_frq_compensation=0,
                            filenames=turb_filesname, no_grid_points=no_grid_points,
                            box_dimension=box_dimension,
                            dont_scale=False)
    
    # add case specific info
    htc.dll.type2_dll__1.init.constant__1 =   [1,P_rated]
    htc.dll.type2_dll__1.init.constant__2 =   [2,min_rot_speed]
    htc.dll.type2_dll__1.init.constant__3 =   [3,rated_rot_speed]
    htc.dll.type2_dll__1.init.constant__4 =   [4,max_torque]
    htc.dll.type2_dll__1.init.constant__5 =   [5,theta_min]
    htc.dll.type2_dll__1.init.constant__11 = [11,K_opt]
    htc.dll.type2_dll__1.init.constant__12 = [12,KpTrq]
    htc.dll.type2_dll__1.init.constant__13 = [13,KiTrq]
    htc.dll.type2_dll__1.init.constant__15 = [15,constant_power]
    htc.dll.type2_dll__1.init.constant__16 = [16,KpPit]
    htc.dll.type2_dll__1.init.constant__17 = [17,KiPit]
    htc.dll.type2_dll__1.init.constant__21 = [21,K1]
    htc.dll.type2_dll__1.init.constant__22 = [22,K2]

    # update name and save file (reprint of _update_name_and_save() b.c. missing kwargs to set_name)
    save_dir = Path(htc_dir)  # sanitize inputs
    # set filename using HTCFile method
    htc.set_name(fname, resdir=res_dir, subfolder=subfolder, htcdir=htc_dir)
    # save the file
    htc.save((save_dir / subfolder / (fname + '.htc')).as_posix())
    return


def main():
    """
    Create the htc files for the different cases, adjusting settings.
    Save the htc files in subfolders corresponding to the different cases.
    This code would be better placed at the end of your make_htc_files.py script...
    """
    # constants for this script
    del_htc_dir = True  # delete htc directory if it already exists?
    master_htc = './_master/remodel.htc'
    opt_path = './data/remodel_flex2.opt'
    wsps = range(4, 25)  # wind speed range

    # control specific: change all 3
    htc_dir = './htc_turb_C12/'  # top-level folder to save htc files (can be path to gbar!)
    res_dir = './res_turb_C12/'  # where HAWC2 should save res files, relative to its working directory
    control_output = load_ctrl_txt(f'res_hawc2s/remodel_hawc2s_ctrl_C12_ctrl_tuning.txt')


    start_seed = 42  # initialize the random-number generator for reproducability
    turbclasses = ['A','B']  # turbulence class
    num_seeds = 6  # Number of different seeds for each wind speed
    # delete the top-level directory if requested
    _clean_directory(htc_dir, del_htc_dir)
    for turbclass in turbclasses:
        # make the files
        random.seed(start_seed)
        subfolder = 'tc' + turbclass.lower()
        for wsp in wsps:
            # Generate multiple seeds for each wind speed
            for _ in range(num_seeds):
                sim_seed = random.randrange(int(2**16))
                htc = MyHTC(master_htc)
                make_single_turb(htc, wsp, turbclass, htc_dir=htc_dir, res_dir=res_dir,
                                subfolder=subfolder, opt_path=opt_path, seed=sim_seed,
                                P_rated = 10638.3,
                                min_rot_speed = 0.6283185307179586,
                                rated_rot_speed = 0.982543516758902,
                                max_torque = 18200000,
                                theta_min = 101,
                                constant_power = 1,
                                KpTrq = control_output['KpTrq_Nm/(rad/s)'],
                                KiTrq = control_output['KiTrq_Nm/rad'],
                                KpPit = control_output['KpPit_rad/(rad/s)'],
                                KiPit = control_output['KiPit_rad/rad'],
                                K1 = control_output['K1_deg'],
                                K2 = control_output['K2_deg^2'],
                                K_opt = control_output['K_Nm/(rad/s)^2']
                )

# the "script" part of this file
if __name__ == '__main__':
    main()
