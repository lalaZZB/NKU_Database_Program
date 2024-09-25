import mysql
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox, QDesktopWidget
from db import Database

class AddTeam(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('添加战队')
        self.setGeometry(200, 100, 400, 300)

        layout = QVBoxLayout()

        form_layout = QFormLayout()

        self.team_name = QLineEdit()
        self.location = QLineEdit()
        self.world_ranking = QLineEdit()
        self.coach_name = QLineEdit()
        self.honors = QLineEdit()

        form_layout.addRow('战队名称:', self.team_name)
        form_layout.addRow('战队所属地:', self.location)
        form_layout.addRow('世界排名:', self.world_ranking)
        form_layout.addRow('教练:', self.coach_name)
        form_layout.addRow('荣誉:', self.honors)

        layout.addLayout(form_layout)

        self.add_button = QPushButton('添加战队', self)
        self.add_button.clicked.connect(self.add_team)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def add_team(self):
        team_name = self.team_name.text()
        location = self.location.text()
        world_ranking = self.world_ranking.text()
        coach_name = self.coach_name.text()
        honors = self.honors.text()

        if not (team_name and location and world_ranking and coach_name and honors):
            QMessageBox.warning(self, '错误', '所有字段均为必填项')
            return

        try:
            self.db.cursor.execute("""
                INSERT INTO teams (team_name, location, world_ranking, coach_name, honors)
                VALUES (%s, %s, %s, %s, %s)
            """, (team_name, location, world_ranking, coach_name, honors))
            self.db.conn.commit()
            QMessageBox.information(self, '成功', '战队添加成功')
        except mysql.connector.Error as err:
            QMessageBox.warning(self, '错误', f'添加战队失败: {err}')
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())