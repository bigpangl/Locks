"""

Project:    Locks
Author:     LanHao
Date:       2020/8/13
Python:     python3.6

"""
import logging
import random,time
from multiprocessing import Process
import threading

from pylocks.locks import SharedAndMutex

def get_read(row:SharedAndMutex):
    """
    周期性获取读锁，释放读锁
    :param row:
    :return:
    """
    logging.basicConfig(level=logging.DEBUG,format='%(process)d %(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s')

    while True:
        t = random.random()
        try:
            with row.Shared:
                time.sleep(t)
            logging.info("完成一次读锁")
        except Exception as e:
            logging.error(f"读锁测试部分发生错误:{e}")

def get_write(row:SharedAndMutex):
    """
    周期性获取写锁，释放写锁
    :param row:
    :return:
    """
    logging.basicConfig(level=logging.DEBUG,format='%(process)d %(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s')
    while True:
        t = random.random()
        try:
            with row.Mutex:
                time.sleep(t)
            logging.info("完成一次写锁")
        except Exception as e:
            logging.error(f"写锁测试部分发生错误:{e}")

class ReadThread(threading.Thread):
    def __init__(self,row:SharedAndMutex):
        self._lock = row
        super(ReadThread, self).__init__()
    def run(self):
        get_read(self._lock)

class WriteThread(ReadThread):
    def run(self):
        get_write(self._lock)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(process)d %(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s')
    row = SharedAndMutex()
    task = []
    for i in range(5): # 读锁
        task.append(Process(target=get_read,args=(row,)))
        # task.append(ReadThread(row))
    for i in range(5):  # 写锁
        task.append(Process(target=get_write,args=(row,)))
        # task.append(WriteThread(row))
    for single in task:
        single.start()
    # for single in task:
    #     single.join()

