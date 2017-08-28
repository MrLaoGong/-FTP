__author__ = 'Mr.Bool'
import socketserver
import configparser
from conf import settings
import json
import hashlib
import os,time
OPERATION_DIR=settings.USER_HOME
STATUS_CODE={
    250:'客户端没有发送命令',
    251:'服务器端没有该命令',
    253:"错误用户名或密码",
    254:'验证成功',
    255:'当前文件夹下文件',
    256:'当前文件夹下为空',
    257:'没有该路径',
    258:'切换成功',
    259:'没有该切换路径',
    260:'文件大小',
    261:'md5验证',
    262:'准备接受文件',
    263:'磁盘空间不足',
    264:'磁盘上存在这个文件',
}
class FTPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.user=''
        print("有客户端连接")
        self.USERNOW_PATH=OPERATION_DIR
        while True:
            self.data=self.request.recv(1024).strip()
            print('客户端发过来的命令为：',self.data)
            if not self.data:
                print('客户端已关闭')
                break;
            data=json.loads(self.data.decode())
            print(data)
            print(self.user)
            if self.user is None:
                print('还没有用户登陆')
            if data.get('action') is not None:
                if hasattr(self,"_%s"%data.get('action')):
                    fun=getattr(self,'_%s'%data.get('action'))
                    fun(data)
                else:
                    print("服务器端没有该方法")
                    self.send_response(251)
            else:
                print('客户端没有发送命令')
                self.send_response(250)
    def send_response(self,status_code,data=None):
        print('发送数据',data)
        response={'status_code':status_code,'status_msg':STATUS_CODE[status_code]}
        if data:
            response.update(data)
        print(response)
        self.request.send(json.dumps(response).encode('utf-8'))
        print('发送完毕')
    def authenticate(self,username,password):
        '验证用户合法性，合法返回用户数据'
        config = configparser.ConfigParser()
        config.read(settings.ACCOUNT_FILE)
        #加密验证
        m=hashlib.md5()
        m.update(password.encode('utf-8'))
        m_pass=m.hexdigest()
        print('原密码：',password,'加密后：',m_pass)
        if username in config.sections():
            _password=config[username]["Password"]
            if _password==m_pass:
                print("验证成功")
                config[username]['Username']=username
                return username
            else:
                print('验证失败')


    def _list(self,*args,**kwargs):
        '查看用户目录'
        print('查看目录功能')
        print(args)
        if args[0].get('dir') is None:
            user_dir=self.USERNOW_PATH
        else:
            user_dir=os.path.join(self.USERNOW_PATH,args[0].get('dir'))
        print(user_dir)
        if os.path.exists(user_dir):
            dirs=os.listdir(user_dir)
            print(dirs)
            if len(dirs)==0:
                self.send_response(256)
            else:
                dirsdata={
                    "dirs":dirs
                }
                self.send_response(255,dirsdata)
        else:
            print('没有该路径')
            self.send_responses(257)
    def _auth(self,*args,**kwargs):
        print('登陆验证',args)
        data=args[0]
        if data.get('username') is None or data.get('password') is None:
            self.send_response(252)
        user=self.authenticate(data.get('username'),data.get('password'))
        if user is None:
            self.send_response(253)
        else:
            print("通过验证",user)
            self.user=user
            self.USERNOW_PATH=os.path.join(OPERATION_DIR,self.user)
            self.send_response(254)
    def getparentpath(self,strpath):
        '获取父目录'
        if not strpath:
            return None
        lspath=os.path.split(strpath)
        print(lspath)
        if lspath[1]:
            return lspath[0];
        lsPath = os.path.split(lspath[0]);
        return lsPath[0];
    def _cd(self,*args,**kwargs):
        '切换目录'
        if args[0].get('dir') is None:
            user_dir=self.USERNOW_PATH
            pass
        elif args[0].get('dir')=='..':
            if OPERATION_DIR==self.USERNOW_PATH:
                return
            print('切换到上一层目录')
            print(self.USERNOW_PATH)
            # print(os.path.pardir(self.USERNOW_PATH))
            # user_dir=os.path.pardir(os.path.abspath(self.USERNOW_PATH))
            user_dir=self.getparentpath(self.USERNOW_PATH)
            print(user_dir)
            pass
        else:
            user_dir=os.path.join(self.USERNOW_PATH,args[0].get('dir'))
        if os.path.exists(user_dir):
            self.USERNOW_PATH=user_dir
            print('当前目录路径为',self.USERNOW_PATH)
            dirdata={
                'dir':self.USERNOW_PATH
            }
            self.send_response(258,dirdata)
            print('切换成功')
            pass
        else:
            print('没有该切换路径')
            self.send_responses(259)
    def _get(self,*args,**kwargs):
        '下载文件'
        data=args[0]
        if data.get('filename') is None:
            print('文件为空')
            return
        fileabspath=os.path.join(OPERATION_DIR,self.user,data.get('filename'))
        if os.path.isfile(fileabspath):
            print('文件存在')
            file_size=os.path.getsize(fileabspath)
            self.send_response(260,data={'file_size':file_size})
            info=self.request.recv(1024)
            print(info)
            rf=open(fileabspath,'rb')
            m=hashlib.md5()
            for line in rf:
                self.request.send(line)
                m.update(line)
            else:
                print(self.request.recv(1024))
                print('传送完成')
                self.send_response(257,data={'md5date':m.hexdigest()})
                rf.close()
    def _put(self,*args,**kwargs):
        '上传文件'
        data=args[0]
        if data.get('filename') is None:
            print('文件不能为空')
            return
        if len(data)==3:
            file=os.path.join(OPERATION_DIR,self.user,data.get('filename'))
            if os.path.isfile(file):
                self.send_response(264)
        else:
            file=os.path.join(OPERATION_DIR,self.user,data.get('filedir'),data.get('filename'))
            if os.path.isfile(file):
                self.send_response(264)
        receivesize=0
        totalsize=data.get('filesize')
        rconfig=configparser.ConfigParser()
        rconfig.read(settings.ACCOUNT_FILE)
        for section in rconfig.sections():
            if section==self.user:
                print(rconfig.get(section,'max'),'----',rconfig.get(section,'size'))
                yusize=int(rconfig.get(section,'max'))-int(rconfig.get(section,'size'))
                print('剩余空间',str(yusize))
                print('文件大小',str(totalsize))
                if totalsize<yusize:
                    self.send_response(262)
                    wf=open(file,'wb')
                    while receivesize!=totalsize:
                        if totalsize-receivesize<1024:
                            data=self.request.recv(totalsize-receivesize)
                        else:
                            data=self.request.recv(1024)
                        wf.write(data)
                        receivesize+=len(data)
                    else:
                        size=int(rconfig.get(self.user,'size'))
                        size+=int(totalsize)
                        rconfig.set(section,'size',str(size))
                        rconfig.write(open(settings.ACCOUNT_FILE,'w'))
                        print('接受完成')
                        print(self.request.recv(1024))
                        wf.close()
                else:
                    print('磁盘空间不够')
                    self.send_response(263)

        pass