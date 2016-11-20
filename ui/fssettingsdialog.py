from PyQt5.Qt import QDialog, QFormLayout, QCheckBox, QLineEdit, QPushButton, QVBoxLayout

from util.fsapp import FSApp


class FSSettingsDialog(QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.app = FSApp.get_instance()

        self.setWindowTitle("Settings")
        self.setMinimumHeight(200)
        self.setMinimumWidth(450)

        layout = QVBoxLayout(self)
        form_layout = QFormLayout()
        self.movie_extensions = QLineEdit(self.app.load_setting("MOVIE_EXTENSIONS"))
        form_layout.addRow("Movie extensions: ", self.movie_extensions)
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.ok_clicked)
        layout.addLayout(form_layout)
        layout.addWidget(ok_button)
        self.setLayout(layout)

    def ok_clicked(self):
        self.app.save_setting("MOVIE_EXTENSIONS", self.movie_extensions.text())
        self.close()
