import os

from PyQt5.QtCore import QAbstractItemModel, QVariant, QModelIndex, Qt

from .fs_treeitem import FS_TreeItem
from .fs_treeitem import FS_ItemType
from .fs_filemanager import FS_FileManager
from util.fs_base import FS_Base


class FS_FileTreeModel(QAbstractItemModel, FS_Base):
    """
    Encapsulates the Linux process hierarchy and acts as a model for the
    associated QTreeView
    """

    def __init__(self, parent=None, path=os.path.curdir):
        FS_Base.__init__(self)
        QAbstractItemModel.__init__(self, parent)

        self._path = path
        self._file_manager = FS_FileManager.get_instance()
        self._file_manager.path = path
        self._root = self._file_manager.items[0]

    @property
    def path(self):
        return self._file_manager.path

    @path.setter
    def path(self, value):
        self.beginResetModel()
        self._root = None
        self._file_manager.path = value
        self._root = self._file_manager.items[0]
        self.endResetModel()

    def columnCount(self, parent=None, *args, **kwargs):
        if parent.isValid():
            parent_item = parent.internalPointer()
            return parent_item.column_count()
        else:
            return self._root.column_count()

    def rowCount(self, parent=None, *args, **kwargs):
        if not parent or parent.column() > 0:
            return 0
        parent_item = parent.internalPointer() if parent.isValid() else self._root
        return parent_item.row_count()

    def data(self, index, role=None):
        item = index.internalPointer() if index.isValid() else self._root

        if role == Qt.DisplayRole:
            return item.data(index.column())
        elif role == Qt.DecorationRole:
            return QVariant()
        elif role == Qt.ToolTipRole:
            return QVariant()
        else:
            return QVariant()

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags
        return QAbstractItemModel.flags(self, index)

    def headerData(self, section, orientation, role=None):
        if (orientation, role) == (Qt.Horizontal, Qt.DisplayRole):
            if 0 <= section < len(FS_TreeItem.ATTRIBUTES):
                return FS_TreeItem.ATTRIBUTES[section]
        return QVariant()

    def index(self, row, column, parent=None):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()
        parent_item = parent.internalPointer() if parent.isValid() else self._root
        child_item = parent_item.child(row)
        index = self.createIndex(row, column, child_item) if child_item else QModelIndex()
        return index

    def parent(self, index=None):
        if not index.isValid():
            return QModelIndex()
        item = index.internalPointer()
        if not item:
            return QModelIndex()
        parent_item = item.parent
        if not parent_item:
            return QModelIndex()
        index = self.createIndex(parent_item.row(), 0, parent_item)
        return index