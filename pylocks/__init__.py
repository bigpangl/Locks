"""

Project:    Locks
Author:     LanHao
Date:       2020/8/13
Python:     python3.6

"""

import abc
import logging
from multiprocessing import  Lock, Event,Value,Semaphore


class ReadAndWriteLock(abc.ABC):
    """

    读写锁的接口,也就是共享锁和排它锁同时存在的锁

    当有进程占用读锁时，写锁无法加上.

    当有写锁等待时，新的读锁不能加入,需要等待.

    读锁归还完毕后,等待中的写锁可以获取写的权限

    我并不知道程序中的读写锁能应用到什么场合

    """

    @abc.abstractmethod
    def read_acquire(self):
        pass
    @abc.abstractmethod
    def read_release(self):
        pass

    @abc.abstractmethod
    def write_acquire(self):
        pass

    @abc.abstractmethod
    def write_release(self):
        pass


class RowDetail(ReadAndWriteLock):
    """
    目标是读写锁,RowDetail 为暂时的一种实现方式.

    后期若有修改,当通过后面的赋值修改以满足接口的调用不变性质

    """
    def __init__(self):
        self._owner_smp:Semaphore = Semaphore(1) # 初始拥有资源

        self._share_use:Value = Value("i",0)
        self._share_use_lock = Lock()
        self._event_only:Event = Event()
        self._event_only.set() # 初始可用
        self._event_only_lock:Lock = Lock()
        logging.debug(f"共享锁/互斥锁 初始化成功")


    def read_acquire(self):
        """
        获取共享锁
        :return:
        """
        try:
            self._owner_smp.acquire() # 独占操作权
            with self._share_use_lock:
                self._share_use.value+=1
                logging.debug(f"获取共享锁成功")
                if self._share_use.value==1:
                    with self._event_only_lock:
                        logging.debug(f"限制互斥锁")
                        self._event_only.clear()
        except Exception as e:
            logging.error(f"获取读锁时发生错误:{e}")
        else:
            pass
        finally:
            self._owner_smp.release() # 归还操作权

    def read_release(self):
        """
        归还读锁
        :return:
        """
        with self._share_use_lock:
            self._share_use.value-=1
            logging.debug(f"归还共享锁成功")
            if self._share_use.value==0:
                with self._event_only_lock:
                    logging.debug(f"归还互斥锁权限")
                    self._event_only.set()

    def write_acquire(self):
        """
        获取写锁
        :return:
        """
        try:
            self._owner_smp.acquire() # 独占操作权,但此处不归还
            self._event_only.wait()
            logging.debug(f"获取互斥锁成功")
        except Exception as e:
            logging.error(f"增加写锁失败:{e}")
        else:
            pass
        finally:
            pass

    def write_release(self):
        """
        归还写锁
        :return:
        """
        try:
            logging.debug(f"归还互斥锁成功")
            self._owner_smp.release()
        except Exception as e:
            logging.error(f"归还互斥锁失败{e}")
        else:
            pass
            # logging.info(f"归还写锁成功")
        finally:
            pass


SharedAndMutex:ReadAndWriteLock = RowDetail
