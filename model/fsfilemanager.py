import threading
import os
from PyQt5.QtCore import QThread

from util.fslogger import FSLogger
from model.fstreeitem import FSTreeItem, FSExtensionType
from task.fsfilescannertask import FSFileScannerContext, FSFileScannerTask


class FSFileManager(object):
    _INST_LOCK = threading.Lock()
    _INSTANCE = None

    @classmethod
    def get_instance(cls):
        """ Method for getting the only instance """
        if cls._INSTANCE is None:
            with cls._INST_LOCK:
                if cls._INSTANCE is None:
                    cls._INSTANCE = FSFileManager()
        assert cls._INSTANCE is not None
        return cls._INSTANCE

    def __new__(cls, *args, **kwargs):
        """ To make sure there will be only one instance """
        if not isinstance(cls._INSTANCE, cls):
            cls._INSTANCE = object.__new__(cls, *args, **kwargs)
        return cls._INSTANCE

    def __init__(self):
        self._logger = FSLogger.get_instance()
        self._path = "."
        self._items = list()

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        assert os.path.isdir(value)
        self._path = value
        self.update()

    @property
    def items(self):
        return self._items

    def update(self):
        self._logger.info("Launch thread ..")
        update_thread = threading.Thread(target=self.update_w)
        update_thread.start()
        self._logger.info("Done")

    def update_w(self):
        self._logger.info("Scanning files in %s", self.path)

        self.items.clear()

        extension_items = dict()

        root_item = FSTreeItem("Extensions", FSExtensionType.TYPE_EXTENSION, path=None, parent=None)

        self.items.append(root_item)

        for root, dirs, files in os.walk(self.path):
            for file in files:
                extension = os.path.splitext(file)[1]

                if extension not in extension_items.keys():
                    extension_items[extension] = FSTreeItem(extension, FSExtensionType.TYPE_EXTENSION, path=None,
                                                            parent=root_item)

                extension_item = extension_items[extension]
                self.items.append(
                    FSTreeItem(file, FSExtensionType.TYPE_FILE, path=os.path.join(root, file), parent=extension_item))

        self._logger.info("%d items found", len(self.items))
