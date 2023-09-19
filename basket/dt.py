from datetime import datetime

d1 = datetime(2023, 9, 14, 13, 50)
dc = datetime.now()

t = (dc - d1).seconds

print(t)
