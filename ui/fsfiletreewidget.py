from PyQt5.Qt import QTreeView, QSizePolicy, QMenu, Qt, QAction, QIcon, QCursor


class FSFileTreeWidget(QTreeView):
    def __init__(self, parent=None):
        QTreeView.__init__(self, parent)

        self.setMinimumWidth(1100)
        self.setMinimumHeight(500)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.setSelectionMode(QTreeView.ExtendedSelection)
        self.setSelectionBehavior(QTreeView.SelectRows)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.setAlternatingRowColors(True)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def current_item(self):
        current_index = self.currentIndex()
        if not current_index or not current_index.isValid():
            return None
        return current_index.internalPointer()

    def show_context_menu(self):
        menu = QMenu(self)
        item = self.current_item()

        if not item:
            return

        actions = list()
        file_menu = menu.addMenu(QIcon("res/delete.svg"), "File operations")
        delete_action = QAction(QIcon("res/delete.svg"), "Delete", file_menu)
        actions.append(delete_action)
        file_menu.addActions(actions)
        file_menu.setEnabled(True)
        menu.setEnabled(True)
        action = menu.exec_(QCursor.pos())
