from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.retro

def melonCrawling(genre, year) : 

    # selenium에서 사용할 웹 드라이버 절대 경로 정보
    chromedriver = 'C:\Sparta\chromedriver'

    # selenum의 webdriver에 앞서 설치한 chromedirver를 연동한다.
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches',['enable-logging'])
    options.add_argument('headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = options)
    
    # driver로 특정 페이지를 크롤링한다.

    driver.get('https://www.melon.com/chart/age/index.htm?chartType=YE&chartGenre='+genre+'&chartDate='+str(year))

    chart = driver.page_source
    soup = BeautifulSoup(chart, 'html.parser')
    
    datas = soup.select('#frm > table > tbody > tr')
    
    for music in datas : 
        albumImageUrl = music.select_one('td:nth-child(3) > div > a > img').get('src')
        title = music.select_one('td:nth-child(4) > div > div > div.ellipsis.rank01 > span').text.strip(' \n')
        rank = music.select_one('td:nth-child(2) > div > span').text
        singer = music.select_one('td:nth-child(4) > div > div > div:nth-child(3) > div.ellipsis.rank02 > a').text
        like = music.select_one('td:nth-child(5) > div > button > span.cnt').text.strip(' \n').strip('총건수\n')
        musics={'Genre':genre, 'year': year, 'rank':rank, 'title':title, 'singer':singer, 'albumImageUrl':albumImageUrl, 'like':int(like.replace(",",""))}
        print(musics)
        db.musics.insert_one(musics)

def insert_all():
    db.musics.drop()
    Genre = ['KPOP', 'POP']
    for g in Genre :
        i = 1980
        while i < 2011 :
            melonCrawling(g, i)
            i +=1
        
insert_all()