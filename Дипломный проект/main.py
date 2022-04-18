'''ETL-процесс разработан для анализа выгружаемых данных на предмет наличия мошеннических операций. 
Ежедневно в папку /input/ выгружаются 3 файла. ETL-процесс считывает их, обрабатывает, затем перемещает в 
папку /archive/ backup-файлы. Процесс поставлен на расписание с суточной периодичностью исполнения в 06:00
Ежедневно накопительным итогом строится отчет о мошеннических операциях. Данные о транзакциях сохраняются в историческую 
таблицу типа SCD1 (de3hd.s_23_DWH_FACT_TRNSCTNS), данные из черного списка паспортов сохраняются в историческую таблицу 
типа SCD2 (de3hd.s_23_DWH_DIM_PSSPRT_BL_HIST), что учитывает возможность исключения некоего паспорта из черного списка'''


import jaydebeapi
import pandas as pd
from datetime import datetime
import os
import py_scripts.init_tables

connect = jaydebeapi.connect(
	'oracle.jdbc.driver.OracleDriver',
	'jdbc:oracle:thin:de3hd/bilbobaggins@de-etl.chronosavant.ru:1521/deoracle',
	['de3hd','bilbobaggins'],
	'ojdbc7.jar')

cursor = connect.cursor()

# 1. Создание таблиц базы данных
# из файла py_scripts.init_tables


# 2. Загрузка данных
def load_stg(path_of_directory, path_to_directory):
	# path_of_directory - папка с выгружаемыми данными
	# path_to_directory - папка archive, куда переместятся отработанные файлы
	# из списка файлов в папке input_data(в которую ежедневно выгружаются данные) создаем датафрейм.
	# file - имя файла, type - сущность данных (passport,terminals,transactions), date - дата изменения, 
	# extension - расширение файла
	
	files_sourse = os.listdir(path_of_directory)
	list_file = []
	for i in files_sourse:
		list_file.append([i, i.split('_')[0], i.split('_')[-1].split('.')[0], i.split('_')[-1].split('.')[1]])
		df_files = pd.DataFrame(list_file, columns = ['file','type','date','extension'])
		df_files['date'] = pd.to_datetime(df_files['date'],format = '%d%m%Y')
	

	#  2.1. Transactions
	# определяем имя файла 
	files = df_files.loc[(df_files['type'] == 'transactions') & (df_files['extension'] == 'txt'), ['file','date']]
	file_name_transactions = files.iat[0, 0]
	date = files.iat[0, 1]

	cursor.execute('alter session set nls_date_format = "DD.MM.RR"')
	cursor.execute('alter session set nls_timestamp_format = "DD.MM.RR HH24:MI:SSXFF"')

	# создаем датафрейм с данными из файла и записываем их в таблицу
	df = pd.read_csv(path_of_directory + file_name_transactions, delimiter=';', decimal=",", header=0, index_col=None)

	cursor.executemany('''
		INSERT INTO de3hd.s_23_STG_TRNSCTNS
		(trans_id, trans_date, amt, card_num, oper_type, oper_result, terminal)
		VALUES (?, to_timestamp(?, 'YYYY.MM.DD HH24:MI:SS'), ?, ?, ?, ?, ?)
	''', df.values.astype(str).tolist())

	# переименовываем и перемещаем файл в archive
	os.replace(path_of_directory + file_name_transactions, path_to_directory + file_name_transactions + '.backup')
	

	#  2.2. Terminals
	# определяем имя файла 
	files = df_files.loc[(df_files['type'] == 'terminals') & (df_files['extension'] == 'xlsx'), ['file','date']]
	file_name_terminals = files.iat[0, 0]
	date = files.iat[0, 1]

	# создаем датафрейм с данными из файла и записываем их в таблицу
	df = pd.read_excel(path_of_directory + file_name_terminals, header=0, index_col=None)
	cursor.executemany('''
		INSERT INTO de3hd.s_23_STG_TRMNLS(terminal_id, terminal_type, terminal_city, terminal_address)
		VALUES (?, ?, ?, ?)
	''', df.values.tolist())

	# переименовываем и перемещаем файл в archive
	os.replace(path_of_directory + file_name_terminals, path_to_directory + file_name_terminals + '.backup')
	

	#  2.3. Passport_blacklist
	# определяем имя файла 
	files = df_files.loc[(df_files['type'] == 'passport') & (df_files['extension'] == 'xlsx'), ['file','date']]
	file_name_passport = files.iat[0, 0]
	date = files.iat[0, 1]

	# создаем датафрейм с данными из файла и записываем их в таблицу
	df = pd.read_excel(path_of_directory + file_name_passport)
	df['date'] = df['date'].dt.strftime("%d-%m-%Y")
	cursor.executemany('''
		INSERT INTO de3hd.s_23_STG_PSSPRT_BLCKLST(entry_dt, passport_num)
		VALUES (?, ?)
	''', df.values.astype('str').tolist())

	# переименовываем и перемещаем файл в archive
	os.replace(path_of_directory + file_name_passport, path_to_directory + file_name_passport + '.backup')


