import pandas as pd

filename = input("파일 이름을 입력해주세요.(확장자까지 ex: test.xls): ")

df_excel = pd.read_excel(filename)

key=df_excel['이용카드']
key_list=set(key.values.tolist())

column=['이용일자','국내/해외','승인번호','이용카드','이용가맹점명','매출구분','할부개월','승인금액/취소(원)','승인금액(USD)','접수/취소']
eng=".xlsx"

for data in key_list:
    excel_name=str(data)+eng
    excel_writer=pd.ExcelWriter(excel_name, engine='xlsxwriter')
    temp=[]
    for i in range(0,df_excel.shape[0]):
        if data == df_excel['이용카드'].loc[i]:
            temp.append(df_excel.loc[i].values.tolist())
    
    df=pd.DataFrame(temp,columns=column)
    df.to_excel(excel_writer, index=False, sheet_name=str(data))
    excel_writer.save()
    print(data,' Save!')
