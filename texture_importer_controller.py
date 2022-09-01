import sys
from datetime import datetime

from PySide2.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, \
                              QGroupBox, QFileDialog, QMessageBox, QTextEdit
from directory_selector_widget import DirectorySelectorWidget
from ibutton import IButton
from texture_importer_lib import TextureImporterLib


class TextureImporterController(QDialog):
    """Manage the core of the tool for execute it main function of import texture files."""

    def __init__(self, parent=None):
        super(TextureImporterController, self).__init__(parent)

        self.types = ['COL', 'SPEC', 'OPAC', 'DISP', 'REFL', 'ROUGH', 'MASK', 'MATTE', 'NORM', 'OCC']
        self.extensions = ['exr', 'tif', 'tx', 'txt']

        self._setup_ui()
        self._initialize()

    def _setup_ui(self):
        """Build the UI of tool."""

        self.setWindowTitle("Texture Importer")
        self.setFixedSize(700, 270)

        self._main_layout = QVBoxLayout(self)
        self._tab_actions = QTabWidget()
        self._tab_actions.setStyleSheet("font-size: 9pt")

        self._directory_layout = QVBoxLayout()
        self._directory_group = QGroupBox()

        self._source_directory_widget = DirectorySelectorWidget(button_text='Source..')
        self._destination_directory_widget = DirectorySelectorWidget(button_text='Destination...')

        self._directory_layout.addLayout(self._source_directory_widget)
        self._directory_layout.addLayout(self._destination_directory_widget)

        self._directory_group.setLayout(self._directory_layout)

        self._log_layout = QVBoxLayout()
        self._log_group = QGroupBox()

        self._log_text_edit = QTextEdit()
        self._log_text_edit.setReadOnly(True)
        self._log_layout.addWidget(self._log_text_edit)
        self._log_group.setLayout(self._log_layout)

        self._button_layout = QHBoxLayout()

        self._import_button = IButton(button_text='Import textures')
        self._clean_button = IButton(button_text='Clean fields')

        self._button_layout.addWidget(self._clean_button)
        self._button_layout.addWidget(self._import_button)

        self._tab_actions.insertTab(0, self._directory_group, '  Directories  ')
        self._tab_actions.insertTab(1, self._log_group, '    Log    ')

        self._main_layout.addWidget(self._tab_actions)
        self._main_layout.addLayout(self._button_layout)

    def _initialize(self):
        """Connect the UI elements with their functionality."""

        self._source_directory_widget.ActionButton.clicked.connect(lambda: self._get_directory(directory_widget= self._source_directory_widget))
        self._destination_directory_widget.ActionButton.clicked.connect(lambda: self._get_directory(directory_widget= self._destination_directory_widget))

        self._clean_button.clicked.connect(self._clean_fields)
        self._import_button.clicked.connect(self._import_textures)

    def _get_directory(self, directory_widget):
        """Open and explorer window and get a directory selected in the system."""

        selected_directory = QFileDialog.getExistingDirectory()
        directory_widget.DirectoryLabel.setText(selected_directory)

    def _clean_fields(self):
        """Clean all fields that are fill with data during using of tool."""

        self._source_directory_widget.DirectoryLabel.setText('')
        self._destination_directory_widget.DirectoryLabel.setText('')
        self._log_text_edit.clear()

    def _import_textures(self):
        """ Manage whole process of texture import since validations, copy process and evaluation of the result."""

        log_msg = '{} :: {}\n'.format(str(datetime.now()), 'Starting import texture process...')

        source_directory = self._source_directory_widget.DirectoryLabel.text()
        destination_directory = self._destination_directory_widget.DirectoryLabel.text()

        # Launching the process of validation and import.
        result, files_counter, log_msg = TextureImporterLib.analyzing_input_data(source_directory=source_directory,
                                                                                 destination_directory=destination_directory,
                                                                                 extensions=self.extensions,
                                                                                 types=self.types,
                                                                                 log_msg=log_msg)

        # Set log info.
        self._log_text_edit.setPlainText(log_msg)

        # Result popup window for user.
        self._result_popup_message(result=result, files_counter=files_counter)

    def _result_popup_message(self, result, files_counter):
        """Evaluate two result variables got of texture importer process and show an interpreted message for user."""

        if len(result) > 0:
            message = '{} files have been copied successfully.\n'.format(str(len(result)))
        else:
            message = 'Files not copied. Maybe invalid files found.\nReview log info.'

        if files_counter == len(result) and files_counter > 0:
            message += 'All files have been copied.'
            self._popup_messagebox(message=message)

        elif files_counter != len(result) and len(result) > 0:
            message += 'Not all files have been copied.\nReview log info.'
            self._popup_messagebox(message=message, icon=QMessageBox.Warning)

        else:
            self._popup_messagebox(message=message, icon=QMessageBox.Critical)

    def _popup_messagebox(self, message='', icon=QMessageBox.Information):
        """Build a popup message box for user."""

        context_data_msgBox = QMessageBox()
        context_data_msgBox.setText(message)
        context_data_msgBox.setIcon(icon)
        context_data_msgBox.exec_()


if __name__ == "__main__":

    app = QApplication(sys.argv)
    texture_importer = TextureImporterController()
    texture_importer.show()
    sys.exit(app.exec_())
