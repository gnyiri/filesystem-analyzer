from .fs_logger import FS_Logger


class FS_Base(object):
    """
    Base class for all PM classes
    """
    ROOT_DIRECTORY = "/proc"

    def __init__(self):
        self._logger = FS_Logger.get_instance()

    @property
    def logger(self):
        return self._logger