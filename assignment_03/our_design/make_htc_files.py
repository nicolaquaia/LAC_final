"""Make all the htc files for the LAC course from a single base file.

Requires myteampack (which requires lacbox).
"""
from myteampack import MyHTC

if __name__ == '__main__':
    ORIG_PATH = './_master/Group1_redesign.htc'
    SAVE_HAWC2S_DIR = '.'
    
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
    