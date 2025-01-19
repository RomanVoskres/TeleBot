import sqlite3

# phone_number = None
# first_name = None
# last_name = None
# user_id = None
#
# last_call_data = None
#
# procedure = None # Процедура которую хочет клиент
#
# appointment_zone = None  # запоминает зону макияжа пользователя
# comuflage = None # камуфляж true false
# communication_method = False  # запоминает метод связи с пользователем
# want_consult = False # Может хотеть на консультацию
# delalaTattoo_v_Broowushka = False
# delalaTattoo_v_zone = False
# want_send_photo = False
#
# training_appointment_id = None

def CreateTable():
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    surname TEXT,
    user_id INTEGER,
    phone_number TEXT,
    last_call_data TEXT,
    procedure INTEGER,
    appointment_zone INTEGER,
    comuflage BLOB,
    communication_method INTEGER,
    want_consult BLOB,
    delalaTattoo_v_Broowushka BLOB,
    delalaTattoo_v_zone BLOB,
    want_send_photo BLOB,
    training_appointment_id TEXT
    )
    ''')

    connection.commit()
    connection.close()

def add_user(name, surname, user_id, phone_number, last_call_data, procedure, appointment_zone, comuflage, communication_method, want_consult, delalaTattoo_v_Broowushka,
             delalaTattoo_v_zone, want_send_photo, training_appointment_id):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()

    cursor.execute('''
    INSERT INTO Users (name, surname, user_id, phone_number, last_call_data, procedure, appointment_zone, comuflage, communication_method, want_consult, 
    delalaTattoo_v_Broowushka, delalaTattoo_v_zone, want_send_photo, training_appointment_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, surname, user_id, phone_number, last_call_data, procedure, appointment_zone, comuflage, communication_method, want_consult, delalaTattoo_v_Broowushka, delalaTattoo_v_zone, want_send_photo, training_appointment_id))

    connection.commit()
    connection.close()


def get_user_by_id(id): # Возвращает по айди
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM Users WHERE id = ?', (id,))
    row = cursor.fetchone()

    connection.close()
    return row

def get_user_by_user_id(user_id): # Возвращает по айди в телеграмме
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM Users WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()

    connection.close()
    return row

def get_name(user_id):
    user = get_user_by_user_id(user_id)
    if user:
        return user[0]
    else:
        return "ошибка"

def get_surname(user_id):
    user = get_user_by_user_id(user_id)
    if user:
        return user[1]
    else:
        return "ошибка"

def get_phone_number(user_id):
    user = get_user_by_user_id(user_id)
    if user:
        return user[3]
    else:
        return "ошибка"

def get_last_call_data(user_id):
    user = get_user_by_user_id(user_id)
    if user:
        return user[4]
    else:
        return "ошибка"

def get_procedure(user_id):
    user = get_user_by_user_id(user_id)
    if user:
        return user[5]
    else:
        return 0

def get_appointment_zone(user_id):
    user = get_user_by_user_id(user_id)
    if user:
        return user[6]
    else:
        return 0

def get_comuflage(user_id):
    user = get_user_by_user_id(user_id)
    if user:
        return user[7]
    else:
        return 0

def get_communication_method(user_id):
    user = get_user_by_user_id(user_id)
    if user:
        return user[8]
    else:
        return 0

def get_want_consult(user_id):
    user = get_user_by_user_id(user_id)
    if user:
        return user[9]
    else:
        return 0

def get_delalaTattoo_v_Broowushka(user_id):
    user = get_user_by_user_id(user_id)
    if user:
        return user[10]
    else:
        return 0

def get_delalaTattoo_v_zone(user_id):
    user = get_user_by_user_id(user_id)
    if user:
        return user[11]
    else:
        return 0

def get_want_send_photo(user_id):
    user = get_user_by_user_id(user_id)
    if user:
        return user[12]
    else:
        return 0

def get_training_appointment_id(user_id):
    user = get_user_by_user_id(user_id)
    if user:
        return user[13]
    else:
        return "ошибка"
