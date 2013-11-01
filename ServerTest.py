#!/usr/bin/env python
# -*- coding:utf8 -*-
import commands
import re

SeList= ['autofs','crond','mysqld','auditd','iptables','haldaemon','rsyslog','httpd','named','vsftpd','smb','xinetd']

def CmdPara(server,cmd='start'):
    cmdline = 'service %s  %s' % (server,cmd)
    return cmdline

def TestRun(server,cmd):
    cmdline = CmdPara(server,cmd)
    output = commands.getoutput(cmdline)
    return output

def MatchStr(match,server,cmd):
    pattern = re.compile(match)
    output = TestRun(server,cmd)
    if pattern.search(output):
        return True
    else:
        return False


def run():
    for server in SeList:
        if MatchStr('pid',server,'status') == True:
            if MatchStr('OK|确定',server,'stop'):
                print '%s  stop PASS' % server
            else:
                print '%s  stop FAIL' % server
        else:
            if  MatchStr('OK|确定',server,'start'):
                print '%s  start PASS' % server

                if MatchStr('OK|确定',server,'stop'):
                     print '%s  stop PASS' % server
                else:
                    print '%s  stop FAIL' % server
            else:
                print '%s  start FAIL' % server


class ServerTest:
    def __init__(self):
        pass

    def Usage(self):
        print'''Usage:ServerTest.py [options] [value]
options:
        -h, --help      帮助信息;
        -v, --version   版本信息;
        -s, --server    测试服务;
             '''
        sys.exit()
   
    def optparser(self,args=sys.argv):
        opts, args = getopt.getopt(args[1:],"hvs:",["help","version","server"])
        try:
            for opt,value in opts:
                if opt in ('-h','--help'):
                    self.Usage()
                if opt in ('-v','--version'):
                    print "Version1.0"
                    sys.exit()
                if opt in ( '-s','--server'):
                    self.server=value
        except Exception,e:
            print str(e)
            self.Usage()


if __name__ == '__main__':
    run()
