#!/usr/bin/python3
# __author:Haidarov Radik__

import random

"""Лото

Правила игры в лото.

Игра ведется с помощью специальных карточек, на которых отмечены числа, 
и фишек (бочонков) с цифрами.

Количество бочонков — 90 штук (с цифрами от 1 до 90).

Каждая карточка содержит 3 строки по 9 клеток. В каждой строке по 5 случайных цифр, 
расположенных по возрастанию. Все цифры в карточке уникальны. Пример карточки:

--------------------------
    9 43 62          74 90
 2    27    75 78    82
   41 56 63     76      86 
--------------------------

В игре 2 игрока: пользователь и компьютер. Каждому в начале выдается 
случайная карточка. 

Каждый ход выбирается один случайный бочонок и выводится на экран.
Также выводятся карточка игрока и карточка компьютера.

Пользователю предлагается зачеркнуть цифру на карточке или продолжить.
Если игрок выбрал "зачеркнуть":
	Если цифра есть на карточке - она зачеркивается и игра продолжается.
	Если цифры на карточке нет - игрок проигрывает и игра завершается.
Если игрок выбрал "продолжить":
	Если цифра есть на карточке - игрок проигрывает и игра завершается.
	Если цифры на карточке нет - игра продолжается.
	
Побеждает тот, кто первый закроет все числа на своей карточке.

Пример одного хода:

Новый бочонок: 70 (осталось 76)
------ Ваша карточка -----
 6  7          49    57 58
   14 26     -    78    85
23 33    38    48    71   
--------------------------
-- Карточка компьютера ---
 7 87     - 14    11      
      16 49    55 88    77    
   15 20     -       76  -
--------------------------
Зачеркнуть цифру? (y/n)

Подсказка: каждый следующий случайный бочонок из мешка удобно получать 
с помощью функции-генератора.

Подсказка: для работы с псевдослучайными числами удобно использовать 
модуль random: http://docs.python.org/3/library/random.html

"""

class Game:

    def __init__(self):
        self.meshok =list(range(1,91))
        self.bohka = 0
        self.out_bohka = 0
        self.zamec()

    def zamec(self):
        for i in range(100):
            x = random.randint(0,89)
            y = random.randint(0,89)
            buf = self.meshok[x]
            self.meshok[x] = self.meshok[y]
            self.meshok[y] = buf

    def __next__(self):
        if self.out_bohka == 90:
            print ("Game over")
            raise StopIteration
        self.out_bohka += 1        
        x = random.randint(0,89)        
        buf = self.meshok[x]
        while buf==0:
            x = random.randint(0,89) 
            buf = self.meshok[x]
        self.meshok[x] = 0
        self.bohka = buf
        return buf

    def winner(self,card):
        if sum(card)==0:
            return True
        else:
            return False

    def __str__(self):
        return "".join(str(self.meshok))

class Loto_card:

    def __init__(self,plname):
        self.card = []
        self.status = 0
        self.pl_name = plname
        self.generic()

    def generic(self):
        for i in range(15):
            x = random.randint(1,91)
            while x in self.card:
                x = random.randint(1,91)
            self.card.append(x)
        self.card = sorted(self.card)
    
    def in_card(self,bohka):
        return bohka in self.card

    def out_card(self,bohka):
        if not bohka in self.card :            
            print("You lose")
            self.status = -1
        else:
            ind = self.card.index(bohka)
            self.card[ind] = 0
        return self.status

    def screen_card(self):
        print("--"*10)
        print("--- " + self.pl_name + " ---")
        row1 =""
        for x in self.card[:5]:
            if x<10:
                if x ==0:
                    row1 +="  - "
                else:
                    row1 +="  "+str(x) + " "
            else:
                row1 +=" " + str(x) + " "
        print(row1)
        row1 =""
        for x in self.card[5:10]:
            if x<10:
                if x ==0:
                    row1 +="  - "
                else:
                    row1 +="  "+str(x) + " "
            else:
                row1 +=" " + str(x) + " "
        print(row1)
        row1 =""
        for x in self.card[10:]:
            if x<10:
                if x ==0:
                    row1 +="  - "
                else:
                    row1 +="  "+str(x) + " "
            else:
                row1 +=" " + str(x) + " "
        print(row1)
        print("--"*10)

    def __str__(self):
        return "".join(str(self.card))

game = Game()
#for i in range(90):
#    print(next(game))
#print (game)
#print (game.bohka)

player = Loto_card("Player")
comp = Loto_card("Comp")
#for i in range(90):
#   bohka = next(game)
#   print(bohka,player)
#   print(player.inCard(bohka))
#print(game.winner(comp.card))

player.screen_card()
comp.screen_card()

bohka = next(game)
print("Достали из мешка: {0}".format(bohka))
hod = input('Зачеркнуть цифру? (y/n),q - выход: ')
while hod != 'q':
    if hod=='y':
        player.out_card(bohka)
    if player.status == -1:
        break
    if comp.in_card(bohka):
        comp.out_card(bohka)
    if game.winner(comp.card):
        print("Comp Winner")
        break
    if game.winner(player.card):
        print("Player Winner")
        break
    player.screen_card()
    comp.screen_card()
    bohka = next(game)
    print("Достали из мешка: {0}".format(bohka))
    hod = input('Зачеркнуть цифру? (y/n),q - выход: ')
    #hod ='n'
