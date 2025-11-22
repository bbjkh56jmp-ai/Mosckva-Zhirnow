from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QDialog, QMessageBox
import sqlite3

class AddEditCoffeeDialog(QDialog):
    def __init__(self, parent=None, coffee_id=None):
        super().__init__(parent)
        uic.loadUi('addEditCoffeeForm.ui', self)
        
        self.coffee_id = coffee_id
        self.setup_ui()
        self.load_coffee_data()
        
        self.saveButton.clicked.connect(self.save_coffee)
        self.cancelButton.clicked.connect(self.reject)
    
    def setup_ui(self):
        self.roastLevelCombo.addItems(['Светлая', 'Средняя', 'Темная', 'Очень темная'])
        self.beanTypeCombo.addItems(['В зернах', 'Молотый'])
        
        if self.coffee_id:
            self.setWindowTitle("Редактирование кофе")
        else:
            self.setWindowTitle("Добавление нового кофе")
    
    def load_coffee_data(self):
        if self.coffee_id:
            try:
                conn = sqlite3.connect('coffee.sqlite')
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT name, roast_level, bean_type, taste_description, price, package_volume
                    FROM coffee WHERE id = ?
                ''', (self.coffee_id,))
                
                coffee_data = cursor.fetchone()
                conn.close()
                
                if coffee_data:
                    self.nameEdit.setText(coffee_data[0])
                    self.roastLevelCombo.setCurrentText(coffee_data[1])
                    self.beanTypeCombo.setCurrentText(coffee_data[2])
                    self.tasteDescriptionEdit.setPlainText(coffee_data[3])
                    self.priceSpin.setValue(float(coffee_data[4]))
                    self.volumeSpin.setValue(coffee_data[5])
                    
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки данных: {e}")
    
    def save_coffee(self):
        name = self.nameEdit.text().strip()
        roast_level = self.roastLevelCombo.currentText()
        bean_type = self.beanTypeCombo.currentText()
        taste_description = self.tasteDescriptionEdit.toPlainText().strip()
        price = self.priceSpin.value()
        volume = self.volumeSpin.value()
        
        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название сорта")
            return
        
        if not taste_description:
            QMessageBox.warning(self, "Ошибка", "Введите описание вкуса")
            return
        
        try:
            conn = sqlite3.connect('coffee.sqlite')
            cursor = conn.cursor()
            
            if self.coffee_id:
                cursor.execute('''
                    UPDATE coffee 
                    SET name = ?, roast_level = ?, bean_type = ?, taste_description = ?, price = ?, package_volume = ?
                    WHERE id = ?
                ''', (name, roast_level, bean_type, taste_description, price, volume, self.coffee_id))
            else:
                cursor.execute('''
                    INSERT INTO coffee (name, roast_level, bean_type, taste_description, price, package_volume)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (name, roast_level, bean_type, taste_description, price, volume))
            
            conn.commit()
            conn.close()
            
            QMessageBox.information(self, "Успех", 
                "Данные успешно сохранены" if self.coffee_id else "Новый кофе успешно добавлен")
            self.accept()
            
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка сохранения: {e}")
        # из инета ошибка
    