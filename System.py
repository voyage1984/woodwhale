import inspect

from PyQt5.QtWidgets import QMessageBox

table_list = ['date','title','article']
db_name  = 'PyQt5_db'
username = 'testuser'
password = 'password'

def func_name():
    funcname = ": "+inspect.stack()[1][3]
    return funcname

def get_username(name):
    username = str(name)
    result = username.split('\'')[1]
    return result


def dialog(self,title,main):
    print('显示弹窗',func_name())
    reply = QMessageBox.question(self, title,
                                 main, QMessageBox.Yes |
                                 QMessageBox.No, QMessageBox.No)

    if reply == QMessageBox.Yes:
        return True
    else:
        return False


if __name__ == '__main__':
    import MyDatabase
    db = MyDatabase.DBModel()
    db.conn(username,password)
