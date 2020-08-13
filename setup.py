"""

Project:    Locks
Author:     LanHao
Date:       2020/8/13
Python:     python3.6

尝试打包成一个专门用于实现各种锁的模块

"""

from setuptools import find_packages, setup

setup(
    name='pylocks',
    version='1.0.0',
    description="锁相关",
    url="https://github.com/bigpangl/Locks",
    author="LanHao",
    author_email="bigpangl@163.com",
    license="GPL-3.0",
    packages=find_packages(),
)
