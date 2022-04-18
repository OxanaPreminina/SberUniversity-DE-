N = int(input())
cnt_1, cnt_2, cnt_3, cnt_4, cnt_5, cnt_6 = 0, 0, 0, 0, 0, 0
for i in range(N):
    list_input = input().split(',')
    flight_id = int(list_input[0])
    status = str(list_input[1])

    if status == 'Scheduled':
        cnt_1 += 1
    elif status == 'On Time':
        cnt_2 += 1
    elif status == 'Delayed':
        cnt_3 += 1
    elif status == 'Departed':
        cnt_4 += 1
    elif status == 'Arrived':
        cnt_5 += 1
    elif status == 'Cancelled':
        cnt_6 += 1

print(cnt_1, cnt_2, cnt_3, cnt_4, cnt_5, cnt_6, sep='\n')