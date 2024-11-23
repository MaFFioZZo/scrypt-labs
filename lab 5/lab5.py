import asyncio
import sqlite3
import sys

import aiohttp
from PyQt5.QtCore import QThread, QTimer, pyqtSignal
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class DataLoader(QThread):
    data_loaded = pyqtSignal(list)

    def run(self):
        asyncio.run(self.load_data())

    async def load_data(self):
        try:
            #подключение
            async with aiohttp.ClientSession() as session:
                async with session.get("https://jsonplaceholder.typicode.com/posts") as response:
                    data = await response.json()
                    #задержка
                    await asyncio.sleep(3)
                    self.data_loaded.emit(data)
        except Exception as e:
            self.data_loaded.emit([])


class DataSaver(QThread):
    data_to_save = []
    progress_updated = pyqtSignal(int)
    save_finished = pyqtSignal()

    def run(self):
        asyncio.run(self.save_data())

    async def save_data(self):
        conn = sqlite3.connect("lab5.db")
        cursor = conn.cursor()
        #таблица
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY, 
                userID INTEGER,
                title TEXT, 
                body TEXT
            )
        """)
        conn.commit()

        total = len(self.data_to_save)
        #сохранение данных
        for i, post in enumerate(self.data_to_save, 1):
            cursor.execute(
                "INSERT OR REPLACE INTO posts (id, userID, title, body) VALUES (?, ?, ?, ?)",
                (post['id'], post['userId'], post['title'], post['body'])
            )
            conn.commit()
            
            #задержка в сохранении
            #await asyncio.sleep(0.1)
            
            self.progress_updated.emit(int((i / total) * 100))
        
        conn.close()
        self.save_finished.emit()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("lab5")
        self.resize(1500, 700)

        #флаги занятости
        self.is_loading = False
        self.is_saving = False

        #основной интерфейс
        self.layout = QVBoxLayout()
        self.load_button = QPushButton("Загрузить данные")
        self.progress_bar = QProgressBar()
        self.status_label = QLabel("Статус: Ожидание комнады")
        self.table_widget = QTableWidget()
        self.table_widget.verticalHeader().setVisible(False)

        self.layout.addWidget(self.load_button)
        self.layout.addWidget(self.progress_bar)
        self.layout.addWidget(self.status_label)
        self.layout.addWidget(self.table_widget)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        #подключение сигналов и таймеров
        self.load_button.clicked.connect(self.start_data_loading)

        #потоки для работы с данными
        self.loader_thread = None
        self.saver_thread = None

    def start_data_loading(self):
        if self.is_loading or self.is_saving:
            self.status_label.setText("Статус: Операция уже выполняется")
            return

        self.status_label.setText("Статус: Загрузка данных...")
        self.progress_bar.setValue(0)

        self.is_loading = True
        self.loader_thread = DataLoader()
        self.loader_thread.data_loaded.connect(self.handle_data_loaded)
        self.loader_thread.finished.connect(self.reset_loading_flag)
        self.loader_thread.start()

    def reset_loading_flag(self):
        self.is_loading = False

    def handle_data_loaded(self, data):
        if not data:
            self.status_label.setText("Ошибка: не удалось загрузить данные")
            return

        self.status_label.setText("Статус: Сохранение данных...")
        self.saver_thread = DataSaver()
        self.saver_thread.data_to_save = data
        self.saver_thread.progress_updated.connect(self.progress_bar.setValue)
        self.saver_thread.save_finished.connect(self.handle_save_finished)
        self.saver_thread.finished.connect(self.reset_saving_flag)

        self.is_saving = True
        self.saver_thread.start()

    def reset_saving_flag(self):
        self.is_saving = False

    def handle_save_finished(self):
        #задержка проверки обновления
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_for_updates)
        self.timer.start(10000)
        
        self.status_label.setText("Статус: Данные успешно сохранены")
        self.update_table_widget()

    def update_table_widget(self):
        conn = sqlite3.connect("lab5.db")
        cursor = conn.cursor()
        cursor.execute("SELECT userID, id, title, body FROM posts")
        rows = cursor.fetchall()
        conn.close()

        self.table_widget.setRowCount(len(rows))
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(["User ID", "ID", "Title", "Body"])

        #заполнение таблицы
        for row_idx, row_data in enumerate(rows):
            for col_idx, value in enumerate(row_data):
                self.table_widget.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

        self.table_widget.resizeColumnsToContents()

    def check_for_updates(self):
        if not self.is_loading and not self.is_saving:
            self.status_label.setText("Статус: Проверка обновлений...")
            self.start_data_loading()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


main()
