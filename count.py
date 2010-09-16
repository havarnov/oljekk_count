#!/usr/bin/env python
# coding=utf8

from __future__ import division
import time, shelve, math, create_UTC, pylab, matplotlib, optparse, sys
utc = create_UTC.create_utc()

class count:

    def open_file(self, file_in):
        self.file = shelve.open(file_in)
        self.year = time.strftime('%Y')

    def count(self, list,year_file,directory):
        #self.act_list = list
        print('{0}/{1}'.format(directory,year_file))
        self.open_file('{0}/{1}'.format(directory,year_file))
        #self.open_file(year_file)
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

    def stats2(self,last_count):
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
		if i < 10:
			i = '0{0}'.format(i)
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

    def graph(self,directory):
        matplotlib.rc('axes',edgecolor='w')
        #matplotlib.rc('text',edgecolor='w')
        fig = pylab.figure(facecolor='grey')
        ax = fig.add_subplot(1,1,1)
        #ax.patch.set_alpha(0.5)
        
        w = time.strftime('%W')
        d = time.strftime('%w')
        d = self.week_day(d)
        h = time.strftime('%H')
        y = self.file['{0}-{1}-{2}-value'.format(w,d,h)]
        x = range(len(y))


        ax.bar(x,y,width=0.5,color='#74201B',align='center',linewidth=0.5,edgecolor='black')
        ax.set_ylabel(u'Antall øl',color='w')
        ax.set_title(u'Oversikt over antall øl jekka siste timen, fordelt på hvert femte minutt',fontstyle='italic',color='w')
        ax.set_xticks(x)
        x_labels = ['{0}:00'.format(h),'{0}:05'.format(h),'{0}:10'.format(h),'{0}:15'.format(h),'{0}:20'.format(h),'{0}:25'.format(h),'{0}:30'.format(h),'{0}:35'.format(h),'{0}:40'.format(h),'{0}:45'.format(h),'{0}:50'.format(h),'{0}:55'.format(h)]
        ax.set_xticklabels(x_labels,color='w')
        ax.set_yticks(y)
        y_labels = self.mkylst(y)
        print(y_labels)
        #ax.set_yticklabels(y_labels,color='w')
        fig.autofmt_xdate() #used to autorotate labels
        #pylab.show()
        pylab.savefig('{3}/images/{0}-{1}-{2}.png'.format(w,d,h,directory),transparent=True)


    def mkylst(self,y):
        m = max(y)
        y2 = []
        for i in range(m+2):
            y2.append(str(i))
        return y2



c = count()


# User Interface
def main():
    p = optparse.OptionParser()
    p.add_option('-d','--dir',action='store',help='Directory where statistic files will be created')
    option, args = p.parse_args()

    if len(sys.argv) == 1:
        p.error('\nNo options passed. \n-h[--help] for usage')
    else:
        year = time.strftime('%Y')
        last = c.count('{0}-count'.format(year),year,option.dir)
        c.stats2(last)
        c.graph(option.dir)



if __name__ == "__main__":
    main()
