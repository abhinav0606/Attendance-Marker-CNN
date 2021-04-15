import pandas as pd
import datetime
start_date= datetime.date(2021,4,1)
end_date  = datetime.date(2022,1,1)

dates=[start_date+datetime.timedelta(n) for n in range(int ((end_date - start_date).days))]
date=[]
for i in dates:
    date.append(str(i))
students_id=[]
for i in range(1,81):
    if i in range(10):
        i="0"+str(i)
    students_id.append("b1180"+str(i))
# print(students_id)
dataframe=pd.DataFrame(index=date,columns=students_id)
print(dataframe)
dataframe.to_excel("Attendance.xlsx")