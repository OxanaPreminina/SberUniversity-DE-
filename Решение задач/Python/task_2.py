''' 2. Вещественное сравнение

Необходимо реализовать функцию is_bigger(num1, num2, eps).
Эта функция принимает 3 параметра:
1. num1 - первое вещественное число
2. num2 - второе вещественное число
3. eps - эпсилон (вещественное число).

Эта функция возвращает логическое True, если число num1 больше или равно num2 хотя бы на епсилон. 
В противном случае она должна вернуть логическое False.

Пример входных данных для функции:
0.6 0.5 0.01
1.0 0.9 0.3
1.0 0.9 0.1

Пример результата работы функции:
True
False
True '''



def is_bigger(num1, num2, eps):
    x = len(str(eps).split('.')[1].rstrip('0'))
    y = len(str(num1).split('.')[1].rstrip('0'))
    z = len(str(num2).split('.')[1].rstrip('0'))
    cnt = max(x, y, z)
    return True if round((num1 - num2), cnt) >= round(eps, cnt) else False


n1 = float(input())
n2 = float(input())
e = float(input())

print(is_bigger(n1, n2, e))
