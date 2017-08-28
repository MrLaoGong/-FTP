__author__ = 'Mr.Bool'
import select
import socket
import queue,json,os
class SelectFTP(object):
    def __init__(self):
        self.server=socket.socket()
        self.server.bind(('0.0.0.0',9001))
        self.server.listen(1000)
        self.server.setblocking(False)
        self.intputs=[self.server,]
        self.outputs=[]
        self.msg_dic={}
        self.count=0
    def handler(self):
        while True:
            readable,writeable,excepational=select.select(self.intputs,self.outputs,self.intputs)
            for r in readable:
                if r is self.server:
                    self.count+=1
                    # print('server',str(self.count))
                    # print("有新的链接")
                    conn,addr=self.server.accept()
                    # print(conn,addr)
                    self.intputs.append(conn)
                    self.msg_dic[conn]=queue.Queue()
                    # print('添加成功')
                else:
                    self.count+=1
                    # print('r',str(self.count))
                    data=r.recv(1024)
                    # print(data)
                    # r.send(data)
                    self.msg_dic[r].put(data)
                    self.outputs.append(r)
            for w in writeable:
                print(w)
                self.count+=1
                data=self.msg_dic[w].get()
                print(data.decode().split())
                if data.decode().split()[0]=='get':
                    self._get(data.decode().split(),w)
                elif data.decode().split()[0]=='put':
                    self._put(data.decode().split(),w)
                self.outputs.remove(w)
            for e in excepational:
                if e in self.outputs:
                    self.outputs.remove(e)
                self.intputs.remove(e)
                del self.msg_dic[e]

    def _put(self,*args):
        '上传'
        print(args)
        connp=args[1]
        data=args[0]
        filename=data[1]
        datafilesize=json.loads(connp.recv(1024).decode())
        filesize=datafilesize.get('filesize')
        receivesize=0
        wf=open(filename,'wb')
        while receivesize!=filesize:
            if filesize-receivesize<1024:
                line=connp.recv(filesize-receivesize)
            else:
                line=connp.recv(1024)
            wf.write(line)
            receivesize+=len(line)
        else:
            wf.close()
            print('上传成功')

    def _get(self,*args):
        '下载'
        print('下载...')
        print(args[0],args[1])
        conng=args[1]
        data=args[0]
        filename=data[1]
        if os.path.isfile(filename):
            filesize=os.path.getsize(filename)
            print('要下载的数据大小：',filesize)
            conng.send(json.dumps({'filesize':filesize}).encode('utf-8'))
            rf=open(filename,'rb')
            sendsize=0
            for line in rf:
                conng.send(line)
                sendsize+=len(line)
            else:
                print('总共发送了',sendsize)
                print('发送完成')
                rf.close()

if __name__=='__main__':
    selectserver=SelectFTP()
    selectserver.handler()