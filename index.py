# MD AHAD ALI
# 20183290242
# mdaliahad@outlook.com
# The project is made by pyQt5. Its a crossplatfrom  gui.
# import some stuff

from os import execl
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import psycopg2  # postgresql database
from PyQt5.uic import loadUiType
import datetime


ui, _ = loadUiType('library.ui')  # loading the library.ui file
login, _ = loadUiType('login.ui')  # loading the login ui file


# login handle start

class Login(QWidget, login):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.Handel_Login)
        style = open('themes/dark_gray.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def Handel_Login(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="library",
            user="postgres",
            password="1814")
        self.cur = self.conn.cursor()

        username = self.lineEdit.text()
        password = self.lineEdit_2.text()

        sql = ''' SELECT * FROM users'''

        self.cur.execute(sql)

        data = self.cur.fetchall()
        for row in data:
            if username == row[1] and password == row[3]:
                print('user match')
                self.window2 = MainApp()
                self.close()
                self.window2.show()

            else:
                self.label.setText(
                    'Make Sure You Enterd Your Username And Password Correctly')


# login handle end

# This is the main class to handle all user interface functionality.
class MainApp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.HandleUiChange()  # UI will change
        self.HandleButton()  # Handle button
        self.Dark_blue_themes()
        self.show_author()
        self.show_category()
        self.show_publisher()
        self.show_category_combobox()
        self.show_author_combobox()
        self.show_publisher_combobox()

        self.Show_All_Clients()
        self.show_all_books()

        self.Show_ALL_OPeration()

    #working with  ui#

    def HandleUiChange(self):
        self.Hiding_Themes()
        self.tabWidget.tabBar().setVisible(False)  # hide tab button

    # handle button process when click.
    def HandleButton(self):
        # show theme ui from theme button
        self.pushButton_5.clicked.connect(self.Show_Themes)
        # Hide theme ui from theme ui button
        self.pushButton_22.clicked.connect(self.Hiding_Themes)
        self.pushButton.clicked.connect(
            self.Open_day_to_day_tab)  # When today button will select , one tab will open
        self.pushButton_2.clicked.connect(
            self.Open_Books_Tab)  # when book button select, another tab will open
        self.pushButton_3.clicked.connect(
            self.Open_Users_Tab)  # when user button will select then another tab will open.
        self.pushButton_4.clicked.connect(
            self.Open_Settings_Tab)  # when setting button is selected then another tab will open.
        self.pushButton_26.clicked.connect(self.Open_Clients_Tab)

        # Connect database functionality in UI
        self.pushButton_7.clicked.connect(self.Add_New_Book)
        self.pushButton_9.clicked.connect(self.Search_Books)
        self.pushButton_8.clicked.connect(self.Edit_Books)
        self.pushButton_15.clicked.connect(self.Add_Category)
        self.pushButton_16.clicked.connect(self.Add_Author)
        self.pushButton_18.clicked.connect(self.Add_Publisher)
        self.pushButton_10.clicked.connect(self.Delete_Books)
        self.pushButton_11.clicked.connect(self.Add_New_users)
        self.pushButton_12.clicked.connect(self.login)
        self.pushButton_13.clicked.connect(self.Edit_Users)
        self.pushButton_6.clicked.connect(self.Dark_Orange_theme)
        self.pushButton_19.clicked.connect(self.Dark_blue_themes)
        self.pushButton_21.clicked.connect(self.Dark_gray_theme)
        self.pushButton_20.clicked.connect(self.QDark_theme)
        self.pushButton_14.clicked.connect(self.Add_New_Client)
        self.pushButton_24.clicked.connect(self.Search_client)
        self.pushButton_25.clicked.connect(self.Edit_Client)
        self.pushButton_23.clicked.connect(self.Delete_Client)

        self.pushButton_17.clicked.connect(self.handle_day_operation)

    # show theme methode

    def Show_Themes(self):
        self.groupBox_3.show()
    # show hide method

    def Hiding_Themes(self):
        self.groupBox_3.hide()

    #setting up today button to one tab#
    def Open_day_to_day_tab(self):
        self.tabWidget.setCurrentIndex(0)
    #setting up book button to another tab#

    def Open_Books_Tab(self):
        self.tabWidget.setCurrentIndex(1)
    #setting up user button to another tab#

    def Open_Users_Tab(self):
        self.tabWidget.setCurrentIndex(3)

    def Open_Clients_Tab(self):
        self.tabWidget.setCurrentIndex(2)

    #setting up setting button to one tab#

    def Open_Settings_Tab(self):
        self.tabWidget.setCurrentIndex(4)


