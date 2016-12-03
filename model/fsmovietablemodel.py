from PyQt5.QtCore import QVariant, QAbstractTableModel, Qt, QModelIndex
from guessit import guessit


class FSMovie(object):
    def __init__(self, path):
        self.path = path
        self.title = str("n/a")
        self.year = str("n/a")
        self.type = str("n/a")
        self.url = str("n/a")

        self.update()

    def update(self):
        description = guessit(self.path)
        if description:
            if 'title' in description.keys():
                self.title = description['title']
            if 'year' in description.keys():
                self.year = description['year']
            if 'type' in description['type']:
                self.type = description['type']


class FSMovieTableModel(QAbstractTableModel):
    HEADERS = ["Title", "Year", "Type", "Url", "Path"]

    TITLE = 0
    YEAR = 1
    TYPE = 2
    URL = 3
    PATH = 4

    def __init__(self, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.movies = list()

    def rowCount(self, index=QModelIndex(), *arg, **kwargs):
        return len(self.movies)

    def columnCount(self, index=QModelIndex(), *arg, **kwargs):
        return len(FSMovieTableModel.HEADERS)

    def sort(self, column, Qt_SortOrder_order=None):
        if column == FSMovieTableModel.PATH:
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
            if column == FSMovieTableModel.TITLE:
                return QVariant(movie.title)
            elif column == FSMovieTableModel.YEAR:
                return QVariant(movie.year)
            elif column == FSMovieTableModel.TYPE:
                return QVariant(movie.type)
            elif column == FSMovieTableModel.URL:
                return QVariant(movie.url)
            elif column == FSMovieTableModel.PATH:
                return QVariant(movie.path)
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
