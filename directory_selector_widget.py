import sys
from PySide2.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel
from ibutton import IButton


class DirectorySelectorWidget(QVBoxLayout):
    def __init__(self, parent=None, button_text=''):
        super(DirectorySelectorWidget, self).__init__(parent=parent)

        self._button_text = button_text

        self._setup_ui()

    @property
    def DirectoryLabel(self):
        return self._directory_label

    @property
    def ActionButton(self):
        return self._action_button

    def _setup_ui(self):

        self._button_layout = QHBoxLayout()

        self._action_button = IButton(button_text=self._button_text)
        self._button_layout.addWidget(self._action_button)
        self._button_layout.addStretch()

        self._directory_label = QLabel('')

        self.addLayout(self._button_layout)
        self.addWidget(self._directory_label)
        self.addStretch()




