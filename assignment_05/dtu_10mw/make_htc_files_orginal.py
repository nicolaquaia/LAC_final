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

    htc = MyHTC(ORIG_PATH)
    htc.make_hawc2s(SAVE_HAWC2S_DIR,
                    rigid=True,
                    append='_hawc2s_multitsr',
                    opt_path='./data/dtu_10mw_multitsr.opt',
                    compute_steady_states=True,
                    save_power=True,
                    save_induction=True)
    

    # rigid opt                  
    htc = MyHTC(ORIG_PATH)
    htc.make_hawc2s(SAVE_HAWC2S_DIR,
                    rigid=True,
                    append='_hawc2s_compute_rigid_opt',
                    opt_path='./data/dtu_10mw_flex_minrotspd.opt',
                    compute_steady_states=False,
                    save_power=False,
                    compute_optimal_pitch_angle = True,
                    minpitch = 0,
                    opt_lambda=8.03746245202556,
                    genspeed= (50*6, 480)
                    )
