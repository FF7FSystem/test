import csv
import re
import json

def task1():
    '''
    Задание №1
    Напишите регулярное выражение, с помощью которого из URL можно извлечь его домен.
    Для проверки вашего регулярного выражения будет использован следующий файл
    с URL-адресами: https://yadi.sk/d/U_pzUDNn3Zx8r7
    '''
    with open ("urls_set_1.csv") as inp:
        cont = csv.reader(inp)
        for i in cont:
            pat = r'http[s]?://(?:[\w]+@)?([\w.-]+)(?:$|[/: ])'
            result = re.findall(pat, i[0])[0]
            #print(i[0],'---->', result)
    return pat      #Ответ на задание №1

'''
Задача — написать скрипт, который будет обрабатывать данный файл в формате json (https://yadi.sk/d/np2eKmoM3Zx8rB).
Скрипт должен сгруппировать покупки по магазинам, в которых они были сделаны.
В результате должен получиться массив, состоящий из трех элементов.
Внутри каждого элемента содержатся название магазина и все покупки, совершенные в нем.
Задачу необходимо решить на Python
'''
def json_load_file(file):       #Валидация  файлов json
    try:
        return json.load(file)
    except ValueError as error:
        print("invalid json: %s" % error)

def check_key(data_context):       #Проверка наличия ключей Shop  и Product в обрабатываемом файле.
    check_key_result=False
    keys={j for i in data_context for j in i.keys()}
    if 'shop' in keys and 'product' in keys:
        check_key_result=True
    return  check_key_result

def task2():
    result=[]
    with open("task_2.json",encoding='utf-8') as read_file:
        data = json_load_file(read_file)    #валидация файла
        if check_key(data):                 #валидация ключей
            unique_shop= {i['shop'] for i in data}  #создание списка уникальных магазнов
            for shop in unique_shop:
                temp_product = []                   #список продуктов приобретенных в каждом из уникальных магазинов
                for lexicon in data:
                    if lexicon['shop'] == shop:
                        temp_product.append(lexicon['product'])
                result.append({'shop': shop, 'product': temp_product})  #запись словаря с именем магазина и продуктов
    return result   #Ответ на задание №2

def task3(arr):
    '''Дан массив из n целых чисел.
    Нужно выбрать n-1 чисел так, чтобы их произведение было максимальным среди всех возможных n-1 наборов.'''
    def chek(temp_arr):     #Проверка, что в списке только Целые числа
        f=True
        for i in temp_arr:
            if not isinstance(i, int):
                f=False
        return f

    if arr:                      #Если массив не пуст
        if chek(arr):               #Если в массиве все элементы целые
            result=1
            if len(arr)>1:          #Если массив имеет более 1 элемента
                arr=sorted(arr)[1:]
            while arr:              #перемножение элементов массива (n-1)
                result*=arr.pop()
            return result               #Ответ на задание №3
        else:
            return 'the list contains no numbers'
    else:
         return 'Epmty list!'



def task4(list1,list2):
    '''Есть два сортированных списка (массива). Нужно написать функцию, которая делает новый сортированный список
     с пересечением элементов этих двух списков '''

    #return sorted(set(list1) & set(list2))  #для случая когда не учитывается вариант,
                                            #что элементы в списках могут повторяться
    result=[]
    for i in list1:
        if i in list2:
            result.append(i)
            list2.remove(i)
    return result           #результирующий список отсортирован согласно условиям (входящие списки отсортированы)
                            #Ответ на задание №4


if __name__ == '__main__':
    #print(task1())
    #print(task2())
    #print(task3([1,2,3,4,5,5]))
    #print(task4([1, 2, 2, 5, 7,7,7, 14,14],[4, 6, 6, 7,7, 9, 14, 15]))
    print('delete #')
