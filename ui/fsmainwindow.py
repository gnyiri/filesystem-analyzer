from PyQt5.Qt import QMainWindow, QAction, QFileDialog, QIcon, QProgressBar, QPushButton, QTabWidget

from util.fsapp import FSApp
from task.fsfilescannertask import FSFileScannerTask, FSFileScannerContext
from .fsfiletreewidget import FSFileTreeWidget
from util.fsbase import FSBase
from model.fs_filetreemodel import FS_FileTreeModel


class FSMainWindow(QMainWindow, FSBase):
    """
    Main Window
    """
    def __init__(self):
        QMainWindow.__init__(self)
        FSBase.__init__(self)

        self.progressbar = None
        self.tab_widget = None
        self.file_tree_widget = None
        self.file_tree_model = None
        self.file_scanner_thread = None

        self.build_ui()
        self.build_content()

    def build_ui(self):
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

        cancel_button = QPushButton(QIcon("res/cancel-button.svg"), "Cancel", self)
        cancel_button.clicked.connect(self.set_path_cancel)

        self.statusBar().addPermanentWidget(self.progressbar)
        self.statusBar().addPermanentWidget(cancel_button)

        self.tab_widget = QTabWidget(self)

        self.file_tree_widget = FSFileTreeWidget()
        self.file_tree_model = FS_FileTreeModel()
        self.file_tree_widget.setModel(self.file_tree_model)
        self.tab_widget.addTab(self.file_tree_widget, "General")
        self.setCentralWidget(self.tab_widget)
        self.show()

    def build_content(self):
        path = self.app.load_setting("path")
        self.set_path(path)

    def set_path_action_handler(self):
        file_dialog = QFileDialog()
        path = file_dialog.getExistingDirectory(self, "Select directory", "/home/", QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        self.logger.info("Path set to %s", path)
        self.set_path(path)
        self.app.save_setting("path", path)

    def set_path(self, path):
        self.progressbar.show()
        self.file_tree_model.reset_root()
        file_scanner_ctxt = FSFileScannerContext(path, self.file_tree_model.root)
        self.file_scanner_thread = FSFileScannerTask(self, file_scanner_ctxt)
        self.file_scanner_thread.notifyProgress.connect(self.update_progress)
        self.file_scanner_thread.notifyFinish.connect(self.set_path_action_finish)
        self.file_scanner_thread.notifyError.connect(self.report_error)
        self.file_scanner_thread.start()

    def set_path_action_finish(self):
        self.progressbar.hide()
        self.file_tree_model.reset_model()
        self.file_tree_widget.setColumnWidth(0, 250)

    def set_path_cancel(self):
        self.file_scanner_thread.stop_flag = True

    def update_progress(self, value):
        self.progressbar.setValue(value)

    def report_error(self, error):
        print(error)
