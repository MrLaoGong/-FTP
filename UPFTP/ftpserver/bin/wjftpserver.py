__author__ = 'Mr.Bool'
import os,sys
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from core import main

if __name__=='__main__':
    print('正在启动服务器')
    main.ArgvHandler()