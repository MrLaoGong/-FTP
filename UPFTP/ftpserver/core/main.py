__author__ = 'Mr.Bool'
from optparse import OptionParser
import socketserver
from core.ftphandler import FTPHandler
class ArgvHandler(object):
    def __init__(self):
        self.parse=OptionParser()
        self.parse.add_option('-s','--host',dest='host',help='服务ip')
        self.parse.add_option('-p','--port',dest='port',type='int',help='服务端口')
        (option,args)=self.parse.parse_args()
        self.verify_args(option,args)
    def verify_args(self,option,args):#verify 判定
        if hasattr(self,args[0]):
            fun=getattr(self,args[0])
            fun()
    def start(self):
        server=socketserver.ThreadingTCPServer(('localhost',9999),FTPHandler)
        server.serve_forever()