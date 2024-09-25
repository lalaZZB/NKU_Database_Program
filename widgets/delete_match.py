import mysql
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox, QListWidget, QLabel, \
    QDesktopWidget
from db import Database

class DeleteMatch(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('删除比赛')
        self.setGeometry(200, 100, 400, 400)

        self.layout = QVBoxLayout()

        self.form_layout = QFormLayout()
        self.team_name = QLineEdit()
        self.organizer_name = QLineEdit()
        self.form_layout.addRow('战队名称:', self.team_name)
        self.form_layout.addRow('赛事主办方名称:', self.organizer_name)
        self.layout.addLayout(self.form_layout)

        self.query_button = QPushButton('查询比赛', self)
        self.query_button.clicked.connect(self.query_matches)
        self.layout.addWidget(self.query_button)

        self.results_list = QListWidget()
        self.layout.addWidget(self.results_list)

        self.confirm_delete_button = QPushButton('确定删除比赛', self)
        self.confirm_delete_button.setEnabled(False)
        self.confirm_delete_button.clicked.connect(self.delete_matches)
        self.layout.addWidget(self.confirm_delete_button)

        self.setLayout(self.layout)

    def query_matches(self):
        team_name = self.team_name.text()
        organizer_name = self.organizer_name.text()

        if not (team_name and organizer_name):
            QMessageBox.warning(self, '错误', '所有字段均为必填项')
            return

        self.results_list.clear()

        try:
            self.db.cursor.execute("""
                SELECT match_name FROM matches 
                WHERE organizer_name=%s 
                AND match_name IN (SELECT match_name FROM participations WHERE team_name=%s)
            """, (organizer_name, team_name))
            matches = self.db.cursor.fetchall()

            if matches:
                for match in matches:
                    self.results_list.addItem(f'比赛名称: {match[0]}')
                self.confirm_delete_button.setEnabled(True)
            else:
                QMessageBox.information(self, '结果', '未找到相关比赛记录')
                self.confirm_delete_button.setEnabled(False)

        except mysql.connector.Error as err:
            QMessageBox.warning(self, '错误', f'查询比赛失败: {err}')
            self.confirm_delete_button.setEnabled(False)

    def delete_matches(self):
        team_name = self.team_name.text()
        organizer_name = self.organizer_name.text()

        if not (team_name and organizer_name):
            QMessageBox.warning(self, '错误', '所有字段均为必填项')
            return

        try:
            # 确保之前的事务已经提交或回滚
            self.db.commit_transaction()

            # 开启新的事务
            self.db.start_transaction()

            # 删除参赛记录
            self.db.cursor.execute("""
                DELETE FROM participations 
                WHERE match_name IN (
                    SELECT match_name FROM matches WHERE organizer_name=%s
                )
                AND team_name=%s
            """, (organizer_name, team_name))

            # 提交事务
            self.db.commit_transaction()
            QMessageBox.information(self, '成功', '参赛记录删除成功')
            self.results_list.clear()
            self.confirm_delete_button.setEnabled(False)
        except mysql.connector.Error as err:
            self.db.rollback_transaction()
            QMessageBox.warning(self, '错误', f'删除参赛记录失败: {err}')
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())