"""

Project:    Locks
Author:     LanHao
Date:       2020/8/13
Python:     python3.6

"""
import logging

from .apis import LockInterface,SharedAndMutexInterface

class Shared(LockInterface):
    """
    共享锁
    """


    def __init__(self, sources: SharedAndMutexInterface):
        self.source: SharedAndMutexInterface = sources

    def acquire(self):
        logging.debug(f"before {self.__class__.__name__} :{self.source}")
        with self.source.owner_smp:
            with self.source.lock_users:  # 修改user 时是枷锁的
                self.source.users.value += 1
                if self.source.users.value == 1:
                    # with self.source.use_status_lock:
                    self.source.use_status.clear()  # 不可独占了
        logging.debug(f"after {self.__class__.__name__}:{self.source}")

    def release(self):
        logging.debug(f"before un{self.__class__.__name__}:{self.source}")
        with self.source.lock_users:  # 归还时是枷锁的
            self.source.users.value -= 1
            if self.source.users.value == 0:
                # with self.source.use_status_lock:
                self.source.use_status.set()  # 允许独占了
        logging.debug(f"after un{self.__class__.__name__}:{self.source}")

class Mutex(Shared):
    """
    互斥锁
    """

    def acquire(self):
        logging.debug(f"before {self.__class__.__name__}:{self.source}")
        self.source.owner_smp.acquire()
        self.source.use_status.wait()
        logging.debug(f"after {self.__class__.__name__}:{self.source}")

    def release(self):
        logging.debug(f"before un{self.__class__.__name__}:{self.source}")

        self.source.owner_smp.release()
        logging.debug(f"after un{self.__class__.__name__}:{self.source}")
