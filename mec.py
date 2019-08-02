#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 13:51:00 2019

@author: RaMy
"""


class MEC:
   
    def __init__(self, mec_name, cpu=0, ram=0, disk=0):
        self.mec_name = mec_name
        self.live_cpu = 0
        self.live_ram = 0
        self.live_disk = 0
        self.cpu_max = self.cpu = cpu
        self.ram_max = self.ram = ram
        self.disk_max = self.disk = disk
        self.list_of_c_vnfs = []

    def set_member(self, c_vnf):
        self.list_of_c_vnfs.append(c_vnf)

    def del_member(self, c_vnf):
        self.list_of_c_vnfs.remove(c_vnf)

    def get_member(self):
        return self.list_of_c_vnfs

    def set_live_cpu(self, c_vnf_cpu):
        self.live_cpu += c_vnf_cpu

    def del_live_cpu(self, c_vnf_cpu):
        self.live_cpu -= c_vnf_cpu

    def get_live_cpu(self):
        return self.live_cpu

    def set_live_ram(self, c_vnf_ram):
        self.live_ram += c_vnf_ram

    def del_live_ram(self, c_vnf_ram):
        self.live_ram -= c_vnf_ram

    def get_live_ram(self):
        return self.live_ram

    def set_live_disk(self, c_vnf_disk):
        self.live_disk += c_vnf_disk

    def del_live_disk(self, c_vnf_disk):
        self.live_disk -= c_vnf_disk

    def get_live_disk(self):
        return self.live_disk

    def set_cpu(self, cpu):
        self.cpu_max = self.cpu = cpu

    def get_cpu(self):
        return self.cpu_max

    def set_ram(self, ram):
        self.ram_max = self.ram = ram

    def get_ram(self):
        return self.ram_max

    def set_disk(self, disk):
        self.disk_max = self.disk = disk

    def get_disk(self):
        return self.disk_max

    def cpu_availability(self, c_vnf_cpu):
        if c_vnf_cpu <= self.cpu:
            self.cpu -= c_vnf_cpu
            return True
        else:
            return False

    def ram_availability(self, c_vnf_ram):
        if c_vnf_ram <= self.ram:
            self.ram -= c_vnf_ram
            return True
        else:
            return False

    def disk_availability(self, c_vnf_disk):
        if c_vnf_disk <= self.disk:
            self.disk -= c_vnf_disk
            return True
        else:
            return False

    def get_rat(self):
        return self.cpu_max, self.ram_max, self.disk_max, self.live_cpu, self.live_ram, self.live_disk


