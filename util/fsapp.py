import threading
import os
from enum import Enum
from PyQt5.Qt import QApplication, QSettings

from .fslogger import FSLogger


class FSExtensionType(Enum):
    TYPE_EXT = 0
    TYPE_FILE = 1
    TYPE_MOVIE = 2
    TYPE_MUSIC = 3
    TYPE_IMAGE = 4


class FSApp(object):
    _INST_LOCK = threading.Lock()
    _INSTANCE = None

    ExtensionSettings = {FSExtensionType.TYPE_MOVIE: "MOVIE_EXTENSIONS",
                         FSExtensionType.TYPE_MUSIC: "MUSIC_EXTENSIONS",
                         FSExtensionType.TYPE_IMAGE: "IMAGE_EXTENSIONS"}

    @classmethod
    def get_instance(cls):
        """ Method for getting the only instance """
        if cls._INSTANCE is None:
            with cls._INST_LOCK:
                if cls._INSTANCE is None:
                    cls._INSTANCE = FSApp()
        assert cls._INSTANCE is not None
        return cls._INSTANCE

    def __new__(cls, *args, **kwargs):
        """ To make sure there will be only one instance """
        if not isinstance(cls._INSTANCE, cls):
            cls._INSTANCE = object.__new__(cls, *args, **kwargs)
        return cls._INSTANCE

    def __init__(self):
        self._logger = FSLogger.get_instance()
        self._settings_file = os.path.join("./", "config.ini")
        self._logger.info("Settings file: %s", self._settings_file)

    def save_setting(self, name, value):
        self._logger.info("Save setting %s -> %s", name, str(value))
        settings = QSettings(self._settings_file, QSettings.NativeFormat)
        settings.setValue(name, value)

    def load_setting(self, name):
        settings = QSettings(self._settings_file, QSettings.NativeFormat)
        value = settings.value(name, "")
        self._logger.info("Load setting %s -> %s", name, str(value))
        return value

    def extension_types(self):
        return self.ExtensionSettings.keys()

    def extension_setting_keys(self):
        return self.ExtensionSettings.values()
