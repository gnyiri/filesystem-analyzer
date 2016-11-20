import logging
import logging.handlers
import sys
import threading


class FSLogger(logging.Logger):
    _INST_LOCK = threading.Lock()
    _INSTANCE = None

    @classmethod
    def get_instance(cls):
        """ Method for getting the only instance """
        if cls._INSTANCE is None:
            with cls._INST_LOCK:
                if cls._INSTANCE is None:
                    __temp = FSLogger()
                    cls._INSTANCE = __temp
        assert cls._INSTANCE is not None
        return cls._INSTANCE

    def __init__(self):
        logging.Logger.__init__(self, "pm")

        self.addHandler(logging.StreamHandler(sys.stdout))