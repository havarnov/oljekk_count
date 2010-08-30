#!/usr/bin/env python

from __future__ import division
import time, shelve, math

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

        return int(self.act_file[list][-1])

    def stats(self, key, key2, value, last_count):
        if self.act_file.has_key(key):
            self.act_key = self.act_file[key]
            self.act_value = self.act_file[value]
            self.act_key2 = self.act_file[key2]
            last_key = int(self.act_key[-1])
            print(last_key)
            last_key2 = self.act_key2[-1]
            print(last_count,' skal vare mindre < enn ',int(last_key2) + 5*60)
            if last_count < int(last_key2) + 5*60:
                self.act_value[-1] =+ 1
                self.act_file[value] = self.act_value
                print('if')
            else:
                last_key = last_key + 5
                self.act_key.append('last_key')
                tm = time.localtime()
                m = tm.tm_min
                t = tm.tm_hour
                m = self.roundint(m,5)
                self.act_key2.append(time.mktime((tm.tm_year,tm.tm_mon,tm.tm_mday,t,m,0,tm.tm_wday,tm.tm_yday,1)))
                self.act_value.append(1)
                self.act_file[key] = self.act_key
                self.act_file[key2] = self.act_key2
                self.act_file[value] = self.act_value
                print('else')
        else:
            tm = time.localtime()
            m = tm.tm_min
            t = tm.tm_hour
            m = self.roundint(m,5)
            self.act_file[key] = ['{0}{1}'.format(t,m)]
            self.act_file[value] = [1]
            self.act_file[key2] = [time.mktime((tm.tm_year,tm.tm_mon,tm.tm_mday,t,m,0,tm.tm_wday,tm.tm_yday,1))]

    def roundint(self,n,p):
        x = (n+p)/p
        x = math.floor(x)
        x = (x * p) - p
        return int(x)

    def print_list(self,list):
        for i in self.act_file[list]:
            print(i)


c = count()

last = c.count('test_list','test.dat') 

c.stats('test_key', 'test_key2','test_value',last)

#c.print_list('test_list')
#c.print_list('test_value')



