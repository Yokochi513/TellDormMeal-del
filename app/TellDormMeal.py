import datetime
import requests
import pdfplumber
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

def analysis_pdf():
    with pdfplumber.open("ryomenu.pdf") as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            dates = tables[0][0]
            breakfast = tables[0][1]
            lunchA = tables[0][9]
            lunchB = tables[0][12]
            dinnerA = tables[0][17]
            dinnerB = tables[0][20]
            return dates,breakfast,lunchA,lunchB,dinnerA,dinnerB