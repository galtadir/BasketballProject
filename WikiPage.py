from bs4 import BeautifulSoup
from urllib.request import urlopen
import re


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


    def check_url(self):
        try:
            page = urlopen(self.url)
            return True
        except:
            return False

    def init_detail(self):
        page = urlopen(self.url)
        soup = BeautifulSoup(page)
        table = soup.find('table', class_='infobox vcard')
        self.name = table.find('caption', class_='fn summary').text
        trs = table.find_all('tr')
        forImage = trs[0]
        if not forImage.find('img')==None:
            self.photo_url = forImage.find('img').get('src')
        counter=0
        for tr in trs[1:]:
            counter= counter+1
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
                    line = tds[0].text
                    line_splited = line.split("/")
                    td_for_draft = trs[counter + 1].find_all('td')
                    # print(td_for_draft[0].text)
                    self.dict_by_year[line_splited[0][0:len(line_splited[0])-1]]= [td_for_draft[0].text + " in" +  line_splited[1]+ "at " + line_splited[2][1:]]
                    # print(self.dict_by_year)
                if th.text == "Career history":
                    counter2 = 1
                    while not trs[counter+counter2+1].find('th').text=="Career highlights and awards":
                        curr = trs[counter+counter2]
                        years = curr.find('th').text
                        years_splited = years.split("–")
                        year = years_splited[0]
                        team = curr.find('td').text
                        if year in self.dict_by_year.keys():
                            self.dict_by_year[year].append("Arrived to " + team)
                        else:
                            self.dict_by_year[year] = ["Arrived to " + team]
                        # print(team.text)
                        counter2=counter2+1
                if th.text == "Career highlights and awards":
                    # print(th.text)
                    curr = trs[counter+1]
                    # print(curr)
                    td_award = curr.find('td')
                    lis = td_award.find_all('li')
                    for li in lis:
                        li_text = li.text
                        if not li_text.find("×")==-1:
                            li_text = li_text.split("×")[1][1:]
                            pass

                        li_text_splited = li_text.split("(")
                        if len(li_text_splited)>1:
                            years = li_text_splited[1].split(")")[0]
                            years_splited = years.split(", ")
                            for year in years_splited:
                                if year.find("–") == -1:
                                    if year in self.dict_by_year.keys():
                                        self.dict_by_year[year].append(li_text_splited[0])
                                    else:
                                        self.dict_by_year[year] = [li_text_splited[0]]
                                else:
                                    first = int(year.split("–")[0])
                                    last = int(year.split("–")[1])
                                    for i in range(first, last + 1):
                                        year = str(i)
                                        if year in self.dict_by_year.keys():
                                            self.dict_by_year[year].append(li_text_splited[0])
                                        else:
                                            self.dict_by_year[year] = [li_text_splited[0]]

                        # print(li_text_splited[0])
                        # print(years_splited)

                    # ul = td_award.find('ul')
                    # print(ul)

        self.dict_by_year = sorted(self.dict_by_year.items(), key=lambda t: t[0])

    def getDictByYear(self):
        return self.dict_by_year


        # self.photo_url= table.find('img').get('src')
        #
        # self.born_date = table.find('span', class_='bday').text

        # self.born_place = table.find('a')


        # print(name)
        return 0

    def print(self):
        print("name",self.name)
        print("photo_url", self.photo_url)
        print("born_place", self.born_place)
        print("born_date", self.born_date)
        print("high_school", self.high_school)
        print("college", self.college)



# lebron = WikiPage("https://en.wikipedia.org/wiki/lebron_james")
# lebron.init_detail()
# print(lebron.dict_by_year)
# lebron.print()
