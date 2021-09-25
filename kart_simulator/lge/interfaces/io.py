import queue

class IOInterface:
    requests = queue.Queue()
    inputs = queue.Queue()