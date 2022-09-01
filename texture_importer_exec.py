import sys
from PySide2.QtWidgets import QApplication
from PySide2.QtGui import QIcon
from texture_importer_controller import TextureImporterController

# Build the app and execute the tool from controller.
app = QApplication(sys.argv)
texture_importer = TextureImporterController()
app.setWindowIcon(QIcon("texture_importer_icon.ico"))
texture_importer.show()
sys.exit(app.exec_())