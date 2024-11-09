import sqlite3
import sys

from PyQt5.QtCore import (
    QAbstractTableModel,
    QModelIndex,
    Qt,
)
from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QFormLayout,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
)


class DatabaseModel(QAbstractTableModel):
    def __init__(self, data):
        super(DatabaseModel, self).__init__()
        self._data = data
        self.headers = ["User ID", "ID", "Title", "Body"]

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]
        return None

    def rowCount(self, index=QModelIndex()):
        return len(self._data)

    def columnCount(self, index=QModelIndex()):
        return len(self.headers)

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.headers[section]
        return None

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("lab 4")
        self.setGeometry(100, 100, 1024, 768)

        #Подключение к базе данных
        self.con = sqlite3.connect("lab4.db")
        self.cur = self.con.cursor()

        #Отрисовка интерфейса
        self.table_view = QTableView()
        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("Поиск в таблице")
        self.search_field.textChanged.connect(self.search)

        self.refresh_button = QPushButton("Обновить")
        self.refresh_button.clicked.connect(self.load_data)

        self.add_button = QPushButton("Добавить")
        self.add_button.clicked.connect(self.add_record)

        self.delete_button = QPushButton("Удалить")
        self.delete_button.clicked.connect(self.delete_record)

        layout = QVBoxLayout()
        layout.addWidget(self.search_field)
        layout.addWidget(self.table_view)
        layout.addWidget(self.refresh_button)
        layout.addWidget(self.add_button)
        layout.addWidget(self.delete_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.load_data()

    def load_data(self):
        self.cur.execute("SELECT * FROM posts")
        rows = self.cur.fetchall()
        self.model = DatabaseModel(rows)
        self.table_view.setModel(self.model)

    def search(self):
        search_text = self.search_field.text()
        query = "SELECT * FROM posts WHERE title LIKE ?"
        self.cur.execute(query, ('%' + search_text + '%',))
        rows = self.cur.fetchall()
        self.model = DatabaseModel(rows)
        self.table_view.setModel(self.model)

    def add_record(self):
        dialog = AddRecordDialog(self.con)
        if dialog.exec_() == QDialog.Accepted:
            self.load_data()

    def delete_record(self):
        selected_index = self.table_view.selectionModel().currentIndex()
        if not selected_index.isValid():
            QMessageBox.warning(self, "Внимание!", "Выберите элемент для удаления.")
            return

        record_id = self.model.data(self.model.index(selected_index.row(), 1), Qt.DisplayRole)
        reply = QMessageBox.question(self, "Удалить?", f"Вы точно хотите удалить элемент №{record_id}?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.cur.execute("DELETE FROM posts WHERE id = ?", (record_id,))
            self.con.commit()
            self.load_data()

class AddRecordDialog(QDialog):
    def __init__(self, connection):
        super(AddRecordDialog, self).__init__()
        self.con = connection
        self.cur = self.con.cursor()

        self.setWindowTitle("Добавить запись")
        self.layout = QFormLayout()

        self.user_id_input = QLineEdit()
        self.title_input = QLineEdit()
        self.body_input = QLineEdit()

        self.layout.addRow("User ID:", self.user_id_input)
        self.layout.addRow("Title:", self.title_input)
        self.layout.addRow("Body:", self.body_input)

        self.add_button = QPushButton("Добавить")
        self.add_button.clicked.connect(self.add_record)
        self.layout.addWidget(self.add_button)

        self.setLayout(self.layout)

    def add_record(self):
        user_id = self.user_id_input.text()
        title = self.title_input.text()
        body = self.body_input.text()

        if not user_id or not title or not body:
            QMessageBox.warning(self, "Внимание!", "Все поля должны быть заполнены.")
            return

        self.cur.execute("SELECT MAX(id) FROM posts")
        max_id = self.cur.fetchone()[0]
        self.cur.execute("INSERT INTO posts (user_id, id, title, body) VALUES (?, ?, ?, ?)", (user_id, max_id + 1, title, body))
        self.con.commit()
        self.accept()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    
main()