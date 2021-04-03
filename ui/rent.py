from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLineEdit, QComboBox, QLabel

from MyDatabase import DBModel

import System

class rent(QWidget):
    count = 5
    borrow = 0

    def __init__(self):
        super().__init__()
        self.db = DBModel()
        self.init()

    def set_db(self,db):
        self.db = db

    def init(self):
        self.init_labels()
        self.user_menus = QComboBox()
        self.user_menus.setFixedSize(150, 35)
        self.user_menus.addItem("用户ID")
        self.user_menus.addItem("用户姓名")
        self.input_user = QLineEdit()
        self.btn_search_user = QPushButton("查询")
        layout_user = QHBoxLayout()
        layout_user.addWidget(self.user_menus)
        layout_user.addWidget(self.input_user)
        layout_user.addWidget(self.btn_search_user)

        layout_user_info = QVBoxLayout()
        layout_user_info.addWidget(self.user_id)
        layout_user_info.addWidget(self.user_name)
        layout_user_info.addWidget(self.rent_rest)

        self.book_info = QLineEdit()
        self.btn_search_book = QPushButton("查询图书")
        layout_book = QHBoxLayout()
        layout_book.addWidget(self.book_info)
        layout_book.addWidget(self.btn_search_book)

        layout_book_info = QVBoxLayout()
        layout_book_info.addWidget(self.book_id)
        layout_book_info.addWidget(self.book_name)
        layout_book_info.addWidget(self.book_num)
        layout_book_info.addWidget(self.book_rest)

        self.btn_rent = QPushButton("借出")
        self.btn_return = QPushButton("归还")
        layout_operation = QHBoxLayout()
        layout_operation.addWidget(self.btn_rent)
        layout_operation.addWidget(self.btn_return)

        layout = QVBoxLayout()
        layout.addLayout(layout_user)
        layout.addLayout(layout_user_info)
        layout.addLayout(layout_book)
        layout.addLayout(layout_book_info)
        layout.addLayout(layout_operation)
        self.setLayout(layout)
        self.init_btns()

    def init_labels(self):
        self.user_name = QLabel("用户姓名：")
        self.user_id = QLabel("用户ID：")
        self.rent_rest = QLabel("可借书数：")
        self.book_id = QLabel("图书ID：")
        self.book_name = QLabel("图书标题：")
        self.book_num = QLabel("索书号：")
        self.book_rest = QLabel("在库：")

    def init_btns(self):
        self.btn_search_user.clicked.connect(self.get_user)
        self.btn_search_book.clicked.connect(self.get_book)
        self.btn_rent.clicked.connect(self.rent_book)
        self.btn_return.clicked.connect(self.return_book)
        self.btn_search_book.setEnabled(0)
        self.btn_rent.setEnabled(0)
        self.btn_return.setEnabled(0)

    def get_user(self):
        self.count = 5
        print("开始查询")
        user = self.input_user.text()
        if len(user)==0:
            System.dialog(self,"错误!","用户信息不能为空值")
            return
        print("获取用户：",user)
        index = self.user_menus.currentIndex()
        print("获取索引：", index)

        if index == 0:
            col = "id"
        elif index == 1:
            col = "username"
        else:
            System.dialog(self,"发生了错误","获取索引出错:"+index)
            return
        userinfo = self.db.get_search_from_table(col,user,"userlist",1)
        if(len(userinfo)==0):
            System.dialog(self,"获取用户失败！","未查询到用户："+user)
            self.btn_search_book.setEnabled(0)
            return
        self.btn_search_book.setEnabled(1)
        self.userlist = []
        for item in userinfo[0]:
            print(item)
            self.userlist.append(str(item).strip())

        print("解析数据成功！")
        print("设置用户id：",self.userlist[0])
        self.user_id.setText("用户ID；"+self.userlist[0])
        print("设置用户姓名：", self.userlist[1])
        self.user_name.setText("用户姓名；"+self.userlist[1])
        for i in range(5,10):
            if(self.userlist[i]=='0'):
                pass
            else:
                self.count-=1

        print("设置可借书数：", self.count)
        self.rent_rest.setText("可借书数："+str(self.count))

    def get_book(self):
        book = self.book_info.text()
        if(len(book)==0):
            System.dialog(self,"错误！","图书id不能为空")
            return
        bookinfo = self.db.get_search_from_table(0,book,"booklist",1)
        if(len(bookinfo)==0):
            System.dialog(self,"错误！","获取图书失败！"+book)
            return
        self.booklist = []
        for item in bookinfo[0]:
            print(item)
            self.booklist.append(str(item).strip())
        self.book_id.setText("图书ID："+self.booklist[0])
        self.book_name.setText("图书标题："+self.booklist[1])
        self.book_num.setText("索书号："+self.booklist[9])
        self.book_rest.setText("在库："+self.booklist[7])
        self.set_opration_btns()

    def set_opration_btns(self):
        self.btn_return.setEnabled(0)
        self.btn_rent.setEnabled(0)
        self.count
        # 借书条件
        """如果书库存<=0或者用户可借书数<=0，不能借书"""
        if (int(self.booklist[7]) <= 0 or self.count<=0):
            self.btn_rent.setEnabled(0)
        else:
            self.btn_rent.setEnabled(1)
        """还书条件: 用户借阅表里有这本书"""
        for i in range(5,10):
            if self.booklist[0] == self.userlist[i]:
                print("图书："+self.booklist[0]+"已被此用户借阅")
                self.btn_return.setEnabled(1)
                self.borrow = i

    def rent_book(self):
        num = int(self.booklist[7])-1
        if(num<0):
            System.dialog(self, "借书失败！", "在库小于0！请联系管理员核实数据!")
            return
        for i in range(5, 10):
            if (self.userlist[i] == '0'):
                borrow = "borrow"+str(i-4)
                if self.db.update_table("userlist",borrow,self.booklist[0],"id",self.userlist[0]):
                    if self.db.update_table("booklist","rest",str(num),"id",self.booklist[0]):
                        System.dialog(self,"借出成功！","已借出："+self.userlist[1]+":"+self.booklist[1])
                        self.renew_labels()
                        return
                    else:
                        System.dialog(self, "更新在库失败！", "请联系管理员核查数据！")
                        return
                else:
                    System.dialog(self, "借书失败！", "请重试")
                    return

    def return_book(self):
        colName = "borrow"+str(self.borrow-4)
        rest = int(self.booklist[7])+1
        if rest > int(self.booklist[8]):
            System.dialog(self, "库存超过总数！", "请联系管理员核实数据")
            return

        if(self.db.update_table("userlist",colName,"0","id",self.userlist[0])):
            if(self.db.update_table("booklist","rest",str(rest),"id",self.booklist[0])):
                System.dialog(self,"还书成功！","用户："+self.userlist[1])
                self.renew_labels()
            else:
                System.dialog(self, "更新在库失败！", "请联系管理员核查数据！")
        else:
            System.dialog(self,"还书失败！","请重试")

    def renew_labels(self):
        self.user_name.setText("用户姓名：")
        self.user_id.setText("用户ID：")
        self.rent_rest.setText("可借书数：")
        self.book_id.setText("图书ID：")
        self.book_name.setText("图书标题：")
        self.book_num.setText("索书号：")
        self.book_rest.setText("在库：")
        self.btn_rent.setEnabled(0)
        self.btn_return.setEnabled(0)
        self.btn_search_book.setEnabled(0)