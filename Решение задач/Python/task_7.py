'''  7. Группировка
Вам дана информация о посадочных талонах. Необходимо сгруппировать данные по вылетам - для каждого рейса определить, 
какие места были куплены. Более формально: для одного flight_id собрать все возможные seat_no.

Формат входных данных:
На первой строчке записано натуральное число N. На последующих N строчках записаны данные об очередном талоне.
Порядок полей в строчке: ticket_no, flight_id, boarding_no, seat_no. Поле flight_id содержит натуральное число.
Поле seat_no содержит номер места. Все поля разделены одной запятой. В самих данных запятых нет.

Формат выходных данных:
Пары строк - на первой строке очередной flight_id, а на второй строке все seat_no через запятую. Выводить flight_id необходимо 
по возрастанию (как числа). Номера мест seat_no внутри одного рейса оставить таким же, как и во входных данных.

Пример входных данных:
5
EXGJGJ521,3,252st,10;C
2Jw2n5l,3,252st,16;F
KUIK2YL,1,Номер:327ggs,30;A
8XSOVGVNDQ,1,Номер:327ggs,51;A
DRXGH62d,5,7733d,62;A

Пример выходных данных:
1
30;A,51;A
3
10;C,16;F
5
62;A
'''


N = int(input())
d = {}
for _ in range(N):
    list_input = input().split(',')
    flight_id = int(list_input[1])
    seat_no = str(list_input[3])
     
    # создан словарь, где ключ - номер места, а значение - номер рейса
    d[seat_no] = flight_id
    
keys = list(d.keys())  # ключи = места
values = list(d.values())  # значения = id самолетов

# множество уникальных упорядоченных значений id самолетов
flight_id_list = list(set(values))
flight_id_list.sort()
ticketlist = []

for num in flight_id_list:
    print(num)
    for i in range(len(keys)):
        if num == values[i]:
            ticketlist.append(keys[i])
    print(",".join(ticketlist))
    ticketlist.clear()



