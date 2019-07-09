import random


class VNF:
    def __init__(self, vnf_name, ethnicity="", cpu=0, ram=0, disk=0):
        self.vnf_name = vnf_name
        self.ethnicity = ethnicity
        self.cpu = cpu
        self.ram = ram
        self.disk = disk

    def set_ethnicity(self, ethnicity):
        self.ethnicity = ethnicity

    def get_ethnicity(self):
        return self.ethnicity

    def set_cpu(self, vnf_cpu):
        self.cpu = vnf_cpu

    def get_cpu(self):
        return self.cpu

    def set_ram(self, vnf_ram):
        self.ram = vnf_ram

    def get_ram(self):
        return self.ram

    def set_disk(self, vnf_disk):
        self.disk = vnf_disk

    def get_disk(self):
        return self.disk

    def get_live_cpu(self):
        live_cpu = 0
        for i in range(self.cpu):
            live_cpu += round(random.uniform(1, 99), 2)
        return round(live_cpu/self.cpu, 2)

    def get_live_ram(self):
        live_ram = 0
        for i in range(self.ram):
            live_ram += round(random.uniform(1, 99), 2)
        return round(live_ram/self.ram, 2)

    def get_sct(self):
        return self.cpu, self.ram, self.get_live_cpu(), self.get_live_ram()
