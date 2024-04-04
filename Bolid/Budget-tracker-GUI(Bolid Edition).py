import sqlite3
import os
from PyQt5 import QtGui
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QInputDialog, QLineEdit
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

DATABASE_FILE = "timeMoney.db"

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("BolidBudget")
        MainWindow.resize(884, 652)
        #Основное окно для дальнейших манипуляций с базой данных
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setStyleSheet("background-color: #0086CD;")
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
        self.pushButton_3.clicked.connect(self.openChangeDialog_button_clicked)
        self.pushButton_4 = QtWidgets.QPushButton(self.Buttons)
        self.pushButton_4.setGeometry(QtCore.QRect(30, 210, 75, 23))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.openDeleteDialog_button_clicked)
        self.textBrowser = QtWidgets.QTextBrowser(self.Buttons)
        self.textBrowser.setGeometry(QtCore.QRect(130, 0, 256, 251))
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser.setStyleSheet("QTextBrowser { background-color: white; }")
        self.lcdNumber = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber.setGeometry(QtCore.QRect(580, 260, 221, 71))
        self.lcdNumber.setObjectName("lcdNumber")
        self.lcdNumber.setStyleSheet("QLCDNumber { background-color: white; }")
        total = calculate_total()
        self.lcdNumber.display(total)
        self.calendarWidget = QtWidgets.QCalendarWidget(self.centralwidget)
        self.calendarWidget.setGeometry(QtCore.QRect(0, 0, 312, 183))
        self.calendarWidget.setObjectName("calendarWidget")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(50, 340, 771, 300))
        self.graphicsView.setObjectName("graphicsView")
        self.graphicsView.setStyleSheet("QGraphicsView { background-color: white; }")
        data = getData()
        self.draw_plot(data)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 884, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # Установка стиля для всех кнопок
        button_style = "QPushButton { background-color: white; }"  # Красный фон, белый текст
        self.pushButton.setStyleSheet(button_style)
        self.pushButton_2.setStyleSheet(button_style)
        self.pushButton_3.setStyleSheet(button_style)
        self.pushButton_4.setStyleSheet(button_style)

        # Создание виджета QLabel
        self.image_label = QtWidgets.QLabel(self.centralwidget)
        self.image_label.setGeometry(QtCore.QRect(-20, 190, 525, 130))  # Установка размеров и позиции
        self.image_label.setObjectName("image_label")
        
        # Загрузка изображения
        pixmap = QtGui.QPixmap("C:/Users/kk300/Downloads/py/logo.png")  # Укажите путь к вашему изображению
        # Установка изображения на QLabel
        self.image_label.setPixmap(pixmap)


        #Диалоговое окно добавления записей в таблицу базы данных
        self.commitDialog = QtWidgets.QDialog()
        self.commitDialog.setWindowTitle("Введите данные")
        self.commitDialog.resize(300, 200)
        self.form_layout = QtWidgets.QFormLayout(self.commitDialog)
        self.date_field = QtWidgets.QDateEdit(self.commitDialog)
        self.form_layout.addRow("Дата:", self.date_field)
        self.incoming_field = QtWidgets.QSpinBox(self.commitDialog)
        self.incoming_field.setRange(0, 2147483647)
        self.form_layout.addRow("Количество зачисленных денег:", self.incoming_field)
        self.spending_field = QtWidgets.QSpinBox(self.commitDialog)
        self.spending_field.setRange(0, 2147483647)
        self.form_layout.addRow("Количество потраченных денег:", self.spending_field)
        self.button_box = QtWidgets.QDialogButtonBox(self.commitDialog)
        self.button_box.commitButton = QtWidgets.QPushButton(self.commitDialog)
        self.button_box.commitButton.setGeometry(QtCore.QRect(30, 150, 75, 23))
        self.button_box.commitButton.clicked.connect(self.on_commit_button_clicked)
        self.button_box.cancelButton = QtWidgets.QPushButton(self.commitDialog)
        self.button_box.cancelButton.setGeometry(QtCore.QRect(200, 150, 75, 23))
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

        #Диалоговое окно для изменения записей с таблицы базы данных
        self.changeDialog = QtWidgets.QDialog()
        self.changeDialog.setWindowTitle("Измените данные")
        self.changeDialog.resize(400, 200)
        self.change_form_layout = QtWidgets.QFormLayout(self.changeDialog)
        self.change_date_field = QtWidgets.QDateEdit(self.changeDialog)
        self.change_form_layout.addRow("Выбор даты:", self.change_date_field)
        self.income_edit_field = QtWidgets.QSpinBox(self.changeDialog)
        self.income_edit_field.setRange(0, 2147483647)
        self.change_form_layout.addRow("Изменить количество зачисленных денег:", self.income_edit_field)
        self.spending_edit_field = QtWidgets.QSpinBox(self.changeDialog)
        self.spending_edit_field.setRange(0, 2147483647)
        self.change_form_layout.addRow("Изменить количество потраченных денег:", self.spending_edit_field)
        self.change_button_box = QtWidgets.QDialogButtonBox(self.changeDialog)
        self.change_button_box.changeButton = QtWidgets.QPushButton(self.changeDialog)
        self.change_button_box.changeButton.setGeometry(QtCore.QRect(30, 150, 75, 23))
        self.change_button_box.changeButton.clicked.connect(self.change_button_clicked)
        self.change_button_box.cancelChangeButton = QtWidgets.QPushButton(self.changeDialog)
        self.change_button_box.cancelChangeButton.setGeometry(QtCore.QRect(150, 150, 75, 23))
        self.change_button_box.cancelChangeButton.clicked.connect(self.quitChangeDialog_button_clicked)
        self.change_form_layout.addWidget(self.watch_button_box)
        
        #Диалоговое окно для удаление определенных записей
        self.deleteDialog = QtWidgets.QDialog()
        self.deleteDialog.setWindowTitle("Удалите данные")
        self.deleteDialog.resize(300, 200)
        self.delete_form_layout = QtWidgets.QFormLayout(self.deleteDialog)
        self.delete_date_field = QtWidgets.QDateEdit(self.deleteDialog)
        self.delete_form_layout.addRow("Выбор даты для удаления данных", self.delete_date_field)
        self.delete_button_box = QtWidgets.QDialogButtonBox(self.deleteDialog)
        self.delete_button_box.deleteButton = QtWidgets.QPushButton(self.deleteDialog)
        self.delete_button_box.deleteButton.setGeometry(QtCore.QRect(30, 90, 75, 23))
        self.delete_button_box.deleteButton.clicked.connect(self.on_deleteFromTable_button_clicked)
        self.delete_button_box.cancelDeleteButton = QtWidgets.QPushButton(self.deleteDialog)
        self.delete_button_box.cancelDeleteButton.setGeometry(QtCore.QRect(180, 90, 75, 23))
        self.delete_button_box.cancelDeleteButton.clicked.connect(self.closeDeleteDialog_button_clicked)





        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def on_add_button_clicked(self): #К первой кнопке
        self.commitDialog.show()
        self.date_field.date().toString("yyyy-MM-dd")

    def on_commit_button_clicked(self): #К первой кнопке
        connection = sqlite3.connect(DATABASE_FILE)
        self.date_field.date().toString("dd.MM.yyyy") 
        date = self.date_field.text()
        income = self.incoming_field.text()
        spending = self.spending_field.text() #TODO переделайте окошко: добавьте поля для доходов и расходов
        addToTable(connection, date, income, spending)#Вот вам функция 
        ui.textBrowser.append("Успешно добавлено!")
        self.commitDialog.close()

    def on_cancel_button_clicked(self): #К первой кнопке
        self.commitDialog.close()

    def on_cancelWatch_button_clicked(self): #Ко второй кнопке
        self.watchDialog.close()

    def on_watchFromTable_button_clicked(self):#Ко второй кнопке
        connection = sqlite3.connect(DATABASE_FILE)
        date = self.watch_date_field.date().toString("dd.MM.yyyy")
        receiveData = outOfTable(connection, date)
        formattedData = "\n".join(map(str, receiveData))
        ui.textBrowser.setText(formattedData)

    def out_of_button_clicked(self): #Ко второй кнопке
        self.watchDialog.show()

    def openChangeDialog_button_clicked(self):
        self.changeDialog.show()
        connection = sqlite3.connect(DATABASE_FILE)
        response = seeAll(connection)
        formattedData = "\n".join(map(str, response))
        ui.textBrowser.append(formattedData)

    def quitChangeDialog_button_clicked(self):
        self.changeDialog.close()

    def change_button_clicked(self):
        connection = sqlite3.connect(DATABASE_FILE)
        response = seeAll(connection)
        formattedData = "\n".join(map(str, response))
        ui.textBrowser.append(formattedData)
        selected_date = self.change_date_field.date().toString("dd.MM.yyyy")
        selected_income = self.income_edit_field.text()
        selected_spending = self.spending_edit_field.text()
        changeTable(connection, selected_date, selected_income, selected_spending)
        ui.textBrowser.append("Данные успешно были изменены!")
        self.changeDialog.close()

    def draw_plot(self, data):
        canvas = FigureCanvas(Figure(figsize=(7, 3)))
        
        canvas.figure.clear()

        ax = canvas.figure.add_subplot(111)

        dates = [entry[0] for entry in data]
        income = [entry[1] for entry in data]
        spending = [entry[2] for entry in data]

        ax.plot(dates, income, label='Доход', color='blue')
        ax.plot(dates, spending, label='Расход', color='red')

        ax.legend()

        ax.set_xlabel('Дата')
        ax.set_ylabel('Деньги')

        canvas.draw()

        scene = QtWidgets.QGraphicsScene()
        plot_item = scene.addWidget(canvas)
        self.graphicsView.setScene(scene)
        
    def on_deleteFromTable_button_clicked(self):
        connection = sqlite3.connect(DATABASE_FILE)
        date = self.delete_date_field.date().toString("dd.MM.yyyy")
        deleteFromTable(connection, date)
        ui.textBrowser.setText("Данные успешно удалены")   

    def openDeleteDialog_button_clicked(self):
        self.deleteDialog.show()

    def closeDeleteDialog_button_clicked(self):
        self.deleteDialog.close()
    
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "BolidBudget"))
        self.pushButton.setText(_translate("MainWindow", "Добавить"))
        self.pushButton_2.setText(_translate("MainWindow", "Посмотреть"))
        self.pushButton_3.setText(_translate("MainWindow", "Изменить"))
        self.pushButton_4.setText(_translate("MainWindow", "Удалить"))
        self.button_box.commitButton.setText(_translate("MainWindow", "Записать"))
        self.button_box.cancelButton.setText(_translate("MainWindow", "Отмена"))
        self.watch_button_box.watchButton.setText(_translate("MainWindow", "Применить"))
        self.watch_button_box.cancelWatchButton.setText(_translate("MainWindow", "Отмена"))
        self.change_button_box.changeButton.setText(_translate("MainWindow", "Изменить"))
        self.change_button_box.cancelChangeButton.setText(_translate("MainWindow", "Отмена"))
        self.delete_button_box.deleteButton.setText(_translate("MainWindow", "Удалить"))
        self.delete_button_box.cancelDeleteButton.setText(_translate("MainWindow", "Отмена"))

