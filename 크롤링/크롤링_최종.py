from bs4 import BeautifulSoup
from tqdm import tqdm
import requests
import pandas


class Alba:

    def __init__(self):
        self.words = ["물류", "상차", "하차", "상하차", "투잡", "배달", "식기",
                      "세척", "발렛", "쿠팡", "남여", "드라마", "품평회", "허브",
                      "생동성", "임상시험", "전화", "서빙", "엑스트라", "영화",
                      "조리보조", "주방", "남녀", "고3", "피킹", "Picking",
                      "냉장", "오렌지라이프", "누구나", "택배", "분류",
                      "연회장", "판매", "포장", "마케팅", "상담", "콜",
                      "AR", "ar", "드라이버", "바운드", "영업", "광고",
                      "촬영", "트레이너", "TM", "접수", "조무사", "조리",
                      "플래너", "야간", "운전", "보안", "주부", "배민",
                      "교육비", "부동산", "면접비", "보너스", "고소득",
                      "보장", "병원", "배송", "연봉", "지원", "남편",
                      "아빠"]

    def crawler(self):
        pass

    def data_to_df(self):
        pass

    def modifier(self):
        pass

    def filter(self):

        for i in range(len(self.data)):
            for j in self.words:
                if j in self.data.title[i]:
                    self.data.label[i] = False
                    continue

        print("\n", "filter complete")


class AlbaHeaven(Alba):

    def __init__(self):
        super().__init__()
        self.data = pandas.DataFrame(
            columns=["title", "area", "officehours", "pay", "recently", "link", "label"])

    def crawler(self, page):

        req = requests.get("http://www.alba.co.kr/job/list/Today.asp?page=" + str(page) + "&pagesize=50&sidocd=&gugun=%C0%FC%C3%BC||&dong=&d_area=&d_areacd=&strAreaMulti=02%7C%7C%C0%FC%C3%BC%7C%7C%2C031%7C%7C%C0%FC%C3%BC%7C%7C&hidJobKind=&hidJobKindMulti=&WorkTime=&searchterm=&AcceptMethod=&ElecContract=&HireTypeCD=&CareerCD=&CareercdUnRelated=&LastSchoolCD=&LastSchoolcdUnRelated=&GenderCD=C01&GenderUnRelated=Y&AgeLimit=0&AgeUnRelated=&PayCD=&PayStart=&WelfareCD=&Special=&WorkWeekCD=&WeekDays=&hidSortCnt=50&hidSortOrder=&hidSortDate=&WorkPeriodCD=&hidSort=&hidSortFilter=Y&hidListView=LIST&WsSrchKeywordWord=&hidWsearchInOut=&hidSchContainText=")
        req.encoding = None
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        result_title = soup.select("#NormalInfo > table > tbody > tr > td.title > a")
        result_area = soup.select("#NormalInfo > table > tbody > tr > td.local.first")
        result_officehours = soup.select("#NormalInfo > table > tbody > tr > td.data ")
        result_pay = soup.select("#NormalInfo > table > tbody > tr > td.pay")
        result_recently = soup.select("#NormalInfo > table > tbody > tr > td.regDate")

        return (result_title, result_area, result_officehours, result_pay,
                result_recently)

    def data_to_df(self, data):

        for i in range(len(data[0])):
            self.data = self.data.append({"title": data[0][i].span.findNext("span").text,
                                          "area": data[1][i].text,
                                          "officehours": data[2][i].text,
                                          "pay": data[3][i].text,
                                          "recently": data[4][i].text,
                                          "link": "http://www.alba.co.kr/" +
                                                  data[0][i]["href"],
                                          "label": True
                                          },
                                         ignore_index=True)


alba = AlbaHeaven()
page = 0
flag = True
while flag:

    page += 1
    print(page)
    result = alba.crawler(page)
    alba.data_to_df(result)
    if len(result[0]) != 50:
        flag = False
        print("end")
        alba.filter()
        print(alba.data)
        pandas.DataFrame.to_excel(alba.data, "alba_heaven.xls")