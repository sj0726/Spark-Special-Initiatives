from fileinput import filename
import gspread

sa = gspread.service_account()
sh = sa.open("WiML Participants List")

wks = sh.worksheet("Sheet1")

print('Rows: ', wks.row_count)
print('Cols: ', wks.col_count)

print(wks.acell('A1').value)
print(wks.cell(3, 4).value)

print(wks.get("A7:E9"))

print(wks.get_all_records())
print(wks.get_all_values())

wks.update('A1', 'test')
wks.update('D2:E3', [['Engineering', 'Tennis'], ['Business', 'Pottery']])
wks.update('F2', '=UPPER(E2)', raw=False)

wks.delete_rows(1)