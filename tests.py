"""

Project:    Locks
Author:     LanHao
Date:       2020/8/13
Python:     python3.6

"""
import logging
import random,time
from multiprocessing import Process

from Locks import ReadAndWriteLock,SharedAndMutex

def get_read(row:ReadAndWriteLock):
    """
    周期性获取读锁，释放读锁
    :param row:
    :return:
    """
    logging.basicConfig(level=logging.DEBUG,format='%(process)d %(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s')
    while True:
        t = random.random()
        try:
            row.read_acquire()
            time.sleep(t)
            row.read_release()
            logging.info("完成一次读锁")
        except Exception as e:
            logging.error(f"读锁测试部分发生错误:{e}")

def get_write(row:ReadAndWriteLock):
    """
    周期性获取写锁，释放写锁
    :param row:
    :return:
    """
    logging.basicConfig(level=logging.DEBUG,format='%(process)d %(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s')
    while True:
        t = random.random()
        try:
            row.write_acquire()
            time.sleep(t)
            row.write_release()
            logging.info("完成一次写锁")
        except Exception as e:
            logging.error(f"写锁测试部分发生错误:{e}")


if __name__ == '__main__':
    row = SharedAndMutex()
    task = []
    for i in range(5): # 读锁
        task.append(Process(target=get_read,args=(row,)))
    for i in range(5):  # 写锁
        task.append(Process(target=get_write,args=(row,)))

    for single in task:
        single.start()