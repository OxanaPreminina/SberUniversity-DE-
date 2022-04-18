import sqlite3
import json
connect = sqlite3.connect('database.db')
cursor = connect.cursor()

# функция создания новых таблиц
def new_table(table):
	try:
		cursor.execute(f'''
			CREATE TABLE {table}(
				name varchar(128),
				lastname varchar(128),
				age integer,
				primary key(name, lastname)
			)
		''')
	except sqlite3.OperationalError:
		print('Таблица с таким названием уже существует')
	connect.commit()



# функция для удаления таблиц
def drop_table(table):
	cursor.execute(f'DROP TABLE {table}')



# функция добавления записи о клиенте
def add_person(person_name, person_lastname, person_age):
	try:
		cursor.execute('''
			INSERT INTO client(name, lastname, age) VALUES(?, ?, ?)
		''', [person_name, person_lastname, person_age])
	
	except sqlite3.OperationalError:
		print('Клиент с такими именем и фамилией уже существует')
	connect.commit()


# функция добавления записей о клиентах из файла json
def add_people():
	with open("data_file.json", "r", encoding="utf-8") as read_file:
		data = json.load(read_file)
	for i in range(len(data)):
		add_person(data[i].setdefault('name'), data[i].setdefault('lastname'), data[i].setdefault('age'))
	connect.commit()


def show_data(table):
	cursor.execute(f'SELECT * FROM {table}')
	for row in cursor.fetchall():
		print(row)



# функция, возвращающая средний возраст клиентов
def avg_age(table):
	cursor.execute(f'SELECT ROUND(AVG(age), 1) FROM {table}')
	row = cursor.fetchone()
	print(row)
	
