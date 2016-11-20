from PyQt5.Qt import QTableView, QSizePolicy, QMenu, Qt, QAction, QIcon, QCursor


class FSMovieTableWidget(QTableView):
    def __init__(self, parent=None):
        QTableView.__init__(self, parent)
