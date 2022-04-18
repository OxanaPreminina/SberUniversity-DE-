def last_letter_n_item_of_Fibonacci(n):
   for i in range(1, n):
      F.append(F[i] + F[i - 1])
   F_n = F[-2]
   return F_n % 10


# считываем данные
n = int(input())
F = [1, 1]


# вызываем функцию
print(last_letter_n_item_of_Fibonacci(n))