# intilize day to day to day operation

    def handle_day_operation(self):
        book_title = self.lineEdit_29.text()
        client_name = self.lineEdit.text()
        type = self.comboBox_9.currentText()
        days_number = self.comboBox_10.currentIndex() + 1
        today_date = (datetime.date.today())
        to_date = today_date + datetime.timedelta(days=days_number)
        self.conn = psycopg2.connect(
            host="localhost",
            database="library",
            user="postgres",
            password="1814")
        self.cur = self.conn.cursor()
        self.cur.execute('''
                         INSERT INTO dayoperations(book_name, client, type, days, date, to_date)
                         VALUES(%s, %s, %s, %s, %s, %s)
                         ''', (book_title, client_name, type, days_number, today_date, to_date))
        self.conn.commit()
        self.statusBar().showMessage('New operation Added')

        self.Show_ALL_OPeration()

    def Show_ALL_OPeration(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="library",
            user="postgres",
            password="1814")
        self.cur = self.conn.cursor()

        self.cur.execute(''' 
                          SELECT book_name, client, type, days, date, to_date FROM dayoperations''')
        data = self.cur.fetchall()
        print(data)
        self.tableWidget.setRowCount(0)

        self.tableWidget.insertRow(0)
        for row, form in enumerate(data):
            for column, item in enumerate(form):
                self.tableWidget.setItem(
                    row, column, QTableWidgetItem(str(item)))
                column += 1

            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)
