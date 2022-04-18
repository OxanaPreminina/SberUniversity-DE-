N = int(input())

for _ in range(N):
    info = input().split(',')
    price = info[2].split('.')
    
    print(
        f'Номер бронирования {info[0]}, забронирован {info[1]}. Цена: {price[0]} руб. {price[1]} коп')
print()

    