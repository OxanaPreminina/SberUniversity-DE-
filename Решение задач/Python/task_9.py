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

