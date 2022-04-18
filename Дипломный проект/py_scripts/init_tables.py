# Файл для создания таблиц базы данных

import jaydebeapi
from datetime import datetime

connect = jaydebeapi.connect(
	'oracle.jdbc.driver.OracleDriver',
	'jdbc:oracle:thin:de3hd/bilbobaggins@de-etl.chronosavant.ru:1521/deoracle',
	['de3hd','bilbobaggins'],
	'ojdbc7.jar')

cursor = connect.cursor()


# Стейджинговые таблицы
def init_tables_STG():
	cursor.execute('''
		CREATE TABLE de3hd.s_23_STG_TRNSCTNS(
			trans_id varchar(128),
			trans_date timestamp,
			amt decimal,
			card_num varchar(128),
			oper_type varchar(128),
			oper_result varchar(128),
			terminal varchar(128),
			-- с учетом того, что данные поступают за предыдущий день:
			ceate_dt timestamp default TRUNC(SYSDATE - 1),
			update_dt timestamp default TRUNC(SYSDATE) - INTERVAL '1' SECOND
		)
	''')

	cursor.execute('''
		CREATE TABLE de3hd.s_23_STG_PSSPRT_BLCKLST(
			entry_dt date,
			passport_num varchar(128),
			deleted_flg integer default 0,
			effective_from_dttm date default (to_date('2021-03-01', 'YYYY.MM.DD')),
			effective_to_dttm date default (to_date('2999-12-31', 'YYYY.MM.DD'))
		)
	''')


	cursor.execute('''
		CREATE TABLE de3hd.s_23_STG_TRMNLS(
			terminal_id varchar(128),
			terminal_type varchar(128),
			terminal_city varchar(128),
			terminal_address varchar(128)
		)
	''')

#  Таблицы фактов
def init_tables_DWH_FACT():
	try:
		cursor.execute('''
			CREATE TABLE de3hd.s_23_DWH_FACT_TRNSCTNS(
				trans_id varchar(128),
				trans_date timestamp,
				amt decimal,
				card_num varchar(128),
				oper_type varchar(128),
				oper_result varchar(128),
				terminal varchar(128),
				create_dt timestamp,
				update_dt timestamp
			)
		''')
	except jaydebeapi.DatabaseError:
		print('Таблица с таким названием уже существует')


# Таблицы измерений
def init_tables_DWH_DIM():
	try:
		cursor.execute('''
			CREATE TABLE de3hd.s_23_DWH_DIM_CRDS(
				card_num varchar(128),
				account_num varchar(128),
				create_dt date,
				update_dt date
			)
		''')

		cursor.execute('''
			INSERT INTO de3hd.s_23_DWH_DIM_CRDS
			SELECT *
			FROM BANK.cards
		''')
	except jaydebeapi.DatabaseError:
		print('Таблица с таким названием уже существует')


	try:
		cursor.execute('''
			CREATE TABLE de3hd.s_23_DWH_DIM_CCNTS(
				account_num varchar(128),
				valid_to date,
				client varchar(128),
				create_dt date,
				update_dt date
			)
		''')

		cursor.execute('''
			INSERT INTO de3hd.s_23_DWH_DIM_CCNTS
			SELECT *
			FROM BANK.accounts
		''')		
	except jaydebeapi.DatabaseError:
		print('Таблица с таким названием уже существует')

	try:
		cursor.execute('''
			CREATE TABLE de3hd.s_23_DWH_DIM_CLNTS(
				client_id varchar(128),
				last_name varchar(128),
				first_name varchar(128),
				patrinymic varchar(128),
				date_of_birth date,
				passport_num varchar(128),
				passport_valid_to date,
				phone varchar(128),
				create_dt date,
				update_dt date
			)
		''')

		cursor.execute('''
			INSERT INTO de3hd.s_23_DWH_DIM_CLNTS
			SELECT *
			FROM BANK.clients
		''')
	except jaydebeapi.DatabaseError:
		print('Таблица с таким названием уже существует')

# Историческая таблица Passport_Blacklist
def init_tables_DWH_DIM_HIST():
	try:
		cursor.execute('''
			CREATE TABLE de3hd.s_23_DWH_DIM_PSSPRT_BL_HIST(
				entry_dt date,
				passport_num varchar(128),
				deleted_flg integer default 0,
				-- условно дату effective_from_dttm принимаем 1.03.21 (первый день накопления данных)
				effective_from_dttm date default (to_date('2021-03-01', 'YYYY.MM.DD')),
				effective_to_dttm date default (to_date('2999-12-31', 'YYYY.MM.DD'))
			)
		''')
	except jaydebeapi.DatabaseError:
		print('Таблица с таким названием уже существует')



# Таблицы отчета по мошенническим операциям
def init_report():	
	# основная таблица с мошенническими операциями, хранящая данные накопительным итогом
	try:
		cursor.execute('''
			CREATE TABLE de3hd.s_23_REP_FRAUND(
				event_dt timestamp,
				passport varchar(128),
				fio varchar(128),
				phone varchar(128),
				event_type varchar(128),
				report_dt timestamp 
			)
		''')
	except jaydebeapi.DatabaseError:
		print('Таблица с таким названием уже существует')

	# временная таблица с мошенническими операциями одного анализируемого дня 
	cursor.execute('''
		CREATE TABLE de3hd.s_23_REP_FRAUND_NEW(
			event_dt timestamp,
			passport varchar(128),
			fio varchar(128),
			phone varchar(128),
			event_type varchar(128),
			report_dt timestamp default current_timestamp
		)
	''')
	
