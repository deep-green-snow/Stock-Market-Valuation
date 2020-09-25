import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

class FinancialStatement:
    __company_code = ""

    def __init__(self, code):
        self.__company_code = code
    
    def __htmlParser(self):
        URL = "https://finance.naver.com/item/main.nhn?code=" + str(self.__company_code)
        try:
            url_source = requests.get(URL)
        except Exception as e:
            try:
                print('1st get financial statement error : ', e)
                print('One more connection try')
                url_source = requests.get(URL)
            except Exception as e:
                print('2nd get financial statement error : ', e)
                return None
    
        html = url_source.text
        soup = BeautifulSoup(html, 'html.parser')

        fsArray = soup.select('div.section.cop_analysis div.sub_section')
        
        if(not fsArray):
            return None
        else:
            return soup.select('div.section.cop_analysis div.sub_section')[0]

    def __getDataArray(self, finance_html):
        th_data = [item.get_text().strip() for item in finance_html.select('thead th')]
        annual_date = th_data[3:7]
        quarter_date = th_data[7:13]

        finance_index = [item.get_text().strip() for item in finance_html.select('th.h_th2')][3:]

        finance_data = [item.get_text().strip() for item in finance_html.select('td')]
        finance_data = np.array(finance_data)
        finance_data.resize(len(finance_index), len(annual_date)+len(quarter_date))

        finance_date = annual_date + quarter_date

        return finance_data, finance_index, finance_date

    def getFS(self, select):
        
        finance_html = self.__htmlParser()
        if(finance_html != None):
            finance_data, finance_index, finance_date = self.__getDataArray(finance_html)
            finance = pd.DataFrame(data=finance_data[0:,0:], index= finance_index, columns=finance_date)
        else:
            finance = pd.DataFrame()
    
        
        if(finance.empty):
            #print("Financial Statement doesn't exist")
            return finance
            
        # 필요한 것
        # ROE PER PBR
        finance = finance.loc[['ROE(지배주주)', 'BPS(원)' ,'EPS(원)', 'PER(배)', 'PBR(배)', '영업이익률', '순이익률', '부채비율', '유보율']]
        finance.rename(index = {'ROE(지배주주)' : 'ROE', 'BPS(원)' : 'BPS', 'EPS(원)' : 'EPS', 'PER(배)' : 'PER', 'PBR(배)' : 'PBR', '영업이익률' : 'ROP', '순이익률' : 'NPM', '부채비율' : 'DR', '유보율' : 'RR' }, inplace = True)
        ### 저평가 기준 ###
        # ROE(자기자본이익률) : 15 ~ 30%
        # BPS(Bookvalue per share) : BPS*ROE = EPS, EPS*ROE(100) = 적정주가
        # EPS(주당 순이익) : EPS*PER = 적정주가 
        # PER : 15이하
        # PBR(주가순자산비율) : 1.5 이하
        #영업이익율 : 5% 이상
        #순이익율 : 5% 이상
        #부채율 : 200% 이하
        #자본유보율 : 1000% 이상
        

        
        #필요한 것
        #ROE PER PBR
        
        if(select == "annual"):
            annual_finance = finance.iloc[:,:3]
            return annual_finance
        elif(select == "quarter"):
            quarter_finance = finance.iloc[:, 4:9]
            return quarter_finance
        else:
            return print("Please choose an option whether you want to see a FS annually or quarterly")

