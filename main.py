import sys
import sqlite3
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QTableWidgetItem, QHeaderView
from PyQt6.QtCore import Qt

class CoffeeApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        
        self.load_coffee_data()
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
    def load_coffee_data(self):
        try:
            conn = sqlite3.connect('coffee.sqlite')
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, name, roast_level, bean_type, taste_description, price, package_volume
                FROM coffee
                ORDER BY id
            ''')
            
            coffee_data = cursor.fetchall()
            
            self.tableWidget.setRowCount(len(coffee_data))
            self.tableWidget.setColumnCount(7)
            self.tableWidget.setHorizontalHeaderLabels([
                'ID', 'Название сорта', 'Степень обжарки', 'Тип', 'Описание вкуса', 'Цена (руб)', 'Объем упаковки (г)'
            ])
            
            for row, coffee in enumerate(coffee_data):
                for col, value in enumerate(coffee):
                    item = QTableWidgetItem(str(value))
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    self.tableWidget.setItem(row, col, item)
            
            for col in [0, 5, 6]:
                for row in range(len(coffee_data)):
                    item = self.tableWidget.item(row, col)
                    if item:
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            conn.close()
            
        except sqlite3.Error as e:
            print(f"Ошибка базы данных: {e}")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = CoffeeApp()
    window.show()
    sys.exit(app.exec())
