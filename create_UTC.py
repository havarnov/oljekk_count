#!/usr/bin/env python

import time,datetime

class create_utc:

    def check_year_start(self,date):
        temp = time.mktime(date.timetuple())
        wday = 7 - time.localtime(temp).tm_wday
        date += datetime.timedelta(days=wday)
        return date

    def week(self,year):
        week = []
        week_delta = datetime.timedelta(weeks=1)
        w = datetime.datetime(year,1,1,0,0)
        w = self.check_year_start(w)
        week.append(time.mktime(w.timetuple()))

        for i in range(51):
            w += week_delta
            week.append(time.mktime(w.timetuple()))

        return week
    
    def day(self,year,week):
        day = []
        week -= 1
        week_delta = datetime.timedelta(weeks=week)
        day_delta = datetime.timedelta(days=1)
        w = datetime.datetime(year,1,1,0,0)
        w = self.check_year_start(w)
        d = w + week_delta
        day.append(time.mktime(d.timetuple()))

        for i in range(6):
            d += day_delta
            day.append(time.mktime(d.timetuple()))

        return day

    def hour(self,year,week,day):
        hour = []
        week -= 1
        week_delta = datetime.timedelta(weeks=week)
        day -= 1
        day_delta = datetime.timedelta(days=day)
        hour_delta = datetime.timedelta(hours=1)
        w = datetime.datetime(year,1,1,0,0)
        w = self.check_year_start(w)
        h = w + week_delta + day_delta
        hour.append(time.mktime(h.timetuple()))

        for i in range(23):
            h += hour_delta
            hour.append(time.mktime(h.timetuple()))

        return hour

    def fmin(self,year,week,day,hour):
        fmin = []
        week -= 1
        week_delta = datetime.timedelta(weeks=week)
        day -= 1
        day_delta = datetime.timedelta(days=day)
        hour -= 1
        hour_delta = datetime.timedelta(hours=hour)
        fmin_delta = datetime.timedelta(minutes=5)
        w = datetime.datetime(year,1,1,0,0)
        w = self.check_year_start(w)
        f = w + week_delta + day_delta + hour_delta
        fmin.append(time.mktime(f.timetuple()))

        for i in range(11):
            f += fmin_delta
            fmin.append(time.mktime(f.timetuple()))

        return fmin

