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
