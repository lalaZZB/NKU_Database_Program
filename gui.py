from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, QLineEdit, QApplication, \
    QDesktopWidget
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPixmap, QFont, QBrush
from db import Database
from widgets.query_player import QueryPlayer
from widgets.query_team import QueryTeam
from widgets.add_player import AddPlayer
from widgets.delete_match import DeleteMatch
from widgets.add_team import AddTeam
import sys

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Admin Login')
        self.setGeometry(100, 50, 1200, 800)
        self.center()

        layout = QVBoxLayout()

        # 设置背景图片
        self.setAutoFillBackground(True)
        palette = self.palette()
        pixmap = QPixmap("images/background.png")
        pixmap = pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        palette.setBrush(self.backgroundRole(), QBrush(pixmap))
        self.setPalette(palette)

        title_label = QLabel('CS赛事数据库管理系统登录', self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont('Arial', 28, QFont.Black))
        title_label.setStyleSheet("color: white;")
        layout.addWidget(title_label)

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText('管理员用户名')
        self.username_input.setFont(QFont('Arial', 12))
        self.username_input.setFixedSize(400, 50)
        layout.addWidget(self.username_input, alignment=Qt.AlignCenter)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText('密码')
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFont(QFont('Arial', 12))
        self.password_input.setFixedSize(400,50)
        layout.addWidget(self.password_input, alignment=Qt.AlignCenter)

        self.login_button = QPushButton('Login', self)
        self.login_button.setFont(QFont('Arial', 12))
        self.login_button.setFixedSize(200, 80)
        self.login_button.clicked.connect(self.handle_login)
        layout.addWidget(self.login_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if self.db.verify_admin(username, password):
            self.main_window = MainWindow()
            self.main_window.show()
            self.close()
        else:
            QMessageBox.warning(self, 'Error', 'Incorrect username or password')

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('CS赛事数据库管理系统')
        self.setGeometry(100, 50, 1200, 800)
        self.center()

        layout = QVBoxLayout()

        # 设置背景图片
        self.setAutoFillBackground(True)
        palette = self.palette()
        pixmap = QPixmap("images/background.png")  # 替换为你的背景图片路径
        pixmap = pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        palette.setBrush(self.backgroundRole(), QBrush(pixmap))
        self.setPalette(palette)

        title_label = QLabel('CS赛事数据库管理系统', self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont('Arial', 28, QFont.Black))
        title_label.setStyleSheet("color: white;")
        layout.addWidget(title_label)

        buttons_layout = QVBoxLayout()

        self.query_player_button = QPushButton('查询选手', self)
        self.query_player_button.setFont(QFont('Arial', 16))
        self.query_player_button.setFixedSize(250, 60)
        self.query_player_button.clicked.connect(self.show_query_player)
        buttons_layout.addWidget(self.query_player_button, alignment=Qt.AlignCenter)

        self.query_team_button = QPushButton('查询战队', self)
        self.query_team_button.setFont(QFont('Arial', 16))
        self.query_team_button.setFixedSize(250, 60)
        self.query_team_button.clicked.connect(self.show_query_team)
        buttons_layout.addWidget(self.query_team_button, alignment=Qt.AlignCenter)

        self.add_player_button = QPushButton('添加选手', self)
        self.add_player_button.setFont(QFont('Arial', 16))
        self.add_player_button.setFixedSize(250, 60)
        self.add_player_button.clicked.connect(self.show_add_player)
        buttons_layout.addWidget(self.add_player_button, alignment=Qt.AlignCenter)

        self.delete_match_button = QPushButton('删除比赛', self)
        self.delete_match_button.setFont(QFont('Arial', 16))
        self.delete_match_button.setFixedSize(250, 60)
        self.delete_match_button.clicked.connect(self.show_delete_match)
        buttons_layout.addWidget(self.delete_match_button, alignment=Qt.AlignCenter)

        self.add_team_button = QPushButton('添加战队', self)
        self.add_team_button.setFont(QFont('Arial', 16))
        self.add_team_button.setFixedSize(250, 60)
        self.add_team_button.clicked.connect(self.show_add_team)
        buttons_layout.addWidget(self.add_team_button, alignment=Qt.AlignCenter)

        layout.addLayout(buttons_layout)

        self.setLayout(layout)

    def show_query_player(self):
        self.query_player_window = QueryPlayer()
        self.query_player_window.show()
        self.query_player_window.center()

    def show_query_team(self):
        self.query_team_window = QueryTeam()
        self.query_team_window.show()
        self.query_team_window.center()

    def show_add_player(self):
        self.add_player_window = AddPlayer()
        self.add_player_window.show()
        self.add_player_window.center()

    def show_delete_match(self):
        self.delete_match_window = DeleteMatch()
        self.delete_match_window.show()
        self.delete_match_window.center()

    def show_add_team(self):
        self.add_team_window = AddTeam()
        self.add_team_window.show()
        self.add_team_window.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
