from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QTableWidget, QTableWidgetItem, QLabel, QProgressBar, QGroupBox
from PyQt5.QtCore import QSize
from  PyQt5.QtGui import QColor
from multiprocessing import Process, Value, Array
import pandas as pd
from time import sleep
import json

TANKS = pd.read_csv("data/assets/tanks.csv")
MAPS = pd.read_csv("data/assets/maps.csv")
MAPS = MAPS[MAPS.standart]

# Наследуемся от QMainWindow
class MainWindow(QMainWindow):
    # Переопределяем конструктор класса
    def __init__(self):
        # Обязательно нужно вызвать метод супер класса
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(1200, 600))             # Устанавливаем размеры
        # Устанавливаем заголовок окна
        self.setWindowTitle("WRParser GUI")
        # Создаём центральный виджет
        central_widget = QWidget(self)
        # Устанавливаем центральный виджет
        self.setCentralWidget(central_widget)

        grid_layout = QGridLayout()             # Создаём QGridLayout
        # Устанавливаем данное размещение в центральный виджет
        central_widget.setLayout(grid_layout)

        groupBox = QGroupBox("Threads")

        grid_layout_labels = QGridLayout()
        self.labels = []
        for i in range(12):
            label = QLabel(f"{i+1}:")
            self.labels.append(label)
            grid_layout_labels.addWidget(label, i % 4, i // 4)
        groupBox.setLayout(grid_layout_labels)
        grid_layout.addWidget(groupBox, 0, 0)

        self.tanks = TANKS
        self.maps = MAPS

        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(len(self.tanks) * len(self.maps))
        self.progress_bar.setFormat("%v/%m | %p%")
        self.progress_bar.setValue(0)
        grid_layout.addWidget(self.progress_bar, 1, 0)

        self.table = QTableWidget(self)  # Создаём таблицу
        # Устанавливаем колонки
        self.table.setColumnCount(len(self.maps) + 3)
        self.table.setRowCount(len(self.tanks))        # и строки в таблице

        # Устанавливаем заголовки таблицы
        self.columns = ["tank", "thread", "replays"] + \
            list(self.maps.work_name)
        self.table.setHorizontalHeaderLabels(self.columns)

        # заполняем первую строку
        self.tanks_list = list(self.tanks.tag)
        for c in range(self.table.columnCount()):
            for r in range(self.table.rowCount()):
                self.table.setItem(r, c, QTableWidgetItem(""))
        for i, tag in enumerate(self.tanks_list):
            self.table.setItem(i, 0, QTableWidgetItem(tag))

        # item.setBackground(QtGui.QColor(200, 255, 200))

        # делаем ресайз колонок по содержимому
        self.table.resizeColumnsToContents()

        grid_layout.addWidget(self.table, 2, 0)   # Добавляем таблицу в сетку

        
    
    def closeEvent(self, event):
        self.hide()
        save_obj = {}
        save_obj["progress_bar"] = self.progress_bar.value()
        table = []
        for c in range(self.table.columnCount()):
            for r in range(self.table.rowCount()):
                item = self.table.item(r, c)
                table.append({
                    "column": c,
                    "row": r,
                    "value": item.text(),
                    "bg": item.background().color().getRgb()
                })
        save_obj.update({"table": table})
        with open("data/logs/status.json", "w") as f:
            json.dump(save_obj, f)

        self.stop.value = 1
        for i in self.processes:
            i.join()
            print(i.name, "joined")

    def load_settings(self):
        with open("data/logs/status.json", "r") as f:
            save_obj = json.load(f)
        self.progress_bar.setValue(save_obj["progress_bar"])
        for i in save_obj["table"]:
            item = QTableWidgetItem(i["value"])
            color = QColor(*i["bg"])
            if color.getRgb() == (0,0,0,255):
                color = QColor(255, 255, 255, 255)
            item.setBackground(color)
            self.table.setItem(i["row"], i["column"], item)

    def startProcess(self, num):
        self.stop = Value("i", 0)
        self.cur_tank = Value("i", 0)
        self.processes = []
        for i in range(num):
            pr = Process(target=parse, args=(i, self.stop, self.cur_tank))
            self.processes.append(pr)
            pr.start()


def parse(p_id, stop, cur_tank):
    global mw
    while stop.value == 0:
        cur_tank.acquire()
        ct = cur_tank.value
        cur_tank.value += 1
        cur_tank.release()
        if len(TANKS) <= ct:
            stop.value = 1
            print("Ended by", p_id+1)
            break
        for _, map_ in MAPS.iterrows():
            if stop.value == 1:
                break
            mw.labels[p_id].setText(
                f"{p_id}: {TANKS.tag.iloc[ct]} | {map_.work_name}")
            print("Process", p_id+1, TANKS.tag.iloc[ct], map_["name"])
            sleep(1)
        else:
            continue
    else:
        print(p_id+1, "is closed")

if __name__ == "__main__":
    import sys
    import os.path
    # global mw
    app = QApplication(sys.argv)

    mw = MainWindow()
    if os.path.isfile("data/logs/status.json"):
        mw.load_settings()

    mw.show()

    mw.startProcess(12)

    sys.exit(app.exec())


