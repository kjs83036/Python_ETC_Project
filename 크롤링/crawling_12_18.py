# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 10:02:24 2019

@author: sktlrkan
"""


from bs4 import BeautifulSoup
from tqdm import tqdm
from datetime import datetime
import requests
import pandas
import numpy


class Alba():
    def __init__(self):

        self.flag = False
        self.result_list = []
        self.words = ["물류", "상차", "하차", "상하차", "투잡", "배달", "식기",
                     "세척", "발렛", "쿠팡", "남여", "드라마", "품평회", "허브",
                     "생동성", "임상시험", "전화", "서빙", "엑스트라", "영화",
                     "조리보조", "주방", "남녀", "고3", "피킹", "Picking",
                     "냉장", "오렌지라이프", "누구나", "택배", "분류",
                      "연회장", "판매", "포장"]
        self.data = pandas.DataFrame(columns=["title", "area", "pay", "time", "recently", "link", "lable"])

    def crawler(self, number_pages):

        for page in tqdm(range(1, number_pages+1)):
            req = requests.get('http://www.albamon.com/list/gi/mon_gi_list.asp?page=' + str(page) +
                               '&gubun=2&ps=50&ob=6&lvtype=1&rArea=,I000&sDutyTerm=,5,10,20&gender=M&gender_chk=1&rAge=31&rAge_Chk=1&rWDate=1&Empmnt_Type=&tc=529')
            req.encoding = None
            html = req.text
            soup = BeautifulSoup(html, 'html.parser')
            result_title = soup.select("#subcontent > form > div.gListWrap > table > tbody > tr > td.subject > div > p.cTit > a")
            result_area = soup.select("#subcontent > form > div.gListWrap > table > tbody > tr > td.area > div")
            result_pay = soup.select("#subcontent > form > div.gListWrap > table > tbody > tr > td.pay > p > img")
            result_recently = soup.select("#subcontent > form > div.gListWrap > table > tbody > tr > td.recently > em")

            for i in range(len(result_title)):
                self.data = self.data.append({"title": result_title[i].text,
                                              "area": result_area[i].text,
                                              "pay": result_pay[i]['alt'],
                                              "time": result_pay[i].findNext("td").text,
                                              "recently": result_recently[i].text,
                                              "link": "http://www.albamon.com/" + result_title[i]["href"],
                                              "lable" : True
                                              },
                                             ignore_index=True
                                             )
        pandas.DataFrame.to_csv(self.data, "alba.csv")
        print("\n", "crawling complete")


    def modifier(self):
        self.data["area"] = self.data["area"].apply(lambda x: x[6:-1] if True else x)
        self.data["time"] = self.data["time"].apply(lambda x: x[7:-7] if True else x)
        # self.data["recently"] = self.data["recently"].apply(lambda x: str(datetime.now().hour+9) + "시" + str(datetime.now().minute - int(x[:2])) + "분" if x[-2:] == "분전" and len(x) == 4 else x)
        # self.data["recently"] = self.data["recently"].apply(lambda x: str(datetime.now().hour+9) + "시" + str(datetime.now().minute - int(x[0])) + "분" if x[-2:] == "분전" and len(x) == 3 else x)
        # self.data["recently"] = self.data["recently"].apply(lambda x: str(datetime.now().hour+9 - int(x[0])) + "시" + str(datetime.now().minute)+ "분" if x[-2:] == "간전" else x)

        print("\n","modifier complete")

    def filter(self):

        for i in range(len(self.data)):
            for j in self.words:
                if j in self.data.title[i]:
                    self.data.lable[i] = False
                    continue

        print("\n","filter complete")

    def print_result(self):

        data_result = self.data.loc[self.data.lable, :]
        return data_result


alba = Alba()
alba.crawler(2)
alba.modifier()
alba.filter()
result = alba.print_result()
print(result)

pandas.DataFrame.to_excel(result, "alba.xls")
