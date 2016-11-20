import os
from PyQt5.QtCore import QThread, pyqtSignal

from model.fstreeitem import FSItemType, FSTreeItem


class FSFileScannerContext(object):
    """
    Context for passing arguments to the thread objects
    """
    def __init__(self, path, root):
        """
        :param path: the root path of the file scanning process
        """
        self.path = path
        self.root = root


class FSFileScannerTask(QThread):
    """
    File scanning task on a separate thread
    """
    notifyProgress = pyqtSignal(int)
    notifyFinish = pyqtSignal()
    notifyError = pyqtSignal(str)

    def __init__(self, parent=None, ctxt=None):
        """
        :param parent: parent object
        :param ctxt: context for passing arguments
        """
        super(QThread, self).__init__(parent)

        self._ctxt = ctxt
        self._stop_flag = False

    @property
    def stop_flag(self):
        return self._stop_flag

    @stop_flag.setter
    def stop_flag(self, value):
        self._stop_flag = value

    def run(self):
        assert isinstance(self._ctxt, FSFileScannerContext)

        if not os.path.isdir(self._ctxt.path):
            self.notifyError.emit("Wrong path!")

        extension_items = dict()

        file_count = 0

        for root, dirs, files in os.walk(self._ctxt.path):
            file_count += len(files)

        iter_count = 0

        for root, dirs, files in os.walk(self._ctxt.path):
            if self.stop_flag:
                break
            for file in files:
                if self.stop_flag:
                    break
                extension = os.path.splitext(file)[1]

                if extension not in extension_items.keys():
                    extension_items[extension] = FSTreeItem(extension, FSItemType.TYPE_EXTENSION, path=None, parent=self._ctxt.root)

                extension_item = extension_items[extension]
                tree_item = FSTreeItem(file, FSItemType.TYPE_FILE, path=os.path.join(root, file), parent=extension_item)

                iter_count += 1
                self.notifyProgress.emit(int((iter_count / file_count) * 100))

        self.notifyFinish.emit()
