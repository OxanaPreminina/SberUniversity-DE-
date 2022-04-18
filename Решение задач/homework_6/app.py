import sqlite3
import json
import re
import datetime 

connect = sqlite3.connect('database.db')
cursor = connect.cursor()


# функция, создающая таблицу users и представление c актуальными данными v_users
def init():
	cursor.execute(''' 
		CREATE TABLE if not exists users(
			id integer primary key autoincrement,
			firstname varchar(128),
			surname varchar(128),
			age integer,
			salary integer,
			deleted_flg integer default 0,
			start_dttm datetime default current_timestamp,
			end_dttm datetime default (datetime('2999-12-31 23:59:59'))
		)
	''')

	cursor.execute('''
		CREATE VIEW if not exists v_users AS
			SELECT
				id,
				firstname,
				surname,
				age,
				salary
			FROM users
			WHERE datetime('now') between start_dttm and end_dttm
			and deleted_flg = 0			
		''')

# функция для добавления пользователя 
def add_user(firstname, surname, age, salary):
	cursor.execute('''
		SELECT count(*)
		FROM users
		where firstname = ?
		and surname = ?
		and age = ?
		and salary = ?
		and end_dttm = datetime('2999-12-31 23:59:59')
	''', [firstname, surname, age, salary])

	if cursor.fetchone()[0] != 0:
		return

	cursor.execute('''
		UPDATE users
		SET end_dttm = datetime('now')
		where firstname = ?
		and surname = ?
		and end_dttm = datetime('2999-12-31 23:59:59')
	''', [firstname, surname])

	cursor.execute('''
		INSERT INTO users(firstname, surname, age, salary)
		VALUES(?, ?, ?, ?)
	''', [firstname, surname, age, salary])

	connect.commit()


# функция для логического удаления пользователей по имени и фамилии 
def deleted_user(firstname, surname):
	cursor.execute('''
		SELECT 
			firstname,
			surname,
			age,
			salary
		FROM v_users
		where firstname = ?
		and surname = ?
		
	''', [firstname, surname])

	user = cursor.fetchone()

	cursor.execute('''
		UPDATE users
		SET end_dttm = datetime('now')
		where firstname = ?
		and surname = ?
		and end_dttm = datetime('2999-12-31 23:59:59')
	''', [user[0], user[1]])

	cursor.execute('''
		INSERT INTO users (firstname, surname, age, salary, deleted_flg)
			VALUES(?, ?, ?, ?, ?)
	''', list(user) + [1])

	connect.commit()



def show_data(sourse):
	cursor.execute(f'SELECT * from {sourse}')
	print('\-_-/'*17)
	print(sourse)
	print('\-_-/'*17)
	for row in cursor.fetchall():
		print(row)
	print()


# функция для сохранения данных о пользователях на указанную дату в csv файл
def load_to_file(path):
	date = input('Введите дату(ГГГГ-ММ-ДД), на которую требуется сохранить данные, или любой символ - для вывода данных на сегодняшнюю дату: ')
	if re.fullmatch(r'\d{4}-\d{2}-\d{2}', date) == None:
		date = 'now'
	result = []
	cursor.execute('''
		SELECT 
			*
		FROM users
		WHERE (datetime(?) between start_dttm and end_dttm) or datetime(?) == date(end_dttm)
	''', [date, date])
	rows = cursor.fetchall()
	columns = [elem[0] for elem in cursor.description]
	for row in rows:
		d = {}
		for i in range(len(columns)):
			d[columns[i]] = row[i]
		result.append(d)
	print(result)
	with open(path, 'w', encoding='utf-8') as f:
		f.write(json.dumps(result, ensure_ascii=False, indent=4))


# init()
# add_user('Вячеслав', 'Васильев', 23, 60000)
# add_user('Евгений', 'Зайцев', 38, 90000)
# add_user('Андрей', 'Румянцев', 43, 115000)
# deleted_user('Андрей', 'Румянцев')
show_data('users')
load_to_file('result.json')
