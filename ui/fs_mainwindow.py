from PyQt5.Qt import QMainWindow, QAction, QFileDialog, QIcon, QProgressBar, QModelIndex

from task.FS_FileScannerTask import FS_FileScannerTask, FS_FileScannerCtxt
from .fs_filetreewidget import FS_FileTreeWidget
from util.fs_base import FS_Base
from model.fs_filetreemodel import FS_FileTreeModel


class FS_MainWindow(QMainWindow, FS_Base):
    """
    Main Window
    """
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
        toolbar = self.addToolBar("Exit")
        toolbar.addAction(set_path_action)

        self.progressbar = QProgressBar(self)
        self.progressbar.hide()
        self.progressbar.setRange(0, 100)

        self.statusBar().addPermanentWidget(self.progressbar)

        self.file_tree_widget = FS_FileTreeWidget(self)
        self.file_tree_model = FS_FileTreeModel(self)
        self.file_tree_widget.setModel(self.file_tree_model)
        self.setCentralWidget(self.file_tree_widget)
        self.show()

    def set_path_action_handler(self):
        file_dialog = QFileDialog()
        path = file_dialog.getExistingDirectory(self, "Select directory", "/home/", QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        self.logger.info("Path set to %s", path)

        self.progressbar.show()

        self.file_tree_model.reset_root()
        file_scanner_ctxt = FS_FileScannerCtxt(path, self.file_tree_model.root)
        file_scanner_thread = FS_FileScannerTask(self, file_scanner_ctxt)
        file_scanner_thread.notifyProgress.connect(self.update_progress)
        file_scanner_thread.notifyFinish.connect(self.set_path_action_finish)
        file_scanner_thread.start()

    def set_path_action_finish(self):
        self.progressbar.hide()
        self.file_tree_model.reset_model()
        self.file_tree_widget.setColumnWidth(0, 150)

    def update_progress(self, value):
        self.progressbar.setValue(value)
