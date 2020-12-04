from PyQt5.QtWidgets import QWidget,QHBoxLayout,QVBoxLayout,QLabel,QPushButton,QListWidget,QGridLayout
from PyQt5.QtWidgets import QApplication

class history_search_result(QWidget):
    def __init__(self):
        super().__init__()
        self.init()

    def init(self):
        self.list = QListWidget()
        self.list.addItem("-----搜索-----")
        self.layout = QGridLayout()
        self.layout.addWidget(self.list,0,0,10,8)
        self.setLayout(self.layout)

    def show_data(self,result):
        print("开始显示...")
        if len(result) == 0:
            print('没有数据！')
            self.list.addItem("没有数据！")
            return
        for line in result:
            data = str(line[0]).strip()
            title = str(line[1]).strip()
            article = str(line[2]).strip()
            string = data+'\t'+title+"\t"+article
            self.list.addItem(string)
            # self.list.addLayout(self.list_view(data,title,article))
        QApplication.processEvents()
        print('显示完成')

    def list_view(self, data, title, article):
        label_data = QLabel(data)
        label_title = QLabel(title)
        label_article = QLabel(article)
        line = QHBoxLayout()
        line.addWidget(label_data)
        line.addWidget(label_title)
        line.addWidget(label_article)

        return line

    def clear_data(self):
        print('开始遍历: history_search_result.clear_data')
        count = self.list.count()
        print('遍历范围:',count)
        for i in range(count):
            self.list.takeItem(0)