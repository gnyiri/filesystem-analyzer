import os
from PyQt5.QtCore import Qt
from PyQt5.Qt import QIcon, QVariant
from enum import Enum

from util.fsbase import FSBase
from util.fsapp import FSExtensionType


class FSTreeItem(FSBase):
    ATTRIBUTES = ["name", "count", "size (mb)", "path"]
    SIZE_DIVISOR = 1024 * 1024

    def __init__(self, name, extension_type=FSExtensionType.TYPE_FILE, path=None, parent=None):
        FSBase.__init__(self)

        self._name = name
        self._extension_type = extension_type
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
        return len(FSTreeItem.ATTRIBUTES)

    def data(self, column, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if column == 0:
                return self.name
            elif column == 1:
                return len(self.children)
            elif column == 2:
                return self.size / FSTreeItem.SIZE_DIVISOR
            elif column == 3:
                return self.path
            else:
                return str("n/a")
        elif role == Qt.DecorationRole:
            if column == 0:
                if self.extension_type == FSExtensionType.TYPE_EXT:
                    return QVariant(QIcon("res/list.svg"))
                else:
                    return QVariant(QIcon("res/office-material.svg"))

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
    def extension_type(self):
        return self._extension_type

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
