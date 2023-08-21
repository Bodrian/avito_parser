import requests                 #как минимум для get
import csv                      #для Записи в таблицы
import re                       #для выделения чисел из числа
import string                   #для удаление из строки символов
from fake_useragent import UserAgent #для эмитации живого браузера
from urllib import request      #для общей выгрузке в html файл - верхний абзац
from bs4 import BeautifulSoup   #парсит страницу
from selenium import webdriver                      #навигация по сайту
from selenium.webdriver.firefox.options import Options #чтобы убрать графический интерфейс
import time                              #чтобы можно было делать паузы
from PIL import Image                               #чтобы открыть картинку и вырезать часть (не нарушаем пунктуацию)
import pytesseract                                  #чтобы из картинки получить число (распознать цифры)
from selenium.common.exceptions import NoSuchElementException #для проверки а наличие кнопки телефона на странице

def telefon(link, self):                                  #self - переменная по которой ищестся кнопка с телефоном
    self111 = '//div[@class="item-phone-big-number js-item-phone-big-number"]//*'
    n = 3                                           #время засыпания между клацаниями по браузеру (зависит от быстродействия компьютера)
    opts = Options()                                #создает переменную отвечающую за параметры фаерфокса
    opts.headless = True                            #убирает графический интерфейс у фаерфркса
    driver = webdriver.Firefox(options=opts)        #открывает firefox
    driver.get(link)                                #вбиваем страницу которую откроет Firefox
    try:                                            #проверяем есть ли кнопка телефона на странице
        driver.find_element_by_xpath(self)
    except NoSuchElementException:
        print('0 - Ошибка - нет кнопки телефона !!!!!!!!!!!!!!!!!!!!!!!!!!!')
        text = '0'
        with open('error.txt', 'a') as errorfile:
            errorfile.write(time.ctime() + ' Ошибка - нет кнопки телефона\n' + page_link + '\n')
    else:                                           #если кнопка телефона есть, то нажимаем на нее
        button = driver.find_element_by_xpath(self) #ищем кнопку
        button.click()                                  #нажимаем на кнопку
        time.sleep(n)                                        #пауза для подгрузки окна
        driver.save_screenshot('avito_screen_tmp.png')  #сохраняем скриншот экрана в файл
        try:                                            #проверяем есть ли кнопка телефона на странице
            driver.find_element_by_xpath(self111)
        except NoSuchElementException:
            print('0 - Ошибка - на кнопке телефона нет телефона !!!!!!!!!!!!!!!!!!!!!!!!!!!')
            text = '0'
            with open('error.txt', 'a') as errorfile:
                errorfile.write(time.ctime() + ' Ошибка - на кнопке телефона нет телефона\n' + page_link + '\n')
        else:
            image = driver.find_element_by_xpath(self111)   #выдираем именно картинку телефона (единственный элемент из класса див)
            location = image.location                       #получаем координаты левой верхней точки на скриншоте - координаты словаря x и y
            size = image.size                               #штрина и высота картинки - координаты словаря width и height
            x = location['x']                               #выдергиваем данные из словаря координаты левого верхнего угла по отдельности
            y = location['y']
            width = size['width']                           #выдергиваем ширину и высоту из словаря
            height = size['height']
            image = Image.open('avito_screen_tmp.png')      #открываем скриншот экрана (не нарушаем пунктуацию)
            image.crop((x, y, x+width, y+height)).save('avito_tel.gif')                                                 #вырезаем картинку телефона и сохраняем ее в файл
            image = Image.open('avito_tel.gif')             #открывем картинку с цифрами
            text = pytesseract.image_to_string(image, lang='eng') #распознаем цифры и выводим их
            text = text.replace(' ', '')                    #удаляет пробелы из номера телефона
            text = text.replace('-', '')                    #удаляет тире из номера телефона
    finally:
        driver.close()                                  #закрывает фаерфокс
        driver.quit()                                   #закрывает геко драйвер       
    return text

def htmlfile(htmlname):                                 #записывает данные в хтмл файл
    avitohtml = open(htmlname, 'a', encoding = 'utf-8')
    avitohtml.write('<tr><td>')
    avitohtml.write('Просм:')            
    avitohtml.write(prosm1)         #пишем кол-во просмотров
    avitohtml.write(' </td><td>')
    avitohtml.write('S = ') 
    avitohtml.write(plosh2)        #пишем площадь
    avitohtml.write(' </td><td>')
    avitohtml.write('Цена: ')
    avitohtml.write(price2)         #пишем цену
    avitohtml.write(' </td><td>')
    avitohtml.write(ss)             #пишем ссылку
    avitohtml.write(' </td><td>')
    avitohtml.write(adress22)       #пишем адрес
    avitohtml.write(' </td><td>')
    avitohtml.write(tip2)           #пишем тип помещения
    avitohtml.write(' </td><td>')
    avitohtml.write(time.ctime())   #пишем время
    avitohtml.write('</td></tr>')
    avitohtml.close()

def dadress(soup, tag):                                         #выдираем текст с тага класс и проверяем что он есть с записью в файл ошибок
    try:
        adress = str(soup.find(class_=tag).text)
    except AttributeError:                                      #если нет адреса
        adress22 = '0'
        with open('error.txt', 'a') as errorfile:
            errorfile.write(time.ctime() + ' Ошибка - нет данных\n' + page_link + '\n' + tag + '\n')
        print('Ошибка - нет данных\n' + page_link + '\n' + tag)
    except Exception:                                           #если ошибка
        adress22 = '0'
        with open('error.txt', 'a') as errorfile:
            errorfile.write(time.ctime() + ' Ошибка - неизвестная ошибка\n' + page_link + '\n')
        print('Ошибка - неизвестная ошибка\n' + page_link + '\n' + tag)
    else:
        adress22 = adress.strip()                               #удаляем пробелы вначале и вконце
    finally:
        return adress22

myUrl = 'https://www.mytoys.ru/product/14861316' # присваиваю переменной урл

while 1:
    page = requests.get(myUrl)
    soup = BeautifulSoup(page.text, 'html.parser')
    links = soup.find_all(class_='sizes-block') #ищем все размеры которых нет
    ##выберает только ссылки для браузера из объяв
    print(links)
    for links1 in links:
        n = 0
        print(links1)
        time.sleep(3)
        #if 'itemprop' in str(links1) :                          #проверяет по атребуту ссылки, что это нужная ссылка
        #    href = 'https://www.avito.ru' + links1.get('href') #участвует в программе
        #else :
        #    print(links1.text)                                  #если в ссылка не того формата, то орываем цикл
        #    continue
 
        #with open(r"vitasuper.html", "r", encoding = 'utf-8') as file:
        #    for line in file: #проверяем наличие ссылки в файле
        #        if links1.get('href') in line :
        #            n = 1
        #            print(time.ctime())                                                 #в случае если элемент уже есть пишем время


        
    time.sleep(1800)
