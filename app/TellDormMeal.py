import datetime
import requests
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
    else:
        print("HTTP_ERROR")