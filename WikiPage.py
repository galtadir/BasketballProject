from bs4 import BeautifulSoup
from urllib.request import urlopen


class WikiPage:
    def __init__(self , url):
        self.url=url
        self.dict_by_year= {}
        self.name=""
        self.photo_url=""
        self.born_place=""
        self.born_date=""
        self.high_school=""
        self.college=""

    def init_detail(self):
        page = urlopen(self.url)
        soup = BeautifulSoup(page)
        table = soup.find('table', class_='infobox vcard')
        self.name = table.find('caption', class_='fn summary').text
        trs = table.find_all('tr')
        forImage = trs[0]
        self.photo_url=forImage.find('img').get('src')
        for tr in trs[1:]:
            th = tr.find('th')
            tds = tr.find_all('td')
            if th!=None:
                if th.text=="Born":
                    self.born_date= tds[0].find('span', class_='bday').text
                    self.born_place = tds[0].find('a').text
                if th.text== "High school":
                    self.high_school = tds[0].find('a').text
                if th.text== "College":
                    self.college = tds[0].find('a').text
                if th.find('a')!=None and th.find('a').text=="NBA draft":
                    print(tds)

        # self.photo_url= table.find('img').get('src')
        #
        # self.born_date = table.find('span', class_='bday').text

        # self.born_place = table.find('a')


        # print(name)
        return 0


lebron = WikiPage("https://en.wikipedia.org/wiki/LeBron_James")
lebron.init_detail()
