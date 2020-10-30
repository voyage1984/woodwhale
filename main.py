import sys
from PyQt5.QtWidgets import QApplication

import Login

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login = Login.LoginWindow()
    login.show()
    sys.exit(app.exec_())
