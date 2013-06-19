#!/usr/bin/env python
# -*- coding:utf8 -*-
import commands
import os,sys,getopt


file = 'source.file'
Test_tupe = ('python','perl','c','java')

class LauageTest:
    def __init__(self,file):
        self.file = file
        self.LANGUAGE = None
        
    def Usage(self):
        print'''Usage:DeveLanguage.py [options] [value]
options:
        -h, --help      帮助信息;
        -v, --version   版本信息;
        -l, --launage   开发语言;
             '''
        sys.exit()
        
    def optparser(self,args=sys.argv):
        opts, args = getopt.getopt(args[1:],"hvl:",["help","version","language"])
        try:
            for opt,value in opts:
                if opt in ('-h','--help'):
                    self.Usage()
                if opt in ('-v','--version'):
                    print "Version1.0"
                    sys.exit()
                if opt == '-l':
                    self.LANGUAGE= value
                
        except Exception,e:
            print str(e)
            self.Usage()
    
    def TestFile(self,content):
        try:
            fp = open(self.file,'w')
            fp.writelines(content)
            fp.close()
        except IOError,e:
            raise
        
    def RemoveFile(self,File):
        if File == None:
            File = self.file
        os.remove(File)
        
    def RunShell(self,cmd):
        try:
            status,output = commands.getstatusoutput(cmd)
            if status != 0:
                raise TestError(output)
        except Exception,e:
            pass 
        
    def CompileFile(self,TEST):
        if TEST == "c":
            cmd = "gcc -o Hello %s" % self.file
            self.RunShell(cmd)
        if TEST == "java":
            cmd = "javac %s" % self.file
            self.RunShell(cmd)
    
    def RunTest(self,TEST):
        if TEST in ("python","perl"):
            content = '''print "Hello World!"
            '''
            cmd = "%s %s" % (TEST,self.file)
        elif TEST == "c":
            self.file = "hello.c"
            content ='''#include <stdio.h>
void main()
{
   printf("hello world!\\n");
  
} '''
            cmd = "./Hello"
            
        elif TEST == "java":
            content = '''class Hello{ 
public static void main(String[] args) {  
  System.out.println("Hello World!"); 
  }
}'''
            self.file = "hello.java"
            cmd = "java Hello"
        else:
            raise TestError("HAVE NO THE LANGUAGE,%s" % TEST) 
                
        self.TestFile(content)
        if TEST in ('c','java'):
            self.CompileFile(TEST)
        self.RunShell(cmd)
        self.RemoveFile(self.file)
        if TEST == 'c':
            self.RemoveFile('Hello')
        if TEST == "java":
            self.RemoveFile('Hello.class')
        
    def run(self,TEST):
        try:
            self.RunTest(TEST)
            print "%6s TEST PASS" % TEST
        except TestError,e:
            print str(e)
            print "%6s TEST FAIL" % TEST
        except Exception,e:
            print str(e)
            print "%6s TEST FAIL" % TEST
            
            
    def main(self):
        self.optparser(sys.argv)
        print "Test Begin\n------------------------------------------------"
        if self.LANGUAGE == None:
            for test in Test_tupe:
                self.run(test)
        else:
            self.run(self.LANGUAGE)
        print "------------------------------------------------" 
        print "Test END"
    
class TestError(Exception):
    def __init__(self,output):
        self.output = "Error:"+output
    
    def __str__(self):
        return self.output
    

if __name__ == '__main__':
    R = LauageTest(file)
    R.main()
