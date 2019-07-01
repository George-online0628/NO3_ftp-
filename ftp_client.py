from socket import *
import sys
import time

class FtpClient(object):
    def __init__(self,s):
        self.s = s

    #获取文件列表
    def do_list(self):
        self.s.send(b'L')
        data = self.s.recv(1024).decode()
        if data == 'OK':
            data = self.s.recv(4096).decode()
            files = data.split('#')
            for file in files:
                print(file)
            print('文件列表展示完毕')
        else:
            #由服务器发送失败原因
            print(data)
    
    #下载文件
    def do_get(self,filename):
        self.s.send(('G ' + filename).encode())
        data = self.s.recv(1024).decode()
        if data == 'OK':
            fd = open(filename,'wb')
            while True:
                data = self.s.recv(1024)
                if data == b'##':
                    break
                fd.write(data)
            fd.close()
            print('%s下载完毕\n'%filename)
        else:
            print(data)

    def do_put(self,filename):
        try:
            f = open(filename,'rb')
        except:
            print('没有找到文件')
            return

        self.s.send(('P ' + filename).encode())
        data = self.s.recv(1024).decode()
        if data == 'OK':
            while True:
                data = f.read(1024)
                if not data:
                    time.sleep(0.1)
                    self.s.send(b'##')
                    break
                self.s.send(data)
            f.close()
            print('%s上传完成'%filename)
        else:
            print(data)



    def do_quit(self):
        self.s.send(b'Q')

def main():
    if len(sys.argv) < 3:
        print('命令行输入有误')
        return
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    ADDR = (HOST,PORT)

    s = socket()

    try:
        s.connect(ADDR)
    except:
        print('连接服务器失败')
        return

    ftp = FtpClient(s)
    while True:
        print('''
            ========= 命令选项 ==========
            ==========  list  ==========
            ==========get file==========
            ==========put file==========
            ==========  quit  ==========
            ============================
            ''')

        cmd = input('请输入命令>>')

        if cmd.strip() == 'list':
            ftp.do_list()
        elif cmd[:3] == 'get':
            filename = cmd.split(' ')[-1]
            ftp.do_get(filename)
        elif cmd.strip() == 'quit':
            ftp.do_quit()
            s.close()
            sys.exit('谢谢使用')
        elif cmd[:3] == 'put':
            filename = cmd.split(' ')[-1]
            ftp.do_put(filename)
        else:
            print('请输入正确的命令！')
            continue






if __name__ == '__main__':
    main()
