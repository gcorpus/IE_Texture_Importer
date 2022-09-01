from PySide2.QtWidgets import QPushButton


class IButton(QPushButton):
    def __init__(self, parent=None, button_text=''):
        super(IButton, self).__init__(parent=parent)

        self._button_text = button_text

        self._setup_ui()

    def _setup_ui(self):

        self.setText(self._button_text)
        self.setStyleSheet("font-size: 9pt")
        self.setMinimumWidth(90)

