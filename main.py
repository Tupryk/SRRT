import random
import time
import numpy as np
import robotic as ry
from rnd_configs import RndConfigs

pairs = [random.sample(range(14), 2) for _ in range(10)]

for p in pairs:
    C0_idx = p[0]
    CT_idx = p[1]

    collision_pairs = [
            "l_fing", "r_fing", 
            "l_fing", "r_fing",  "l_fing", "table",  "l_fing", "wall",  "l_fing", "box",
            "r_fing", "r_fing",  "r_fing", "table",  "r_fing", "wall",  "r_fing", "box"
        ]

    # relevant_frames = ["l_fing", "r_fing", "obj"]
    relevant_frames = ["obj"]

    D = RndConfigs('twoFingers.g', 'rnd_twoFingers.h5')
    D.set_config(C0_idx)
    C0 = ry.Config()
    C0.addConfigurationCopy(D.C)
    C0_frame_state = C0.getFrameState()
    C0.view()

    D.set_config(CT_idx)
    CT = ry.Config()
    CT.addConfigurationCopy(D.C)
    CT_frame_state = CT.getFrameState()
    CT.view()

    srrt = ry.SRRT_PathFinder()
    srrt.setInfo(collision_pairs, relevant_frames)
    srrt.setStartGoal(C0, CT)
    ret = srrt.solve()

    ret.x = ret.x.reshape(-1, len(C0.getFrameState().flatten()))

    # C0.view(True)
    for fs in ret.x:
        C0.setFrameState(fs)
        C0.view()
        time.sleep(.05)
    # C0.view(True)

    file_name = f"C0-{C0_idx}_CT-{CT_idx}"
    np.save(f"data/ball0.5/{file_name}.npy", ret.x)
