''' 4. Дубликаты

К сожалению, обнаружилось, что в данных о посадочных талонах есть дубликаты (повторяющиеся значения).
Дубликатом считаются строки, у которых одинаковы одновременно поля ticket_no и flight_id. Необходимо убрать дубликаты строк 
и оставить только первые вхождения. Порядок записей менять не надо.

Формат входных данных:
На первой строчке записано натуральное число N. На последующих N строчках записаны данные об очередном талоне.
Порядок полей в строчке: ticket_no, flight_id, boarding_no, seat_no. Все поля разделены одной запятой. В самих данных запятых нет.

Формат выходных данных:
Необходимо вывести все исходные строчки, без дубликатов. В каждой строчке записаны исходные поля ticket_no, 
flight_id, boarding_no, seat_no. Все поля разделены одной запятой.

Пример входных данных:
7
EXGJGJ521,1,252st,10;C
EXGJGJ521,1,252st,11;C
2Jw2n5l,2,753ss,16;F
KUIK2YL,3,327ggs,30;A
KUIK2YL,3,328ggs,30;B
8XSOVGVNDQ,4,mn001,51;A
DRXGH62d,5,7733d,62;A

Пример выходных данных:
EXGJGJ521,1,252st,10;C
2Jw2n5l,2,753ss,16;F
KUIK2YL,3,327ggs,30;A
8XSOVGVNDQ,4,mn001,51;A
DRXGH62d,5,7733d,62;A
'''


N = int(input())
list_output = [1, 2]
for i in range(N):
    list_input = input().split(',')
    ticket_no = str(list_input[0])
    flight_id = int(list_input[1])
    if ticket_no == list_output[0] and flight_id == list_output[1]:
        continue
    
    boarding = str(list_input[2])
    seat_no = str(list_input[3])

    list_output = [ticket_no, flight_id, boarding, seat_no]

    print(*list_output, sep=',', end='\n')
