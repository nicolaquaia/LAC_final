"""Make all the htc files for the LAC course from a single base file.

Requires myteampack (which requires lacbox).
"""
from myteampack import MyHTC
from lacbox.io import load_ctrl_txt

if __name__ == '__main__':
    ORIG_PATH = './_master/Group1_redesign.htc'
    SAVE_HAWC2S_DIR = '.'
    SAVE_HAWC2S_STEP = 'htc/'

    # make flex hawc2s file from lecture 6, step 1
    htc = MyHTC(ORIG_PATH)
    htc.make_hawc2s(SAVE_HAWC2S_DIR,
                rigid=False,
                append='_hawc2s_flex',
                opt_path='./data/Group1_redesign_3_columns.opt',
                compute_steady_states=False,
                compute_optimal_pitch_angle=True,
                save_power=False,
                genspeed= (3, 8.337868262998404),
                gearratio = 1.0,
                minpitch = 0,
                opt_lambda=7.263157,
                maxpow = 10641.618
                )

    # assignment 3 part 1
    # make flex hawc2s file from lecture 6, step 2 and 3
    # remove region
    htc = MyHTC(ORIG_PATH)
    htc.make_hawc2s_ctrltune(SAVE_HAWC2S_DIR,
                rigid=False,
                append='_hawc2s_ctrltune',
                opt_path='./data/Group1_redesign_flex2.opt',
                compute_steady_states=True,
                compute_controller_input = True,
                save_power = True,
                genspeed= (3, 8.337868262998404),
                gearratio = 1.0,
                minpitch = 0,
                opt_lambda=7.263157,
                maxpow = 10641.618,
                partial_load = (0.05, 0.7),
                full_load = (0.06, 0.7),
                gain_scheduling = 2,
                constant_power = 1
                )

    # assignment 3 part 2
    htc = MyHTC(ORIG_PATH)
    data_fqc_damp = [[0.05,0.01,0.10,0.05,0.01,0.10],[0.7,0.7,0.7,0.7,0.7,0.7],[1,1,1,0,0,0]]
    for k in range(len(data_fqc_damp[0])):
        htc = MyHTC(ORIG_PATH)
        htc.make_hawc2s_ctrltune(SAVE_HAWC2S_DIR,
                        rigid=False,
                        append=f'_hawc2s_ctrl_C{k+1}',
                        opt_path='./data/Group1_redesign_flex.opt',
                        compute_steady_states=True,
                        compute_controller_input = True,
                        minpitch = 0,
                        opt_lambda=7.263157,
                        genspeed= (3, 8.337868262998404),
                        gearratio=1.0,
                        partial_load = (0.05, 0.7),
                        full_load = (data_fqc_damp[0][k], data_fqc_damp[1][k]),
                        gain_scheduling = 2,
                        constant_power = data_fqc_damp[2][k]
        )

        control_output = load_ctrl_txt(f'res_hawc2s/Group1_redesign_hawc2s_ctrl_C{k+1}_ctrl_tuning.txt')
        htc = MyHTC(ORIG_PATH)
        htc.make_step(SAVE_HAWC2S_STEP,
                    append=f'_hawc2s_step_C{k+1}',
                    compute_steady_states=True,
                    compute_controller_input = True,
                    save_power = True,
                    genspeed= (0, 8.337868262998404),
                    gearratio = 1.0,
                    P_rated = 10638.3,
                    min_rot_speed = 0,
                    rated_rot_speed = 0.87336,
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
                    tower_shadow_method = 0

        )