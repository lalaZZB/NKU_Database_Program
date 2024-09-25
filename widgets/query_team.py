import mysql.connector
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QMessageBox, QInputDialog, QDesktopWidget, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtGui import QPalette, QBrush, QPixmap
from db import Database

class QueryTeam(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('查询战队')
        self.setGeometry(100, 50, 1200, 800)  # Increase the window size

        # Set background image
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap("images/teams.png")))
        self.setPalette(palette)

        layout = QVBoxLayout()

        form_layout = QVBoxLayout()

        self.team_name = QLineEdit()
        self.team_name.setPlaceholderText('请输入战队名称')
        self.team_name.setFixedSize(200, 45)  # Set fixed size
        form_layout.addWidget(self.team_name)

        self.query_button = QPushButton('查询战队', self)
        self.query_button.setFixedSize(200, 45)  # Set fixed size
        self.query_button.clicked.connect(self.query_team)
        form_layout.addWidget(self.query_button)

        self.modify_win_rate_button = QPushButton('修改胜率', self)
        self.modify_win_rate_button.setFixedSize(200, 45)  # Set fixed size
        self.modify_win_rate_button.clicked.connect(self.modify_win_rate)
        form_layout.addWidget(self.modify_win_rate_button)

        # Center the form layout
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addLayout(form_layout)
        hbox.addStretch(1)

        layout.addLayout(hbox)

        self.result_table = QTableWidget()
        self.result_table.setColumnCount(6)
        self.result_table.setHorizontalHeaderLabels(['战队名称', '所属地', '世界排名', '教练', '荣誉', '近期胜率'])
        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.result_table.setFixedSize(900, 450)  # Set fixed size
        result_hbox = QHBoxLayout()
        result_hbox.addStretch(1)
        result_hbox.addWidget(self.result_table)
        result_hbox.addStretch(1)

        layout.addLayout(result_hbox)

        self.setLayout(layout)

    def query_team(self):
        team_name = self.team_name.text()
        if not team_name:
            QMessageBox.warning(self, '错误', '请输入战队名称')
            return

        try:
            self.db.cursor.execute("SELECT * FROM teams WHERE team_name=%s", (team_name,))
            team = self.db.cursor.fetchone()
            self.result_table.setRowCount(1)
            if team:
                for col, data in enumerate(team):
                    self.result_table.setItem(0, col, QTableWidgetItem(str(data)))
            else:
                QMessageBox.warning(self, '错误', '战队不存在')
                self.result_table.setRowCount(0)
        except mysql.connector.Error as err:
            QMessageBox.warning(self, '错误', f'查询失败: {err}')

    def modify_win_rate(self):
        team_name = self.team_name.text()
        new_rate, ok = QInputDialog.getDouble(self, '修改胜率', '请输入新的胜率:', 0, -999, 999, 2)
        if ok:
            try:
                self.db.cursor.callproc('update_win_rate', [team_name, new_rate])
                self.db.conn.commit()
                QMessageBox.information(self, '成功', '胜率修改成功')
            except mysql.connector.Error as err:
                QMessageBox.warning(self, '错误', f'修改胜率失败: {err}')

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
