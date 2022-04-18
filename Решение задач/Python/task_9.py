''' 9. Полеты по расписанию
Вам даны данные о рейсах:
1. scheduled_departure - Время вылета по расписанию
2. scheduled_arrival - Время прилёта по расписанию
3. actual_departure - Фактическое время вылета
4. actual_arrival - Фактическое время прилёта

Считается, что самолет выполнил рейс по расписанию, если фактическое время отличаются меньше, чем на 30 минут от времени по расписанию 
(надо учитывать разницу как для вылета, так и прилета). Другими словами и для вылета и для прилета разница во времени должна быть 
меньше, чем 1800 секунд. Определите по данным, успел ли совершиться полет по расписанию.

Формат входных данных:
На первой строчке записано натуральное число N. На последующих N строчках записаны данные об очередном полете.
Порядок полей в строчке: scheduled_departure, scheduled_arrival, actual_departure, actual_arrival.
Все поля разделены одной запятой. В самих данных запятых нет.
Время во всех полях записано в формате: ГГГГ-ММ-ДДTЧЧ:ММ

Формат выходных данных:
N строчек. На каждой строчке Yes, если соответствующий рейс успел по расписанию и No наоборот.

Пример входных данных:
3
2020-07-18T16:00,2020-07-18T19:00,2020-07-18T16:20,2020-07-18T19:10
2020-07-18T16:00,2020-07-18T19:50,2020-07-18T16:20,2020-07-18T19:10
2020-07-18T16:00,2020-07-18T19:00,2020-07-18T16:20,2020-07-18T19:50

Пример выходных данных:
Yes
No
No
'''


def date_time(N):
    N_list = N.split('T')
    n = N_list[0].split('-')
    m = N_list[1].split(':')
    y = int(n[0])
    mon = int(n[1])
    if int(n[1][0]) == 0:
        mon = int(n[1][1])
    d = int(n[2])
    h = int(m[0])
    if int(m[0][0]) == 0:
        h = int(m[0][1])
    mnt = int(m[1])

    return datetime(y, mon, d, h, mnt)

N = int(input())
from datetime import *
for i in range(N):
    str_input = input().split(',')
    list_input = [str_input[i] for i in range(len(str_input))]
    scheduled_departure = list_input[0]
    scheduled_arrival = list_input[1]
    actual_departure = list_input[2]
    actual_arrival = list_input[3]

    sched_dep = date_time(scheduled_departure)
    sched_arr = date_time(scheduled_arrival)
    act_dep = date_time(actual_departure)
    act_arr = date_time(actual_arrival)

    delta1 = act_dep - sched_dep
    delta2 = act_arr - sched_arr

    if abs(round(delta1.total_seconds(), 0)) < 1800 and abs(round(delta2.total_seconds(), 0)) < 1800:
        print('Yes')
    else:
        print('No')