# 3. Добавляем данные в таблицы фактов
def entry_fact():
	# 3.1. Transactions
	cursor.execute('''
		INSERT INTO de3hd.s_23_DWH_FACT_TRNSCTNS
		SELECT *
		FROM de3hd.s_23_STG_TRNSCTNS
	''')


# 4. Добавляем данные в историческую таблицу de3hd.s_23_DWH_DIM_PSSPRT_BLHIST 
def entry_hist():
	
	# 4.2.1. Определяем новые записи
	cursor.execute('''
		CREATE TABLE de3hd.s_23_STG_NEW_TMP_PSSPRT_BL as
			SELECT 
				t1.passport_num,
				t1.entry_dt
			FROM de3hd.s_23_STG_PSSPRT_BLCKLST t1
			LEFT JOIN de3hd.s_23_DWH_DIM_PSSPRT_BL_HIST t2
				ON t1.passport_num = t2.passport_num 
				AND t2.deleted_flg = 0
				AND current_timestamp BETWEEN t2.effective_from_dttm AND t2.effective_to_dttm
			WHERE t2.passport_num is null
	''')

	# 4.2.2. Определяем удаленные из черного списка записи
	cursor.execute('''
		CREATE TABLE de3hd.s_23_STG_DEL_TMP_PSSPRT_BL as
			SELECT 
				t1.passport_num,
				t1.entry_dt
			FROM de3hd.s_23_DWH_DIM_PSSPRT_BL_HIST t1
			LEFT JOIN de3hd.s_23_STG_PSSPRT_BLCKLST t2
				ON t1.passport_num = t2.passport_num 
				AND t1.deleted_flg = 0
				AND current_timestamp BETWEEN t1.effective_from_dttm AND t1.effective_to_dttm
			WHERE t1.passport_num is null
	''')

	# 4.2.3 закрываем актуальность удаленных записей
	cursor.execute('''
		UPDATE de3hd.s_23_DWH_DIM_PSSPRT_BL_HIST
		SET effective_to_dttm = TRUNC(SYSDATE - 1)
		WHERE passport_num IN 
			(SELECT passport_num FROM de3hd.s_23_STG_DEL_TMP_PSSPRT_BL)
		AND effective_to_dttm = to_date('2999-12-31', 'YYYY.MM.DD') 
	''')


	# 4.2.4. Добавляем новые записи в итоговую таблицу с черным списком паспортов
	cursor.execute('''
		INSERT INTO de3hd.s_23_DWH_DIM_PSSPRT_BL_HIST (entry_dt, passport_num, effective_from_dttm)
		SELECT 
			entry_dt,
			passport_num,
			entry_dt
		FROM de3hd.s_23_STG_NEW_TMP_PSSPRT_BL
	''')


	# 4.2.5. Добавляем удаленные записи в итоговую таблицу с черным списком паспортов
	# и логически удаляем их
	cursor.execute('''
		INSERT INTO de3hd.s_23_DWH_DIM_PSSPRT_BL_HIST (entry_dt, passport_num, deleted_flg)
		SELECT 
			entry_dt,
			passport_num,
			1
		FROM de3hd.s_23_STG_DEL_TMP_PSSPRT_BL
	''')


