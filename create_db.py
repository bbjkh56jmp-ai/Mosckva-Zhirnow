import sqlite3
import os

def create_database():
    if os.path.exists('coffee.sqlite'):
        os.remove('coffee.sqlite')
    
    conn = sqlite3.connect('coffee.sqlite')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE coffee (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roast_level TEXT NOT NULL,
            bean_type TEXT NOT NULL,
            taste_description TEXT NOT NULL,
            price REAL NOT NULL,
            package_volume INTEGER NOT NULL
        )
    ''')
    
    sample_data = [
        ('Эфиопия Иргачеффе', 'Светлая', 'В зернах', 
         'Яркий цветочный аромат с нотами бергамота и цитрусов, легкая винная кислинка', 
         1250.0, 250),
        
        ('Колумбия Супремо', 'Средняя', 'В зернах', 
         'Сбалансированный вкус с ореховыми и шоколадными нотами, карамельное послевкусие', 
         980.0, 250),
        
        ('Бразилия Сантос', 'Темная', 'Молотый', 
         'Крепкий насыщенный вкус с горьковатым послевкусием, нотами темного шоколада', 
         750.0, 200),
        
        ('Гватемала Антигуа', 'Средняя', 'В зернах', 
         'Пряный аромат с шоколадными и карамельными нотами, дымное послевкусие', 
         1100.0, 250),
        
        ('Кения АА', 'Светлая', 'Молотый', 
         'Яркая кислинка с ягодными и винными нотами, томатный акцент', 
         1350.0, 200),
        
        ('Италия Эспрессо', 'Очень темная', 'В зернах', 
         'Интенсивный крепкий вкус для эспрессо, горьковатый с пряными нотами', 
         890.0, 250),
        
        ('Коста-Рика Тарразу', 'Средняя', 'В зернах', 
         'Чистый вкус с фруктовыми нотами и сладким послевкусием, легкая ореховая текстура', 
         1420.0, 250),
        
        ('Вьетнам Далат', 'Темная', 'Молотый', 
         'Насыщенный вкус с земляными нотами, легкая пряность и долгое послевкусие', 
         680.0, 200)
    ]
    # взял из интернета
    
    cursor.executemany('''
        INSERT INTO coffee (name, roast_level, bean_type, taste_description, price, package_volume)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', sample_data)
    
    conn.commit()
    conn.close()
    print("База данных coffee.sqlite успешно создана!")

if __name__ == '__main__':
    create_database()
