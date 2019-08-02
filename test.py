from environment import ENV
import numpy as np


C = ENV(3, 2)
C.generate_mec()
C.generate_vnfs()
C.get_state()
C.view_infrastructure()
C.step(14)
# C.view_infrastructure()
