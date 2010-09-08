#!/usr/bin/env python

from __future__ import division
import time, shelve, math, create_UTC
utc = create_UTC.create_utc()

class count:

    def open_file(self, file_in):
        self.file = shelve.open(file_in)
        self.year = file_in

    def count(self, list,year):
        #self.act_list = list
        self.open_file(year)
        #self.act_file = shelve.open(file)
        if self.file.has_key(list):
            temp_list = self.file[list]
            temp_list.append(time.time())
            self.file[list] = temp_list
        else:
            self.file[list] = [time.time()]

        return self.file[list][-1]

    def stats(self, key, value, last_count):
        if self.act_file.has_key(key):
            self.act_key = self.act_file[key]
            self.act_value = self.act_file[value]
            last_key = self.act_key[-1]
            if last_count < int(last_key) + 5*60:
                self.act_value[-1] += 1
                self.act_file[value] = self.act_value
            else:
                tm = time.localtime()
                m = tm.tm_min
                t = tm.tm_hour
                m = self.roundint(m,5)
                self.act_key.append(time.mktime((tm.tm_year,tm.tm_mon,tm.tm_mday,t,m,0,tm.tm_wday,tm.tm_yday,1)))
                self.act_value.append(1)
                self.act_file[key] = self.act_key
                self.act_file[value] = self.act_value
        else:
            tm = time.localtime()
            m = tm.tm_min
            t = tm.tm_hour
            m = self.roundint(m,5)
            self.act_file[value] = [1]
            self.act_file[key] = [time.mktime((tm.tm_year,tm.tm_mon,tm.tm_mday,t,m,0,tm.tm_wday,tm.tm_yday,1))]

    def stats2(self,week,wday,hour,last_count):
        if self.file.has_key('week'):
            self.stats3(last_count)
            print('if')
        else:
            week = []
            for i in range(52):
                week.append(i + 1)
            self.file['week'] = week
            wday = []
            for i in range(7):
                wday.append(i)
            hour = []
            for i in range(24):
                hour.append(i)
            for i in week:
                for j in wday:
                    for k in hour:
                        self.file['{0}-{1}-{2}'.format(i,j,k)] = utc.fmin(int(self.year),i,j,k)
                        self.file['{0}-{1}-{2}-value'.format(i,j,k)] = [0,0,0,0,0,0,0,0,0,0,0,0]
            self.stats3(last_count)

    def stats3(self,last_count):
        w = time.strftime('%W')
        d = time.strftime('%w')
        d = self.week_day(d)
        h = time.strftime('%H')
        h = int(h)+1
        print(w,d,h)
        last_utc = self.file['{0}-{1}-{2}'.format(w,d,h)]
        value = self.file['{0}-{1}-{2}-value'.format(w,d,h)]
        for i in range(12):
            print(last_count,'storre enn',last_utc[i],' mindre enn',last_utc[i]+300)
            if last_count >= last_utc[i] and last_count < last_utc[i]+300: 
                value[i] += 1

        self.file['{0}-{1}-{2}-value'.format(w,d,h)] = value 



    def week_day(self,day):
        day = int(day)
        if day in range(1,6):
            day -= 1
        else:
            day = 6
        return day + 1

    def roundint(self,n,p):
        x = (n+p)/p
        x = math.floor(x)
        x = (x * p) - p
        return int(x)

    def print_list(self,list):
        for i in self.file[list]:
            return i

    #def graph(self):




c = count()

last = c.count('test_list','2010') 
c.stats2(36,2,23,last)
#c.stats('test_key','test_value',last)

#c.create_hour('0')

#c.print_list('test_list')
c.print_list('35-4-12-value')
for i in range(1,12):
    for j in range(1,7):
        for k in range(1,52):
            if c.print_list('{0}-{1}-{2}-value'.format(k,j,i)) > 0:
                print('jippi')



