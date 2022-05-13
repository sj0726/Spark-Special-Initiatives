from fileinput import filename
import gspread
import json
import time

sa = gspread.service_account()
sh = sa.open("Central Candidates List")

wks = sh.worksheet("Sheet1")

f = open("berkeley2020.json", "r")
data = json.load(f)

currRow = 1174

for x in data['data']:
    print(x['name'])
    range = 'A{0}:F{0}'.format(str(currRow))
    updateVal = [[x['name'], x['institution:'], x['position'], x['description'], x['contact'], x['personal page']]]
    print(range)
    print(updateVal)
    wks.update(range, updateVal)
    currRow += 1
    time.sleep(1) # google limits per minute per user per project write requests to 60

# print('Rows: ', wks.row_count)
# print('Cols: ', wks.col_count)

# print(wks.acell('A1').value)
# print(wks.cell(3, 4).value)

# print(wks.get("A7:E9"))

# print(wks.get_all_records())
# print(wks.get_all_values())

# wks.update('A1', 'test')
# wks.update('D2:E3', [['Engineering', 'Tennis'], ['Business', 'Pottery']])
# wks.update('F2', '=UPPER(E2)', raw=False)

# wks.delete_rows(1)