__author__ = 'Mr.Bool'
import configparser
import os
config = configparser.ConfigParser()
config.read(u'C:/Users/Mr.Bool/Desktop/python作业/选课系统/UPFTP/ftpserver/conf/accounts.cfg')
for section in config.sections():
    if not os.path.exists(section):
        os.makedirs(section)