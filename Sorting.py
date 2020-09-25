import pandas as pd

class Sorting:
    __sorting_df = pd.DataFrame()
    __current_price = 0
    __nDataCnt = 0

    def __init__(self, df, price):
        self.__sorting_df = df
        self.__current_price = price
        self.__nDataCnt = len(self.__sorting_df.columns)

    # Finding underestimated stock by indexes in the FS
    def algorithm(self):
        bCheckROE = True
        bCheckBPS = True
        bCheckEPS = True
        bCheckPER = True
        bCheckPBR = True
        bCheckROP = True
        bCheckNPM = True
        bCheckDR = True
        bCheckRR = True
        nEmptyROEcnT = 0
        nEmptyBPScnT = 0
        nEmptyEPScnT = 0
        nEmptyPERcnT = 0
        nEmptyPBRcnT = 0 
        nEmptyROPcnT = 0
        nEmptyNPMcnT = 0
        nEmptyDRcnT = 0
        nEmptyRRcnT = 0

        for col in range(self.__nDataCnt):
            ROE = self.__sorting_df.loc['ROE'][col].replace(',', '')
            EPS = self.__sorting_df.loc['EPS'][col].replace(',', '')
            BPS = self.__sorting_df.loc['BPS'][col].replace(',', '')
            PER = self.__sorting_df.loc['PER'][col].replace(',', '')
            PBR = self.__sorting_df.loc['PBR'][col].replace(',', '')
            ROP = self.__sorting_df.loc['ROP'][col].replace(',', '')
            NPM = self.__sorting_df.loc['NPM'][col].replace(',', '')
            DR = self.__sorting_df.loc['DR'][col].replace(',', '')
            RR = self.__sorting_df.loc['RR'][col].replace(',', '')

            # ROE(자기자본이익률) : 15 ~ 30%
            if(ROE != "" and ROE != "-"):
                if(float(ROE) < 15 or float(ROE) > 30):
                    bCheckROE = False
            else: nEmptyROEcnT += 1 
                
            #적정주가 1 : EPS * ROE(100)
            if(BPS != "" and BPS != "-"):
                # EPS(주당 순이익) : EPS*ROE = 적정주가
                if(ROE != "" and ROE != "-"):
                    mEPS = float(BPS)*float(ROE)/100 
                    if(float(mEPS) * float(ROE) < 0.95*self.__current_price):
                        bCheckBPS = False
            else: nEmptyBPScnT += 1

            # PER : 15이하 #EPS 개정(EPS = BPS * ROE)
            if(PER != "" and PER != "-"):
                if(float(PER) > 15):
                    bCheckPER = False
                #  # 적정주가 2, EPS(주당 순이익) : EPS*PER = 적정주가 
                if(EPS != "" and EPS != "-"):
                    if(float(EPS) * float(PER) < 0.95*self.__current_price):
                        bCheckEPS = False
                else: nEmptyEPScnT += 1
            else: nEmptyPERcnT += 1

            # PBR(주가순자산비율) : 1.5 이하
            if(PBR != "" and PBR != "-"):
                if(float(PBR) > 0.8):
                    bCheckPBR = False
            else: nEmptyPBRcnT += 1

            #영업이익율 : 5% 이상
            if(ROP != "" and ROP != "-"):
                if(float(ROP) < 6):
                    bCheckROP = False
            else: nEmptyROPcnT += 1

            #순이익율 : 5% 이상
            if(NPM != "" and NPM != "-"):
                if(float(NPM) < 6):
                    bCheckNPM = False
            else: nEmptyNPMcnT += 1
            
            #부채율 : 200% 이하
            if(DR != "" and DR != "-"):
                if(float(DR) > 180):
                    bCheckDR = False
            else: nEmptyDRcnT += 1
            
            #자본유보율 : 1000% 이상
            if(RR != "" and RR != "-"):
                if(float(RR) < 1100):
                    bCheckRR = False
            else: nEmptyRRcnT += 1

            #매출액  : PSR = 현재 주가 / 주당 매출액 < 0.75 //
            #상장주식수 //
            #PEGR : PER / EPS성장율평균 (3~5년 EPS성장률 기하평균) //

            # If empty table, do not append on the underestimated stock list
        if(nEmptyROEcnT >= self.__nDataCnt): bCheckROE = False
        if(nEmptyBPScnT >= self.__nDataCnt): bCheckBPS = False
        if(nEmptyEPScnT >= self.__nDataCnt): bCheckEPS = False
        if(nEmptyPERcnT >= self.__nDataCnt): bCheckPER = False
        if(nEmptyPBRcnT >= self.__nDataCnt): bCheckPBR = False
        if(nEmptyROPcnT >= self.__nDataCnt): bCheckROP = False 
        if(nEmptyNPMcnT >= self.__nDataCnt): bCheckNPM = False 
        if(nEmptyDRcnT >= self.__nDataCnt): bCheckDR = False 
        if(nEmptyRRcnT >= self.__nDataCnt): bCheckRR = False  

        return [bCheckROE, bCheckEPS, bCheckPER, bCheckPBR, bCheckROP, bCheckNPM, bCheckDR, bCheckRR]