# initialize Database in Book page

    def show_all_books(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="library",
            user="postgres",
            password="1814")
        self.cur = self.conn.cursor()

        self.cur.execute(
            ''' SELECT book_code, book_name, book_description, book_category, book_author, book_publisher, book_price FROM book ''')
        data = self.cur.fetchall()
        self.tableWidget_5.setRowCount(0)
        self.tableWidget_5.insertRow(0)

        for row, form in enumerate(data):
            for column, item in enumerate(form):
                self.tableWidget_5.setItem(
                    row, column, QTableWidgetItem(str(item)))
                column += 1
            row_position = self.tableWidget_5.rowCount()
            self.tableWidget_5.insertRow(row_position)
        self.conn.close()

    def Add_New_Book(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="library",
            user="postgres",
            password="1814")
        self.cur = self.conn.cursor()

        book_title = self.lineEdit_2.text()
        book_description = self.textEdit.toPlainText()
        book_code = self.lineEdit_3.text()
        book_category = self.comboBox_3.currentText()
        book_author = self.comboBox_4.currentText()
        book_publisher = self.comboBox_5.currentText()
        book_price = self.lineEdit_4.text()

        self.cur.execute('''
            INSERT INTO book(book_name, book_description, book_code, book_category, book_author, book_publisher, book_price)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (book_title, book_description, book_code, book_category, book_author, book_publisher, book_price))

        self.conn.commit()
        self.statusBar().showMessage('New Book Added')

        self.lineEdit_2.setText('')
        self.textEdit.setPlainText('')
        self.lineEdit_3.setText('')
        self.comboBox_3.setCurrentIndex(0)
        self.comboBox_4.setCurrentIndex(0)
        self.comboBox_5.setCurrentIndex(0)
        self.lineEdit_4.setText('')
        self.show_all_books()


# search book from database and show to the UI

    def Search_Books(self):

        self.conn = psycopg2.connect(
            host="localhost",
            database="library",
            user="postgres",
            password="1814")
        self.cur = self.conn.cursor()

        book_title = self.lineEdit_8.text()
        sql = '''SELECT * FROM book WHERE book_name= %s'''
        self.cur.execute(sql, [(book_title)])
        data = self.cur.fetchone()

        print(data)
        self.lineEdit_6.setText(data[1])
        self.textEdit_2.setPlainText(data[2])
        self.lineEdit_5.setText(data[1])
        self.comboBox_7.setCurrentText(data[4])
        self.comboBox_6.setCurrentText(data[5])
        self.comboBox_8.setCurrentText(data[6])
        self.lineEdit_7.setText(str(data[7]))


# edit book from database and show to the UI

    def Edit_Books(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="library",
            user="postgres",
            password="1814")
        self.cur = self.conn.cursor()

        book_title = self.lineEdit_6.text()
        book_description = self.textEdit_2.toPlainText()
        book_code = self.lineEdit_5.text()
        book_category = self.comboBox_7.currentText()
        book_author = self.comboBox_6.currentText()
        book_publisher = self.comboBox_8.currentText()
        book_price = self.lineEdit_7.text()

        search_book_title = self.lineEdit_8.text()

        self.cur.execute('''
            UPDATE book SET book_name=%s, book_description=%s, book_code=%s, book_category=%s, book_author=%s, book_publisher=%s, book_price=%s WHERE book_name= %s
            ''', (book_title, book_description, book_code, book_category, book_author, book_publisher, book_price, search_book_title))

        self.conn.commit()
        self.statusBar().showMessage('book updated')
        self.show_all_books()


# delete book from database and show to the UI


    def Delete_Books(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="library",
            user="postgres",
            password="1814")
        self.cur = self.conn.cursor()

        book_title = self.lineEdit_6.text()

        warning = QMessageBox.warning(
            self, 'Delete Book', "Are you sure?", QMessageBox.Yes | QMessageBox.No)
        if warning == QMessageBox.Yes:
            sql = '''DELETE FROM book WHERE book_name=%s'''
            self.cur.execute(sql, [(book_title)])
            self.conn.commit()
            self.statusBar().showMessage('Book Deleted')
            self.show_all_books()


# Initillize client

    def Show_All_Clients(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="library",
            user="postgres",
            password="1814")
        self.cur = self.conn.cursor()

        self.cur.execute(
            ''' SELECT client_name, client_email, client_nationalid FROM clients ''')
        data = self.cur.fetchall()
        self.tableWidget_6.setRowCount(0)
        self.tableWidget_6.insertRow(0)

        for row, form in enumerate(data):
            for column, item in enumerate(form):
                self.tableWidget_6.setItem(
                    row, column, QTableWidgetItem(str(item)))
                column += 1
            row_position = self.tableWidget_6.rowCount()
            self.tableWidget_6.insertRow(row_position)
        self.conn.close()

    def Add_New_Client(self):
        client_name = self.lineEdit_18.text()
        client_email = self.lineEdit_19.text()
        client_nationalId = self.lineEdit_24.text()
        self.conn = psycopg2.connect(
            host="localhost",
            database="library",
            user="postgres",
            password="1814")
        self.cur = self.conn.cursor()
        self.cur.execute('''
                         INSERT INTO clients(client_name, client_email, client_nationalid)
                         VALUES (%s, %s, %s)
                         ''', (client_name, client_email, client_nationalId))
        self.conn.commit()
        self.conn.close()
        self.statusBar().showMessage("New client Added")
        self.Show_All_Clients()

    def Search_client(self):
        client_nationalid = self.lineEdit_28.text()
        self.conn = psycopg2.connect(
            host="localhost",
            database="library",
            user="postgres",
            password="1814")
        self.cur = self.conn.cursor()

        sql = '''SELECT * FROM clients WHERE client_nationalid=%s'''
        self.cur.execute(sql, [(client_nationalid)])
        data = self.cur.fetchone()
        print(data)

        self.lineEdit_25.setText(data[1])
        self.lineEdit_26.setText(data[2])
        self.lineEdit_27.setText(data[3])

    def Edit_Client(self):

        client_original_national_id = self.lineEdit_28.text()
        client_name = self.lineEdit_25.text()
        client_email = self.lineEdit_26.text()
        client_nationalId = self.lineEdit_27.text()
        self.conn = psycopg2.connect(
            host="localhost",
            database="library",
            user="postgres",
            password="1814")
        self.cur = self.conn.cursor()
        self.cur.execute('''
                         UPDATE clients SET client_name=%s, client_email=%s, client_nationalid=%s WHERE client_nationalid= %s
                         ''', (client_name, client_email, client_nationalId, client_original_national_id))
        self.conn.commit()
        self.conn.close()
        self.statusBar().showMessage('Client Data update')
        self.Show_All_Clients()

    def Delete_Client(self):
        client_original_national_id = self.lineEdit_28.text()
        worning_message = QMessageBox.warning(
            self, "Delete client", "Are you sure you want to delete?", QMessageBox.Yes | QMessageBox.No)

        self.conn = psycopg2.connect(
            host="localhost",
            database="library",
            user="postgres",
            password="1814")
        self.cur = self.conn.cursor()
        sql = ''' DELETE FROM clients WHERE client_nationalid=%s'''
        self.cur.execute(sql, [(client_original_national_id)])
        self.conn.commit()
        self.conn.close()
        self.statusBar().showMessage(' Client delete!')
        self.Show_All_Clients()


# Initialize Database in Users page

    def Add_New_users(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="library",
            user="postgres",
            password="1814")
        self.cur = self.conn.cursor()

        username = self.lineEdit_9.text()
        email = self.lineEdit_10.text()
        password = self.lineEdit_12.text()
        password2 = self.lineEdit_11.text()

        if password == password2:
            self.cur.execute('''
                             INSERT INTO users(user_name, user_email, user_password)
                             VALUES (%s, %s, %s)
                             ''', (username, email, password))

            self.conn.commit()
            self.statusBar().showMessage('New user Added')
        else:
            self.label_17.setText('Your password is not matched!')

    def login(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="library",
            user="postgres",
            password="1814")
        self.cur = self.conn.cursor()

        username = self.lineEdit_14.text()
        password = self.lineEdit_13.text()

        sql = '''SELECT * FROM users'''

        self.cur.execute(sql)
        data = self.cur.fetchall()
        for row in data:
            if username == row[1] and password == row[3]:
                print('user match')
                self.statusBar().showMessage(" Login Successful!")
                self.groupBox_4.setEnabled(True)

                self.lineEdit_17.setText(row[1])
                self.lineEdit_20.setText(row[2])
                self.lineEdit_15.setText(row[3])

    def Edit_Users(self):
        username = self.lineEdit_17.text()
        email = self.lineEdit_20.text()
        password = self.lineEdit_15.text()
        password2 = self.lineEdit_16.text()

        original_name = self.lineEdit_14.text()

        if password == password2:
            self.conn = psycopg2.connect(
                host="localhost",
                database="library",
                user="postgres",
                password="1814")
            self.cur = self.conn.cursor()

            self.cur.execute('''
                UPDATE users SET user_name =%s, user_email=%s, user_password=%s WHERE user_name=%s
                ''', (username, email, password, original_name))
            self.conn.commit()
            self.statusBar().showMessage(' User Data update successfully')

        else:
            print('make sure you enterd your password correctly')

# initialize database in category page
    def Add_Category(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="library",
            user="postgres",
            password="1814")
        self.cur = self.conn.cursor()

        # selecting text and storing in the variable
        category_name = self.lineEdit_21.text()
        self.cur.execute('''
            INSERT INTO category(category_name) VALUES (%s)
        ''', (category_name,))  # inserting values
        self.conn.commit()  # subitting in database
        # in the statusbar this message will show.
        self.statusBar().showMessage('New Category Added')
        self.lineEdit_21.setText('')
        self.show_category()
        self.show_category_combobox()

    def show_category(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="library",
            user="postgres",
            password="1814")
        self.cur = self.conn.cursor()
        self.cur.execute(''' SELECT category_name FROM category''')
        data = self.cur.fetchall()

        if data:
            self.tableWidget_2.setRowCount(0)
            self.tableWidget_2.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget_2.setItem(
                        row, column, QTableWidgetItem(str(item)))
                    column += 1
                row_position = self.tableWidget_2.rowCount()
                self.tableWidget_2.insertRow(row_position)


# Initialize database in author page

    def Add_Author(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="library",
            user="postgres",
            password="1814")
        self.cur = self.conn.cursor()

        # selecting text and storing in the variable
        author_name = self.lineEdit_22.text()
        self.cur.execute('''
            INSERT INTO authors(author_name) VALUES (%s)
        ''', (author_name,))  # inserting values
        self.conn.commit()  # subitting in database
        self.lineEdit_22.setText('')
        # in the statusbar this message will show.
        self.statusBar().showMessage('New Author Added')
        self.show_author()
        self.show_author_combobox()

    def show_author(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="library",
            user="postgres",
            password="1814")
        self.cur = self.conn.cursor()
        self.cur.execute(''' SELECT author_name FROM authors''')
        data = self.cur.fetchall()

        if data:
            self.tableWidget_3.setRowCount(0)
            self.tableWidget_3.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget_3.setItem(
                        row, column, QTableWidgetItem(str(item)))
                    column += 1
                row_position = self.tableWidget_3.rowCount()
                self.tableWidget_3.insertRow(row_position)


# Initialize database as apublisher

    def Add_Publisher(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="library",
            user="postgres",
            password="1814")
        self.cur = self.conn.cursor()

        # selecting text and storing in the variable
        publisher_name = self.lineEdit_23.text()
        self.cur.execute('''
            INSERT INTO publisher(publisher_name) VALUES (%s)
        ''', (publisher_name,))  # inserting values
        self.conn.commit()  # subitting in database
        self.lineEdit_23.setText('')
        # in the statusbar this message will show.
        self.statusBar().showMessage('New publisher Added')
        self.show_publisher()
        self.show_publisher_combobox()

    def show_publisher(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="library",
            user="postgres",
            password="1814")
        self.cur = self.conn.cursor()
        self.cur.execute(''' SELECT publisher_name FROM publisher''')
        data = self.cur.fetchall()

        if data:
            self.tableWidget_4.setRowCount(0)
            self.tableWidget_4.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget_4.setItem(
                        row, column, QTableWidgetItem(str(item)))
                    column += 1
                row_position = self.tableWidget_4.rowCount()
                self.tableWidget_4.insertRow(row_position)

# Run this app

# show settings data in ui
# add new book

    def show_category_combobox(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="library",
            user="postgres",
            password="1814")
        self.cur = self.conn.cursor()
        self.cur.execute('''SELECT category_name FROM category''')
        data = self.cur.fetchall()

        self.comboBox_3.clear()
        for category in data:
            print(category[0])
            self.comboBox_3.addItem(category[0])
            self.comboBox_7.addItem(category[0])

    def show_author_combobox(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="library",
            user="postgres",
            password="1814")
        self.cur = self.conn.cursor()
        self.cur.execute('''SELECT author_name FROM authors''')
        data = self.cur.fetchall()

        self.comboBox_4.clear()
        for category in data:
            print(category[0])
            self.comboBox_4.addItem(category[0])
            self.comboBox_6.addItem(category[0])

    def show_publisher_combobox(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="library",
            user="postgres",
            password="1814")
        self.cur = self.conn.cursor()
        self.cur.execute('''SELECT publisher_name FROM publisher''')
        data = self.cur.fetchall()

        self.comboBox_5.clear()
        for category in data:
            print(category[0])
            self.comboBox_5.addItem(category[0])
            self.comboBox_8.addItem(category[0])


# UI themes make

    def Dark_blue_themes(self):
        style = open('themes/dark_blue.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def Dark_gray_theme(self):
        style = open('themes/dark_gray.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def Dark_Orange_theme(self):
        style = open('themes/dark_orange.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def QDark_theme(self):
        style = open('themes/qdark.css', 'r')
        style = style.read()
        self.setStyleSheet(style)


def main():
    app = QApplication(sys.argv)
    window = Login()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
