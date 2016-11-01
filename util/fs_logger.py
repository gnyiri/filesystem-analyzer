import logging
import logging.handlers
import sys
import threading


class FS_Logger(logging.Logger):
    _INST_LOCK = threading.Lock()
    _INSTANCE = None

    @classmethod
    def get_instance(cls):
        """ Method for getting the only instance """
        if cls._INSTANCE is None:
            with cls._INST_LOCK:
                if cls._INSTANCE is None:
                    cls._INSTANCE = FS_Logger()
        assert cls._INSTANCE is not None
        return cls._INSTANCE

    def __new__(cls, *args, **kwargs):
        """ To make sure there will be only one instance """
        if not isinstance(cls._INSTANCE, cls):
            cls._INSTANCE = object.__new__(cls, *args, **kwargs)
        return cls._INSTANCE

    def __init__(self):
        logging.Logger.__init__(self, "pm")

        self.addHandler(logging.StreamHandler(sys.stdout))