# 5. Создаем отчет по мошенническим операциям
# 5.1. Данные по мошенническим операциям собираем во временной таблице de3hd.s_23_REP_FRAUND_NEW
def create_report():

	#  5.1.1. Совершение операции при просроченном или заблокированном паспорте
	#  Принимаем, что операции, совершенные в день окончания срока действия паспорта, валидны
	cursor.execute('''
		INSERT INTO de3hd.s_23_REP_FRAUND_NEW(event_dt, passport, fio, phone, event_type)
			SELECT
				t1.trans_date AS event_dt,
				t4.passport_num AS passport,
				(t4.last_name||' '||t4.first_name||' '||t4.patrinymic) AS fio,
				t4.phone,
				'Совершение операции при просроченном или заблокированном паспорте' AS event_type
			FROM de3hd.s_23_STG_TRNSCTNS t1
			INNER JOIN de3hd.s_23_DWH_DIM_CRDS t2 ON t1.card_num = trim(t2.card_num)
			INNER JOIN de3hd.s_23_DWH_DIM_CCNTS t3 ON t2.account_num = t3.account_num
			INNER JOIN de3hd.s_23_DWH_DIM_CLNTS t4 ON t3.client = t4.client_id
			WHERE (t4.passport_num IN (
				SELECT 
					passport_num
				FROM de3hd.s_23_STG_PSSPRT_BLCKLST
				)
			) OR t4.passport_valid_to + INTERVAL '0 23:59:59' DAY TO SECOND < t1.trans_date
			ORDER BY event_dt
	''')

	#  5.1.2. Совершение операции при недействующем договоре
	#  Принимаем, что операции, совершенные в день окончания срока действия договора, валидны
	cursor.execute('''
		INSERT INTO de3hd.s_23_REP_FRAUND_NEW(event_dt, passport, fio, phone, event_type)
			SELECT
				t1.trans_date AS event_dt,
				t4.passport_num AS passport,
				(t4.last_name||' '||t4.first_name||' '||t4.patrinymic) AS fio,
				t4.phone,
				'Совершение операции при недействующем договоре' AS event_type
			FROM de3hd.s_23_STG_TRNSCTNS t1
			INNER JOIN de3hd.s_23_DWH_DIM_CRDS t2 ON t1.card_num = trim(t2.card_num)
			INNER JOIN de3hd.s_23_DWH_DIM_CCNTS t3 ON t2.account_num = t3.account_num
			INNER JOIN de3hd.s_23_DWH_DIM_CLNTS t4 ON t3.client = t4.client_id
			WHERE t3.valid_to + INTERVAL '0 23:59:59' DAY TO SECOND < t1.trans_date
			ORDER BY event_dt
		''')

	# 5.1.3. Совершение операций в разных городах в течении одного часа
	# Для обнаружения данного и следующего нарушения используем историческую таблицу фактов, чтобы иметь
	# возможность отследить операции около полуночи предыдущих суток
	cursor.execute('''
		INSERT INTO de3hd.s_23_REP_FRAUND_NEW(event_dt, passport, fio, phone, event_type)
			SELECT
				t1.trans_date AS event_dt,
				t4.passport_num AS passport,
				(t4.last_name||' '||t4.first_name||' '||t4.patrinymic) AS fio,
				t4.phone,
				'Совершение операций в разных городах в течении одного часа' AS event_type
			FROM de3hd.s_23_DWH_FACT_TRNSCTNS t1
			INNER JOIN de3hd.s_23_DWH_DIM_CRDS t2 ON t1.card_num = trim(t2.card_num)
			INNER JOIN de3hd.s_23_DWH_DIM_CCNTS t3 ON t2.account_num = t3.account_num
			INNER JOIN de3hd.s_23_DWH_DIM_CLNTS t4 ON t3.client = t4.client_id
			WHERE t1.trans_id IN (
				SELECT 
					trans_id
				FROM (
					SELECT 
						t1.trans_id,
						t1.trans_date,
						t2.terminal_city, 
						t1.card_num,
						lag(t2.terminal_city) over(partition by t1.card_num order by t1.trans_date) AS lag_terminal_city,
						lag(t1.trans_date) over(partition by t1.card_num order by t1.trans_date) AS lag_trans_date
					FROM de3hd.s_23_DWH_FACT_TRNSCTNS t1
					INNER JOIN de3hd.s_23_STG_TRMNLS t2 ON t1.terminal = t2.terminal_id
					)
				WHERE terminal_city <> lag_terminal_city
				AND (lag_trans_date - trans_date) DAY TO SECOND <= INTERVAL '60' MINUTE
				)
			ORDER BY event_dt
		''')

	# 5.1.4. Попытка подбора суммы
	cursor.execute('''
		INSERT INTO de3hd.s_23_REP_FRAUND_NEW(event_dt, passport, fio, phone, event_type)
			SELECT
				t1.trans_date AS event_dt,
				t4.passport_num AS passport,
				(t4.last_name||' '||t4.first_name||' '||t4.patrinymic) AS fio,
				t4.phone,
				'Попытка подбора суммы' AS event_type
			FROM de3hd.s_23_DWH_FACT_TRNSCTNS t1
			INNER JOIN de3hd.s_23_DWH_DIM_CRDS t2 ON t1.card_num = trim(t2.card_num)
			INNER JOIN de3hd.s_23_DWH_DIM_CCNTS t3 ON t2.account_num = t3.account_num
			INNER JOIN de3hd.s_23_DWH_DIM_CLNTS t4 ON t3.client = t4.client_id
			WHERE t1.trans_id IN (
				SELECT
					trans_id
				FROM (
					SELECT 
						trans_id,
						trans_date,
						amt,
						card_num,
						oper_result,
						lag(trans_date) over(partition by card_num order by trans_date) as lag_trans_date_1,
						lag(trans_date, 2) over(partition by card_num order by trans_date) as lag_trans_date_2,
						lag(trans_date, 3) over(partition by card_num order by trans_date) as lag_trans_date_3,
						amt - (lag(amt) over(partition by card_num order by trans_date)) as delta_amt_1,
						(lag(amt) over(partition by card_num order by trans_date)) - 
									(lag(amt, 2) over(partition by card_num order by trans_date)) as delta_amt_2,
						(lag(amt, 2) over(partition by card_num order by trans_date)) - 
									(lag(amt, 3) over(partition by card_num order by trans_date)) as delta_amt_3,                
						lag(oper_result) over(partition by card_num order by trans_date) as lag_oper_result_1,
						lag(oper_result, 2) over(partition by card_num order by trans_date) as lag_oper_result_2,
						lag(oper_result, 3) over(partition by card_num order by trans_date) as lag_oper_result_3
					FROM de3hd.s_23_DWH_FACT_TRNSCTNS
					)
				WHERE oper_result = 'SUCCESS' AND lag_oper_result_1 = 'REJECT' 
				AND lag_oper_result_2 = 'REJECT' AND lag_oper_result_3 = 'REJECT'
				AND delta_amt_1 < 0 AND delta_amt_2 < 0 AND delta_amt_3 < 0 
				AND (trans_date - lag_trans_date_3) DAY TO SECOND <= INTERVAL '20' MINUTE
			)
		''')


