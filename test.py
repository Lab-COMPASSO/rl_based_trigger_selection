from environment import ENV


C = ENV(1, 3)
C.generate_mec()
C.generate_vnfs()
# C.get_state()
C.view_infrastructure()
C.scale_down(1, "CPU")
C.view_infrastructure()
