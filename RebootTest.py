#!/usr/bin/env python
# -*- coding:utf8 -*-
#author:Scemoon
#mail:mengsan8325150@gmail.com
#description: PC OR SEVER REBOOT TEST


import os,sys,time
import ConfigParser

numberfile='/tmp/number.txt'
TIMES = 50 
INTERVAL = 300

class ReBoot:
    def __init__(self,numberfile,TIMES,INTERVAL):
        self.file = numberfile
        self.TIMES = TIMES
        self.OTIME = 0
        self.FAIL = 0
        self.TRUE = 0
        self.INTERVAL = INTERVAL
        self.ParserInit()
        
    #判断文件是否存在，不存在创建文件，并写入信息
    def FileExists(self):
        if not os.path.exists(self.file):
            os.mknod(self.file)
            self.FileWrite()
        else:
            self.FileRead()
        
    def FileWrite(self):
        self.cf.add_section("REBOOT")
        self.cf.set("REBOOT", "TIMES", self.TIMES)
        self.cf.set("REBOOT", "TIME",self.OTIME)
        self.cf.set("REBOOT", "FAIL",self.FAIL)
        self.cf.set("REBOOT", "TRUE",self.TRUE)
        self.cf.write(open(self.file,'w'))
    
    def FileRead(self):
        self.cf.read(self.file)
        self.TIMES = self.cf.getint("REBOOT", "TIMES")
        self.OTIME =  self.cf.getfloat("REBOOT", "TIME")
        self.FAIL = self.cf.getint("REBOOT", "FAIL")
        self.TRUE = self.cf.getint("REBOOT", "TRUE")
    #读写文件方法定义
    def ParserInit(self):
        self.cf=ConfigParser.ConfigParser()
        #self.cf.read(self.file)
        
    def TimeStamp(self):
        return time.mktime(time.localtime())
        
    def run(self):
        self.FileExists()
        if self.TIMES ==0:
            sys.exit()
        if self.OTIME == 0:
            self.cf.set("REBOOT", "TIME", self.TimeStamp())
            self.cf.write(open(self.file,'w'))
            os.system("reboot")
        else:
            nowtime = self.TimeStamp()
            diffence = float(nowtime) - self.OTIME
            if diffence >= self.INTERVAL:
                self.FAIL = self.FAIL + 1
                self.TIMES = self.TIMES - 1
                self.TRUE = self.TRUE + 1
            else:
                self.TRUE = self.TRUE + 1
            self.TIMES = self.TIMES - 1
            self.cf.set("REBOOT", "TIMES", self.TIMES)
            self.cf.set("REBOOT", "TIME", self.TimeStamp())
            self.cf.set("REBOOT", "FAIL",self.FAIL)
            self.cf.set("REBOOT", "TRUE",self.TRUE)
            self.cf.write(open(self.file,'w'))
            os.system('reboot')
        

if __name__=="__main__":
    #time.sleep(60)
    R = ReBoot(numberfile,TIMES,INTERVAL)
    R.run()