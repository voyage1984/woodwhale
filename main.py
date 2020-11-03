import sys
from PyQt5.QtWidgets import QApplication

from ui.home import Ui_home as Home


if __name__ == '__main__':
    app = QApplication(sys.argv)

    home = Home()
    home.show()

    sys.exit(app.exec_())
