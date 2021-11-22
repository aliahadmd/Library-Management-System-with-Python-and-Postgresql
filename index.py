# MD AHAD ALI
# 20183290242
# mdaliahad@outlook.com
# The project is made by pyQt5. Its a crossplatfrom  gui.
# import some stuff

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import psycopg2  # postgresql database
from PyQt5.uic import loadUiType


ui, _ = loadUiType('library.ui')  # loading the .ui file


# This is the main class to handle all user interface functionality.
class MainApp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.HandleUiChange()  # UI will change
        self.HandleButton()  # Handle button
        self.show_author()
        self.show_category()
        self.show_publisher()
        self.show_category_combobox()
        self.show_author_combobox()
        self.show_publisher_combobox()

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

        # Connect database functionality in UI
        self.pushButton_7.clicked.connect(self.Add_New_Book)
        self.pushButton_9.clicked.connect(self.Search_Books)
        self.pushButton_8.clicked.connect(self.Edit_Books)
        self.pushButton_15.clicked.connect(self.Add_Category)
        self.pushButton_16.clicked.connect(self.Add_Author)
        self.pushButton_18.clicked.connect(self.Add_Publisher)
        self.pushButton_10.clicked.connect(self.Delete_Books)

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
        self.tabWidget.setCurrentIndex(2)
    #setting up setting button to one tab#

    def Open_Settings_Tab(self):
        self.tabWidget.setCurrentIndex(3)


# initialize Database in Book page

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
        book_category = self.comboBox_3.currentIndex()
        book_author = self.comboBox_4.currentIndex()
        book_publisher = self.comboBox_5.currentIndex()
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
        self.comboBox_7.setCurrentIndex(data[4])
        self.comboBox_6.setCurrentIndex(data[5])
        self.comboBox_8.setCurrentIndex(data[6])
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
        book_category = self.comboBox_7.currentIndex()
        book_author = self.comboBox_6.currentIndex()
        book_publisher = self.comboBox_8.currentIndex()
        book_price = self.lineEdit_7.text()

        search_book_title = self.lineEdit_8.text()

        self.cur.execute('''
            UPDATE book SET book_name=%s, book_description=%s, book_code=%s, book_category=%s, book_author=%s, book_publisher=%s, book_price=%s WHERE book_name= %s
            ''', (book_title, book_description, book_code, book_category, book_author, book_publisher, book_price, search_book_title))

        self.conn.commit()
        self.statusBar().showMessage('book updated')


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


# Initialize Database in Users page

    def Add_New_users(self):
        pass

    def login(self):
        pass

    def Edit_Users(self):
        pass

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


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
