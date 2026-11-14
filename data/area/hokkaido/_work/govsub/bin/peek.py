import sys, openpyxl
for p in sys.argv[1:]:
    wb=openpyxl.load_workbook(p,read_only=True)
    for ws in wb.worksheets:
        print("==",p.split('/')[-1],ws.title,ws.max_row,ws.max_column)
        for i,r in enumerate(ws.iter_rows(values_only=True)):
            if i<6: print(i+1,[str(c)[:40] if c is not None else '' for c in r][:60])
            else: break
