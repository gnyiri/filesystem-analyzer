import os
from enum import Enum

from util.fs_base import FS_Base


class FS_ItemType(Enum):
    TYPE_EXTENSION = 1
    TYPE_FILE = 2


class FS_TreeItem(FS_Base):
    ATTRIBUTES = ["name", "count", "size (mb)", "path"]
    SIZE_DIVISOR = 1024 * 1024

    def __init__(self, name, item_type, path=None, parent=None):
        FS_Base.__init__(self)

        self._name = name
        self._item_type = item_type
        self._parent = parent
        if self._parent:
            self._parent.append_child(self)
        self._size = 0
        self._path = path
        self._children = list()

        if self._path:
            try:
                stat = os.stat(self._path)
                self._size = stat.st_size
            except Exception as e:
                self.logger.exception(e)
                return

        # self.logger.debug("Created item %s, %s", name, path)

    @property
    def parent(self):
        return self._parent

    @property
    def children(self):
        return self._children

    def child(self, index):
        return self.children[index] if 0 <= index < len(self.children) else None

    def row_count(self):
        return len(self.children)

    def column_count(self):
        return len(FS_TreeItem.ATTRIBUTES)

    def data(self, column):
        if column == 0:
            return self.name
        elif column == 1:
            return len(self.children)
        elif column == 2:
            return self.size / FS_TreeItem.SIZE_DIVISOR
        elif column == 3:
            return self.path
        else:
            return str("n/a")

    def append_child(self, child):
        assert child
        self.children.append(child)

    def row(self, child=None):
        if not child:
            if self._parent:
                return self.parent.children.index(self)
            return 0
        else:
            if child in self.children:
                return self.children.index(child)
            return 0

    @property
    def item_type(self):
        return self._item_type

    @property
    def name(self):
        return self._name

    @property
    def size(self):
        size = self._size
        for child in self._children:
            size += child.size
        return size

    @property
    def path(self):
        return self._path
