import sqlite3
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(884, 652)
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

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def on_add_button_clicked(self):
        connection = sqlite3.connect("timeMoney.db")
        addToTable(connection)
        ui.textBrowser.append("Успешно добавлено!")

    def out_of_button_clicked(self):
        connection = sqlite3.connect("timeMoney.db")
        outOfTable(connection)
        receiveData = outOfTable(connection)
        formattedData = "\n".join(map(str, receiveData))
        ui.textBrowser.setText(formattedData)
        connection.close()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Добавить"))
        self.pushButton_2.setText(_translate("MainWindow", "Посмотреть"))
        self.pushButton_3.setText(_translate("MainWindow", "Изменить"))
        self.pushButton_4.setText(_translate("MainWindow", "Удалить"))


def addToTable(connection):
    try:
        cursor = connection.cursor()
    except sqlite3.Error as e:
        print(f"Ошибка подключения к базе данных: {e}")

    cursor.execute('INSERT INTO Tracking (date, money) values ("2016-02-06", 3450)')
    connection.commit()
    connection.close()

def outOfTable(connection):
    try:
        cursor = connection.cursor()
    except sqlite3.Error as e:
        print(f"Ошибка подключения к базе данных: {e}")
    cursor.execute("SELECT (money, date) FROM Tracking")
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
