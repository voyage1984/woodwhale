import inspect

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QMessageBox, QListWidgetItem
from ui.model import listmodel
from ui.model import historymodel
from ui.model import bookmodel

col_name = (['date','title','article'],['id','title','author'])
db_name  = 'PyQt5_db'
username = 'testuser'
password = 'password'

def parsing(list,code):
    try:
        i = list.split(code)
    except Exception as e:
        print(e)
        return ""
    return i

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

def set_historylist(o_list,i_list,col1,col2,col3):
    print('开始设置list',func_name())
    list = []
    set_historyitem(o_list,col1,col2,col3)
    for line in i_list:
        data = str(line[0]).strip()
        title = str(line[1].encode('latin-1').decode('gbk')).strip()
        article = str(line[2].encode('latin-1').decode('gbk')).strip()
        set_historyitem(o_list, data, title, article)


def set_historyitem(o_list,col1,col2,col3):
    model = historymodel.historymodel(col1,col2,col3)
    myitem = QListWidgetItem()
    myitem.setSizeHint(QSize(200, 50))
    o_list.addItem(myitem)
    o_list.setItemWidget(myitem, model)

def set_recommendlist(o_list,i_list,col1,col2,col3):
    print('开始设置list', func_name())
    list = []
    set_recommenditem(o_list,col1,col2,col3)
    for line in i_list:
        id = str(line[0]).strip()
        list.append(id)
        title = str(line[1].encode('latin-1').decode('gbk')).strip()
        author =str(line[2].encode('latin-1').decode('gbk')).strip()
        set_recommenditem(o_list,id,title,author)
    return list

def set_recommenditem(o_list,col1,col2,col3):
    model = listmodel.listmodel(col1,col2,col3)
    myitem = QListWidgetItem()
    myitem.setSizeHint(QSize(200, 50))
    o_list.addItem(myitem)
    o_list.setItemWidget(myitem, model)

def set_book_list(o_list,i_list):
    print('开始设置list', func_name())
    list = []
    set_bookitem(o_list,"编号","标题","作者","出版社","出版日","索书号")
    for line in i_list:
        id = str(line[0]).strip()
        list.append(id)
        title = str(line[1]).strip()
        author =str(line[2]).strip()
        company = str(line[3]).strip()
        publish = str(line[4]).strip()
        booknum = str(line[9]).strip()
        set_bookitem(o_list,id,title,author,company,publish,booknum)
    return list

def set_bookitem(o_list,col1,col2,col3,col4,col5,col6):
    model = bookmodel.bookmodel(col1,col2,col3,col4,col5,col6)
    myitem = QListWidgetItem()
    myitem.setSizeHint(QSize(200, 50))
    o_list.addItem(myitem)
    o_list.setItemWidget(myitem, model)

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

def parsingdate(date):
    return int(date.replace("-",""))



if __name__ == '__main__':
    import MyDatabase
    db = MyDatabase.DBModel()
    db.conn(username,password)
    list = db.get_all_from_table('recommend')
    for i in list:
        print(i[0])
