'''
Необходимо разработать программу, которая умеет анализировать данные из трех разных источников.
На вход подаются 3 файла, которые содержат результаты тестирования.
Файл 1 и Файл 2 содержат логи выполнения тестов, а Файл 3 содержит проверки этих тестов.
Результатом работы программы должен быть JSON файл, являющийся результатом слияния трех файлов по общему ключу.
JSON файл, должен содержать массив объектов. В объекте должны быть следующие поля:
название теста - статус теста - ожидаемое значение проверки - реальное значение проверки
'''

from datetime import datetime, timedelta
import json,jsonschema

def json_load_file(data):       #Валидация всех загружаемых файлов json
    try:
        return json.load(data)
    except ValueError as error:
        print("invalid json: %s" % error)

def valid(file,schema):          #Валидация соответствия загруженного json и его chema
    try:
        jsonschema.validate(file,schema)
    except jsonschema.ValidationError as e:
        print (e.message)

def treatment_file_type1(file):        # обработка фалйла типа 1 и запись данных в temp_result
    for i in file['logs']:
        res = 1 if i["output"]=="fail" else 0
        temp_result.update({datetime.fromtimestamp(i["time"]):[{'Name_test':i['test'],'res':res}]})

def treatment_file_type2(file):         # обработка фалйла типа 1 и запись данных в temp_result
    months = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
              'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
    for i in file["suites"]:
        for j in i["cases"]:
            time_t = j['time'].split(',')
            time_t = time_t[1][:-3].split()
            temp_t = time_t[0].split('-')
            time_t = '20' + temp_t[2] + '-' + months[temp_t[1]] + '-' + temp_t[0]+ 'T' + time_t[1]
            temp_result.update({datetime.strptime(time_t, "%Y-%m-%dT%H:%M:%S"): [{'Name_test': i['name']+'-'+j['name'], 'res':j["errors"]}]})

def treat_and_comparison(file):         # обработка фалйла типа 3 сравнение с temp_result
    for i in file["captures"]:
        time_t=i['time'].split('+')
        temp_zone=time_t[1].split(':')
        time_test=datetime.strptime(time_t[0], "%Y-%m-%dT%H:%M:%S")+timedelta(hours=int(temp_zone[0]),minutes=int(temp_zone[1]))
        if time_test in temp_result:
            test_data=temp_result.pop(time_test)[0]
            checked_temp = 0 if  i["expected"] == i["actual"] else 1
            checked= "checked - check and test match up" if test_data['res']==checked_temp else "checked - check and test do not match"
            result.append({'Name_test': test_data['Name_test'],'Status': checked,"Expected": i["expected"],"Actual": i["actual"]})
    if temp_result:
        for i in temp_result.values():
            i=i[0]
            result.append({'Name_test': i['Name_test'], 'Status': 'Not verified', "expected": 'not known', "actual": 'not known'})

def load_and_treat(file_name,chem_name,treatment):  #Загрузка файла конкретного типа, валидация, передача в функцию обработки типа файла или сравнения
    content_file=open(file_name)            #открытие файла в индетификатор
    content_chema = open(chem_name)
    file = json_load_file(content_file)     #проверка содержимого файла (что это json), загрузка его содержимого
    schema = json_load_file(content_chema)
    content_file.close()
    content_chema.close()
    valid(file,schema)                      #сравнение содержимого файла и его схемы
    if treatment == 'type1':
        treatment_file_type1(file)
    elif treatment == 'type2':
        treatment_file_type2(file)
    elif treatment == 'type3':
        treat_and_comparison(file)

if __name__ == '__main__' :
    #def main():                 вставить,чтобы код не стартовал при импорте из другого файла или оформить отдельной функцией)
    result=[]
    temp_result={}
    load_and_treat(file_name=r'file1.json',chem_name=r"file1_chema.json",treatment='type1')
    load_and_treat(file_name=r'file2.json',chem_name=r"file2_chema.json",treatment='type2')
    load_and_treat(file_name=r'file3.json',chem_name=r"file3_chema.json",treatment='type3')

    with open (r"result.json",'w') as write_file:           #Записать результаты обработки всех фалов в файл
        json.dump(result, write_file, sort_keys=True,indent=4)