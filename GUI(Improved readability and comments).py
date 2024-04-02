import sqlite3
from PyQt5 import QtCore, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(884, 652)
        
        # Основное окно для манипуляций с базой данных
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # Виджеты кнопок
        self.Buttons = QtWidgets.QWidget(self.centralwidget)
        self.Buttons.setGeometry(QtCore.QRect(490, 0, 381, 251))
        self.Buttons.setObjectName("Buttons")
        
        # Кнопка "Добавить"
        self.pushButton = QtWidgets.QPushButton(self.Buttons)
        self.pushButton.setGeometry(QtCore.QRect(30, 20, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.on_add_button_clicked)
        
        # Кнопка "Посмотреть"
        self.pushButton_2 = QtWidgets.QPushButton(self.Buttons)
        self.pushButton_2.setGeometry(QtCore.QRect(30, 80, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.out_of_button_clicked)
        
        # Виджет текстового браузера
        self.textBrowser = QtWidgets.QTextBrowser(self.Buttons)
        self.textBrowser.setGeometry(QtCore.QRect(130, 0, 256, 251))
        self.textBrowser.setObjectName("textBrowser")
        
        # Виджеты для ввода даты и денег
        self.date_field = None
        self.money_field = None
        
        # Диалоговое окно добавления записей в таблицу базы данных
        self.commitDialog = QtWidgets.QDialog() 
        self.setupCommitDialog()
        
        # Диалоговое окно просмотра записей с таблицы базы данных
        self.watchDialog = QtWidgets.QDialog()
        self.setupWatchDialog()

        # Установка виджетов
        self.setupWidgets(MainWindow)

    def setupWidgets(self, MainWindow):
        """Установка виджетов."""
        self.setupMainWindow(MainWindow)
        self.setupMenuBar(MainWindow)
        self.setupStatusBar(MainWindow)

    def setupMainWindow(self, MainWindow):
        """Установка основного окна."""
        MainWindow.setCentralWidget(self.centralwidget)
        
    def setupMenuBar(self, MainWindow):
        """Установка меню."""
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 884, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

    def setupStatusBar(self, MainWindow):
        """Установка строки состояния."""
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

    def setupCommitDialog(self):
        """Установка диалогового окна для добавления записей."""
        self.commitDialog.setWindowTitle("Введите данные")
        self.commitDialog.resize(300, 200)
        self.form_layout = QtWidgets.QFormLayout(self.commitDialog)
        self.date_field = QtWidgets.QDateEdit(self.commitDialog)
        self.date_field.setCalendarPopup(True)
        self.form_layout.addRow("Дата:", self.date_field)
        self.money_field = QtWidgets.QLineEdit(self.commitDialog)
        self.form_layout.addRow("Количество денег:", self.money_field)
        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.on_commit_button_clicked)
        self.button_box.rejected.connect(self.commitDialog.reject)
        self.form_layout.addWidget(self.button_box)

    def setupWatchDialog(self):
        """Установка диалогового окна для просмотра записей."""
        self.watchDialog.setWindowTitle("Введите данные")
        self.watchDialog.resize(300, 200)
        self.watch_form_layout = QtWidgets.QFormLayout(self.watchDialog)
        self.watch_date_field = QtWidgets.QDateEdit(self.watchDialog)
        self.watch_date_field.setCalendarPopup(True)
        self.watch_form_layout.addRow("Дата:", self.watch_date_field)
        self.watch_button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.watch_button_box.accepted.connect(self.on_watchFromTable_button_clicked)
        self.watch_button_box.rejected.connect(self.watchDialog.reject)
        self.watch_form_layout.addWidget(self.watch_button_box)

    def on_add_button_clicked(self):
        """Обработчик нажатия кнопки 'Добавить'."""
        self.commitDialog.show()

    def on_commit_button_clicked(self):
        """Обработчик нажатия кнопки 'Ok' в диалоговом окне добавления записей."""
        connection = sqlite3.connect("timeMoney.db")
        date = self.date_field.date().toString("yyyy-MM-dd")
        money = self.money_field.text()
        data_tuple = (date, money)
        addToTable(connection, data_tuple)
        ui.textBrowser.append("Успешно добавлено!")
        self.commitDialog.close()

    def on_cancel_button_clicked(self):
        """Обработчик нажатия кнопки 'Отмена' в диалоговом окне добавления записей."""
        self.commitDialog.close()

    def on_cancelWatch_button_clicked(self):
        """Обработчик нажатия кнопки 'Отмена' в диалоговом окне просмотра записей."""
        self.watchDialog.close()

    def on_watchFromTable_button_clicked(self):
        """Обработчик нажатия кнопки 'Ok' в диалоговом окне просмотра записей."""
        connection = sqlite3.connect("timeMoney.db")
        date = self.watch_date_field.date().toString("yyyy-MM-dd")
        data_tuple = (date,)
        receiveData = outOfTable(connection, data_tuple)
        formattedData = "\n".join(map(str, receiveData))
        ui.textBrowser.setText(formattedData)
        connection.close()

    def out_of_button_clicked(self):
        """Обработчик нажатия кнопки 'Посмотреть'."""
        self.watchDialog.show()

    def retranslateUi(self, MainWindow):
        """Установка переводов."""
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Добавить"))
        self.pushButton_2.setText(_translate("MainWindow", "Посмотреть"))
        self.pushButton_3.setText(_translate("MainWindow", "Изменить"))
        self.pushButton_4.setText(_translate("MainWindow", "Удалить"))
        self.button_box.commitButton.setText(_translate("MainWindow", "Записать"))
        self.button_box.cancelButton.setText(_translate("MainWindow", "Отмена"))
        self.watch_button_box.watchButton.setText(_translate("MainWindow", "Применить"))
        self.watch_button_box.cancelWatchButton.setText(_translate("MainWindow", "Отмена"))


def addToTable(connection, data_tuple):
    """Добавить данные в базу данных."""
    try:
        cursor = connection.cursor()
        cursor.execute("""INSERT INTO Tracking (date, money) VALUES (?, ?)""", data_tuple)
        connection.commit()
        connection.close()
    except sqlite3.Error as e:
        print(f"Ошибка при добавлении данных в базу данных: {e}")

def outOfTable(connection, data_tuple):
    """Получить данные из базы данных."""
    try:
        cursor = connection.cursor()
        cursor.execute("""SELECT money, date FROM Tracking WHERE date = ?""", data_tuple)
        info = cursor.fetchall()
        connection.commit()
        return info
    except sqlite3.Error as e:
        print(f"Ошибка при получении данных из базы данных: {e}")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
