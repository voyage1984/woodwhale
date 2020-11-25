from PyQt5.QtWidgets import QWidget,QLabel,QVBoxLayout

class recommend(QWidget):
    def __init__(self):
        super().__init__()
        self.init()

    def init(self):
        label = QLabel("今日推荐")
        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)