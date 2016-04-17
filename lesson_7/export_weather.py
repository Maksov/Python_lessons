# __author:Haidarov Radik__
""" Яндекс.Погода (экспорт)

Сделать скрипт, экспортирующий данные из базы данных погоды, 
созданной скриптом weather.py. Экспорт происходит в формате CSV или JSON.

Скрипт запускается из коммандной строки и получает на входе:
export_weather.py --csv filename [<город>]
export_weather.py --json filename [<город>]

Экспорт происходит в файл filename.
Опционально можно задать в коммандной строке город. В этом случае 
экспортируются только данные по указанному городу. Если города нет в базе -
выводится соответствующее сообщение.


"""
import sys
import csv
import json
import sqlite3
import datetime

db_filename = 'weather.db'

def export_csv(filename,city):
    encoding = 'utf-8'
    csv.register_dialect('excel-semicolon', delimiter=';')
    sql_str = "select (Select city from cites where weath_city.idcity = cites.id) as cityname,(Select country from countres where weath_city.id_country = countres.id) as countryname,data,w_day,w_night from weath_city where idcity="+str(city)
    if city == 0:
        sql_str = "select (Select city from cites where weath_city.idcity = cites.id) as cityname,(Select country from countres where weath_city.id_country = countres.id) as countryname,data,w_day,w_night from weath_city"
        
    with open(filename, 'w', encoding=encoding) as csvfile:
        writer = csv.writer(csvfile, dialect='excel-semicolon')
        writer.writerow( ('Город', 'Страна', 'Дата','Темп. днем','Темп. ночью') )
        with sqlite3.connect(db_filename) as conn:
            cur = conn.cursor()    
            for row in cur.execute(sql_str):
                writer.writerow( (row[0],row[1],row[2],row[3],row[4]) )
        conn.close
        
def export_json(filename,city):
    sql_str = "select (Select city from cites where weath_city.idcity = cites.id) as cityname,(Select country from countres where weath_city.id_country = countres.id) as countryname,data,w_day,w_night from weath_city where idcity="+str(city)
    if city == 0:
        sql_str = "select (Select city from cites where weath_city.idcity = cites.id) as cityname,(Select country from countres where weath_city.id_country = countres.id) as countryname,data,w_day,w_night from weath_city"
    f = open(filename, 'w')
    f.write('{')
    with sqlite3.connect(db_filename) as conn:
        cur = conn.cursor()    
        for row in cur.execute(sql_str):
            rjson = "city:{0},country:{1},data:{2},day:{3},night:{4}".format(row[0],row[1],row[2],row[3],row[4])
            f.write("{" + rjson + "},")
    conn.close
    f.write("{export:" + str(datetime.date.today())+ '}')
    f.write('}')
    f.close()

def exists_city(city):
    b = True
    with sqlite3.connect(db_filename) as conn:
        cur = conn.cursor()    
        cur.execute("select * from cites where id=" + str(city))
        row = cur.fetchone()
        if row == None:
            b = False
        else:
            b = True
    conn.close()
    return b


def main():

    if len(sys.argv) > 4 or len(sys.argv) <2:
        print('usage: python export_weather.py {--csv | --json} file [<город>]')
        sys.exit(1)        
    option = sys.argv[1]
    filename = sys.argv[2]
    city = 0
    if len(sys.argv) == 4:
        city = sys.argv[3]

    if city != 0:
        if exists_city(city) == False:
            print('City not found!')
            sys.exit(1)    
    if option == '--csv':
        export_csv(filename,city)
    elif option == '--json':
        export_json(filename,city)
    else:
        print('unknown option: ' + option)
        sys.exit(1)

    #city = 3917 - код города белфаст
    #print(exists_city(city))
    #filename = "exp39.json"
    #export_csv(filename,city)
    #export_json(filename,city)
    
if __name__ == '__main__':
    main()
