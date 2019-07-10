from environment import ENV


C = ENV(3, 3)
C.generate_mec()
C.generate_vnfs()
# C.get_state()
C.view_infrastructure()
C.migrate(1, 2)
C.view_infrastructure()
