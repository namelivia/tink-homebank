import sqlite3

database_file = 'categories.db'

def get_category(description):
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    cursor.execute(f"SELECT category_id FROM items WHERE name = '{description}'")
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
    cursor.execute(f"SELECT name FROM categories WHERE id = {id}")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    if len(data) == 0:
        return None
    return data[0][0]
