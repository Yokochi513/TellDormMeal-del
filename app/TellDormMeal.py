import datetime
import requests
import pdfplumber
import json
from dateutil.relativedelta import relativedelta

def get_MealData():
    date = datetime.date.today()
    weekday = date.weekday()
    monday = (date + relativedelta(days=-weekday)).strftime("%Y/%m%d")
    Year,MonthDay = monday.split("/")

    pdf_url = "https://www.tsuyama-ct.ac.jp/images/hokushinryou/menu/ryoumenu-R06" + MonthDay + ".pdf"

    res = requests.get(pdf_url, allow_redirects=True, verify=False)

    if res.status_code == 200:
        open("ryoumenu.pdf", "wb").write(res.content)
        print("HTTP_SUCCESS")
        return True
    else:
        print("HTTP_ERROR")
        return False


def analysis_pdf():
    with pdfplumber.open("ryoumenu.pdf") as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            dates = tables[0][0]
            breakfast = tables[0][1]
            lunchA = tables[0][9]
            lunchB = tables[0][12]
            dinnerA = tables[0][17]
            dinnerB = tables[0][20]
            return dates,breakfast,lunchA,lunchB,dinnerA,dinnerB


def make_json():
    try:
        f = open("ryoumenu.json","r")
        dict_json = json.load(f)
        f.close()

        for i in range(7):
            dates,breakfast,lunchA,lunchB,dinnerA,dinnerB =  analysis_pdf()

            dict_json["food"][i]["date"] = dates[i+2]

            if isinstance(breakfast[i+2], str):
                dict_json["food"][i]["breakfast"] = breakfast[i+2]
            else:
                dict_json["food"][i]["breakfast"] = ""

            if isinstance(lunchA[i+2], str):
                dict_json["food"][i]["lunchA"] = lunchA[i+2]
            else:
                dict_json["food"][i]["lunchA"] = ""
            
            if isinstance(lunchB[i+2], str):
                dict_json["food"][i]["lunchB"] = lunchB[i+2]
            else:
                dict_json["food"][i]["lunchB"] = ""

            if isinstance(dinnerA[i+2], str):
                dict_json["food"][i]["dinnerA"] = dinnerA[i+2]
            else:
                dict_json["food"][i]["dinnerA"] = ""

            if isinstance(lunchB[i+2], str):
                dict_json["food"][i]["dinnerB"] = dinnerB[i+2]
            else:
                dict_json["food"][i]["dinnerB"] = ""

        new_json = open("ryoumenu.json", "w")
        json.dump(dict_json,new_json,indent=4)
        return True
    
    except:
        return False


def read_json(weekday):
    f = open("ryoumenu.json", "r")
    now_json = json.load(f)
    f.close()
    date = now_json["food"][weekday]["date"]
    breakfast = now_json["food"][weekday]["breakfast"]
    lunchA = now_json["food"][weekday]["lunchA"]
    lunchB = now_json["food"][weekday]["lunchB"]
    dinnerA = now_json["food"][weekday]["dinnerA"]
    dinnerB = now_json["food"][weekday]["dinnerB"]

    return date,breakfast,lunchA,lunchB,dinnerA,dinnerB


def notice_update():
    print(datetime.datetime.now())

    if json_already_update():
        return False
    else:
        if get_MealData():
            return True
        else:
            return False


def json_already_update():
    f = open("ryoumenu.json", "r")
    now_json = json.load(f)
    f.close()

    weekday = datetime.date.today().weekday()
    thisWeekMonDate = datetime.date.today() + relativedelta(days=-weekday)
    thisWeekMon = thisWeekMonDate.strftime("%Y/%m%d").split("/")[1]
    
    MonOrigin = now_json["food"][0]["date"].split("月")
    month = MonOrigin[0]
    date = MonOrigin[1].split("日")[0]
    if len(month) == 1:
        month = "0" + month
    if len(date) == 1:
        date = "0" + date
    WJsonMonday = month + date

    if WJsonMonday == thisWeekMon:
        return True
    else:
        return False


def manual_update():
    get_MealData()
    make_json()


def today():
    weekday = datetime.date.today().weekday()
    date,breakfast,lunchA,lunchB,dinnerA,dinnerB = read_json(weekday= weekday)
    return date,breakfast,lunchA,lunchB,dinnerA,dinnerB


def tomorrow():
    tomorrow = datetime.date.today() + relativedelta(days=1)
    tomorrowWeekday = tomorrow.weekday()
    date,breakfast,lunchA,lunchB,dinnerA,dinnerB = read_json(weekday= tomorrowWeekday)
    return date,breakfast,lunchA,lunchB,dinnerA,dinnerB