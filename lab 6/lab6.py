import sys

import pandas as pd
import seaborn as sns
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class DataVisualizerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("lab6")
        self.setGeometry(100, 100, 800, 600)

        self.data = None
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout()
        self.main_widget.setLayout(self.layout)

        #загрузка табилцы
        self.load_button = QPushButton("Загрузить CSV", self)
        self.load_button.clicked.connect(self.load_data)
        self.layout.addWidget(self.load_button)

        #статистика
        self.stats_label = QLabel("Статистика: данные не загружены")
        self.layout.addWidget(self.stats_label)

        #выбор графика
        self.chart_type = QComboBox(self)
        self.chart_type.addItems(["Линейный график", "Гистограмма", "Круговая диаграмма"])
        self.layout.addWidget(self.chart_type)

        #построение графика
        self.plot_button = QPushButton("Построить график", self)
        self.plot_button.clicked.connect(self.plot_graph)
        self.layout.addWidget(self.plot_button)

        #ввод данных вручную
        self.add_data_layout = QHBoxLayout()
        self.new_data_input = QLineEdit(self)
        self.new_data_input.setPlaceholderText("Введите новые значения...")
        self.add_data_layout.addWidget(self.new_data_input)
        self.add_button = QPushButton("Добавить данные", self)
        self.add_button.clicked.connect(self.add_data)
        self.add_data_layout.addWidget(self.add_button)
        self.layout.addLayout(self.add_data_layout)

        #поле для графика
        self.canvas = FigureCanvas(Figure(figsize=(5, 3)))
        self.layout.addWidget(self.canvas)
        self.ax = self.canvas.figure.add_subplot(111)

    #загрузка файла
    def load_data(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Выберите CSV файл", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if file_name:
            self.data = pd.read_csv(file_name)
            self.update_stats()

    #обновление статистики
    def update_stats(self):
        if self.data is not None:
            stats = f"Статистика:\nКоличество строк: {self.data.shape[0]}\nКоличество столбцов: {self.data.shape[1]}"
            for col in self.data.columns:
                stats += f"\n{col}: мин={self.data[col].min()}, макс={self.data[col].max()}" if pd.api.types.is_numeric_dtype(self.data[col]) else ""
            self.stats_label.setText(stats)

    #построение графика
    def plot_graph(self):
        if self.data is None:
            self.stats_label.setText("Сначала загрузите данные!")
            return

        chart_type = self.chart_type.currentText()
        self.ax.clear()

        if chart_type == "Линейный график":
            sns.lineplot(data=self.data, x="Date", y="Value1", ax=self.ax)
            self.ax.set_title("Линейный график: Date, Value1")
            self.ax.set_xlabel("Date")
            self.ax.set_ylabel("Value1")
        elif chart_type == "Гистограмма":
            sns.barplot(data=self.data, x="Date", y="Value2", ax=self.ax)
            self.ax.set_title("Гистограмма: Date, Value2")
            self.ax.set_xlabel("Date")
            self.ax.set_ylabel("Value2")
        elif chart_type == "Круговая диаграмма":
            self.data["Category"].value_counts().plot.pie(ax=self.ax, autopct='%1.1f%%')
            self.ax.set_xlabel("")
            self.ax.set_ylabel("")
            self.ax.set_title("Круговая диаграмма: Category")

        if chart_type != "Круговая диаграмма":
            self.ax.set_aspect("auto")

        self.canvas.draw()
        self.update_stats()

    #добавление данных вручную
    def add_data(self):
        if self.data is None:
            self.stats_label.setText("Сначала загрузите данные!")
            return

        new_data = self.new_data_input.text()
        if not new_data.strip():
            self.stats_label.setText("Введите данные в формате: Date,Category,Value1,Value2,BooleanFlag")
            return

        try:
            #2023-01-01,A,123,123.123,True
            new_row = new_data.split(",")
            if len(new_row) != 5:
                raise ValueError("Введите данные в формате: Date,Category,Value1,Value2,BooleanFlag")

            new_row_dict = {
                "Date": new_row[0].strip(),
                "Category": new_row[1].strip(),
                "Value1": int(new_row[2].strip()),
                "Value2": float(new_row[3].strip()),
                "BooleanFlag": new_row[4].strip().lower() in ["true", "1", "yes"]
            }

            self.data = pd.concat([self.data, pd.DataFrame([new_row_dict])], ignore_index=True)
            self.update_stats()
            self.plot_graph()

            self.new_data_input.clear()
            self.stats_label.setText("Новая строка успешно добавлена!")
        except Exception as e:
            self.stats_label.setText(f"Ошибка добавления данных: {str(e)}")


def main():
    app = QApplication(sys.argv)
    main_window = DataVisualizerApp()
    main_window.show()
    sys.exit(app.exec_())

main()