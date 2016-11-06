from .fs_logger import FS_Logger
from .fs_app import FS_App


class FS_Base(object):
    """
    Base class for all PM classes
    """
    ROOT_DIRECTORY = "/proc"

    def __init__(self):
        self._logger = FS_Logger.get_instance()
        self._app = FS_App.get_instance()

    @property
    def logger(self):
        return self._logger

    @property
    def app(self):
        return self._app
