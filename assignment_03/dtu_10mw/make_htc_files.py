"""Make all the htc files for the LAC course from a single base file.

Requires myteampack (which requires lacbox).
"""
from myteampack import MyHTC

if __name__ == '__main__':
    ORIG_PATH = './_master/dtu_10mw.htc'
    SAVE_HAWC2S_DIR = '.'

    # make rigid hawc2s file for single-wsp opt file
    htc = MyHTC(ORIG_PATH)
    htc.make_hawc2s(SAVE_HAWC2S_DIR,
                    rigid=True,
                    append='_hawc2s_1wsp',
                    opt_path='./data/dtu_10mw_1wsp.opt',
                    compute_steady_states=True,
                    save_power=True)

    # make rigid hawc2s file for multi-tsr opt file
    htc = MyHTC(ORIG_PATH)
    htc.make_hawc2s(SAVE_HAWC2S_DIR,
                    rigid=True,
                    append='_hawc2s_7wsp',
                    opt_path='./data/dtu_10mw_multitsr.opt',
                    compute_steady_states=True,
                    save_power=True)

    # make flex hawc2s file from lecture 6, step 1
    htc = MyHTC(ORIG_PATH)
    htc.make_hawc2s(SAVE_HAWC2S_DIR,
                rigid=False,
                append='_hawc2s_25wsp',
                opt_path='./data/dtu_10mw_3_columns.opt',
                compute_steady_states=False,
                compute_optimal_pitch_angle=True,
                save_power=False,
                genspeed= (6, 9.6),
                gearratio = 1.0,
                minpitch = 0,
                opt_lambda=7.5,
                maxpow = 10641.618
                )
    
    # make flex hawc2s file from lecture 6, step 2 and 3
    htc = MyHTC(ORIG_PATH)
    htc.make_hawc2s_ctrltune(SAVE_HAWC2S_DIR,
                rigid=False,
                append='_hawc2s_25wsp_ctrltune',
                opt_path='./res_hawc2s/dtu_10mw_hawc2s_25wsp.opt',
                compute_steady_states=True,
                compute_controller_input = True,
                save_power = True,
                genspeed= (6, 9.6),
                gearratio = 1.0,
                minpitch = 0,
                opt_lambda=7.5,
                maxpow = 10641.618,
                partial_load = (0.05, 0.7),
                full_load = (0.05, 0.7),
                gain_scheduling = 2,
                constant_power = 1
                )
  

    htc = MyHTC(ORIG_PATH)
    htc.make_hawc2s(SAVE_HAWC2S_DIR,
                    rigid=False,
                    append='_hawc2s_camp',
                    opt_path='./data/dtu_10mw_flex_minrotspd.opt',
                    compute_steady_states=False,
                    compute_stability_analysis=False,
                    save_modal_amplitude=False,
                    compute_optimal_pitch_angle = True,
                    minpitch = 0,
                    opt_lambda=7.5,
                    genspeed= (6, 9.6),
                    gearratio = 1.0,
                    maxpow = 10641.618,
                    )    
    
    # INSERT CODE HERE WHEN PROMPTED (A0)
 
    # make ctrltune
    htc = MyHTC(ORIG_PATH)    
    htc.make_hawc2s_ctrltune(SAVE_HAWC2S_DIR,
                    rigid=False,
                    append='_hawc2s_ctrl',
                    opt_path='./data/Group1_redesign_flex.opt',
                    compute_steady_states=True,
                    compute_controller_input = True,
                    minpitch = 0,
                    opt_lambda=7.263157,
                    genspeed= (0, 8.337868262998404),
                    gearratio=1.0,
                    partial_load = (0.05, 0.7),
                    full_load = (0.06, 0.7),
                    gain_scheduling = 2,
                    constant_power = 1
                    )
    

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
                        genspeed= (0, 8.337868262998404),
                        gearratio=1.0,
                        partial_load = (0.05, 0.7),
                        full_load = (data_fqc_damp[0][k], data_fqc_damp[1][k]),
                        gain_scheduling = 2,
                        constant_power = data_fqc_damp[2][k]
                        )