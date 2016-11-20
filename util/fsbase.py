from .fslogger import FSLogger
from .fsapp import FSApp


class FSBase(object):
    """
    Base class for all PM classes
    """
    ROOT_DIRECTORY = "/proc"

    def __init__(self):
        self._logger = FSLogger.get_instance()
        self._app = FSApp.get_instance()

    @property
    def logger(self):
        return self._logger

    @property
    def app(self):
        return self._app
