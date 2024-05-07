import calendar
import datetime

now_month = datetime.datetime.now().month
now_year = datetime.datetime.now().year

print(calendar.month(now_year, now_month, 0, 0))
