import time
import random
import numpy as np
import robotic as ry
from rnd_configs import RndConfigs


C0_idx_s = [11, 12, 6, 6]
CT_idx_s = [6, 10, 12, 4]

for i in range(len(C0_idx_s)):

    C0_idx = C0_idx_s[i]
    CT_idx = CT_idx_s[i]

    D = RndConfigs('twoFingers.g', 'rnd_twoFingers.h5')
    D.set_config(C0_idx)
    C0 = ry.Config()
    C0.addConfigurationCopy(D.C)
    C0.view()

    D.set_config(CT_idx)
    CT = ry.Config()
    CT.addConfigurationCopy(D.C)
    CT_frame_state = CT.getFrameState()
    CT.view()

    file_name = f"C0-{C0_idx}_CT-{CT_idx}"
    frame_sequence = np.load(f"data/{file_name}.npy")
    print(frame_sequence.shape)

    C0.view(True)
    for fs in frame_sequence:
        C0.setFrameState(fs)
        C0.view()
        time.sleep(.05)
    C0.view(True)
