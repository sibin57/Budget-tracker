import sqlite3
from PyQt5 import QtCore, QtWidgets

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(884, 652)
        #Основное окно для дальнейших манипуляций с базой данных
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Buttons = QtWidgets.QWidget(self.centralwidget)
        self.Buttons.setGeometry(QtCore.QRect(490, 0, 381, 251))
        self.Buttons.setObjectName("Buttons")
        self.pushButton = QtWidgets.QPushButton(self.Buttons)
        self.pushButton.setGeometry(QtCore.QRect(30, 20, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.on_add_button_clicked)
        self.pushButton_2 = QtWidgets.QPushButton(self.Buttons)
        self.pushButton_2.setGeometry(QtCore.QRect(30, 80, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.out_of_button_clicked)
        self.pushButton_3 = QtWidgets.QPushButton(self.Buttons)
        self.pushButton_3.setGeometry(QtCore.QRect(30, 150, 75, 23))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.Buttons)
        self.pushButton_4.setGeometry(QtCore.QRect(30, 210, 75, 23))
        self.pushButton_4.setObjectName("pushButton_4")
        self.textBrowser = QtWidgets.QTextBrowser(self.Buttons)
        self.textBrowser.setGeometry(QtCore.QRect(130, 0, 256, 251))
        self.textBrowser.setObjectName("textBrowser")
        self.lcdNumber = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber.setGeometry(QtCore.QRect(580, 260, 221, 71))
        self.lcdNumber.setObjectName("lcdNumber")
        self.calendarWidget = QtWidgets.QCalendarWidget(self.centralwidget)
        self.calendarWidget.setGeometry(QtCore.QRect(0, 0, 312, 183))
        self.calendarWidget.setObjectName("calendarWidget")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(50, 340, 771, 261))
        self.graphicsView.setObjectName("graphicsView")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 884, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        #Диалоговое окно добавления записей в таблицу базы данных
        self.commitDialog = QtWidgets.QDialog() 
        self.commitDialog.setWindowTitle("Введите данные")
        self.commitDialog.resize(300, 200)
        self.form_layout = QtWidgets.QFormLayout(self.commitDialog)
        self.date_field = QtWidgets.QLineEdit(self.commitDialog)
        self.form_layout.addRow("Дата:", self.date_field)
        self.money_field = QtWidgets.QLineEdit(self.commitDialog)
        self.form_layout.addRow("Количество денег:", self.money_field)
        self.button_box = QtWidgets.QDialogButtonBox(self.commitDialog)
        self.button_box.commitButton = QtWidgets.QPushButton(self.commitDialog)
        self.button_box.commitButton.setGeometry(QtCore.QRect(30, 65, 75, 23))
        self.button_box.commitButton.clicked.connect(self.on_commit_button_clicked)
        self.button_box.cancelButton = QtWidgets.QPushButton(self.commitDialog)
        self.button_box.cancelButton.setGeometry(QtCore.QRect(30, 130, 75, 23))
        self.button_box.cancelButton.clicked.connect(self.on_cancel_button_clicked)
        self.form_layout.addWidget(self.button_box)
        #Диалоговое окно просмотра записей с таблицы базы данных
        self.watchDialog = QtWidgets.QDialog()
        self.watchDialog.setWindowTitle("Введите данные")
        self.watchDialog.resize(300, 200)
        self.watch_form_layout = QtWidgets.QFormLayout(self.watchDialog)
        self.watch_date_field = QtWidgets.QDateEdit(self.watchDialog)
        self.watch_form_layout.addRow("Дата:", self.watch_date_field)
        self.watch_button_box = QtWidgets.QDialogButtonBox(self.watchDialog)
        self.watch_button_box.watchButton = QtWidgets.QPushButton(self.watchDialog)
        self.watch_button_box.watchButton.setGeometry(QtCore.QRect(30, 65, 75, 23))
        self.watch_button_box.watchButton.clicked.connect(self.on_watchFromTable_button_clicked)
        self.watch_button_box.cancelWatchButton = QtWidgets.QPushButton(self.watchDialog)
        self.watch_button_box.cancelWatchButton.setGeometry(QtCore.QRect(30, 130, 75, 23))
        self.watch_button_box.cancelWatchButton.clicked.connect(self.on_cancelWatch_button_clicked)
        self.watch_form_layout.addWidget(self.watch_button_box)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def on_add_button_clicked(self): #К первой кнопке
        date = self.calendarWidget.selectedDate().toString("yyyy-MM-dd")
        self.date_field.setText(date)
        self.commitDialog.show()
        
        
    def on_commit_button_clicked(self): #К первой кнопке
        connection = sqlite3.connect("D:\\Проекты\\project_popov\\timeMoney.db")
        date = self.calendarWidget.selectedDate().toString("yyyy-MM-dd")
        self.date_field.setText(date)
        money = self.money_field.text()
        data_tuple = (date, money)
        addToTable(connection, data_tuple)
        ui.textBrowser.append("Успешно добавлено!")
        self.commitDialog.close()

    def on_cancel_button_clicked(self): #К первой кнопке
        self.commitDialog.close()
    
    def on_cancelWatch_button_clicked(self): #Ко второй кнопке
        self.watchDialog.close()
    
    def on_watchFromTable_button_clicked(self):#Ко второй кнопке
        connection = sqlite3.connect("D:\\Проекты\\project_popov\\timeMoney.db")
        date = self.watch_date_field.date().toString("yyyy-MM-dd")
        data_tuple = (date,)
        receiveData = outOfTable(connection, data_tuple)
        formattedData = "\n".join(map(str, receiveData))
        ui.textBrowser.setText(formattedData)
        connection.close()

    def out_of_button_clicked(self): #Ко второй кнопке
        self.watchDialog.show()
        
        

    def retranslateUi(self, MainWindow):
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
    try:
        cursor = connection.cursor()
    except sqlite3.Error as e:
        print(f"Ошибка подключения к базе данных: {e}")    

    cursor.execute("""INSERT INTO Tracking (date, money) values (?, ?)""", data_tuple)
    connection.commit()
    connection.close()

def outOfTable(connection, data_tuple):
    try:
        cursor = connection.cursor()
    except sqlite3.Error as e:
        print(f"Ошибка подключения к базе данных: {e}")  
    cursor.execute("""SELECT money, date FROM Tracking WHERE date = ?""", data_tuple)
    info = cursor.fetchall()
    connection.commit()
    return info
    

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

