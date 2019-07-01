#示例一个文件一半一半的烤到两个文件下
from multiprocessing import Process
import os

filename = './bytes.png'
size = os.path.getsize(filename)

def copy1():
    f = open(filename,'rb')
    s = size // 2
    fw = open('file1.png','wb')
    while True:
        if s < 1024:
            data = f.read(s)
            fw.write(data)
            break
        data = f.read(1024)
        fw.write(data)
        s -= 1024
    f.close()
    fw.close()

def copy2():
    f = open(filename,'rb')
    f.seek(size // 2,0)
    fw = open('file2.png','wb')
    while True:
        data = f.read(1024)
        if not data:
            break
        fw.write(data)
    f.close()
    fw.close()

p1 = Process(target = copy1)
p2 = Process(target = copy2)
p1.start()
p2.start()
p1.join()
p2.join()








