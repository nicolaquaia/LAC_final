"""Make all the htc files for the LAC course from a single base file.

Requires myteampack (which requires lacbox).
"""
from myteampack import MyHTC
from lacbox.io import load_ctrl_txt

if __name__ == '__main__':
    ORIG_PATH = './_master/remodel.htc'
    SAVE_HAWC2S_DIR = '.'
    SAVE_HAWC2S_STEP = '.'

    # make rigid hawc2s file for single-wsp opt file
    htc = MyHTC(ORIG_PATH)
    htc.make_hawc2s(SAVE_HAWC2S_DIR,
                    rigid=True,
                    append='_hawc2s_1wsp',
                    opt_path='./data/remodel_1wsp.opt',
                    compute_steady_states=True,
                    save_power=True,
                    save_induction=True,
                    minpitch = 0
                    )

    htc = MyHTC(ORIG_PATH)
    # make rigid hawc2s file for multi-wsp opt file
    htc.make_hawc2s(SAVE_HAWC2S_DIR,
                    rigid=True,
                    append='_hawc2s_multitsr',
                    opt_path='./data/remodel_multitsr.opt',
                    compute_steady_states=True,
                    save_power=True,
                    save_induction=True,
                    minpitch = 0
                    )
                  
    htc = MyHTC(ORIG_PATH)
    # make rigid hawc2s file for compute rigid opt file
    htc.make_hawc2s(SAVE_HAWC2S_DIR,
                    rigid=True,
                    append='_hawc2s_compute_rigid_opt',
                    opt_path='./data/remodel_3_columns.opt',
                    compute_steady_states=False,
                    save_power=False,
                    compute_optimal_pitch_angle = True,
                    minpitch = 0,
                    opt_lambda=8.03746245202556,
                    genspeed= (50*6, 50*9.382599449704426),
                    windspeed =(3, 25, 23)
                    )
    
    htc = MyHTC(ORIG_PATH)
    # make rigid hawc2s file for compute rigid opt file
    htc.make_hawc2s(SAVE_HAWC2S_DIR,
                    rigid=True,
                    append='_hawc2s_compute_rigid_shaved',
                    opt_path='./data/remodel_rigid_shaved.opt',
                    compute_steady_states=True,
                    save_power=True,
                    compute_optimal_pitch_angle = False,
                    minpitch = 0,
                    opt_lambda=8.03746245202556,
                    genspeed= (50*6, 50*9.382599449704426),
                    windspeed =(3, 25, 23)
                    )


    htc = MyHTC(ORIG_PATH)
    # make rigid hawc2s file for compute rigid opt file
    htc.make_hawc2s(SAVE_HAWC2S_DIR,
                    rigid=False,
                    append='_hawc2s_flex',
                    opt_path='./data/remodel_rigid.opt',
                    compute_steady_states=True,
                    save_power=False,
                    compute_optimal_pitch_angle = True,
                    minpitch = 0,
                    opt_lambda=8.03746245202556,
                    genspeed= (50*6, 50*9.382599449704426),
                    windspeed =(3, 25, 23))
    
    htc = MyHTC(ORIG_PATH)
    # make rigid hawc2s file for compute rigid opt file
    htc.make_hawc2s(SAVE_HAWC2S_DIR,
                    rigid=False,
                    append='_hawc2s_compute_flex_shaved',
                    opt_path='./data/remodel_flex_shaved.opt',
                    compute_steady_states=True,
                    save_power=True,
                    compute_optimal_pitch_angle = False,
                    minpitch = 0,
                    opt_lambda=8.03746245202556,
                    genspeed= (50*6, 50*9.382599449704426),
                    windspeed =(3, 25, 23)
                    )
    

    # controller
    # remove region
    htc = MyHTC(ORIG_PATH)
    htc.make_hawc2s_ctrltune(SAVE_HAWC2S_DIR,
                rigid=False,
                append='_hawc2s_ctrltune',
                opt_path='./data/remodel_flex2.opt',
                compute_steady_states=True,
                compute_controller_input = True,
                save_power = True,
                genspeed= (6, 9.382599449704426),
                gearratio = 1.0,
                minpitch = 0,
                opt_lambda=8.03746245202556,
                maxpow = 10641.618,
                partial_load = (0.05, 0.7),
                full_load = (0.06, 0.7),
                gain_scheduling = 2,
                constant_power = 1,
                windspeed = (4, 25, 22)
                )

    # assignment 3 part 2
    htc = MyHTC(ORIG_PATH)
    #data_fqc_damp = [[0.05,0.01,0.10,0.05,0.01,0.10,0.06,0.04,0.05,0.05],[0.7,0.7,0.7,0.7,0.7,0.7,0.7,0.7,0.8,0.65],[1,1,1,0,0,0,1,1,1,1]]
    data_fqc_damp = [[0.05,0.01,0.10,0.05,0.01,0.10, 0.08,0.06,0.04,0.04,0.04,0.04,0.04],   # omega
                     [0.7 ,0.7 ,0.7 ,0.7 ,0.7 ,0.7 , 0.7 ,0.7 ,0.7 ,0.9 ,0.8 ,0.6 ,0.5 ],   # zeta
                     [1  , 1  , 1  , 0  , 0  , 0   , 1,   1,   1   ,1   ,1   ,1   ,1   ]]   # const power = 1, const torque = 0
    
    for k in range(len(data_fqc_damp[0])):
        htc = MyHTC(ORIG_PATH)
        htc.make_hawc2s_ctrltune(SAVE_HAWC2S_DIR,
                        rigid=False,
                        append=f'_hawc2s_ctrl_C{k+1}',
                        opt_path='./data/remodel_flex2.opt',
                        compute_steady_states=True,
                        compute_controller_input = True,
                        minpitch = 0,
                        opt_lambda=8.03746245202556,
                        genspeed= (6, 9.382599449704426),
                        gearratio=1.0,
                        partial_load = (0.05, 0.7),
                        full_load = (data_fqc_damp[0][k], data_fqc_damp[1][k]),
                        gain_scheduling = 2,
                        constant_power = data_fqc_damp[2][k]
        )

        control_output = load_ctrl_txt(f'res_hawc2s/remodel_hawc2s_ctrl_C{k+1}_ctrl_tuning.txt')
        htc = MyHTC(ORIG_PATH)
        htc.make_step(SAVE_HAWC2S_STEP,
                    append=f'_hawc2_step_C{k+1}',
                    compute_steady_states=True,
                    compute_controller_input = True,
                    save_power = True,
                    genspeed= (6, 9.382599449704426),
                    gearratio = 1.0,
                    P_rated = 10638.3,
                    min_rot_speed = 0.6283185307179586,
                    rated_rot_speed = 0.982543516758902,
                    max_torque = 18200000,
                    theta_min = 0,
                    constant_power = 1,
                    KpTrq = control_output['KpTrq_Nm/(rad/s)'],
                    KiTrq = control_output['KiTrq_Nm/rad'],
                    KpPit = control_output['KpPit_rad/(rad/s)'],
                    KiPit = control_output['KiPit_rad/rad'],
                    K1 = control_output['K1_deg'],
                    K2 = control_output['K2_deg^2'],
                    K_opt = control_output['K_Nm/(rad/s)^2'],
                    time_stop = 1001,
                    wsp = 4,
                    shear_format = [3,0],
                    tint = 0,
                    turb_format = 0,
                    tower_shadow_method = 0,
                    time = [0,1001]
        )

