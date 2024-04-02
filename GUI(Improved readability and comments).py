import sqlite3
from PyQt5 import QtCore, QtWidgets

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        """Настройка пользовательского интерфейса"""
        self.setObjectName("MainWindow")
        self.resize(884, 652)

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        # Виджет календаря
        self.calendarWidget = QtWidgets.QCalendarWidget(self.centralwidget)
        self.calendarWidget.setGeometry(QtCore.QRect(0, 0, 312, 183))
        self.calendarWidget.setObjectName("calendarWidget")

        # Виджет текстового браузера
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(490, 0, 381, 251))
        self.textBrowser.setObjectName("textBrowser")

        # Виджет LCD-дисплея
        self.lcdNumber = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber.setGeometry(QtCore.QRect(580, 260, 221, 71))
        self.lcdNumber.setObjectName("lcdNumber")

        # Виджет графики
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(50, 340, 771, 261))
        self.graphicsView.setObjectName("graphicsView")

        # Кнопка "Добавить"
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(30, 20, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.on_add_button_clicked)

        # Кнопка "Посмотреть"
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(30, 80, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.on_watch_button_clicked)

        # Кнопка "Изменить"
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(30, 150, 75, 23))
        self.pushButton_3.setObjectName("pushButton_3")

        # Кнопка "Удалить"
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(30, 210, 75, 23))
        self.pushButton_4.setObjectName("pushButton_4")

        self.setCentralWidget(self.centralwidget)

        # Меню и строка состояния
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 884, 21))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi()

    def on_add_button_clicked(self):
        """Обработчик нажатия кнопки "Добавить"."""
        dialog = CommitDialog(self)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.textBrowser.append("Успешно добавлено!")

    def on_watch_button_clicked(self):
        """Обработчик нажатия кнопки "Посмотреть"."""
        dialog = WatchDialog(self)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            pass  # Обработать результат из диалогового окна просмотра

    def retranslateUi(self):
        """Перевод пользовательского интерфейса."""
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Добавить"))
        self.pushButton_2.setText(_translate("MainWindow", "Посмотреть"))
        self.pushButton_3.setText(_translate("MainWindow", "Изменить"))
        self.pushButton_4.setText(_translate("MainWindow", "Удалить"))

class CommitDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Введите данные")
        self.resize(300, 200)
        self.layout = QtWidgets.QVBoxLayout(self)

        self.date_field = QtWidgets.QLineEdit()
        self.layout.addRow("Дата:", self.date_field)

        self.money_field = QtWidgets.QLineEdit()
        self.layout.addRow("Количество денег:", self.money_field)

        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.layout.addWidget(self.button_box)

        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def get_data(self):
        """Получить данные из диалогового окна."""
        return self.date_field.text(), self.money_field.text()

class WatchDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Введите данные")
        self.resize(300, 200)
        self.layout = QtWidgets.QVBoxLayout(self)

        self.date_field = QtWidgets.QLineEdit()
        self.layout.addRow("Дата:", self.date_field)

        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.layout.addWidget(self.button_box)

        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def get_date(self):
        """Получить дату из диалогового окна."""
        return self.date_field.text()

def addToTable(connection, data_tuple):
    """Добавить данные в базу данных."""
    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Tracking (date, money) VALUES (?, ?)", data_tuple)
        connection.commit()
    except sqlite3.Error as e:
        print(f"Ошибка при добавлении данных в базу данных: {e}")
    finally:
        connection.close()

def outOfTable(connection, data_tuple):
    """Получить данные из базы данных."""
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT money, date FROM Tracking WHERE date = ?", data_tuple)
        info = cursor.fetchall()
        return info
    except sqlite3.Error as e:
        print(f"Ошибка при получении данных из базы данных: {e}")
    finally:
        connection.close()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
