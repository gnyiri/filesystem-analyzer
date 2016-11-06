import os

from PyQt5.QtCore import QAbstractItemModel, QVariant, QModelIndex, Qt

from .fs_treeitem import FS_TreeItem, FS_ItemType

from util.fs_base import FS_Base


class FS_FileTreeModel(QAbstractItemModel, FS_Base):
    """
    Encapsulates the file extension/file hierarchy as a model for the
    associated QTreeView
    """

    def __init__(self, parent=None):
        FS_Base.__init__(self)
        QAbstractItemModel.__init__(self, parent)

        self._root = None

    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, value):
        self._root = value

    def reset_root(self):
        self.root = FS_TreeItem("Extensions", FS_ItemType.TYPE_EXTENSION, path=None, parent=None)

    def reset_model(self):
        self.logger.info("Refresh tree")
        self.modelReset.emit()

    def columnCount(self, parent=None, *args, **kwargs):
        if not self._root:
            return 0
        if parent.isValid():
            parent_item = parent.internalPointer()
            return parent_item.column_count()
        else:
            return self._root.column_count()

    def rowCount(self, parent=None, *args, **kwargs):
        if not self._root:
            return 0
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