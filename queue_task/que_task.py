from config.config import queue


def func_queue(func):
    queue.enqueue(func)