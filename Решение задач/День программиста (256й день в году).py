# объявление функции
def programmer_day(year):
   if 1700 <= year < 1918:
      if year % 4 != 0:
         day = day_of_year(constant)
      else:
         day = day_of_leap_year(constant)
   if 1918 < year <= 2500:
      if year % 400 == 0 or (year % 4 == 0 and year % 100 != 0):
         day = day_of_leap_year(constant)
      else:
         day = day_of_year(constant)
   if year == 1918:
      months[1] = 15
      day = day_of_year(constant)

   return day
 

 
def day_of_year(day):
   n = 0
   for i in range(len(months)):
      if n < day:
         n += int(months[i])
      else:
         date = day - (n - int(months[i - 1]))
         Monht = Months[i - 1]
         break

   print(date, Monht)
   return


def day_of_leap_year(day):
   n = 0
   for i in range(len(months_leap_year)):
      if n < day:
         n += int(months_leap_year[i])
      else:
         date = day - (n - int(months_leap_year[i - 1]))
         Monht = Months[i - 1]
         break

   print(date, Monht)
   return
 

# считываем данные
Year = int(input())
months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
months_leap_year = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
Months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
constant = 256

# вызываем функцию
print(programmer_day(Year))


