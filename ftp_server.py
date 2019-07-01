#!\usr\bin\env python3
#coding=utf-8
'''
name:George
email:276227382@qq.com
date:20190701
introduce:ftp文件服务器
env:python3.5
'''
from socket import *
import time
import os
import sys
import signal


FILE_PATH ='./ftpFile/'
HOST = '0.0.0.0'
PORT = 8000
ADDR = (HOST,PORT)

class FtpServer(object):
    def __init__(self,c):
        self.c = c

    def do_list(self):
        print('查看文件操作')
        #获取文件列表
        file_list = os.listdir(FILE_PATH)
        if not file_list:
            self.c.send('文件库为空')
            return
        else:
            self.c.send(b'OK')
            time.sleep(0.1)

        files = ''
        for file in file_list:
            #当不是隐藏文件并且是普通文件时
            if file[0] != '.' and os.path.isfile(FILE_PATH + file):
                files = files + file + '#'
        self.c.sendall(files.encode())

    def do_get(self,filename):
        print('文件下载操作')
        try:
            fd = open(FILE_PATH + filename,'rb')
        except:
            self.c.send('文件不存在'.encode())
            return
        self.c.send(b'OK')
        time.sleep(0.1)

        while True:
            data = fd.read(1024)
            if not data:
                time.sleep(0.1)
                self.c.send(b'##')
                break
            self.c.send(data)
        print('文件发送完毕')

    def do_put(self,filename):
        print('文件上传操作')
        try:
            f = open(FILE_PATH + filename,'wb')
        except:
            self.c.send('上传失败'.encode())
            return
        self.c.send(b'OK')
        while True:
            data = self.c.recv(1024)
            if data == b'##':
                break
            f.write(data)
        f.close()
        print('上传完毕')



def main():
    s = socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)
    s.listen(5)
    
    #处理子进程退出
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)
    print('Listen the port 8000....')

    while True:
        try:
            c,addr = s.accept()
        except KeyboardInterrupt:
            s.close()
            sys.exit('服务器退出')
        except Exception as e:
            print('服务器异常:',e)
            continue

        print('已连接客户端:',addr)

        #创建子进程
        pid = os.fork()
        if pid == 0:
            s.close()
            ftp = FtpServer(c)
            #判断客户端请求
            while True:
                data = c.recv(1024).decode()
                if not data or data[0] == 'Q':
                    c.close()
                    sys.exit('客户端退出')
                elif data[0] == 'L':
                    ftp.do_list()
                elif data[0] == 'G':
                    filename = data.split(' ')[-1]
                    ftp.do_get(filename)
                elif data[0] == 'P':
                    filename = data.split(' ')[-1]
                    ftp.do_put(filename)
        else:
            c.close()
            continue



if __name__ == '__main__':
    main()