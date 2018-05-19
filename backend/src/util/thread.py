import threading
import logging

class Thread(threading.Thread):

    def __init__(self,group=None, target=None, name=None,
                 args=(), kwargs=None, *, daemon=None):
        super().__init__(group=group, target=target, name=name, daemon=daemon)

        self.args = args
        self.kwargs = kwargs
        self.name = name
        self.target = target

    def run(self):
        logging.info('running thread %s with target %s', self.name, self.target)
        self.target(*self.args)