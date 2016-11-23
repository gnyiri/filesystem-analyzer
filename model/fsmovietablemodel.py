from PyQt5.QtCore import QVariant, QAbstractTableModel, Qt, QModelIndex


class FSMovie(object):
    def __init__(self, file, path, title=None, url=None):
        self.file = file
        self.path = path
        self.title = title
        self.url = url


class FSMovieTableModel(QAbstractTableModel):
    HEADERS = ["File", "Path", "Title", "Url"]
    FILE = 0
    PATH = 1
    TITLE = 2
    URL = 3

    def __init__(self, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.movies = list()

    def rowCount(self, index=QModelIndex(), *arg, **kwargs):
        return len(self.movies)

    def columnCount(self, index=QModelIndex(), *arg, **kwargs):
        return len(FSMovieTableModel.HEADERS)

    def sort(self, column, Qt_SortOrder_order=None):
        if column == FSMovieTableModel.FILE:
            self.movies = sorted(self.movies, key=lambda movie: movie.filename)
        elif column == FSMovieTableModel.PATH:
            self.movies = sorted(self.movies, key=lambda movie: movie.path)
        elif column == FSMovieTableModel.TITLE:
            self.movies = sorted(self.movies, key=lambda movie: movie.title)
        elif column == FSMovieTableModel.URL:
            self.movies = sorted(self.movies, key=lambda movie: movie.url)
        self.reset()

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self.movies)):
            return QVariant()
        movie = self.movies[index.row()]
        column = index.column()
        if role == Qt.DisplayRole:
            if column == FSMovieTableModel.FILE:
                return QVariant(movie.file)
            elif column == FSMovieTableModel.PATH:
                return QVariant(movie.path)
            elif column == FSMovieTableModel.TITLE:
                return QVariant(movie.title)
            elif column == FSMovieTableModel.URL:
                return QVariant(movie.url)
        return QVariant()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:
                return QVariant(int(Qt.AlignLeft | Qt.AlignVCenter))
            return QVariant(int(Qt.AlignRight | Qt.AlignVCenter))
        if role != Qt.DisplayRole:
            return QVariant()
        if orientation == Qt.Horizontal:
            return QVariant(FSMovieTableModel.HEADERS[section])
        else:
            return QVariant(int(section + 1))

    def add_movie(self, movie):
        self.beginInsertRows(QModelIndex(), 0, 1)
        self.movies.append(movie)
        self.endInsertRows()

    def reset_model(self):
        self.modelReset.emit()
