import FinancialStatement
import CurrentStockPrice
import Sorting
import pandas as pd 

code_df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13', header=0)[0] 

# 종목코드가 6자리이기 때문에 6자리를 맞춰주기 위해 설정해줌 
code_df.종목코드 = code_df.종목코드.map('{:06d}'.format)

# 우리가 필요한 것은 회사명과 종목코드이기 때문에 필요없는 column들은 제외해준다.
code_df = code_df[['회사명', '종목코드']]


# 한글로된 컬럼명을 영어로 바꿔준다.
code_df = code_df.rename(columns={'회사명': 'name', '종목코드': 'code'})


# Excel file where I will write the result of analysis
writer = pd.ExcelWriter('가치투자.xlsx', engine='xlsxwriter', datetime_format='yyyy mm')

underEstimated_Diamond = []
underEstimated_Gold = []
underEstimated_Silver = []
underEstimated_Bronze = []

# Exception
# 1. No FS
# 2. Cannot get Price
nNoFS = 0
NoFS = []
nCannotGetPrice = 0
CannotGetPrice = []

for idx in code_df.index:
    company_code = code_df.iloc[idx]['code']
    print(idx, company_code)

    # Get Financial Statement of the company I selected above by code
    fs = FinancialStatement.FinancialStatement(company_code)
    fs_df = fs.getFS('annual')

    # Get current stock price of the company I selected above by code
    csp = CurrentStockPrice.CurrentStockPrice(company_code)
    current_price = csp.getPrice()

    if(fs_df.empty):
        print("Financial Statement doesn't exist")
        nNoFS += 1
        NoFS.append(code_df.iloc[idx]['name'])
        continue

    if(current_price <= 0):
        print("Cannot get price info")
        nCannotGetPrice += 1
        CannotGetPrice.append(code_df.iloc[idx]['name'])
        continue

    check_list = []
    sorting = Sorting.Sorting(fs_df, current_price)
    check_list = sorting.algorithm()  

    # 7~8 : Gold, 5~6 : Silver, 3~4 : Bronze
    if(check_list.count(True) >= 8): underEstimated_Diamond.append(code_df.iloc[idx]['name'])
    elif(check_list.count(True) >= 7): underEstimated_Gold.append(code_df.iloc[idx]['name'])
    elif(check_list.count(True) >= 6): underEstimated_Silver.append(code_df.iloc[idx]['name'])
    elif(check_list.count(True) >= 4): underEstimated_Bronze.append(code_df.iloc[idx]['name'])
    #     fs_df.to_excel(writer, sheet_name = code_df.iloc[idx]['name'])
    #     writer.save()
print("No FinancialStatement : {}".format(nNoFS))
print(NoFS) 
print("Cannot get price info : {}".format(nCannotGetPrice))
print(CannotGetPrice)
print("Diamond(8개 만족) : ",underEstimated_Diamond)
print("Gold(7개 만족) : ",underEstimated_Gold)
print("Silver(6개 만족) : ", underEstimated_Silver)
print("Bronze(4~5개 만족) : ", underEstimated_Bronze)