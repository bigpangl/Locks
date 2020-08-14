"""

Project:    Locks
Author:     LanHao
Date:       2020/8/13
Python:     python3.6

"""
from multiprocessing import Lock, Event, Value

from .base import Shared, Mutex
from .apis import LockInterface, SharedAndMutexInterface


class SharedAndMutex(SharedAndMutexInterface):
    """
    共享/ 互斥锁  的配对使用,具体实现
    """

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

        self.owner_smp: Lock = Lock()  # 抢占部分,释放与否造成多种用法

        self.users: Value = Value("i", 0)  # 被共享锁占用的使用人数
        self.lock_users: Lock = Lock()  # 归还锁时，不需抢占资源就可以修改users 数量,所以需要枷锁防止冲突
        self.use_status: Event = Event()
        self.use_status.set()  # 初始状态设置为可用

    @property
    def Shared(self) -> LockInterface:
        return Shared(self)

    @property
    def Mutex(self) -> LockInterface:
        return Mutex(self)
