#!/usr/bin/env python
# -*- coding:utf8 -*-
#reboot cycle testing
#author:Scemoon
#mail:mengsan8325150@gmail.com
#description:

import sys
import os
import getopt
import commands
import time
from exmodules import *

TIMES=2
INTERVAL=10
HOST=None
TOTAL = {"PASS":0,"FAIL":0}

class Boot:
    def __init__(self,TIMES,INTERVAL,HOST):
        self.TIMES = TIMES
        self.INTERVAL = INTERVAL
        self.HOST = HOST
        self.PINGTIMES = 10
        self.PASSWORD =None
    def Usage(self):
        print'''Usage:Rreboot.py [options] value
options:
        -h,          帮助信息;
        -v,          版本信息;
        -H, hostip   远程主机;
        -p, password 远程主机root密码;
        -T, times    测试次数,默认100;
        -i, num sec  重启失败判断间隔时间，默认180秒;
             '''
        sys.exit()

    def optparser(self,args=sys.argv):
        opts, args = getopt.getopt(args[1:],"hvH:p:i:T:",["help","host","password","interval","--times"])
        try:
            for opt,value in opts:
                if opt in ('-h','--help'):
                    self.Usage()
                if opt == '-v':
                    print "Version2.0"
                    sys.exit()
                if opt in ('-H','--host'):
                    self.HOST = value
                if opt in ('-p','--password'):
                    self.PASSWORD = value    
                if opt in ( '-i','--interval'):
                    self.INTERVAL = value
                if opt in ('-T','--times'):
                    self.TIMES = value
        except Exception,e:
            print e
            self.Usage()

    def Rping(self):
        pingcmd = "ping -c %s %s" %(self.PINGTIMES,self.HOST)
        status,output = commands.getstatusoutput(pingcmd)
        if status != 0:
            return False
        else:
            return True

    def TestBefore(self):
        if self.HOST == None:
            print "主机不能为空"
            self.Usage()
        if self.PASSWORD == None:
            print "主机密码不能为空"
            self.Usage()
        if self.Rping():
            return True
        else:
            print "HOST IP不通，请检查您的IP地址"
            self.Usage()

    def Reboot(self,cmd='reboot'):
        try:
            s = pxssh.pxssh()
            s.login(self.HOST,'root',self.PASSWORD)
            s.sendline(cmd)
        except pxssh.ExceptionPxssh,e:
            print str(e)
            print "pxssh failed on login."
            
    def MonHost(self):
        i = 1
        while i < sys.maxinit:
            status = self.Rping()
            if status == True:
                return True
                break
            i = i + 1

    def Run(self):
        i = 1
        while i <= self.TIMES:
            time.sleep(self.INTERVAL)
            Tstatus = self.Rping()
            print "第%d次重启：    %s" % (i,Tstatus)
            if Tstatus == True:
                TOTAL["PASS"]=TOTAL["PASS"]+1
                self.Reboot()
            else:
                TOTAL["FAIL"]=TOTAL["FAIL"]+1
                print "远程主机重启失败，请手动去重启"
                if self.MonHost()==True:
                    self.Reboot()
            i = i + 1

    def main(self):
        self.optparser()
        self.TestBefore()
        print "TEST BEGIN"
        print "-----------------------------------------------------------"
        self.Reboot()
        time.sleep(self.INTERVAL)
        self.Run()
        print "统计："
        print "PASS:%d FAIL:%d" %(TOTAL["PASS"],TOTAL["FAIL"])
        print "-----------------------------------------------------------"
        print "TEST END"

if __name__ == '__main__':
    boot = Boot(TIMES,INTERVAL,HOST)
    boot.main()
    