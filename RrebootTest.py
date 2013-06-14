#!/usr/bin/env python
# -*- coding:utf8 -*-
#author:Scemoon
#mail:mengsan8325150@gmail.com
#description: PC OR SEVER REBOOT TEST

import sys
import os
import getopt
import commands
import time
import logging
from pexpect import pxssh


TIMES=2
INTERVAL=180
HOST=None
PASSWORD = None
TOTAL = {"PASS":0,"FAIL":0}
LOGLEVEL = logging.INFO

class Boot:
    def __init__(self,TIMES,INTERVAL,HOST,PASSWORD):
        self.TIMES = TIMES
        self.INTERVAL = INTERVAL
        self.HOST = HOST
        self.PINGTIMES = 10
        self.PASSWORD = PASSWORD
        self.logger = logging.getLogger('RBT')
        self.logger.setLevel(LOGLEVEL)
        console = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(name)s %(asctime)s %(levelname)-3s %(message)s','%Y-%m-%d %H:%M:%S')
        console.setFormatter(formatter)
        self.logger.addHandler(console)
        
            
        
    def Usage(self):
        print'''Usage:Rreboot.py [options] value
options:
        -h, --help      帮助信息;
        -v, --version   版本信息;
        -H, --host      远程主机;
        -p, --password  远程主机root密码;
        -T  --times     测试次数,默认50;
        -i, --interval  重启失败判断间隔时间，默认180秒;
        -d ,--debug     调试模式;
             '''
        sys.exit()

    def optparser(self,args=sys.argv):
        opts, args = getopt.getopt(args[1:],"hvqdH:p:i:T:",["help","version","host","password","interval","--times"])
        try:
            for opt,value in opts:
                if opt in ('-h','--help'):
                    self.Usage()
                if opt in ('-v','--version'):
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
                if opt in ('-d','--debug'):
                    LOGLEVEL=logging.DEBUG
                    
        except Exception,e:
            print e
            self.Usage()

    def Rping(self):
        pingcmd = "ping -c %s %s" %(self.PINGTIMES,self.HOST)
        self.logger.debug("判断主机是否活动")
        status,output = commands.getstatusoutput(pingcmd)
        if status != 0:
            return False
        else:
            return True
        self.logger.debug(output)
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
            self.logger.error("HOST IP不通，请检查您的IP地址")
            self.Usage()

    def Reboot(self,cmd='reboot'):
        try:
            s = pxssh.pxssh()
            s.login(self.HOST,'root',self.PASSWORD, original_prompt=r"[#$]",login_timeout=60,port=None,auto_prompt_reset=True)
            s.sendline(cmd)
            s.prompt()
            #print s.before
            s.logout()
        except pxssh.ExceptionPxssh,e:
            self.logger.debug(e)
            self.logger.error("pxssh failed on login.")
        except Exception,e:
            self.logger.debug(e)
            
        
    def MonHost(self):
        i = 1
        while i < sys.maxint:
            status = self.Rping()
            if status == True:
                return True
                self.logger.info("系统已经重启")
                break
            i = i + 1

    def Run(self):
        i = 1
        while i <= self.TIMES:
            self.logger.info("请耐心等待 %s 秒" % self.INTERVAL)
            time.sleep(self.INTERVAL)
            Tstatus = self.Rping()
            self.logger.info("第%d次重启：    %s" % (i,Tstatus))
            if Tstatus == True:
                TOTAL["PASS"]=TOTAL["PASS"]+1
                if i != self.TIMES:
                    self.Reboot()
            else:
                TOTAL["FAIL"]=TOTAL["FAIL"]+1
                self.logger.error("远程主机重启失败，请手动去重启")
                if self.MonHost()==True:
                    if i != self.TIMES:
                        self.Reboot()
            i = i + 1

    def main(self):
        self.optparser()
        self.TestBefore()
        self.logger.info("TEST BEGIN")
        print "-----------------------------------------------------------"
        self.Reboot('reboot')
        self.Run()
        print 
        print 
        print "======"
        print "统计："
        print "======"
        print "总共重启%d次" % TIMES
        print "PASS:%d    FAIL:%d" %(TOTAL["PASS"],TOTAL["FAIL"])
        print "===================================="
        "-----------------------------------------------------------"
        self.logger.info("TEST END")

if __name__ == '__main__':
    boot = Boot(TIMES,INTERVAL,HOST,PASSWORD)
    boot.main()
    
