#!/usr/bin/env python

from __future__ import division
import time, shelve, math, create_UTC, pylab
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
            #print('if')
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
        #print(w,d,h)
        last_utc = self.file['{0}-{1}-{2}'.format(w,d,h)]
        value = self.file['{0}-{1}-{2}-value'.format(w,d,h)]
        for i in range(12):
            #print(last_count,'storre enn',last_utc[i],' mindre enn',last_utc[i]+300)
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

    def graph(self):
        fig = pylab.figure()
        ax = fig.add_subplot(1,1,1)
        w = time.strftime('%W')
        d = time.strftime('%w')
        d = self.week_day(d)
        h = time.strftime('%H')
        y = self.file['{0}-{1}-{2}-value'.format(w,d,h)]
        x = range(len(y))
        ax.bar(x,y,width=0.1,facecolor='#777777',align='center')
        ax.set_ylabel('Counts')
        ax.set_title('Antall ol jekka!',fontstyle='italic')
        group_labels = ['{0}:00'.format(h),'{0}:05'.format(h),'{0}:10'.format(h),'{0}:15'.format(h),'{0}:20'.format(h),'{0}:25'.format(h),'{0}:30'.format(h),'{0}:35'.format(h),'{0}:40'.format(h),'{0}:45'.format(h),'{0}:50'.format(h),'{0}:55'.format(h)]
        ax.set_xticklabels(group_labels)
        #fig.autofmt_xdate() #used to autorotate labels
        pylab.show()



c = count()

last = c.count('test_list','2010') 
c.stats2(36,3,19,last)

c.graph()




