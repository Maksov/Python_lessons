# __author:Haidarov Radik__
""" Яндекс.Погода

Есть публичный урл со списком городов:
http://weather.yandex.ru/static/cities.xml

Для этих городов можно получить данные о погоде, подставив id города в шаблон:
http://export.yandex.ru/weather-ng/forecasts/<id города>.xml

Необходимо написать скрипт, который:
1. Создает файл базы данных SQLite с следующей структурой данных (если файла 
   базы данных не существует):

    Погода
        id                  INTEGER PRIMARY KEY
        Город               VARCHAR(255)
        Дата                DATE
        Температура днем    INTEGER
        Температура ночью   INTEGER

2. Скачивает и парсит XML со списком городов
3. Выводит список стран из файла и предлагает пользователю выбрать страну
4. Скачивает XML файлы погоды в городах выбранной страны
5. Парсит последовательно каждый из файлов и добавляет данные о погоде в базу
   данных. Если данные для данного города и данного дня есть в базе - обновить
   температуру в существующей записи.


Температура днем и температура ночью берется из 
forecast/day/day_part@day_short/temperature и 
forecast/day/day_part@night_short/temperature соответственно:

<forecast ...>
    <day date="...">
        <day_part typeid="5" type="day_short">
            <temperature>29</temperature> 
            ...
        </day_part>
        <day_part typeid="6" type="night_short">
            <temperature>18</temperature>
            ...
        </day_part>
    </day>
</forecast>

Вот небольшое решение
https://pogoda.yandex.ru/static/cities.xml в нем
<city id="28630" region="11202" head="0" type="2" country="Россия" part="Челябинская область" resort="0" climate="">Златоуст</city>
http://meteoinfo.ru/rss/forecasts/28630 - в виде rss
не все города даже в России присуствуют

При повторном запуске скрипта:
- используется уже скачанный файл с городами
- используется созданная база данных, новые данные добавляются и обновляются

Важное примечание:

Доступ к данным в XML файлах происходит через простансво имен:
<forecast ... xmlns="http://weather.yandex.ru/forecast ...>

Чтобы работать с простанствами имен удобно пользоваться такими функциями:

# Получим пространство имен из первого тега:
def gen_ns(tag):
    if tag.startswith('{'):
        ns, tag = tag.split('}')
        return ns[1:]
    else:
        return ''

tree = ET.parse(f)
root = tree.getroot()

# Определим словарь с namespace
namespaces = {'ns': gen_ns(root.tag)}

# Ищем по дереву тегов
for day in root.iterfind('ns:day', namespaces=namespaces):
    ...

"""
import os
import sqlite3
import urllib.request
import datetime
import re
from xml.etree import ElementTree as ET
from collections import OrderedDict, namedtuple

cities_filename = "cities.xml"
urllib.request.urlretrieve("http://weather.yandex.ru/static/cities.xml", cities_filename)
db_filename = 'weather.db'
todir = 'temp'

def extract_weather(id_country):
    #39 - Britain
    if os.path.exists(todir) == False:
            os.mkdir(todir)
    with sqlite3.connect(db_filename) as conn:
        cur = conn.cursor()    
        for row in cur.execute("select * from cites where id_country="+id_country):
            print(row[0],row[2])
            idcity = row[0]
            temp_filename = '{0}/temp_{1}_{2}.xml'.format(todir,str(id_country),row[0])
            urllib.request.urlretrieve("http://meteoinfo.ru/rss/forecasts/"+str(row[0]), temp_filename)
            if os.path.getsize(temp_filename) == 0:
                os.remove(temp_filename)
            else:
                with open(temp_filename, 'r', encoding='utf-8') as f:
                    tree = ET.parse(f)
                root = tree.getroot()
                i = 0
                for child in root[0].findall('item'):
                    #print(child[0].text,child[2].text,child[5].text)
                    data = datetime.date.today()+datetime.timedelta(days=i)
                    i = i + 1
                    w_desc = child[2].text
                    #print(desc)
                    id_weath = ''.join((str(id_country),str(idcity),str(data).replace('-','')))
                    reg = re.compile(r''' (.{2}[d]?)°''',re.VERBOSE | re.DOTALL)
                    res = reg.findall(w_desc)
                    #print(res[0],res[1])
                    conn.execute('insert or replace into weath_city (id,id_country,idcity,data,w_night,w_day,w_desc) VALUES (?,?,?,?,?,?,?)',(id_weath,id_country,idcity,data,res[0],res[1],w_desc))
                    conn.commit()
    conn.close();
"""
Белфаст, 17 апреля
Переменная облачность, без осадков. Температура ночью 1°, днём 10°. Ветер западный, 8 м/с. Атмосферное давление ночью 754 мм рт.ст., днём 755 мм рт.ст.Вероятность осадков 40%
927111933
""" 


with sqlite3.connect(db_filename) as conn:
    conn.execute('create table if not exists countres (id INTEGER PRIMARY KEY,country TEXT);')
    conn.execute('create table if not exists cites (id INTEGER PRIMARY KEY,id_country INTEGER,city TEXT);')
    conn.execute('create table if not exists weath_city (id INTEGER PRIMARY KEY,idcity INTEGER,id_country INTEGER,data DATE,w_day FLOAT,w_night FLOAT,w_desc TEXT);')
conn.close()

with open(cities_filename, 'r', encoding='utf-8') as f:
    tree = ET.parse(f)
root = tree.getroot()
id_country = 0
for child in root:
   #print(child.get('name'))
    country = child.get('name')
    id_country += 1
    with sqlite3.connect(db_filename) as conn:
        conn.execute('insert or ignore into countres (id,country) VALUES (?,?)',(id_country,country))
        conn.commit()
    conn.close()
    print(country + " -->")
    for city in child.findall('city'):
        id_city = city.get('id')
        name_city = city.text
   #    print (id_city, name_city)
        with sqlite3.connect(db_filename) as conn:
            conn.execute('insert or ignore into cites (id,id_country,city) VALUES (?,?,?)',(id_city,id_country,name_city))
            conn.commit()
        conn.close()
    print(country + " -- OK")
print("cities.xml -- OK")
#---download
with sqlite3.connect(db_filename) as conn:
    cur = conn.cursor()    
    for row in cur.execute("select * from countres"):
        print(row)
conn.close()
county_in = input('Введите страну (id): ')
with sqlite3.connect(db_filename) as conn:
    cur = conn.cursor()    
    cur.execute("select * from countres where id=" + str(county_in))
    row = cur.fetchone()
    if row == None:
        print ('Такой страны не знаю!')
        county_in = -1
    else:
        print(row[0],row[1])
conn.close()
if county_in != -1:
    extract_weather(county_in)
