import sys
import sqlite3
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QTableWidgetItem, QHeaderView, QMessageBox, QDialog
from PyQt6.QtCore import Qt
from addEditCoffeeForm import AddEditCoffeeDialog

class CoffeeApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        
        self.load_coffee_data()
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        self.addButton.clicked.connect(self.add_coffee)
        self.editButton.clicked.connect(self.edit_coffee)
        self.deleteButton.clicked.connect(self.delete_coffee)
        
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
            QMessageBox.critical(self, "Ошибка", f"Ошибка базы данных: {e}")
    
    def get_selected_coffee_id(self):
        selected_items = self.tableWidget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Предупреждение", "Пожалуйста, выберите запись о кофе")
            return None
        return int(self.tableWidget.item(selected_items[0].row(), 0).text())
    
    def add_coffee(self):
        dialog = AddEditCoffeeDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_coffee_data()
    
    def edit_coffee(self):
        coffee_id = self.get_selected_coffee_id()
        if coffee_id is None:
            return
        
        dialog = AddEditCoffeeDialog(self, coffee_id)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_coffee_data()
    
    def delete_coffee(self):
        coffee_id = self.get_selected_coffee_id()
        if coffee_id is None:
            return
        
        reply = QMessageBox.question(
            self, 
            "Подтверждение удаления", 
            f"Вы уверены, что хотите удалить запись с ID {coffee_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                conn = sqlite3.connect('coffee.sqlite')
                cursor = conn.cursor()
                cursor.execute("DELETE FROM coffee WHERE id = ?", (coffee_id,))
                conn.commit()
                conn.close()
                self.load_coffee_data()
                QMessageBox.information(self, "Успех", "Запись успешно удалена")
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка при удалении: {e}")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = CoffeeApp()
    window.show()
    sys.exit(app.exec())
