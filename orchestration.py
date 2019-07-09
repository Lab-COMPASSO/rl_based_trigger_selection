from environment import ENV
from c_vnf import VNF
from mec import MEC


def migrate(vnf_id, mec_dest_id):

    pass


def scale_up(vnf_id, resource_type, resource_unit):
    pass


def scale_down(vnf_id, resource_type, resource_unit):
    pass


def orchestration():
    nb_mec = 3
    nb_vnfs = 3
    # MECs
    min_cpu = 50
    max_cpu = 100
    min_ram = 50
    max_ram = 100
    min_disk = 4096
    max_disk = 12288
    # Containers
    min_c_cpu = 1
    max_c_cpu = 4
    min_c_ram = 1
    max_c_ram = 4
    min_c_disk = 512
    max_c_disk = 4096

    c = ENV(nb_mec, nb_vnfs, min_cpu, max_cpu, min_ram, max_ram, min_disk, max_disk, min_c_cpu, max_c_cpu, min_c_ram,
            max_c_ram, min_c_disk, max_c_disk)
    c.generate_mec()
    c.generate_vnfs()
    c.save_topology("environment")