#TODO добавьте функционал для кнопки удаления, используйте deleteFromTable(connection, date)

#Функции для работы с БД

def seeAll(connection):
        try:
            cursor = connection.cursor()
        except sqlite3.Error as e:
            print(f"Ошибка подключения к базе данных: {e}")
        cursor.execute("SELECT date, income, spending FROM budget")
        response = cursor.fetchall()
        connection.commit()
        connection.close()
        return response

def addToTable(connection, date, income, spending):
    """Функция добавления записей в БД
    :connection: объект sql подключения
    :date: строка даты в формате "yyyy-MM-dd"
    :income: число, денежный доход
    :spending: число, денежный расход
    """
    try:
        cursor = connection.cursor()
    except sqlite3.Error as e:
        print(f"Ошибка подключения к базе данных: {e}")

    cursor.execute("INSERT INTO budget (date, income, spending) values (?, ?, ?)", (date, income, spending))
    connection.commit()
    connection.close()

def outOfTable(connection, date):
    """Функция получения записей из БД по дате
    :connection: объект sql подключения
    :date: строка даты в формате "yyyy-MM-dd"
    :return: кортеж вида (date, income, spending) (str, int, int)
    """
    try:
        cursor = connection.cursor()
    except sqlite3.Error as e:
        print(f"Ошибка подключения к базе данных: {e}")
    cursor.execute("SELECT date, income, spending FROM budget WHERE date = ?", (date,))
    response = cursor.fetchall()
    connection.commit()
    connection.close()
    return response

