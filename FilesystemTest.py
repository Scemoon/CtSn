#!/usr/bin/env python
# -*- coding:utf8 -*-
#author:Scemoon
#mail:mengsan8325150@gmail.com
#description: 文件系统兼容性测试
import os,sys
import commands
import subprocess
import getopt

DEVICE = None
FSTYPE = None 
FSTUPE = ('ext2','ext3','ext4')

class FsTest:
    def __init__(self,DEVICE,FSTYPE):
        self.DEVICE = DEVICE
        self.FSTYPE = FSTYPE
        self.mpoint = '/mnt/fstest'
        if not os.path.exists(self.mpoint):
            os.mkdir(self.mpoint)
        
    def Usage(self):
        print'''Usage:FilesystemTest.py [options] value
options:
        -h, --help      帮助信息;
        -v, --version   版本信息;
        -f              文件系统格式;
        -d              分区设备;
             '''
        sys.exit()
        
    def optparser(self,args=sys.argv):
        opts, args = getopt.getopt(args[1:],"hvd:f:",["help","version"])
        try:
            for opt,value in opts:
                if opt in ('-h','--help'):
                    self.Usage()
                if opt in ('-v','--version'):
                    print "Version1.0"
                    sys.exit()
                if opt == '-d':
                    self.DEVICE = value
                if opt == '-f':
                    self.FSTYPE = value     
        except Exception,e:
            print e
            self.Usage()
    
    def RunShell(self,cmd):
        try:
            status,output = commands.getstatusoutput(cmd)
            return status
        except Exception,e:
            print str(e)
            raise
            
    def MkFs(self,fstype='',extar='',other=''):
        if fstype== '':
            fstype = self.FSTYPE
        cmd = "%s mkfs -t %s %s %s" %(other,fstype,extar,self.DEVICE)
        self.RunShell(cmd)
    
    def MountFs(self,extar = ''):
        cmd = 'mount %s %s %s ' %(extar,self.DEVICE,self.mpoint)
        self.RunShell(cmd)
        
    def IsMount(self):
        try:
            mount_output = subprocess.Popen(["mount"],stdout=subprocess.PIPE)
            for line in mount_output.stdout.readlines():
                if line.find(self.DEVICE) <> -1:
                    return True
                else:
                    return False
        except Exception,e:
            print str(e)
            raise 
    def Test(self):
        pass
        
    def UnMount(self):
        try:
            cmd = 'unmount %s' % self.mpoint
        except Exception,e:
            print str(e)
            sys.exit()
            
    def run(self,fstype):
        try:
            if self.IsMount() == True:
                self.UnMount()
            print "%s Test Begin\n------------------------------------------------" % fstype
            self.MkFs(fstype)
            print "创建%s文件系统成功" % fstype
            self.MountFs()
            print "挂载%s分区到%s成功" %(self.DEVICE,self.mpoint)
            self.Test()
            print "%s编码测试PASS" % fstype
            self.UnMount()
            if not self.IsMount():
                print "卸载%s分区成功" % self.DEVICE
            else: 
                print "卸载%s分区失败" % self.DEVICE
            print "%s TEST PASS" % fstype
        except Exception,e:
            #print str(e)
            print "%s TEST FAIL" % fstype
        finally:
            print "%s Test END\n------------------------------------------------" % fstype
    
    def main(self):
        self.optparser(sys.argv)
        if self.DEVICE == None:
            print "分区设备不能为空，请指定分区设备"
            self.Usage()
        
        if self.FSTYPE == None:
            for fstype in FSTUPE:
                self.run(fstype)
        else:
            self.run(self.FSTYPE)
        
if __name__ == '__main__':
    ft = FsTest(DEVICE,FSTYPE)
    ft.main()
    