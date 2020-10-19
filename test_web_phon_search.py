import requests,re


def get_html(url):
    '''функция возвращает содержимое страницы указанной в url'''
    # В случае работы с сайтами требующими сертификат необходимо
    # выход функции оформить requests.get(url, verify=False).text
    # Будет ругаться в консоль но делать дело.
    # или просто получить сертификат на 3 месяца с letsencrypt.org
    return requests.get(url).text

def search_phone(ref):
    '''функция ищет в тексте получаемо страницы телефоны согласно шаблону, выдает общий список'''
    pat_short=r'[\D]{3}((?:\d){3}[ -](?:\d){2}[ -](?:\d){2})[\W]'   #шаблон номера без кода города и 8/+7
    pat_long=r'[\W]((?:\+7|8)(?:[ --\)-]{,2})(?:(?:\d){3})?(?:[ \)-]{,2})(?:\d){3}[ -]?(?:\d){2}[ -]?(?:\d){2})[\W]'    #Номера с кодом города и сотовые
    result1 = re.findall(pat_long, ref)
    result2 = re.findall(pat_short, ref)
    return result1+result2

def format_phone(arr):
    '''функция приводит все телефоны из списка к единому формату и возвращает только уникальные телефонные номера'''
    for id,item in enumerate(arr):
        temp=item
        if len(item) < 10:  #Если телефонный номер короткий (длина с учетом формата ###-##-##)
            temp='8495'+temp
        if temp[0:2]=='+7': #Если телефонный номер начинается с +7 приводим все к единому формату
            temp = '8' + temp[2:]
        arr[id]=''.join([i for i in temp if i.isdigit()])
    arr=set(arr)
    return  arr if arr else 'Номера телефонов не найдены'

link_list=[r'https://repetitors.info',r'https://hands.ru/company/about/']   #Входные данные в виде ссылок на страници

for url in link_list:
    ref=get_html(url)
    phone_list=search_phone(ref)
    out=format_phone(phone_list)
    print ('Уникальные телефонные номера на страничке: ',url,out)

'''При наличии ссылки и найденых по ней номерам телефонов можно осуществить  сравнение со старыми данными и актуализировать их'''
'''В скрипте не реализован парсинг динамических страниц и ругается на отсутствие сертификата при просмотре HTTPS, это можно доделать'''