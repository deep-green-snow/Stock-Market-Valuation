import pandas as pd 

class CurrentStockPrice:
    __company_code = ""

    def __init__(self, code):
        self.__company_code = code
    
    def __get_url(self): 
        url = 'http://finance.naver.com/item/sise_day.nhn?code={code}'.format(code=self.__company_code)
        return url

    def getPrice(self):
        url = self.__get_url()
        price_df = pd.DataFrame()
        html = ""
        try :
            html = pd.read_html(url, header = 0)
        except Exception as e:
            try:
                print('1st get price error : ', e)
                print('One more connection try')
                html = pd.read_html(url, header = 0) 
            except Exception as e:
                print('2st get price error : ', e)
                return 0
            #print(type(html))
            #print(html)

        # except urllib.error.HTTPError as e:
        #     html = pd.read_html(url, header = 0)[0]
        #     if(html)
        # except urllib.error.URLError as e:
        #     html = pd.read_html(url, header = 0)[0]
        # except socket.timeout as e:
        #     html = pd.read_html(url, header = 0)[0]

        price_df = price_df.append(html[0], ignore_index=True)
        price_df = price_df['종가']
        price = price_df[1]
        return price

