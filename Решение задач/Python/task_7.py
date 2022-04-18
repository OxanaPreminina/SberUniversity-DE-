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



