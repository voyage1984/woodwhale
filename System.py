import inspect

from PyQt5.QtWidgets import QMessageBox

col_name = ['date','title','article']
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


def clear_data(self):
    print('开始遍历:',func_name())
    count = self.list.count()
    print('遍历范围:',count)
    for i in range(count):
        self.list.takeItem(0)


def dialog(self,title,main):
    print('显示弹窗',func_name())
    reply = QMessageBox.question(self, title,
                                 main, QMessageBox.Yes |
                                 QMessageBox.No, QMessageBox.No)

    if reply == QMessageBox.Yes:
        return True
    else:
        return False

def set_list(o_list,i_list):
    print('开始设置list',func_name())
    for line in i_list:
        # print(line[1].encode('latin-1', errors='ignore').decode('gbk', errors='ignore'))
        print(line[0])
        data = str(line[0]).strip()
        title = str(line[1].encode('latin-1').decode('gbk')).strip()
        article = str(line[2].encode('latin-1').decode('gbk')).strip()
        string = data + '\t' + title + '\t' + article
        o_list.addItem(string)

def get_item(item):
    result = item.text().split("\t")
    return result

def is_item(date):
    print('解析结果：',date)
    try:
        result = date.replace('-','')
        result = result.replace(':','')
        result = result.replace('.','')
        result = result.replace(' ','')
        print('result = ',result)
        if result.isdigit():
            print('数据对象：',date)
            return True
        else:
            print('非数据对象')
            return False
    except:
        print('发生了错误！',func_name())
        return False



if __name__ == '__main__':
    import MyDatabase
    db = MyDatabase.DBModel()
    db.conn(username,password)
    list = db.get_all_from_table('recommend')
    for i in list:
        print(i[0])
