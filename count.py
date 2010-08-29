#!/usr/bin/env python

import time, shelve

class count:

    def open_file(self, file):
        shelve.open(file)

    def count(self, list, file):
        self.act_list = list
        #self.act_file = self.open_file(file)
        self.act_file = shelve.open(file)
        if self.act_file.has_key(list):
            temp_list = self.act_file[list]
            temp_list.append(time.time())
            self.act_file[list] = temp_list
        else:
            self.act_file[list] = [time.time()]

    def print_list(self):
        for i in self.act_file[self.act_list]:
            print(i)


c = count()

c.count('test_list','test.dat') 

c.print_list()
