from PyQt5.Qt import QMainWindow, QAction, QFileDialog, QIcon

from .fs_filetreewidget import FS_FileTreeWidget
from util.fs_base import FS_Base
from model.fs_filetreemodel import FS_FileTreeModel


class FS_MainWindow(QMainWindow, FS_Base):

    def __init__(self):
        QMainWindow.__init__(self)
        FS_Base.__init__(self)

        self.setWindowTitle("Filesystem Analyzer")

        set_path_action = QAction(QIcon("res/directory-submission-symbol.svg"), "Set path", self)
        set_path_action.setShortcut("Ctrl+N")
        set_path_action.triggered.connect(self.set_path_action_handler)

        menu_bar = self.menuBar()
        action_menu = menu_bar.addMenu("&Action")
        action_menu.addAction(set_path_action)
        self.toolbar = self.addToolBar("Exit")
        self.toolbar.addAction(set_path_action)

        self.file_tree_widget = FS_FileTreeWidget(self)
        self.file_tree_model = FS_FileTreeModel(self)
        # self.process_tree_model = PM_ProcessTreeModel(self)
        # self.process_tree_widget.setModel(self.process_tree_model)
        self.file_tree_widget.setModel(self.file_tree_model)
        self.setCentralWidget(self.file_tree_widget)
        self.show()

    def set_path_action_handler(self):
        file_dialog = QFileDialog()
        path = file_dialog.getExistingDirectory(self, "Select directory", "/home/", QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        self.logger.debug("Path set to %s", path)
        self.file_tree_model.path = path