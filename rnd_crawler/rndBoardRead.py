import requests
from bs4 import BeautifulSoup as bs
import csv
import datetime

# +++++++++++ Util Area start +++++++++++++++++++++++++++++++++
def getYesterdayList():
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    day_of_week = ['월', '화', '수', '목', '금', '토', '일']
    yesterday_list = [yesterday]

    # yesterday가 일요일 경우 전 주 금요일까지 조회
    if '일' == day_of_week[yesterday.weekday()]:
        yesterday_list.append(yesterday - datetime.timedelta(days=1))
        yesterday_list.append(yesterday - datetime.timedelta(days=2))

    print('전일 :', yesterday, day_of_week[yesterday.weekday()])
    print('크롤링 날짜 :', yesterday_list)
    print('-----------------------------------------------------------------------------------')
    return yesterday_list

def yesterdayCheck(day_list, board_date):
    if board_date is None:
        return False
    result = False
    for yesterday in day_list:
        if yesterday == board_date:
            result = True
    return result

def validDate(date_str):
    """날짜를 검증합니다"""
    date_str = date_str.strip()
    if date_str in ('', None):
        return None
    date_str = date_str.replace(' ', '').replace(',', '-').replace('.', '-').replace('/', '-')

    if date_str[-1] == '-':
        date_str = date_str[:-1]

    # datetime 객체로 변환
    date_time_str = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    result = datetime.date(date_time_str.year, date_time_str.month, date_time_str.day)
    return result

def validTitle(title_str):
    """글제목을 검증합니다"""
    title_str = title_str.strip()
    title_str = title_str.replace('  ', '').replace('\t', '').replace('\n', '')
    return title_str

def csvReadUrl(src):

    csv_reader = csv.DictReader(open(src, encoding='UTF8'))
    url_field_names = csv_reader.fieldnames
    url_dict_list = []

    for row in csv_reader.reader:
        url_dict = {}
        if 'X' == row[7]:  # Crawler
            continue
        for index, h in enumerate(url_field_names):
            url_dict[h] = row[index].strip()
        url_dict_list.append(url_dict)
    return url_dict_list


# +++++++++++ Util Area end +++++++++++++++++++++++++++++++++
row_num = 10 - 2 # index 값 보정
url_dict_list = csvReadUrl('csv/url_list.csv')
print(url_dict_list[row_num])
yesterday_list = getYesterdayList()

def printRnD(csv_info):
    print(csv_info['부처'], '---', csv_info['기관'], '---------------------------------------')
    print(csv_info['URL'])
    url = csv_info['URL']
    select_tr = csv_info['TR']
    select_title = csv_info['Title']
    select_date = csv_info['Date']
    etc_str = csv_info['etc']

    req = requests.get(url)
    if 'utf-8' == etc_str:
        req.encoding = 'utf-8'
    elif 'euc-kr' == etc_str:
        req.encoding = 'euc-kr'

    html = req.text
    # print(html)
    soup = bs(html, 'lxml')
    board_list = soup.select(
        select_tr
    )
    # print(boardList)
    for i in board_list:
        title_list = i.select_one(select_title)
        title = validTitle(title_list.text)
        board_no = ''
        date_list = i.select_one(select_date)
        board_date = validDate(date_list.text) # datetime객체로 반환
        # 전일 공고만 출력
        if yesterdayCheck(yesterday_list, board_date):
            print(board_no, title, board_date)
    print('-----------------------------------------------------------------------')

for index, info in enumerate(url_dict_list):
    print('csv Row Num :',index + 2)
    printRnD(info)

# printRnD(urlDictList[rowNum])
print('++++++++++++++++++++++ 조회 완료 ++++++++++++++++++++++')

# for csvInfo in urlDictList:
#     printRnD(csvInfo)