import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

mainHref = 'https://dg-trade.ru/catalog/'

hrefs=[]
links=[]

def getHtml(url):
    """Получение HTML"""
    r = requests.get(url).text
    return r


def getCategory(html):
    """"Получение ссылок на категории"""
    content = BeautifulSoup(html)
    urls = content.find_all('a', class_="thumb")

    for url in urls:
        hrefs.append('https://dg-trade.ru'+url.get('href'))

    return hrefs


def getPages(hrefs):
    """Получение ссылок на каждый товар"""

    for href in hrefs:
        content = BeautifulSoup(getHtml(href))

        try:
            div = content.find_all('div', class_='nums')[-1]
            mountPages = int(div.find_all('a',class_='dark_link')[-1].text)

        except: mountPages = 1

        if mountPages > 1:
            urls = content.find_all('a', class_="thumb shine")
            urls2 = content.find_all('a', class_="thumb")

            for url in urls:
                if len(url.get('href').split('/')) > 5:
                    if 'https://dg-trade.ru' + url.get('href') not in links:
                            links.append('https://dg-trade.ru' + url.get('href'))
            for url in urls2:
                if len(url.get('href').split('/')) > 5:
                    if 'https://dg-trade.ru' + url.get('href') not in links:
                        links.append('https://dg-trade.ru' + url.get('href'))

            for i in range(2,mountPages+1):

                url = href+'?PAGEN_1='+str(i)
                content = BeautifulSoup(getHtml(url))
                urls = content.find_all('a', class_="thumb shine")
                urls2 = content.find_all('a', class_="thumb")

                for url in urls:
                    if len(url.get('href').split('/')) > 5:
                        if 'https://dg-trade.ru' + url.get('href') not in links:
                            links.append('https://dg-trade.ru'+url.get('href'))
                for url in urls2:
                    if len(url.get('href').split('/')) > 5:
                        if 'https://dg-trade.ru' + url.get('href') not in links:
                            links.append('https://dg-trade.ru' + url.get('href'))

        urls = content.find_all('a', class_="thumb shine")
        urls2 = content.find_all('a', class_="thumb")

        for url in urls:
            if len(url.get('href').split('/'))>5:
                if 'https://dg-trade.ru' + url.get('href') not in links:
                    links.append('https://dg-trade.ru' + url.get('href'))
        for url in urls2:
            if len(url.get('href').split('/'))>5:
                if 'https://dg-trade.ru' + url.get('href') not in links:
                    links.append('https://dg-trade.ru' + url.get('href'))

    return links

def getParametrs(links):
    """Получение параметров от каждого товара"""
    brand=[]
    articul= []
    name =[]
    linkPhoto=[]
    warehouse =['-']
    back=['-']
    var=['-']
    weight=[]
    availability=[]
    description=[]
    deliveryTime= ['расчитать доставку']
    price=[]
    priseSale=['-']
    garant=[]
    boughtClick=['есть']
    optPrice=['-']
    analog=['-']
    goods=['-']
    maker=[]
    Maker=[]
    teg=['-']
    reviews=[]
    mark=['-']
    applicability=[]
    counter=0
    date=[]
    time=[]
    rubrica=[]

    for link in links:
        counter+=1
        content = BeautifulSoup(getHtml(link))
        name.append(content.find('h1',id='pagetitle').text)
        try:linkPhoto.append('https://dg-trade.ru/'+content.find('a', class_='fancy popup_link').get('href'))
        except:linkPhoto.append('-')
        try:availability.append(content.find('span', class_='store_view').text)
        except:availability.append('-')
        try:price.append(content.find('div', class_='price').text[1:])
        except:price.append('-')
        rub=content.find_all('span', itemprop="name")
        rubrica.append(rub[2].text)

        all=content.find_all('td', class_="char_name")
        names=[]
        value = []
        for i in all:
            names.append(i.text[2:-2])# тут хроним производителя страну и тд

        meaning=content.find_all('td', class_="char_value")
        for mean in meaning:
            value.append(mean.text)# здесь храним германию и тд

        try:
            maker.append(value[names.index('Производитель:')][35:-32])
            brand.append(value[names.index('Производитель:')][35:-32])
        except:
            maker.append('-')
            brand.append('-')
        try:Maker.append(value[names.index('Страна изготовления:')][35:-32])
        except:Maker.append('-')
        try:garant.append(value[names.index('Гарантия:')][35:-32])
        except:garant.append('-')
        try:weight.append(value[names.index('Фасовка:')][35:-32])
        except:weight.append('-')
        try:articul.append(value[names.index('Доп. артикулы:')][35:-32])
        except:articul.append('-')

        try:
            if content.find('div', id="reviews_content").text.find('У данного товара нет отзывов.')!=19:
                reviews.append('ecть')
            else:
                reviews.append('-')
        except:reviews.append('-')

        try:
            disc=content.find('div',class_="col-md-6")
            p=disc.find_all('p')
            try:description.append(p[0].text)
            except:description.append('-')
            try:applicability.append(p[1].text)
            except:applicability.append('-')
        except:
            applicability.append('-')
            description.append('-')

        now = datetime.now()
        t = now.strftime("%H:%M")
        t2 = now.strftime("%d.%m.%Y")
        date.append(t2)
        time.append(t)

    products=[date,time,links,brand,articul,description,linkPhoto,warehouse*counter,
              back*counter,var*counter,weight,availability,deliveryTime*counter,price,
              priseSale*counter,garant,boughtClick*counter,optPrice*counter,analog*counter,
              goods*counter,Maker,maker,rubrica,teg*counter,reviews,mark*counter,applicability]

    return products

def writeExcel(products):
    """Запись в Excel файл"""
    title=['Дата','Время','Источник','Бренд','Артикул','Описание','Изображение','Склад',
           'Возврат','Вероятность выдачи данным поставщиком (?)','Вес','Наличие','Срок доставки',
           'Цена','Цена со скидкой','Гарантия','Купить в 1 клик','Оптовая цена','Аналогом чего является',
           'Сопутствующие товары','Страна производитель','Производитель','Рубрика','Теги','Отзывы',
           'Общая оценка/рейтинг товара','Применяемость']

    d = {title[i]: products[i] for i in range(27)}
    df = pd.DataFrame(d)
    df.to_excel('C:\Renata\m.xlsx')


writeExcel(getParametrs(getPages(getCategory(getHtml(mainHref)))))
