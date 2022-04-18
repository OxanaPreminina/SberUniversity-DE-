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