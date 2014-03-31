#!/usr/bin/env python
# -*- coding:utf-8 -*-

# name:crack.py

import os,sys,getopt
import subprocess



DICT_FILE = None
DICT_DIR = None
BSSID = None
CAP_FILE = None

def usage():
    print '''
    Usage: crack.py [options] args
    options: -h --help, 帮助信息
             -f --file, 密码字典文件
             -d --dir, 密码字典目录
             -b --bssid, 路由MAC
             -c --cap, 捕获的日志文件         
        '''
    sys.exit()
    
def getopts(argv=sys.argv):
    global DICT_FILE
    global DICT_DIR
    global BSSID
    global CAP_FILE
    
    try:
        opts, args = getopt.getopt(argv[1:],"hf:d:b:c:",['help', 'file', 'dir', 'bssid', 'cap'])
    except getopt.GetoptError:
        usage()
      
    for opt,value in opts:
        
        if opt in ('-h','--help'):
            usage()
            
        if opt in ('-f', '--file'):
            if os.path.isfile(value):
                DICT_FILE = value
            else:
                print "正确的字典文件"
                sys.exit()
        if opt in ('-d', '--dir'):
            if os.path.isdir(value):
                DICT_DIR = value
            else:
                print "请输入正确的字典目录"
                sys.exit()
        if opt in ('-c', '--cap'):
            if os.path.isfile(value):
                 CAP_FILE = value
            else:
                print "请输入正确cap文件"
                sys.exit()
                
        if opt in ('-b', '--bssid'):
            BSSID=value
            
def run(cap_file, dict_file, bssid=None):
  
    if bssid is None:
        arg_list = ['aircrack-ng', cap_file, '-w', dict_file]
    else:
        arg_list = ['aircrack-ng', cap_file, '-b', bssid, '-w', dict_file ]

    try:
        subprocess.call(arg_list)
    except Exception:
        print sys.exc_info()
            
def run_dir(cap_file, dict_dir, bssid=None):
    for root, dirs, files in os.walk(dict_dir):
        for file in files:
            file_path = os.path.join(root, file)
            run(cap_file, file_path, bssid)

            

        
def main():
    global DICT_FILE
    global DICT_DIR
    global BSSID
    global CAP_FILE
    
    getopts()
   
    if CAP_FILE is None:
        print "请输入cap文件"
        sys.exit()
    
    if DICT_DIR is not None:
        run_dir(CAP_FILE, DICT_DIR, BSSID)
    elif DICT_FILE is not None:
        run(CAP_FILE, BSSID, DICT_FILE)
    else:
        print "输入有效的字典文件"
    
        
if __name__ == '__main__':
    main()
    
    
                
                