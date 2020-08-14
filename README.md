# Locks

基于python ，完成一个进程安全的,共享锁/互斥锁模型。

用于模拟数据库中单行数据的读写时的共享锁和互斥锁。

使用python 进程模块下的进程锁，进程事件，进程信号以及进程变量初步实现，无第三方依赖。

## 使用方法

#### 共享/ 互斥锁

```python
from pylocks.locks import SharedAndMutex
from pylocks.apis import SharedAndMutexInterface


lock:SharedAndMutexInterface = SharedAndMutex()
with lock.Shared:
    print("hello word ") # 共享锁
    
with lock.Mutex:
    print("helo word ")  # 互斥锁
```