# 6. Добавляем новые записи из таблицы de3hd.s_23_REP_FRAUND_NEW в итоговую таблицу de3hd.s_23_REP_FRAUND
def create_new_rows_to_report():
	
	# 6.1. Определяем новые записи и заносим их во временную таблицу de3hd.s_23_TMP_RP_FRND_NW
	cursor.execute('''
		CREATE TABLE de3hd.s_23_TMP_RP_FRND_NW as
			SELECT 
				t1.event_dt,
				t1.passport,
				t1.fio,
				t1.phone,
				t1.event_type,
				t1.report_dt
			FROM de3hd.s_23_REP_FRAUND_NEW t1
			LEFT JOIN de3hd.s_23_REP_FRAUND t2
			ON t1.event_dt = t2.event_dt AND t1.passport = t2.passport
			WHERE t2.event_dt is null
	''')

	# 6.2. Добавляем новые записи в итоговую таблицу с мошенническими операциями
	cursor.execute('''
		INSERT INTO de3hd.s_23_REP_FRAUND (
			event_dt,
			passport,
			fio,
			phone,
			event_type,
			report_dt
		) SELECT 
			event_dt,
			passport,
			fio,
			phone,
			event_type,
			report_dt
		FROM de3hd.s_23_TMP_RP_FRND_NW
	''')


# 7. Удаление временных таблиц
# 7.1. Таблицы отчета 
def delete_tmp_report():
	cursor.execute('DROP TABLE de3hd.s_23_TMP_RP_FRND_NW')
	cursor.execute('DROP TABLE de3hd.s_23_REP_FRAUND_NEW')
	
# 7.2. стейджинговые таблицы
def delete_table_STG():
	cursor.execute('DROP TABLE de3hd.s_23_STG_TRNSCTNS')
	cursor.execute('DROP TABLE de3hd.s_23_STG_TRMNLS')
	cursor.execute('DROP TABLE de3hd.s_23_STG_PSSPRT_BLCKLST')

# 7.3. временные таблицы tmp и представление Passport_blasklist
def delete_tmp_passport_blacklist():
	cursor.execute('DROP TABLE de3hd.s_23_STG_NEW_TMP_PSSPRT_BL')
	cursor.execute('DROP TABLE de3hd.s_23_STG_DEL_TMP_PSSPRT_BL')


#  8. Пути до директорий
path_of_directory = '/home/de3hd/s_23/input_data/'
path_to_directory = '/home/de3hd/s_23/archive/'


# 9. Вызов функций
py_scripts.init_tables.init_tables_STG()
py_scripts.init_tables.init_tables_DWH_DIM()
py_scripts.init_tables.init_tables_DWH_FACT()
py_scripts.init_tables.init_tables_DWH_DIM_HIST()
py_scripts.init_tables.init_report()
load_stg(path_of_directory, path_to_directory)
entry_fact()
entry_hist()
create_report()
create_new_rows_to_report()
delete_table_STG()
delete_tmp_report()
delete_tmp_passport_blacklist()













# для отладки процесса
# def delete_table_DWH_FACT():
# 	cursor.execute('DROP TABLE de3hd.s_23_DWH_FACT_TRNSCTNS')

# def delete_table_report():
# 	cursor.execute('DROP TABLE de3hd.s_23_REP_FRAUND')

# def delete_report_new():
# 	cursor.execute('DROP TABLE de3hd.s_23_REP_FRAUND_NEW')

# delete_table_report()
# delete_table_DWH_FACT()
# delete_report_new()