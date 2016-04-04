#!/usr/bin/python3
# __author:Haidarov Radik__

"""
Это пример небольшой программы для рисования кругов и квадратов.
Вам нужно на основе этой программы сделать небольшую "танцевальную" сценку с
использованием кругов, квардратов и треугольников. Сделать всё это нужно в
объектно ориентированном стиле.

Какие классы нужно реализовать:

-Многоугольник(на его основе сделать квадрат и правильный треугольник)
--класс должне уметь отрисовывать себя
--премещаться в некоторм направлении заданом координатами x, y
--увеличивать(необязательно)
--поворачивать(необязательно)

-Квардрат(наследуется от многоугольника)
--метод __init__ принимает координаты середины, ширину и цвет

-Треугольник(наследуется от многоугольника)
--метод __init__ принимает координаты середины, длинну грани и цвет

-Круг
--метод __init__ принимает координаты середины, радиус и цвет
--класс должне уметь отрисовывать себя
--премещаться в некоторм направлении заданом координатами x, y
--увеличивать(необязательно)

Также рекомендую создать вспомогательный сласс Vector для представления
точек на плоскости и различных операций с ними - сложение, умножение на число,
вычитаные.


Из получившихся классов нужно составить какую-нибудь динамическую сцену.
Смотрите пример example.gif
"""

import turtle
import time
import math
import random

class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y


class Figure:
    def __init__(self,coords,x,y,color): #coords = list[Point]
        self.coords = coords
        self.color = color
        self.x_center = x
        self.y_center = y

    def Draw(self,ttl):
        ttl.color(self.color)
        ttl.penup()
        ttl.setpos(self.coords[0].x,self.coords[0].y)
        ttl.pendown()
        for point in self.coords[1:]:
            ttl.goto(point.x,point.y)
        ttl.penup()

    def Clear(self,ttl):
        ttl.color('white')
        ttl.penup()
        ttl.setpos(self.coords[0].x,self.coords[0].y)
        ttl.pendown()
        for point in self.coords[1:]:
            ttl.goto(point.x,point.y)
        ttl.penup()

    def Move(self,ttl,x,y):
        self.Clear(ttl)
        ttl.color(self.color)
        ttl.penup()
        dx = self.coords[0].x - x
        dy = self.coords[0].y - y
        dist =  math.hypot(dx, dy)
        ttl.setpos(self.coords[0].x+dist,self.coords[0].y+dist)        
        ttl.pendown()
        for point in self.coords[1:]:            
            ttl.goto(point.x+dist,point.y+dist)
        for point in self.coords:
            point.x +=dist
            point.y +=dist
        ttl.penup()  

class Square(Figure):

    def __init__(self,x,y,h,color):
        self.color = color
        self.storona = h
        self.x = x
        self.y = y
        pol = math.ceil(h/2)
        point1 = Point(x - pol,y - pol)
        point2 = Point(x + pol,y - pol)
        point3 = Point(x - pol,y + pol)
        point4 = Point(x + pol,y + pol)
        coords = [point1,point2,point4,point3,point1]
        self.coords = coords
        super().__init__(self.coords,self.x,self.y,color)

class Tringle(Figure):
    
    def __init__(self,x,y,h,color):
        self.color = color
        self.storona = h
        self.x = x
        self.y = y
        R = math.ceil(h / math.sqrt(3))
        H = math.ceil((h * math.sqrt(3)) / 2)
        pol = math.ceil(h/2)
        point1 = Point(x,y - R)
        point2 = Point(x + pol,y - H)
        point3 = Point(x - pol,y - H)
        coords = [point1,point2,point3,point1]
        self.coords = coords
        super().__init__(self.coords,self.x,self.y,color)

class Circle:
    def __init__(self,x,y,radius,color):
        self.x = x
        self.y = y
        self.r = radius
        self.color = color
        
    def Draw(self,ttl):
        ttl.color(self.color)
        ttl.penup()
        ttl.setpos(self.x, self.y)
        ttl.pendown()
        ttl.circle(self.r)

    def Clear(self,ttl):
        ttl.color('white')
        ttl.penup()
        ttl.setpos(self.x, self.y)
        ttl.pendown()
        ttl.circle(self.r)

    def Move(self,ttl,new_x,new_y):
        self.Clear(ttl)
        self.x = new_x
        self.y = new_y
        self.Draw(ttl)

    def Scale(self,ttl,new_r):
        self.Clear(ttl)
        self.r = new_r
        self.Draw(ttl)


