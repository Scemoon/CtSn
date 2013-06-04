#!/usr/bin/env python
# -*- coding:utf8 -*-
#author:Scemoon
#mail:mengsan8325150@gmail.com
#description: PC OR SEVER REBOOT TEST


import os,sys,time
import ConfigParser

numberfile='/tmp/number.txt'
TIMES = 50 
INTERVAL = 180
WTIME = 20

class ReBoot:
    def __init__(self,numberfile,TIMES,INTERVAL):
        self.file = numberfile
        self.TIMES = TIMES
        self.INTERVAL = INTERVAL
        self.FileExists()
        self.ParserInit()
        
    #判断文件是否存在，不存在创建文件，并写入信息
    def FileExists(self):
        if not os.path.exists(self.file):
            os.makedirs(self.file)
        else:
            pass
        
    def Filerw(self):
        pass
        self.
    
    #读写文件方法定义
    def ParserInit(self):
        self.cf=ConfigParser.ConfigParser()
        self.cf.read(self.file)  
        


def _read_number():
    fr=open(NUMBER_FILE,'r')
    line=fr.readline()
    if len(line)>=1:
        return int(line.strip())
    else:
        fr.close()
        _write_number(number)
        _reboot()
    fr.close()
def _write_number(NUMBER):
    fw=open(NUMBER_FILE,'w')
    fw.write(NUMBER)
    fw.close()


def _file_check():
    return os.path.isfile(NUMBER_FILE)


def _reboot():
    file_stat=_file_check()
    if file_stat==False:
        _write_number(number)
        time.sleep(time)
        os.system("reboot")
    else:
        NUMBER=_read_number()
        if NUMBER >= 1:
            NUMBER = NUMBER - 1
            _write_number(str(NUMBER))
            time.sleep(time)
            os.system("reboot")
        else:
            os.system('exit')

if __name__=="__main__":
    _reboot()