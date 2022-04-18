''' 6. Фильтрация
Задан набор flight_id, которые интересуют нас для дальнейшей работы. Необходимо отфильтровать исходный набор данных по этим flight_id.
Другими словами вывести только те записи, у которых flight_id один из интересующих (см. формат входных данных).

Формат входных данных:
На первой строчке записаны интересующие flight_id, разделенные запятой. На второй строчке записано натуральное число N.
На последующих N строчках записаны данные об очередном талоне. Порядок полей в строчке: ticket_no, flight_id, boarding_no, seat_no.
Все поля разделены одной запятой. В самих данных запятых нет.

Формат выходных данных:
Необходимо вывести те строчки, чьи flight_id подходят под условие. Порядок строк оставить такой же, как и во входных данных.

Пример входных данных:
1,2
5
EXGJGJ521,1,252st,10;C
2Jw2n5l,2,753ss,16;F
KUIK2YL,3,327ggs,30;A
8XSOVGVNDQ,4,mn001,51;A
DRXGH62d,5,7733d,62;A

Пример выходных данных:
EXGJGJ521,1,252st,10;C
2Jw2n5l,2,753ss,16;F
'''



string = input().split(',')
N = int(input())

model = [int(string[i]) for i in range(len(string))]
for i in range(N):
    list_input=input().split(',')
    ticket_no=str(list_input[0])
    flight_id = int(list_input[1])
    if flight_id not in model:
        continue
    
    boarding=str(list_input[2])
    seat_no=str(list_input[3])

    list_output=[ticket_no, flight_id, boarding, seat_no]

    print(*list_output, sep=',', end='\n')