def changeTable(connection, date, income, spending):
    """Функция изменения записей в БД
    :connection: объект sql подключения
    :date: строка, дата записи в формате "yyyy-MM-dd"
    :income: число, новый денежный доход
    :spending: число, новый денежный расход
    :return: bool, успех операции (было ли что-то изменено)
    """
    try:
        cursor = connection.cursor()
    except sqlite3.Error as e:
        print(f"Ошибка подключения к базе данных: {e}")

    
    cursor.execute("UPDATE budget SET income = ?, spending = ? WHERE date = ?", (income, spending, date))
    response = cursor.fetchall()
    connection.commit()
    connection.close()
    

def deleteFromTable(connection, date):
    """Функция удаления записей из БД по дате
    :connection: объект sql подключения
    :date: строка даты в формате "yyyy-MM-dd"
    :return: bool, успех операции
    """
    try:
        cursor = connection.cursor()
    except sqlite3.Error as e:
        print(f"Ошибка подключения к базе данных: {e}")
    cursor.execute("DELETE FROM budget WHERE date = ?", (date,))
    connection.commit()
    connection.close()

def checkDatabase():
    """Функция для проверки существования БД.
    Если БД не существует, то функция её генерирует
    """
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        conn.cursor().execute("""
            CREATE TABLE IF NOT EXISTS budget (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                date        TEXT NOT NULL,
                income      INTEGER,
                spending    INTEGER
            );
                              """)
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def getData():
    connection = sqlite3.connect(DATABASE_FILE)
    try:
        cursor = connection.cursor()
    except sqlite3.Error as e:
        print(f"Ошибка подключения к базе данных: {e}")

    cursor.execute("SELECT date, income, spending FROM budget")
    data = cursor.fetchall()
    connection.close()

    return data

def calculate_total():
        connection = sqlite3.connect(DATABASE_FILE)
        cursor = connection.cursor()
        
        # Выполняем запрос для получения общей суммы
        cursor.execute("SELECT SUM(income) - SUM(spending) FROM budget")
        total = cursor.fetchone()[0] or 0  # Если запрос вернул None, устанавливаем значение по умолчанию 0

        connection.close()
        
        return total


if __name__ == "__main__":
    import sys
    checkDatabase()
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
