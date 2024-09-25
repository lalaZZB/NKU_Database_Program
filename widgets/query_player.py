import mysql.connector
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QMessageBox, QDesktopWidget, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtGui import QPalette, QBrush, QPixmap
from db import Database

class QueryPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('查询选手')
        self.setGeometry(100, 50, 1200, 800)  # Increase the window size

        # Set background image
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap("images/players.png")))
        self.setPalette(palette)

        layout = QVBoxLayout()

        form_layout = QVBoxLayout()

        self.player_name = QLineEdit()
        self.player_name.setPlaceholderText('请输入选手姓名')
        self.player_name.setFixedSize(200, 45)  # Set fixed size
        form_layout.addWidget(self.player_name)

        self.query_by_name_button = QPushButton('根据姓名查询', self)
        self.query_by_name_button.setFixedSize(200, 45)  # Set fixed size
        self.query_by_name_button.clicked.connect(self.query_player_by_name)
        form_layout.addWidget(self.query_by_name_button)

        self.team_name = QLineEdit()
        self.team_name.setPlaceholderText('请输入战队名称')
        self.team_name.setFixedSize(200, 45)  # Set fixed size
        form_layout.addWidget(self.team_name)

        self.query_by_team_button = QPushButton('根据战队查询', self)
        self.query_by_team_button.setFixedSize(200, 45)  # Set fixed size
        self.query_by_team_button.clicked.connect(self.query_players_by_team)
        form_layout.addWidget(self.query_by_team_button)

        # Center the form layout
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addLayout(form_layout)
        hbox.addStretch(1)

        layout.addLayout(hbox)

        self.result_table = QTableWidget()
        self.result_table.setColumnCount(6)
        self.result_table.setHorizontalHeaderLabels(['战队名称', '号码', '姓名', '出生日期', '国籍', '位置'])
        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.result_table.setFixedSize(900, 450)  # Set fixed size
        result_hbox = QHBoxLayout()
        result_hbox.addStretch(1)
        result_hbox.addWidget(self.result_table)
        result_hbox.addStretch(1)

        layout.addLayout(result_hbox)

        self.setLayout(layout)

    def query_player_by_name(self):
        player_name = self.player_name.text()
        if not player_name:
            QMessageBox.warning(self, '错误', '请输入选手姓名')
            return

        try:
            self.db.cursor.execute("SELECT * FROM players WHERE name=%s", (player_name,))
            player = self.db.cursor.fetchone()
            self.result_table.setRowCount(1)
            if player:
                for col, data in enumerate(player):
                    self.result_table.setItem(0, col, QTableWidgetItem(str(data)))
            else:
                QMessageBox.warning(self, '错误', '选手不存在')
                self.result_table.setRowCount(0)
        except mysql.connector.Error as err:
            QMessageBox.warning(self, '错误', f'查询失败: {err}')

    def query_players_by_team(self):
        team_name = self.team_name.text()
        if not team_name:
            QMessageBox.warning(self, '错误', '请输入战队名称')
            return

        try:
            self.db.cursor.execute("SELECT * FROM team_players WHERE team_name=%s", (team_name,))
            players = self.db.cursor.fetchall()
            if players:
                self.result_table.setRowCount(len(players))
                for row, player in enumerate(players):
                    for col, data in enumerate(player):
                        self.result_table.setItem(row, col, QTableWidgetItem(str(data)))
            else:
                QMessageBox.warning(self, '错误', '该战队下没有选手')
                self.result_table.setRowCount(0)
        except mysql.connector.Error as err:
            QMessageBox.warning(self, '错误', f'查询失败: {err}')

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
