"""Make all the htc files for the LAC course from a single base file.

Requires myteampack (which requires lacbox).
"""
from myteampack import MyHTC

if __name__ == '__main__':
    ORIG_PATH = './_master/Group1_redesign.htc'
    SAVE_HAWC2S_DIR = '.'

    # make rigid hawc2s file for single-wsp opt file
    htc = MyHTC(ORIG_PATH)
    htc.make_hawc2s(SAVE_HAWC2S_DIR,
                    rigid=True,
                    append='_hawc2s_1wsp',
                    opt_path='./data/Group1_redesign_1wsp.opt',
                    compute_steady_states=True,
                    save_power=True,
                    save_induction=True,
                    minpitch = 0,
                    opt_lambda=7.263157,
                    genspeed= (0, 50*8.337868262998404))

    htc = MyHTC(ORIG_PATH)
    # make rigid hawc2s file for multi-wsp opt file
    htc.make_hawc2s(SAVE_HAWC2S_DIR,
                    rigid=True,
                    append='_hawc2s_multiwsp',
                    opt_path='./data/Group1_redesign_multiwsp.opt',
                    compute_steady_states=True,
                    save_power=True,
                    save_induction=True,
                    minpitch = 0,
                    opt_lambda=7.263157,
                    genspeed= (0, 50*8.337868262998404))
                    
    
    htc = MyHTC(ORIG_PATH)
    # make rigid hawc2s file for compute rigid opt file
    htc.make_hawc2s(SAVE_HAWC2S_DIR,
                    rigid=True,
                    append='_hawc2s_compute_rigid_opt',
                    opt_path='./data/dtu_10mw_rigid.opt',
                    compute_steady_states=False,
                    save_power=False,
                    compute_optimal_pitch_angle = True,
                    minpitch = 0,
                    opt_lambda=7.263157,
                    genspeed= (0, 50*8.337868262998404))
    
    # INSERT CODE HERE WHEN PROMPTED 

