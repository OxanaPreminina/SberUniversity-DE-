''' 5. Популярный рейс
Необходимо найти идентификатор самого популярного рейса.
Другими словами - тот flight_id, который встречался наибольшее количество раз во входных данных. Если таких рейсов несколько, 
то необходимо вывести их все на одной строке через пробел в порядке возрастания их значения.

Формат входных данных:
На первой строчке записано натуральное число N. На последующих N строчках записаны данные об очередном талоне.
Порядок полей в строчке: ticket_no, flight_id, boarding_no, seat_no. В поле flight_id записано целое число больше 0.
Все поля разделены одной запятой. В самих данных запятых нет.

Формат выходных данных:
Одна строчка, содержащая все flight_id для самых популярных рейсов.
Flight_id разделены пробелом и идут в порядке возрастания значения (как числа).

Пример входных данных:
5
EXGJGJ521,3,252st,10;C
2Jw2n5l,3,252st,16;F
KUIK2YL,1,Номер:327ggs,30;A
8XSOVGVNDQ,1,Номер:327ggs,51;A
DRXGH62d,5,7733d,62;A

Пример выходных данных:
1 3
'''

N = int(input())
list_all_id = []

x = [0]
for i in range(N):
    str_input = input().split(',')
    list_input = [str(str_input[i]) for i in range(len(str_input))]
    list_all_id.append(list_input[1])
    list_all_id = [int(list_all_id[i]) for i in range(len(list_all_id))]
    
from collections import Counter
cnt = Counter(list_all_id).most_common()
popular_flight = [cnt[0][0]]
for i in range(1, len(cnt) + 1):
    if cnt[i][1] == cnt[0][1]:
        popular_flight.append(cnt[i][0])
    else:
        break

for i in range(len(popular_flight)):
    popular_flight[i] = int(popular_flight[i])

popular_flight.sort()

print(*popular_flight, sep=' ')
