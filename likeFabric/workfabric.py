__author__ = 'Mr.Bool'
import paramiko
import getpass
import threading
hostlist=['localhsot','localhost','localhost']
hostaction=['执行命令','上传下载']
class FTPClient(object):
    def __init__(self):
        self.ssh = paramiko.SSHClient()
        pass
    def ssh_connect(self,host,port,username,password):
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=host,port=port,username=username,password=password)
    def ssh_cmd(self,*args):
        while True:
            cmd=input(">>:")
            stdin,stdout,stderr=self.ssh.exec_command(cmd)
            result=stdout.read()
            print(result.decode())
    def sftp_connect(self,host,port,username,password):
        transport=paramiko.Transport((host,port))
        transport.connect(username=username,password=password)
        self.sftp=paramiko.SFTPClient.from_transport(transport)
    def get(self,*args):
        serverpath=args[0].split()[2]
        localpath=args[0].split()[1]
        self.sftp.get(serverpath,localpath)
    def put(self,*args):
        serverpath=args[0].split()[2]
        localpath=args[0].split()[1]
        self.sftp.put(localpath,serverpath)
    def stop_sftp(self):
        self.sftp.close()
    def interactive(self):
        while True:
            cmd=input(">>:").strip()
            cmd_str=cmd.split()[0]
            if hasattr(self,cmd_str):
                func=getattr(self,cmd_str)
                func(cmd)

def login():
    port=input("输入端口")
    username=input('输入用户名')
    password=input('输入密码')
    return [port,username,password]
def main():
    while True:
        for index,host in enumerate(hostlist):
            print(index,host)
        choice_host=input('请输入选择的主机编号')
        while True:
            for index,action in enumerate(hostaction):
                print(index,action)
            choice_action=input('请输入选择的动作编号')
            if int(choice_action)==0:
                while True:
                    connectinfo=login()
                    port = connectinfo[0]
                    username=connectinfo[1]
                    password=connectinfo[2]
                    ftp=FTPClient()
                    ftp.ssh_cmd(hostlist[int(choice_host)],int(port),username,password)
                    ftp.ssh_cmd()
            if int(choice_action)==1:
                while True:
                    connectinfo=login()
                    port = connectinfo[0]
                    username=connectinfo[1]
                    password=connectinfo[2]
                    sftp=FTPClient()
                    sftp.sftp_connect(hostlist[int(choice_host)],int(port),username,password)
                    sftp.interactive()

t=threading.Thread(target=main,args=())
t.start()