def main():

    turtle.tracer(0, 0) #устанавливаем все задержки в 0, чтобы рисовалось мгновенно
    turtle.hideturtle() #убираем точку посередине

    ttl = turtle.Turtle() #создаём объект черепашки для рисования
    ttl.hideturtle() #делаем её невидимой

    while True:
        time.sleep(0.5) #засыпаем на полсекунды, чтобы увидеть что нарисовали
        ttl.clear() #очищаем всё нарисованое ранее
        x = random.randint(-100, 100) #получаем случайные координаты
        y = random.randint(-100, 100)
        circle = Circle(x,y,40,'Red')
        circle.Draw(ttl)
        turtle.update()#т.к. мы сделали turtle.tracer(0, 0) нужно обновить экран, чтобы увидеть нарисованное
        time.sleep(0.5)
        x = random.randint(-100, 100) #получаем случайные координаты
        y = random.randint(-100, 100)
        circle.Move(ttl,x,y)
        turtle.update()
        time.sleep(0.5)
        circle.Scale(ttl,80)
        turtle.update()
        x = random.randint(-100, 100) #получаем случайные координаты
        y = random.randint(-100, 100)
        sq = Square(x,y,50,'blue')
        sq.Draw(ttl)
        turtle.update()
        time.sleep(0.5)
        sq.Draw(ttl)
        turtle.update()
        time.sleep(0.5)
        x = random.randint(-100, 100) #получаем случайные координаты
        y = random.randint(-100, 100)
        sq.Move(ttl,x,y)
        turtle.update()    
        x = random.randint(-100, 100) #получаем случайные координаты
        y = random.randint(-100, 100)
        tring = Tringle(x,y,75,'black')
        tring.Draw(ttl)
        turtle.update()
        time.sleep(0.5)
        tring.Draw(ttl)
        turtle.update()
        time.sleep(0.5)
        x = random.randint(-100, 100) #получаем случайные координаты
        y = random.randint(-100, 100)
        tring.Move(ttl,x,y)
        turtle.update()

        time.sleep(0.5) #засыпаем на полсекунды, чтобы увидеть что нарисовали
        x = random.randint(-100, 100) #получаем случайные координаты
        y = random.randint(-100, 100)
        circle2 = Circle(x,y,40,'Violet')
        circle2.Draw(ttl)
        turtle.update()#т.к. мы сделали turtle.tracer(0, 0) нужно обновить экран, чтобы увидеть нарисованное
        time.sleep(0.5)
        x = random.randint(-100, 100) #получаем случайные координаты
        y = random.randint(-100, 100)
        circle2.Move(ttl,x,y)
        turtle.update()
        time.sleep(0.5)
        circle2.Scale(ttl,80)
        turtle.update()
        x = random.randint(-100, 100) #получаем случайные координаты
        y = random.randint(-100, 100)
        sq2 = Square(x,y,50,'Yellow')
        sq2.Draw(ttl)
        turtle.update()
        time.sleep(0.5)
        sq2.Draw(ttl)
        turtle.update()
        time.sleep(0.5)
        x = random.randint(-100, 100) #получаем случайные координаты
        y = random.randint(-100, 100)
        sq2.Move(ttl,x,y)
        turtle.update()    
        x = random.randint(-100, 100) #получаем случайные координаты
        y = random.randint(-100, 100)
        tring2 = Tringle(x,y,75,'Orange')
        tring2.Draw(ttl)
        turtle.update()
        time.sleep(0.5)
        tring2.Draw(ttl)
        turtle.update()
        time.sleep(0.5)
        x = random.randint(-100, 100) #получаем случайные координаты
        y = random.randint(-100, 100)
        tring2.Move(ttl,x,y)
        turtle.update()
    

if __name__ == '__main__':
    main()
