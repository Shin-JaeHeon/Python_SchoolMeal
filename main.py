import requests
from bs4 import BeautifulSoup
import re
import datetime 
 
def getHtml(url):
   html = ""
   res = requests.get(url)
   if res.status_code == 200:
      html = res.text
   return html
 
 
def getSchoolMeal(code, ymd, weekday): # code = "조식 1, 중식 2, 석식 3
    schoolCode = code # int 형으로 바꿔줍니다.
    schoolYmd = ymd # string 형으로 바꿔줍니다.
    
    url1 = "http://stu.sen.go.kr/sts_sci_md01_001.do?"
    url2 = "schulCode=B100000658&schulCrseScCode=4&schulKndScCode=04" #schulCode = 학교 코드, schulKndScCode = (01 : 유치원, 02 : 초등학교, 03 : 중학교, 04 : 고등학교)
    url3 = "&schMmealScCode=%d&schYmd=%s" % (schoolCode, schoolYmd)
    URL = url1 + url2 + url3
    html = getHtml(URL)
    
    soup = BeautifulSoup(html, 'html.parser') #html 소스를 BeautifulSoup 모듈에 넣어줍니다.
    element = soup.find_all("tr")
    element = element[2].find_all('td')
    
    try: #불필요한 html 태그들을 지워줍니다!
        element = element[weekday] # 요일에 맞는 급식을 선택합니다.
        element = str(element) # 불러온 html코드를 string 형태로 바꿔줍니다.
        element = '\n' + element
        element = element.replace('[', '') #여기서부터 html 태그들을 지워줍니다.
        element = element.replace(']', '')
        element = element.replace('<br/>', '\n')
        element = element.replace('<td class="textC last">', '')
        element = element.replace('<td class="textC">', '')
        element = element.replace('</td>', '')
        element = element.replace('(h)', '')
        element = element.replace('.', '')
        element = re.sub(r"\d", "", element)
    except:
        element = "\n급식이 없습니다..."
    return element
 

code = input("조식, 중식, 석식을 선택하세요 : ")
if(code == "조식"): code = 1 #조식, 중식, 석식에 맞는 코드 번호로 바꿔줍니다.
elif(code == "중식"): code = 2
elif(code == "석식"): code = 3
ymd = input("날짜를 입력하세요 (ex : 2018.06.26) : ")
y = ymd[0:4]
m = ymd[5:7]
d = ymd[8:10]
n = datetime.date(int(y), int(m),int(d)).weekday()
print( getSchoolMeal(code, ymd, n+1)) 
