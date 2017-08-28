__author__ = 'Mr.Bool'
from optparse import OptionParser
import socket,json,os
class FTPClient(object):
    def __init__(self):
        self.sock=socket.socket()
        self.sock.connect(("localhost",9001))
    def get_response(self):
        data=self.sock.recv(1024).decode()
        response=json.loads(data)
        return response
    def interactive(self):
        while True:
            order=input('>>:').strip()
            self.sock.send(order.encode('utf-8'))
            list_cmd=order.split()
            if hasattr(self,'_%s'%list_cmd[0]):
                func=getattr(self,'_%s'%list_cmd[0])
                func(list_cmd)
            else:
                print('没有该命令')
    def _get(self,args):
        '下载文件'
        print(args)
        self.sock.send(json.dumps(args).encode('utf-8'))
        response=json.loads(self.sock.recv(1024))
        filesize=response.get('filesize')
        received=0
        wf=open(args[1],'wb')
        while received!=filesize:
            if filesize-received<1024:
                line=self.sock.recv(filesize-received)
            else:
                line=self.sock.recv(1024)
            wf.write(line)
            received+=len(line)
        else:
            wf.close()
            print('接受完成')



    def _put(self,args):
        '上传文件'
        print(args)
        filename=args[1]
        if os.path.isfile(filename):
            filesize=os.path.getsize(filename)
            self.sock.send(json.dumps({'filesize':filesize}).encode('utf-8'))
            rf=open(filename,'rb')
            for line in rf:
                self.sock.send(line)
            else:
                rf.close()
                print('上传成功')
if __name__=="__main__":
    ftp=FTPClient()
    ftp.interactive()