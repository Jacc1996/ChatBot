import sqlite3

def create_database():
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            name TEXT
        )
    ''')

    conn.commit()
    conn.close()

def insert_user(user_id, name):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (user_id, name) VALUES (?, ?)', (user_id, name))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    # Get user input interactively
    user_id = int(input("Enter user ID: "))
    name = input("Enter user name: ")

    create_database()
    insert_user(user_id, name)

    print(f"User with ID {user_id} and name '{name}' added successfully!")