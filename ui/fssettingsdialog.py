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
        self.extension_inputs = list()
        for extension_setting_key in self.app.extension_setting_keys():
            extension_input = QLineEdit(self.app.load_setting(extension_setting_key))
            self.extension_inputs.append(extension_input)
            form_layout.addRow(extension_setting_key + ":", extension_input)

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.ok_clicked)
        layout.addLayout(form_layout)
        layout.addWidget(ok_button)
        self.setLayout(layout)

    def ok_clicked(self):
        for extension_input, extension_setting_key in zip(self.extension_inputs, self.app.extension_setting_keys()):
            self.app.save_setting(extension_setting_key, extension_input.text())
        self.close()
