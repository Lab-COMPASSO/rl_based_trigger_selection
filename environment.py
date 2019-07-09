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

    def view_infrastructure(self):
        """
        :return: a view of the current configuration of the environment
        """

        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        for i in range(self.nb_mec):
            print("*********************************--  MEC number {} --******************************".format(i+1))
            print(self.mec[i].mec_name)
            print(self.mec[i].get_member())
            print(self.mec[i].cpu)
            print(self.mec[i].ram)
            print(self.mec[i].disk)
        print("###########################################################################")

        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        for i in range(self.nb_vnfs):
            print("*********************************--  VNF number {} --******************************".format(i+1))
            print(self.vnfs[i].vnf_name)
            print(self.vnfs[i].cpu)
            print(self.vnfs[i].ram)
            print(self.vnfs[i].disk)
        print("###########################################################################")

    def get_mec(self):
        """
        :return: a list of MECs in the network
        """
        return self.mec

    def generate_mec(self):
        """
        :return: generate MECs in the environment
        """

        for i in range(self.nb_mec):
            self.mec[i] = MEC(i, randint(self.min_cpu, self.max_cpu), randint(self.min_ram, self.max_ram),
                              randint(self.min_disk, self.max_disk))

    def generate_vnfs(self):
        """
        :return: generate VNFs in the environment
        """
        i = 0
        while i < self.nb_vnfs:
            for mec in sample(list(self.mec), 1):
                cpu = randint(self.min_c_cpu, self.max_c_cpu)
                ram = randint(self.min_c_ram, self.max_c_ram)
                disk = randint(self.min_c_disk, self.max_c_disk)
                if self.mec[mec].cpu_availability(cpu) and self.mec[mec].ram_availability(ram) and \
                        self.mec[mec].disk_availability(disk):
                    self.vnfs[i] = VNF(vnf_name=i, ethnicity=str(mec), cpu=cpu, ram=ram, disk=disk)
                    self.mec[mec].set_member(i)
                    self.mec[mec].set_live_cpu(cpu)
                    self.mec[mec].set_live_ram(ram)
                    self.mec[mec].set_live_disk(disk)
                    i += 1

    def get_rat(self, mec_id):
        """
        :param mec_id:
        :return: data related to the RAT trigger
        """
        cpu_percentage = round(self.mec[mec_id].live_cpu * 100 / self.mec[mec_id].cpu_max, 2)
        ram_percentage = round(self.mec[mec_id].live_ram * 100 / self.mec[mec_id].ram_max, 2)
        disk_percentage = round(self.mec[mec_id].live_disk * 100 / self.mec[mec_id].disk_max, 2)
        return cpu_percentage, ram_percentage, disk_percentage

    def get_sct(self, vnf_id):
        """
        :param vnf_id:
        :return: data related to the SCT trigger
        """
        return self.vnfs[vnf_id].get_live_cpu(), self.vnfs[vnf_id].get_live_ram()

    def get_state(self):
        """
        :return: a given state of the environment in a given time-step 't'
        """
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

    def migrate(self, vnf_id, mec_dest_id):
        """
        :param vnf_id:
        :param mec_dest_id:
        :return: migrate a given container from one MEC to another one, True if migrated otherwise False
        """
        if int(self.vnfs[vnf_id].ethnicity) == mec_dest_id:
            print("Container cannot be migrated to the same host !!!")
            return False
        if self.mec[mec_dest_id].cpu_availability(self.vnfs[vnf_id].cpu) and \
                self.mec[mec_dest_id].ram_availability(self.vnfs[vnf_id].ram) and \
                self.mec[mec_dest_id].disk_availability(self.vnfs[vnf_id].disk):

            # Remove the container's details from the source MEC
            self.mec[int(self.vnfs[vnf_id].ethnicity)].del_member(vnf_id)
            self.mec[int(self.vnfs[vnf_id].ethnicity)].del_live_cpu(self.vnfs[vnf_id].cpu)
            self.mec[int(self.vnfs[vnf_id].ethnicity)].del_live_ram(self.vnfs[vnf_id].ram)
            self.mec[int(self.vnfs[vnf_id].ethnicity)].del_live_disk(self.vnfs[vnf_id].disk)
            self.mec[int(self.vnfs[vnf_id].ethnicity)].cpu = self.mec[int(self.vnfs[vnf_id].ethnicity)].cpu + \
                self.vnfs[vnf_id].cpu
            self.mec[int(self.vnfs[vnf_id].ethnicity)].ram = self.mec[int(self.vnfs[vnf_id].ethnicity)].ram + \
                self.vnfs[vnf_id].ram
            self.mec[int(self.vnfs[vnf_id].ethnicity)].disk = self.mec[int(self.vnfs[vnf_id].ethnicity)].disk + \
                self.vnfs[vnf_id].disk

            # Addition of the container's details to the destination MEC
            self.mec[mec_dest_id].set_member(vnf_id)
            self.mec[mec_dest_id].set_live_cpu(self.vnfs[vnf_id].cpu)
            self.mec[mec_dest_id].set_live_ram(self.vnfs[vnf_id].ram)
            self.mec[mec_dest_id].set_live_disk(self.vnfs[vnf_id].disk)
            return True

        # Roll-back procedure in case of migration's failure
        return False

    def scale_up(self, vnf_id, resource_type):
        if resource_type == "CPU":
            cpu_resource_unit = randint(self.min_c_cpu, self.max_c_cpu)
            if self.mec[int(self.vnfs[vnf_id].ethnicity)].cpu_availability(cpu_resource_unit):
                self.vnfs[vnf_id].cpu = self.vnfs[vnf_id].cpu + cpu_resource_unit
                return True
        elif resource_type == "RAM":
            ram_resource_unit = randint(self.min_c_ram, self.max_c_ram)
            if self.mec[int(self.vnfs[vnf_id].ethnicity)].ram_availability(ram_resource_unit):
                self.vnfs[vnf_id].ram = self.vnfs[vnf_id].ram + ram_resource_unit
                return True
        elif resource_type == "DISK":
            disk_resource_unit = randint(self.min_c_disk, self.max_c_disk)
            if self.mec[int(self.vnfs[vnf_id].ethnicity)].disk_availability(disk_resource_unit):
                self.vnfs[vnf_id].disk = self.vnfs[vnf_id].disk + disk_resource_unit
                return True
        return False

    def scale_down(self, vnf_id, resource_type):
        if resource_type == "CPU":
            if self.vnfs[vnf_id].cpu == 1:
                print("Container with 1 core CPU cannot scale down !!!")
                return False
            cpu_resource_unit = randint(self.min_c_cpu, self.max_c_cpu)
            while self.vnfs[vnf_id].cpu - cpu_resource_unit <= 0:
                cpu_resource_unit = randint(self.min_c_cpu, self.max_c_cpu)
            self.mec[int(self.vnfs[vnf_id].ethnicity)].cpu = self.mec[int(self.vnfs[vnf_id].ethnicity)].cpu + \
                cpu_resource_unit
            self.vnfs[vnf_id].cpu = self.vnfs[vnf_id].cpu - cpu_resource_unit
            return True
        elif resource_type == "RAM":
            if self.vnfs[vnf_id].ram == 1:
                print("Container with 1 GB of Memory cannot scale down !!!")
                return False
            ram_resource_unit = randint(self.min_c_ram, self.max_c_ram)
            while self.vnfs[vnf_id].ram - ram_resource_unit <= 0:
                ram_resource_unit = randint(self.min_c_ram, self.max_c_ram)
            self.mec[int(self.vnfs[vnf_id].ethnicity)].ram = self.mec[int(self.vnfs[vnf_id].ethnicity)].ram + \
                ram_resource_unit
            self.vnfs[vnf_id].ram = self.vnfs[vnf_id].ram - ram_resource_unit
            return True
        elif resource_type == "DISK":
            if self.vnfs[vnf_id].disk == 512:
                print("Container with 512 MB of Disk cannot scale down !!!")
                return False
            disk_resource_unit = randint(self.min_c_disk, self.max_c_disk)
            while self.vnfs[vnf_id].disk - disk_resource_unit <= 0:
                disk_resource_unit = randint(self.min_c_disk, self.max_c_disk)
            self.mec[int(self.vnfs[vnf_id].ethnicity)].disk = self.mec[int(self.vnfs[vnf_id].ethnicity)].disk + \
                disk_resource_unit
            self.vnfs[vnf_id].disk = self.vnfs[vnf_id].disk - disk_resource_unit
            return True
        return False

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


