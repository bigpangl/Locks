"""

Project:    Locks
Author:     LanHao
Date:       2020/8/14
Python:     python3.6

"""
import abc
from typing import List, Dict
from multiprocessing import Lock, Event, Value


class LockInterface(abc.ABC):
    """
    基础锁类别
    """

    @abc.abstractmethod
    def acquire(self):
        pass

    @abc.abstractmethod
    def release(self):
        pass

    def __enter__(self):
        self.acquire()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()


class SharedAndMutexInterface(object):
    """
    共享/ 互斥锁
    """
    args: List = None
    kwargs: Dict = None

    owner_smp: Lock = None
    users: Value = None
    lock_users: Lock = None
    use_status: Event = None

    @property
    @abc.abstractmethod
    def Shared(self) -> LockInterface:
        pass

    @property
    @abc.abstractmethod
    def Mutex(self) -> LockInterface:
        pass

    def __str__(self):
        return f"owner_smp:{self.owner_smp},uses:{self.users.value},use_status:{self.use_status.is_set()}"
