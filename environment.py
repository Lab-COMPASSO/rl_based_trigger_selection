from random import randint, sample
from mec import MEC
from c_vnf import VNF
import pickle


class ENV:

    def __init__(self, nb_mec=0, nb_vnfs=0, min_cpu=50, max_cpu=100, min_ram=50, max_ram=100, min_disk=4096,
                 max_disk=122819, min_c_cpu=1, max_c_cpu=4, min_c_ram=1, max_c_ram=4, min_c_disk=512,
                 max_c_disk=4096):

        self.nb_mec = nb_mec
        self.nb_vnfs = nb_vnfs
        # MECs
        self.min_cpu = min_cpu
        self.max_cpu = max_cpu
        self.min_ram = min_ram
        self.max_ram = max_ram
        self.min_disk = min_disk
        self.max_disk = max_disk
        # Containers
        self.min_c_cpu = min_c_cpu
        self.max_c_cpu = max_c_cpu
        self.min_c_ram = min_c_ram
        self.max_c_ram = max_c_ram
        self.min_c_disk = min_c_disk
        self.max_c_disk = max_c_disk

        self.mec = {}
        self.vnfs = {}

    def get_mec(self):
        return self.mec

    def generate_mec(self):
        """
        :return: a list of MECs in the network
        """

        for i in range(self.nb_mec):
            self.mec[i] = MEC(i, randint(self.min_cpu, self.max_cpu), randint(self.min_ram, self.max_ram),
                              randint(self.min_disk, self.max_disk))
            # print(self.mec[i].mec_name)
            # print(self.mec[i].cpu_max)
            # print(self.mec[i].ram_max)
            # print(self.mec[i].disk_max)
            # print(self.mec[i].get_rat())

    def generate_vnfs(self):
        """
        :return: the generated VNFs
        """

        i = 0
        while i < self.nb_vnfs:
            for mec in sample(list(self.mec), 1):
                cpu = randint(self.min_c_cpu, self.max_c_cpu)
                ram = randint(self.min_c_ram, self.max_c_ram)
                disk = randint(self.min_c_disk, self.max_c_disk)
                if self.mec[mec].cpu_availability(cpu) and self.mec[mec].ram_availability(ram) and \
                        self.mec[mec].disk_availability(disk):
                    self.vnfs[i] = VNF(vnf_name=i, pm=self.mec[mec], ethnicity=str(mec),
                                       cpu=cpu,
                                       ram=ram,
                                       disk=disk)
                    i += 1

            # print(self.vnfs[i].vnf_name)
            # print(self.vnfs[i].ethnicity)
            # print(self.vnfs[i].cpu)
            # print(self.vnfs[i].ram)
            # print(self.vnfs[i].disk)
            # print(self.vnfs[i].get_sct())
        # print(self.mec[0].get_rat())
        for j in range(self.nb_mec):
            print("mec{}".format(j))
            print(self.mec[j].get_member())

    def get_rat(self, mec_id):
        cpu_percentage = round(self.mec[mec_id].live_cpu * 100 / self.mec[mec_id].cpu_max, 2)
        ram_percentage = round(self.mec[mec_id].live_ram * 100 / self.mec[mec_id].ram_max, 2)
        disk_percentage = round(self.mec[mec_id].live_disk * 100 / self.mec[mec_id].disk_max, 2)
        return cpu_percentage, ram_percentage, disk_percentage

    def get_sct(self, vnf_id):
        return self.vnfs[vnf_id].get_live_cpu(), self.vnfs[vnf_id].get_live_ram()

    def get_state(self):
        state = []
        for i in range(self.nb_mec):
            temp = []
            if len(self.mec[i].get_member()) != 0:
                mec_cpu_percentage, mec_ram_percentage, mec_disk_percentage = self.get_rat(i)
                temp.extend([mec_cpu_percentage, mec_ram_percentage, mec_disk_percentage])
                for j in range(len(self.mec[i].get_member())):
                    vnf_cpu_percentage, vnf_ram_percentage = self.get_sct(self.vnfs[j].vnf_name)
                    temp.extend([vnf_cpu_percentage, vnf_ram_percentage])
                sub_state = tuple(temp)
                state.append(sub_state)
        print(state)
        return state

    def save_topology(self, file_name):
        """
        :param file_name:
        :return: implemented in order to save the current object that contain all the required data (save the topology)
        """

        my_data = [self.nb_mec, self.nb_vnfs, self.min_cpu, self.max_cpu, self.min_ram, self.max_ram, self.min_disk,
                   self.max_disk, self.min_c_cpu, self.max_c_cpu, self.min_c_ram, self.max_c_ram, self.min_c_disk,
                   self.max_c_disk, self.mec, self.vnfs]

        with open(file_name + '.dat', 'wb') as fp:
            pickle.dump(my_data, fp)

    def restore_topology(self, file_name):
        """
        :param file_name:
        :return: the saved data from the previous created topology
        """
        with open(file_name + '.dat', 'rb') as fp:
            my_data = pickle.load(fp)

        self.nb_mec = my_data[0]
        self.nb_vnfs = my_data[1]
        self.min_cpu = my_data[2]
        self.max_cpu = my_data[3]
        self.min_ram = my_data[4]
        self.max_ram = my_data[5]
        self.min_disk = my_data[6]
        self.max_disk = my_data[7]
        self.min_c_cpu = my_data[8]
        self.max_c_cpu = my_data[9]
        self.min_c_ram = my_data[10]
        self.max_c_ram = my_data[11]
        self.min_c_disk = my_data[12]
        self.max_c_disk = my_data[13]
        self.mec = my_data[14]
        self.vnfs = my_data[15]


