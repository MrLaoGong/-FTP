__author__ = 'Mr.Bool'
from optparse import OptionParser
import socket
import getpass
import hashlib,json,os
class FTPClient(object):
    def __init__(self):
        self.parse=OptionParser()
        self.parse.add_option("-s","--host",dest="host",help="ip地址")
        self.parse.add_option("-p","--port",dest="port",type='int',help="端口号")
        self.option,self.args=self.parse.parse_args()
        self.makeconnect()
    def makeconnect(self):
        if self.option.host and self.option.port:
            if self.option.port>0 and self.option.port<65535:
                print('端口可用')
                pass
            else:
                print('端口设置错误')
                exit('Err:port 必须 大于0 小于65535')
        print('尝试连接')
        self.sock=socket.socket()
        print(self.option.host,'---',self.option.port)
        self.sock.connect((self.option.host,self.option.port))
    def authenticate(self):#authentivatevt.	证明是真实的
        count=0
        while count<3:
            name=input("请输入用户名")
            password=getpass.getpass("请输入密码")
            count+=1
            return self.get_auth_result(name,password)
        exit()
    def get_response(self):
        data=self.sock.recv(1024).decode()
        response=json.loads(data)
        return response
    '验证方法'
    def get_auth_result(self,username,password):
        m=hashlib.md5()
        m.update(password.encode('utf-8'))
        data={
            'action':'auth',
            'username':username,
            'password':m.hexdigest()
        }
        self.sock.send(json.dumps(data).encode('utf-8'))
        response=self.get_response()
        if response.get('status_code')==254:
            print('登陆成功')
            self.user=username
            return True
        else:
            print(response.get('status_msg'))
            return False


    def interactive(self):
        if self.authenticate():
            while True:
                order=input('[%s]:'%self.user).strip()
                list_cmd=order.split()
                if hasattr(self,'_%s'%list_cmd[0]):
                    func=getattr(self,'_%s'%list_cmd[0])
                    func(list_cmd)
                else:
                    print('没有该命令')
    def _cd(self,args):
        print('切换目录')
        if len(args)==1:
            print('请输入切换的目录')
            exit()
        else:
            data={
                'action':'cd',
                'dir':args[1]
            }
        self.sock.send(json.dumps(data).encode('utf-8'))
        response=self.get_response()
        print(response)
        if response.get('status_code')==258:
            print(response.get('status_msg'))
            dir=response.get('dir').split(self.user)
            print('成功切换到目录',dir[1])
        elif response.get('status_code')==259:
            print(response.get('status_msg'))

    def _list(self,args):
        if len(args)==1:
            data={
            'action':'list',
            }
        else:
            data={
                'action':'list',
                'dir':args[1]
            }
        self.sock.send(json.dumps(data).encode('utf-8'))
        response=self.get_response()
        print(response)
        if response.get('status_code')==255:
            print(response.get('status_msg'))
            dirs=response.get('dirs')
            for d in dirs:
                print(d)
        elif response.get('status_code')==256:
            print(response.get('status_msg'))
        elif response.get('status_code')==257:
            print(response.get('status_msg'))
    def _put(self,args):
        '上传文件'
        pass
    def show_progress(self,total):
        received_size=0
        current_size=0
        while received_size<total:
            if int((received_size/total)*100)>current_size:
                print('#')
                current_size=int((received_size/total)*100)
            new_size=yield
            received_size+=new_size
    def show_progress(self,total):
        received_size=0
        current_size=0
        while received_size<total:
            if int((received_size/total)*100)>current_size:
                print('#',end="")
                current_size=int((received_size/total)*100)
            new_size=yield
            received_size+=new_size
    def _get(self,args):
        '下载文件'
        if args[1]:
            data={
                'action':'get',
                'filename':args[1]
            }
            self.sock.send(json.dumps(data).encode('utf-8'))
            response=self.get_response()
            print(response)
            if response.get('status_code')==260:
                self.sock.send(b'I am ready')
                print('准备接受')
                receivedsize=0
                wf=open(r'%s'%args[1],'wb')
                m=hashlib.md5()
                progress=self.show_progress(response.get('file_size'))
                progress.__next__()
                while receivedsize!=response.get('file_size'):
                    if response.get('file_size')-receivedsize<1024:
                        data=self.sock.recv(response.get('file_size')-receivedsize)
                    else:
                        data=self.sock.recv(1024)
                    m.update(data)
                    wf.write(data)
                    receivedsize+=len(data)
                    try:
                        progress.send(len(data))
                    except StopIteration as e:
                        print('100%')
                        print('接收完成')
                        self.sock.send(b'ok')
                        mdata=self.get_response()
                        if mdata.get('md5date')==m.hexdigest():
                            print('验证完成')
                            wf.close()
            pass
        else:
            print('没有文件信息')
            return
        pass
    def __md5_requeired(self,list_cmd):
        '是否使用md5校验'
        if '--md5' in list_cmd:
            return True
    def _put(self,args):
        '上传文件'
        if os.path.isfile(args[1]):
            '文件存在'
            file_size=os.path.getsize(args[1])
            if len(args)==2:
                data={
                    'action':'put',
                    'filesize':file_size,
                    'filename':args[1]
                }
            else:
                data={
                    'action':'put',
                    'filesize':file_size,
                    'filename':args[1],
                    'filedir':args[2]
                }
            self.sock.send(json.dumps(data).encode('utf-8'))
            response=self.get_response()
            print(response)
            pross=self.show_progress(file_size)
            pross.__next__()
            if response.get('status_code')==262:
                '开始发送'
                print('开始发送')
                rf=open(args[1],'rb')
                for line in rf:
                    self.sock.send(line)
                    try:
                        pross.send(len(line))
                    except StopIteration as e:
                        print('100%')
                        print('发送完成')
                else:
                    print('关闭文件')
                    rf.close()
            elif response.get('status_code')==263:
                print("磁盘空间不足")
                return
            elif response.get('status_code')==264:
                print('磁盘存在该文件')
                return
        else:
            print('没有该文件')
            return
if __name__=='__main__':
    ftp=FTPClient()
    ftp.interactive()#交互