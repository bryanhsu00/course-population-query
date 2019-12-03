import requests
from bs4 import BeautifulSoup

class Course():

    def __init__(self):
        self.headers = {
                'Host': 'ccweb.ncnu.edu.tw',
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                'Accept-Encoding': 'gzip, deflate, br',
                # 'Referer': 'https://ccweb.ncnu.edu.tw/student/aspmaker_course_opened_semester_stat_viewlist.php',
                'Connection': 'keep-alive',
                'Cookie': '_ga=GA1.3.246235210.1550630345; __utma=67500430.246235210.1550630345.1555346476.1555394753.4; __utmz=67500430.1555394753.4.4.utmcsr=doc.ncnu.edu.tw|utmccn=(referral)|utmcmd=referral|utmcct=/ncnu/index.php; PHPSESSID=b64f57a778987784dbeb3c496f6b148d',
                'Upgrade-Insecure-Requests': '1',
                'Cache-Control': 'max-age=0',
            }
        self.allCourse = self.getCourse()
        self.allClassification = self.getClassification()
        self.addClassifyLabel()

    def getCourse(self, url = None):
        if url is None:
            url = 'https://ccweb.ncnu.edu.tw/student/aspmaker_course_opened_detail_viewlist.php?cmd=search&t=aspmaker_course_opened_detail_view&z_year=%3D&x_year=1072&z_courseid=%3D&x_courseid=&z_cname=LIKE&x_cname=&z_deptid=%3D&x_deptid=99&z_division=LIKE&x_division=&z_grade=%3D&x_grade=&z_teachers=LIKE&x_teachers=&z_not_accessible=LIKE&x_not_accessible='

        res = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(res.text,"html.parser")
        tbl = soup.find_all('table')[0].find_all('td')
        titles = ['year', 'courseid', 'class', 'cname',
                'deptid', 'division', 'grade', 'teachers', 
                'place', 'not_accessible', 'time', 'limit', 
                'seleced_no']
        course = []

        for i in range(0, len(tbl), 14):
            d = {}
            for t, j in zip(titles, range(i+1, i+14)):
                d[t] = tbl[j].text.strip()
            course.append(d)

        changeOption = soup.find_all("div", class_="input-group-btn")[1].find('a').attrs

        if 'href' in changeOption:
            nextUrl = 'https://ccweb.ncnu.edu.tw/student/' + changeOption['href']
            return course + self.getCourse(nextUrl)
        else:
            return course

    def getClassification(self):
        url = 'https://ccweb.ncnu.edu.tw/student/ncnu_coremin_detail_viewlist.php'
        res = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(res.text,"html.parser").find_all('a', {"data-caption":"檢視主資料/細資料"})[2:]
        uurl = 'https://ccweb.ncnu.edu.tw/student/'
        
        d = {}
        for i in soup:
            res = requests.get(uurl + i['href'], headers=self.headers)
            soup2 = BeautifulSoup(res.text,"html.parser")    
            title = soup2.find("span", {"id": "el_ncnu_coremin_detail_view__68385FC3985E5225"})
            title = title.text.strip()[2:][:-6]
            tbl = soup2.find_all("table")[1].find_all("tr")[1:]
            d[title] = []
            for j in tbl:
                courseName = j.find_all("span")[3].text.strip().split()[0]
                d[title].append(courseName)

        return d

    def addClassifyLabel(self):
        for courseData in self.allCourse:
            for index, content in self.allClassification.items():
                for c in content:
                    if c == courseData['cname']:
                        courseData['classify'] = index
                        # print(index, courseData['cname'])

    def filterCourse(self, condition):
        result = []
        
        for i in self.allCourse:
            try:
                if i['classify'] in condition:
                    result.append(i)
            except:
                i['classify'] = '自然-工程與科技'
                if i['classify'] in condition:
                    result.append(i)

        if "只顯示人數未滿" in condition:
            result = [i for i in result if int(i['limit']) > int(i['seleced_no'])]
        
        return result
