#!/usr/bin/python3
# __author:Haidarov Radik__

"""Упражнение "Количество слов"

Функция main() ниже уже определена и заполнена. Она вызывает функции 
print_words() и print_top(), которые вам нужно заполнить.

1. Если при вызове файла задан флаг --count, вызывается функция 
print_words(filename), которая подсчитывает, как часто каждое слово встречается 
в тексте и выводит:
слово1 количество1
слово2 количество2
...

Выводимый список отсортируйте в алфавитном порядке. Храните все слова 
в нижнем регистре, т.о. слова "Слон" и "слон" будут обрабатываться как одно 
слово.

2. Если задан флаг --topcount, вызывается функция print_top(filename),
которая аналогична функции print_words(), но выводит только топ-20 наиболее 
часто встречающихся слов, таким образом первым будет самое часто встречающееся 
слово, за ним следующее по частоте и т.д.

Используйте str.split() (без аргументов), чтобы разбить текст на слова.

Отсекайте знаки припинания при помощи str.strip() с знаками припинания 
в качестве аргумента.

Совет: не пишите всю программу сразу. Доведите ее до какого-то промежуточного 
состояния и выведите вашу текущую структуру данных. Когда все будет работать 
как надо, перейдите к следующему этапу.

Дополнительно: определите вспомогательную функцию, чтобы избежать дублирования 
кода внутри print_words() и print_top().

"""

import sys

# +++ваш код+++
# Определите и заполните функции print_words(filename) и print_top(filename).
# Вы также можете написать вспомогательную функцию, которая читает файл,
# строит по нему словарь слово/количество и возвращает этот словарь.
# Затем print_words() и print_top() смогут просто вызывать эту вспомогательную функцию.

def strip_str(s):
    s = s.strip(',')
    s = s.strip('.')
    s = s.strip('!')
    s = s.strip('?')
    s = s.strip(':')
    s = s.strip(';')
    s = s.strip('"')
    return s

def print_top(filename):
    f = open(filename,'r',encoding='utf-8')
    words = []
    for word in f.read().split():
        words.append(strip_str(word.lower()))    
    w_count={}
    for x in words:
        w_count.setdefault(x,0)
        w_count[x] += 1
    w_count = sorted(w_count.items(),reverse = True,key = lambda x: x[-1])
    i = 0
    for key,value in w_count:
        i +=1
        if i>20: break
       # print(i,key,value)
        print('{0:>10} {1:<2}'.format(key,value))

def print_words(filename):
    f = open(filename,'r',encoding='utf-8')
    words = []
    for word in f.read().split():
        words.append(strip_str(word.lower()))    
    w_count={}
    for x in words:
        w_count.setdefault(x,0)
        w_count[x] += 1
    for key in sorted(w_count.keys()):        
        print('{0:>10} {1:<2}'.format(key,w_count[key]))        

###

# Это базовый код для разбора аргументов коммандной строки.
# Он вызывает print_words() и print_top(), которые необходимо определить.
def main():
    if len(sys.argv) != 3:
        print('usage: python wordcount.py {--count | --topcount} file')
        sys.exit(1)
    option = sys.argv[1]
    filename = sys.argv[2]    
    if option == '--count':
        print_words(filename)
    elif option == '--topcount':
        print_top(filename)
    else:
        print('unknown option: ' + option)
    sys.exit(1)

if __name__ == '__main__':
    main()
