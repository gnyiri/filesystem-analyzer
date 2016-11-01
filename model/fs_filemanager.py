import threading
import os

from util.fs_logger import FS_Logger
from model.fs_treeitem import FS_TreeItem, FS_ItemType


class FS_FileManager(object):
    _INST_LOCK = threading.Lock()
    _INSTANCE = None

    @classmethod
    def get_instance(cls):
        """ Method for getting the only instance """
        if cls._INSTANCE is None:
            with cls._INST_LOCK:
                if cls._INSTANCE is None:
                    cls._INSTANCE = FS_FileManager()
        assert cls._INSTANCE is not None
        return cls._INSTANCE

    def __new__(cls, *args, **kwargs):
        """ To make sure there will be only one instance """
        if not isinstance(cls._INSTANCE, cls):
            cls._INSTANCE = object.__new__(cls, *args, **kwargs)
        return cls._INSTANCE

    def __init__(self):
        self._logger = FS_Logger.get_instance()
        self._path = "."
        self._items = list()
        self.update()

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
        self._logger.info("Scanning files in %s", self.path)

        self.items.clear()

        extension_items = dict()

        root_item = FS_TreeItem("Extensions", FS_ItemType.TYPE_EXTENSION, path=None, parent=None)

        self.items.append(root_item)

        for root, dirs, files in os.walk(self.path):
            for file in files:
                extension = os.path.splitext(file)[1]

                if extension not in extension_items.keys():
                    extension_items[extension] = FS_TreeItem(extension, FS_ItemType.TYPE_EXTENSION, path=None,
                                                             parent=root_item)

                extension_item = extension_items[extension]
                self.items.append(
                    FS_TreeItem(file, FS_ItemType.TYPE_FILE, path=os.path.join(root, file), parent=extension_item))

        self._logger.info("%d items found", len(self.items))
