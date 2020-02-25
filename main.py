import pandas as pd 

code_df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13', header=0)[0] 


# 종목코드가 6자리이기 때문에 6자리를 맞춰주기 위해 설정해줌 
code_df.종목코드 = code_df.종목코드.map('{:06d}'.format)

# 우리가 필요한 것은 회사명과 종목코드이기 때문에 필요없는 column들은 제외해준다.
code_df = code_df[['회사명', '종목코드']]

# 한글로된 컬럼명을 영어로 바꿔준다.
code_df = code_df.rename(columns={'회사명': 'name', '종목코드': 'code'})
#code_df.head()

def get_url(item_name, code_df): 
    code = code_df.query("name=='{}'".format(item_name))['code'].to_string(index=False)
    url = 'http://finance.naver.com/item/sise_day.nhn?code={code}'.format(code=code.lstrip())
    
    print("요청 URL = {}".format(url)) 
    return url

## XlsxWriter 엔진으로 Pandas writer 객체 만들기
writer = pd.ExcelWriter('가치투자.xlsx', engine='xlsxwriter', datetime_format='yyyy mm')

#가치 투자 기업들
my_items = ['NAVER','삼성전자'
            ,'LG유플러스','SK이노베이션','LG전자','카카오',
            'SK텔레콤','현대자동차','한컴MDS','LG화학']

for index, item in enumerate(my_items):
    item_name = item
    url = get_url(item_name, code_df)

    # 일자 데이터를 담을 df라는 DataFrame 정의
    df = pd.DataFrame() 

    # 1페이지에서 20페이지의 데이터만 가져오기
    for page in range(1, 201):
        pg_url = '{url}&page={page}'.format(url=url, page=page)
        df = df.append(pd.read_html(pg_url, header=0)[0], ignore_index=True) 

    # df.dropna()를 이용해 결측값 있는 행 제거
    df = df.dropna() 

    # 한글로 된 컬럼명을 영어로 바꿔줌
    df = df.rename(columns= {'날짜': 'date', '종가': 'close', '전일비': 'diff', '시가': 'open', '고가': 'high', '저가': 'low', '거래량': 'volume'})

    # 데이터의 타입을 int형으로 바꿔줌 
    df[['close', 'diff', 'open', 'high', 'low', 'volume']] = df[['close', 'diff', 'open', 'high', 'low', 'volume']].astype(int) 

    # 컬럼명 'date'의 타입을 date로 바꿔줌 
    df['date'] = pd.to_datetime(df['date']) 

    # 일자(date)를 기준으로 오름차순 정렬 
    df = df.sort_values(by=['date'], ascending=True) 
    
    ## DataFrame을 xlsx에 쓰기
    df.to_excel(writer, sheet_name=item)
    workbook = writer.book
    worksheet = writer.sheets[item]
    chart = workbook.add_chart({'type' : 'line'})
    chart.add_series({
                    'categories': [item, 2, 1, 2001, 1],
                    'values':     [item, 2, 2, 2001, 2],
                    'line':       {'color': 'blue'},
                    })
    chart.set_x_axis({'name': '날짜'})
    chart.set_y_axis({'name': '종가'})
    worksheet.insert_chart('J3', chart)

    ## Pandas writer 객체 닫기
writer.save()
print('done')
