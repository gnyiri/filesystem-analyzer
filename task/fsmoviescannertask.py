import os
from PyQt5.QtCore import QThread, pyqtSignal

from model.fsmovietablemodel import FSMovie


class FSMovieScannerContext(object):
    """
    Context for passing arguments to the thread objects
    """
    def __init__(self, path, movies):
        """
        :param path: the root path of the movie scanning process
        """
        self.path = path
        self.movies = movies


class FSMovieScannerTask(QThread):
    """
    File scanning task on a separate thread
    """
    notifyProgress = pyqtSignal(int)
    notifyFinish = pyqtSignal()
    notifyError = pyqtSignal(str)

    def __init__(self, parent=None, context=None):
        """
        :param parent: parent object
        :param context: context for passing arguments
        """
        super(QThread, self).__init__(parent)

        self._context = context
        self._stop_flag = False

    @property
    def stop_flag(self):
        return self._stop_flag

    @stop_flag.setter
    def stop_flag(self, value):
        self._stop_flag = value

    def run(self):
        assert isinstance(self._context, FSMovieScannerContext)

        if not os.path.isdir(self._context.path):
            self.notifyError.emit("Wrong path!")

        file_count = 0

        for root, dirs, files in os.walk(self._context.path):
            file_count += len(files)

        iter_count = 0

        for root, dirs, files in os.walk(self._context.path):
            if self.stop_flag:
                break
            for file in files:
                if self.stop_flag:
                    break
                extension = os.path.splitext(file)[1]

                iter_count += 1
                self._context.movies.append(FSMovie(file, os.path.join(root, file), "title", "url"))
                self.notifyProgress.emit(int((iter_count / file_count) * 100))

        self.notifyFinish.emit()
