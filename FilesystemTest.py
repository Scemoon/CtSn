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
            print str(e)
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
        if self.RunShell(cmd) !=0:
            raise TestError('%s 创建文件系统失败' % fstype) 
    
    def MountFs(self,extar = ''):
        cmd = 'mount %s %s %s ' %(extar,self.DEVICE,self.mpoint)
        if self.RunShell(cmd) != 0:
            raise TestError("挂在%s分区失败" % self.DEVICE)
        
    def IsMount(self):
        try:
            mount_output = subprocess.Popen(["mount"],stdout=subprocess.PIPE)
            for line in mount_output.stdout.readlines():
                if line.find(self.DEVICE) != -1:
                    return True
                else:
                    return False
        except Exception,e:
            print str(e)
            raise 
        
    def ChineseTest(self):
        chinesepath=os.path.join(self.mpoint,'中文dir')
        chinesefile=os.path.join(self.mpoint,'中文file')
        try:
        #创建中文目录
            os.mkdir(chinesepath)
        #创建中文文件
            os.mkdir(chinesefile)
        except Exception,e:
            print str(e)
            raise TestError("不支持中文")
        if not os.path.isdir(chinesepath):
            raise TestError("创建中文目录失败")
        if not os.path.isfile(chinesefile):
            raise TestError("创建中文文件失败")
             
        try:
            fp = open(chinesefile,'r+')
            fp.write("中文汉字 ")
            fp.close()
        except IOError,e:
            print str(e)
            raise TestError("写入中文出错")
        
        
    def UnMount(self):
        try:
            cmd = 'unmount %s' % self.mpoint
        except Exception,e:
            print str(e)
            raise
            
    def run(self,fstype):
        try:
            if self.IsMount() == True:
                self.UnMount()
            print "%s Test Begin\n------------------------------------------------" % fstype
            self.MkFs(fstype)
            print "创建%s文件系统成功" % fstype
            self.MountFs()
            print "挂载%s分区到%s成功" %(self.DEVICE,self.mpoint)
            if self.IsMount() == False:
                raise TestError("%s挂在失败" % fstype)
            self.ChineseTest()
            print "%s编码测试PASS" % fstype
            self.UnMount()
            print "%s TEST PASS" % fstype
        except TestError,e:
            print str(e)
            print "%s TEST FAIL" % fstype
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
        
class TestError(Exception):
    def __init__(self,output):
        self.output = output
    
    def __str__(self):
        print self.output
        
if __name__ == '__main__':
    ft = FsTest(DEVICE,FSTYPE)
    ft.main()
    