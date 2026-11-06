import sys, openpyxl
p=sys.argv[1]; wb=openpyxl.load_workbook(p,read_only=True); ws=wb.worksheets[0]
rows=list(ws.iter_rows(min_row=2,max_row=4,values_only=True))
for j in range(int(sys.argv[2]),len(rows[0])):
    print(j,[rows[k][j] for k in range(3)])
