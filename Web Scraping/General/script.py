from fileinput import filename
# from turtle import update
import gspread
import json
import time
import datetime

sa = gspread.service_account()
sh = sa.open("Spark! Mentor Sheets")

wks = sh.worksheet("Final Result")
print()

# f = open("PhD.json")
# data = json.load(f)

# currRow = 79

# for x in data['data']:
#     print(x['name'])
#     range = 'A{0}:F{0}'.format(str(currRow))
#     updateVal = [[x['name'], x['institution'], x['position'], x['description'], x['contact'], x['personal page']]]
#     print(updateVal)
#     wks.update(range, updateVal)
#     currRow += 1
#     time.sleep(1) # google limits per minute per user per project write requests to 60

# print('Rows: ', wks.row_count)
# print('Cols: ', wks.col_count)

# print(wks.acell('A1').value)
# print(wks.cell(3, 4).value)

emails = wks.get("A2:C282")
emails = [(x[0], x[1].lower(), x[2]) for x in emails]
print(emails)
for e in emails:
    tstamp = datetime.datetime.strptime(e, )
emailCount = {}

# for e in emails:
#     emailCount[e[0]] = e[1]

# print(emailCount)
# print(len(emailCount))

# currRow = 2

# for c in emailCount:
#     print(c)
#     range = 'C{0}'.format(str(currRow))
#     updateVal = [[emailCount[c]]]
#     print(updateVal)
#     metadata.update(range, updateVal)
#     currRow += 1
#     time.sleep(1) # google limits per minute per user per project write requests to 60

# print(wks.get_all_records())
# print(wks.get_all_values())

# wks.update('A1', 'test')
# wks.update('D2:E3', [['Engineering', 'Tennis'], ['Business', 'Pottery']])
# wks.update('F2', '=UPPER(E2)', raw=False)

# wks.delete_rows(1)