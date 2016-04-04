#!/usr/bin/python3
# __author:Haidarov Radik__

""" Ремонт в квартире 

Есть квартира (2 комнаты и кухня). В квартире планируется ремонт: нужно 
поклеить обои, покрасить потолки и положить пол.

Необходимо рассчитать стоимость материалов для ремонта.

Из описания следуют следующие классы:
= Строительные материалы
  = Обои
  = Потолочная краска
  = Ламинат
= Комната
= Квартира

Подробнее, с методами (+) и атрибутами (-):
= Строительные материалы
  - площадь (кв. м)
  - цена за единицу (рулон, банку, упаковку)
  = Обои
    - ширина рулона
    - длина рулона
  = Потолочная краска
    - вес банки
    - расход краски
  = Ламинат
    - длина доски
    - ширина доски
    - кол-во досок в упаковке
= Комната
  - ширина
  - высота
  - длина
  - ширина окна
  - ширина двери
  + поклеить обои
  + покрасить потолок
  + положить пол
  + посчитать смету на комнату
  + при создании комнаты сразу передавать все атрибуты в конструктор __init__()
= Квартира
  - комнаты
  + добавить комнату
  + удалить комнату
  + посчитать смету на всю квартиру
  + при создании можно передать сразу все комнаты в конструктор

Необходимо создать стройматериалы, назначить им цены и размеры.
Создать комнаты, поклеить, покрасить и положить все на свои места.
Cоздать квартиру, присвоить ей комнаты и посчитать общую смету.

Подсказка: для округления вверх и вниз используйте:
import math
math.ceil(4.2)  # 5
math.floor(4.2) # 4

Примечание: Для простоты, будем считать, что обои над окном и над дверью 
не наклеиваются.
----------------

Дополнительно:
Сделать у объекта квартиры метод, выводящий результат в виде сметы:

[Комната: ширина: 3 м, длина: 5 м, высота: 2.4 м]
Обои        400x6=2400 руб.
Краска     1000x1=1000 руб.
Ламинат     800x8=6400 руб.
[Комната: ширина: 3 м, длина: 4 м, высота: 2.4 м]
Обои        400x5=2000 руб.
Краска     1000x1=1000 руб.
Ламинат     800x7=5600 руб.
[Кухня: ширина: 3 м, длина: 3 м, высота: 2.4 м]
Обои        400x4=1600 руб.
Краска     1000x1=1000 руб.
Ламинат     800x5=4000 руб.
---------------------------
Итого: 25000 руб.

"""

import math

class Material:
    '''
    Класс хранит в себе площадь, которую обработает материал и стоимость за данную площадь
    '''
    def __init__(self,plos, price):
        self.plos = float(plos)
        self.price = float(price)

class Laminat(Material):
    '''
    Класс хранит описание матриала ламинат, цена за упаковку и расчет площади упаковки
    '''
    def __init__(self,dlin,shir,kol,price):
        self.dlin = float(dlin)
        self.shir = float(shir)
        self.kol = int(kol)
        super().__init__(self.dlin*self.shir*self.kol,price)

class Kraska(Material):
    '''
    Класс хранит описание матриала краска, цена за банку и объем(вес) и расчет площади 
    '''    
    def __init__(self,ves,rashod,price):
        self.ves = float(ves)
        self.rashod = float(rashod)
        super().__init__(self.ves*self.rashod,price)

class Oboi(Material):
    '''
    Класс хранит описание матриала обои, цена за рулон и расчет площади рулона
    '''
    def __init__(self,dlin,shir,price):
        self.dlin = float(dlin)
        self.shir = float(shir)
        super().__init__(self.dlin*self.shir,price)

class Room:
    '''
    Класс хранит описание комнаты
    '''    
    def __init__(self,name,dlin,shir,wiso,shir_ok,shir_dv):
        self.name = name
        self.dlin = float(dlin)
        self.shir = float(shir)
        self.wiso = float(wiso)
        self.shir_ok = float(shir_ok)
        self.shir_dv = float(shir_dv)
        self.itogo = 0

    def __str__(self):
        return '[Комната: {0}, длина: {1} м., ширина: {2} м., высота: {1} м.]'.format(self.name,self.dlin,self.shir,self.wiso)

    def oboi(self):
        #расчет затрат - обои - на комнату
        Fplo = (self.dlin + self.shir)*2*self.wiso
        Dplo = self.shir_dv * self.wiso
        Oplo = self.shir_ok * self.wiso
        RabPlo = Fplo - Dplo - Oplo
        RylonKol = math.ceil(RabPlo/oboi.plos)
        self.itogo += RylonKol*oboi.price
        return 'Обои: {0}x{1}={2} руб.'.format(oboi.shir,RylonKol,RylonKol*oboi.price)

    def potolok(self):
        #расчет затрат - покраска потолка - на комнату
        RabPlo = self.shir*self.dlin
        BankiKol = math.ceil(RabPlo/kraska.plos)
        self.itogo += BankiKol*kraska.price
        return 'Краска: {0}x{1}={2} руб.'.format(kraska.ves,BankiKol,BankiKol*kraska.price)

    def pol(self):
        #расчет затрат - положить ламинат - на комнату
        RabPlo = self.shir*self.dlin
        LamKol = math.ceil(RabPlo/laminat.plos)
        self.itogo += LamKol*laminat.price
        return 'Лаинат: {0}x{1}={2} руб.'.format(laminat.shir,LamKol,LamKol*laminat.price)

    def read_smeta(self):        
        #смета на комнату
        print(self)
        print(self.oboi())
        print(self.potolok())
        print(self.pol())
        print('Итого: {0}'.format(self.itogo))
        pass

class Apartment:
    '''
    Класс хранит описание квартиры, список комнат
    '''
    def __init__(self,rooms):
        self.rooms = rooms

    def __str__(self):
        str_rooms = ''
        for room in self.rooms:
            str_rooms +='Room: {0}, длина: {1} м., ширина: {2} м., высота: {1} м.'.format(room.name,room.dlin,room.shir,room.wiso)
            str_rooms += '\n'
        return str_rooms

    def addRoom(self,room):
        #добавить комнату
        self.rooms.append(room)

    def delRoom(self,room_index):
        #удалить комнату по ее номеру
        self.rooms.pop(room_index)

    def read_smeta(self):
        #смета на квартиру
        itogo = 0
        for room in self.rooms:
            room.read_smeta()
            itogo += room.itogo
        print('-'*25)
        print('Итого: {0}'.format(itogo))

# комнаты
room1 = Room('room 1',5,3,2.4,0.8,0.8)
room2 = Room('room 2',4,3,2.4,1.6,0.8)
kyx = Room('kyx',3,3,2.4,0.8,0.8)

flat = Apartment([room1,room2])
flat.addRoom(kyx)
#print(flat)
#flat.delRoom(1)
#print(flat)

# материалы

oboi = Oboi(2.5,0.8,700)
kraska = Kraska(1.5,3.5,500)
laminat = Laminat(2.5,0.5,12,1200)

#смета
#room1.read_smeta()
flat.read_smeta()
