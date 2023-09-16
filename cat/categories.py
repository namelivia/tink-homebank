import sqlite3

database_file = 'categories.db'

def insert_item(category_name, description):
    category_id = _get_id_by_name(category_name)
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO items (category_id, name) VALUES (?, ?)", (category_id, description))
    conn.commit()
    cursor.close()
    conn.close()

def get_category(description):
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    cursor.execute("SELECT category_id FROM items WHERE name = ?", (description,))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    if len(data) == 0:
        return None
    category_id = data[0][0]
    return _get_category_name_by_id(category_id)

def get_all_categories():
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM categories")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return [entry[0] for entry in data]

def _get_category_name_by_id(id):
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM categories WHERE id = ?", (id,))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    if len(data) == 0:
        return None
    return data[0][0]

def _get_id_by_name(name):
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM categories WHERE name = ?", (name,))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    if len(data) == 0:
        return None
    return data[0][0]
