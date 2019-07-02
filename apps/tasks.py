"""
声明高并发下执行的任务
"""
from . import capp


@capp.task
def add_order(**order_info):
    pass