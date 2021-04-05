from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFrame, QStackedLayout, QLabel, QLineEdit, \
    QComboBox, QTextEdit, QListView

from MyDatabase import DBModel
import System

class user_manage(QWidget):
    def __init__(self):
        super().__init__()
        self.db = DBModel()
        self.init()

    def setdb(self,db):
        self.db = db

    def init(self):
        self.left()
        self.right()
        self.setConnect()
        layout = QHBoxLayout()
        layout.addLayout(self.l_layout)
        layout.addLayout(self.r_layout)
        self.setLayout(layout)

    def setConnect(self):
        self.search_btn.clicked.connect(self.search_user)
        self.pswd_btn.clicked.connect(self.change_pswd)
        self.cancel_btn.clicked.connect(self.cancel_user)

    def search_user(self):
        self.pswd_btn.setEnabled(0)
        self.cancel_btn.setEnabled(0)
        user = self.input.text()
        print("查询用户"+user)
        if(len(user)==0):
            System.dialog(self,"错误！","请输入查询用户")
            return
        index = self.menus.currentIndex()
        print("获得索引："+str(index))
        col = ""
        if index == 0:
            col += "id"
        else:
            col += "username"
        userinfo = self.db.get_search_from_table(col,user,"userlist",1)
        if(len(userinfo)==0):
            System.dialog(self,"错误！","未查询到用户："+user)
            return
        print(userinfo)
        self.userlist = []
        for item in userinfo[0]:
            print(item)
            self.userlist.append(str(item).strip())

        print("解析数据成功！")
        self.count = 5
        sex = ""
        for i in range(5, 10):
            if (self.userlist[i] == '0'):
                pass
            else:
                self.count -= 1
        if self.count == 5:
            self.cancel_btn.setEnabled(1)
        self.pswd_btn.setEnabled(1)
        if self.userlist[4]=='1':
            sex = "男"
        else:
            sex = "女"

        self.id.setText(self.userlist[0])
        self.name.setText(self.userlist[1])
        self.sex.setText(sex)
        self.birthday.setText(self.userlist[3])
        self.rent.setText(str(self.count))

    def change_pswd(self):
        id = self.userlist[0]
        pswd1 = self.pswd1_input.text()
        pswd2 = self.pswd2_input.text()
        if(pswd1!=pswd2):
            System.dialog(self,"错误！","两次密码不匹配")
            return
        elif len(pswd2)==0:
            System.dialog(self, "错误！", "密码不能为空")
            return
        if(self.db.update_table("userlist","pswd",pswd1,"id",id)):
            System.dialog(self,"成功","更新密码成功！")
            self.pswd2_input.setText("")
            self.pswd1_input.setText("")
            return
        else:
            System.dialog(self,"失败!","更新密码失败！")
            return

    def cancel_user(self):
        id = self.userlist[0]
        self.cancel_btn.setEnabled(0)
        self.pswd_btn.setEnabled(0)
        if(System.dialog(self,"确认注销?","此操作无法撤销！")):
            if(self.db.delete_data("userlist","id",id)):
                System.dialog(self,"注销成功！","已注销用户："+id)
                self.userlist = None
                self.id.setText("")
                self.name.setText("")
                self.sex.setText("")
                self.birthday.setText("")
                self.rent.setText("")
                return

    """布局：左，图片+用户信息"""
    def left(self):
        self.l_layout = QVBoxLayout()
        self.label_pic = QLabel(self)
        self.l_layout.setContentsMargins(20,20,0,0)
        self.label_pic.setPixmap(QPixmap('./src/boy.jpg'))
        self.label_pic.setFixedSize(300, 300)
        self.l_layout.setAlignment(Qt.AlignTop)
        self.l_layout.addWidget(self.label_pic)
        self.labels()

    """布局：左，用户信息"""
    def labels(self):
        label_user = QLabel("用户信息:")
        label_user.setFont(QFont("Microsoft YaHei",12,QFont.Black))
        label_id = QLabel("ID:")
        label_name = QLabel("姓名:")
        label_sex = QLabel("性别:")
        label_birthday = QLabel("生日:")
        label_rent = QLabel("可借阅:")
        label_id.setFixedSize(50,25)
        label_id.setFont(QFont("NSimSun", 10, QFont.Black))
        label_name.setFixedSize(50,25)
        label_name.setFont(QFont("NSimSun", 10, QFont.Black))
        label_sex.setFixedSize(50,25)
        label_sex.setFont(QFont("NSimSun", 10, QFont.Black))
        label_birthday.setFixedSize(50,25)
        label_birthday.setFont(QFont("NSimSun", 10, QFont.Black))
        label_rent.setFixedSize(50,25)
        label_rent.setFont(QFont("NSimSun", 10, QFont.Black))
        self.id = QLabel("")
        self.name = QLabel("")
        self.sex = QLabel("")
        self.birthday = QLabel("")
        self.rent = QLabel("")
        
        id_line = QHBoxLayout()
        id_line.addWidget(label_id)
        id_line.addWidget(self.id)
        id_line.setContentsMargins(0,10,0,0)

        name_line = QHBoxLayout()
        name_line.addWidget(label_name)
        name_line.addWidget(self.name)
        name_line.setContentsMargins(0,10,0,0)

        sex_line = QHBoxLayout()
        sex_line.addWidget(label_sex)
        sex_line.addWidget(self.sex)
        sex_line.setContentsMargins(0,10,0,0)

        birthday_line = QHBoxLayout()
        birthday_line.addWidget(label_birthday)
        birthday_line.addWidget(self.birthday)
        birthday_line.setContentsMargins(0,10,0,0)

        rent_line = QHBoxLayout()
        rent_line.addWidget(label_rent)
        rent_line.addWidget(self.rent)
        rent_line.setContentsMargins(0,10,0,10)
        
        labels = QVBoxLayout()
        labels.addWidget(label_user)
        labels.addLayout(id_line)
        labels.addLayout(name_line)
        labels.addLayout(sex_line)
        labels.addLayout(birthday_line)
        labels.addLayout(sex_line)
        labels.addLayout(rent_line)

        self.l_layout.addLayout(labels)

    """布局：右"""
    def right(self):
        self.r_layout = QVBoxLayout()
        self.r_layout.setAlignment(Qt.AlignTop)
        self.r_layout.setSpacing(40)
        self.search_line()
        self.pswd_line()
        self.btn_line()
        self.info_line()
        self.pswd_btn.setEnabled(0)
        self.cancel_btn.setEnabled(0)

    """布局：右，搜索栏"""
    def search_line(self):
        self.menus = QComboBox()
        self.menus.setView(QListView())
        self.menus.setStyleSheet("QComboBox QAbstractItemView::item {min-height: 25px;}")
        self.menus.setFixedSize(50, 35)
        self.menus.addItem("ID")
        self.menus.addItem("姓名")
        self.input = QLineEdit()
        self.input.setFont(QFont("NSimSun", 12, QFont.Black))
        self.input.setFixedSize(400,35)
        self.search_btn = QPushButton("搜索")
        self.search_btn.setFixedSize(60,35)
        firstline = QHBoxLayout()
        firstline.addWidget(self.menus)
        firstline.addWidget(self.input)
        firstline.addWidget(self.search_btn)
        firstline.setAlignment(Qt.AlignLeft)
        firstline.setContentsMargins(0,70,0,0)
        self.r_layout.addLayout(firstline)

    """布局：右，按钮栏"""
    def btn_line(self):
        self.pswd_btn = QPushButton("修改密码")
        self.cancel_btn = QPushButton("注销账户")
        self.pswd_btn.setFixedSize(100,40)
        self.cancel_btn.setFixedSize(100,40)
        line = QHBoxLayout()
        # line.setContentsMargins(0,10,0,10)
        line.setAlignment(Qt.AlignLeft)
        line.addWidget(self.pswd_btn)
        line.addWidget(self.cancel_btn)
        self.r_layout.addLayout(line)

    """布局：右，提示栏"""
    def info_line(self):
        info = QLabel()
        # info.setAlignment(Qt.AlignTop)
        infomation = """注意：
            在这里进行的操作都无法撤销，请谨慎操作
        """
        info.setStyleSheet("background:transparent;border:2px solid black;")
        info.setText(infomation)
        info.setFixedSize(500,100)
        info.setFont(QFont("Microsoft YaHei",12,QFont.Black))
        self.r_layout.addWidget(info)

    """布局：右，密码"""
    def pswd_line(self):
        pswd1_label = QLabel("新密码:")
        pswd2_label = QLabel("新密码:")
        pswd1_label.setFont(QFont("",12,QFont.Black))
        pswd2_label.setFont(QFont("",12,QFont.Black))
        pswd1_label.setFixedSize(50,35)
        pswd2_label.setFixedSize(50,35)
        self.pswd1_input = QLineEdit()
        self.pswd2_input = QLineEdit()
        self.pswd1_input.setFixedSize(400,35)
        self.pswd2_input.setFixedSize(400,35)
        pswd1_line = QHBoxLayout()
        pswd2_line = QHBoxLayout()
        pswd1_line.addWidget(pswd1_label)
        pswd1_line.addWidget(self.pswd1_input)
        pswd2_line.addWidget(pswd2_label)
        pswd2_line.addWidget(self.pswd2_input)
        pswd1_line.setAlignment(Qt.AlignLeft)
        pswd2_line.setAlignment(Qt.AlignLeft)
        pswd_line = QVBoxLayout()
        pswd_line.setAlignment(Qt.AlignLeft)
        pswd_line.addLayout(pswd1_line)
        pswd_line.addLayout(pswd2_line)
        self.r_layout.addLayout(pswd_line)

