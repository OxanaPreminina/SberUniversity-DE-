N = int(input())
list_output = []
for _ in range(N):
    str_input = input().split(',')
    list_input = [int(str_input[i]) for i in range(len(str_input))]
    for i in range(len(list_input)):
        list_output.append(list_input[i])

import collections
id_cnt = collections.Counter(list_output)

key_list = list(id_cnt.keys())  # список ключей
val_list = list(id_cnt.values())  # список значений

id_in_every = []

# определяем индекс искомого значения и по нему находим искомый ключ
for i in range(len(key_list)):
    if val_list[i] == N:
        id_in_every.append(key_list[i])

id_in_every.sort()

print(*id_in_every, sep=',')

