import asyncio
import aiohttp
import datetime
import dateutil.relativedelta
import requests
from nltk.probability import FreqDist
from nltk import word_tokenize
from nltk.corpus import stopwords
import nltk
import string
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
import json
from lxml import html

# nltk.download('punkt')
# nltk.download('stopwords')

stopwords_dict = {i: 0 for i in stopwords.words('english')} #Словарь предлогов и коротких слов, которые необходимо удалить из основного текста


def give_me_my_urls(api_key):
    """
    Получение списка статей по запросу из Гугл АПИ
    :param api_key: Ключ апи
    :return: Список урлов на статьи
    """
    date_now = (datetime.date.today())
    date_was = datetime.date.today() - dateutil.relativedelta.relativedelta(months=1)
    url = f'http://newsapi.org/v2/everything?q=russia&from={date_was}&to={date_now}&hl=en-US&gl=US&apiKey={api_key}'
    res = requests.get(url)
    res_dict = res.json()
    return [i['url'] for i in res_dict['articles']]


def remove_chars_from_text(text, chars):
    """
    Удаление символов из текста
    :param text:    текст
    :param chars: что удалить
    :return:
    """
    return "".join([ch for ch in text if ch not in chars])


def create_cloud(word_dict):
    """
    Создание картинки Облака слов из переданного словаря (Самые популярные 50 слов)
    :param word_dict: Для понимания это Словарь, ключ - склово, значение - числов повторений в тексте
    :return: ничего
    """
    text_raw = " ".join(dict(word_dict.most_common(50)))
    wordcloud = WordCloud(max_font_size=50, max_words=50, background_color="white").generate(text_raw)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig('cloud.png')


def give_me_my_dict(content):
    """
    обработка контента статьи.
    Выдергивание текста по XPath
    Перевод в нижний регистр
    Регуляркой выбирается только текст, точки и апострофы
    Удалыются "ненужные" символы, предлоги и т.д.
    разбивается на слова
    подсчитывается количество повторений слов - Создается словарь
    Из словаря исключаются "стоп слова"
    :param content: Контент странички
    :return: Словарь повторения слов
    """
    if content:
        tree = html.fromstring(content)
        film_list_lxml = tree.xpath(
            '///body//*[not(name()="script" or name()="iframe" or name()="button" or name()="button" or name()="style")]/text()')
        content_url = ' '.join(film_list_lxml).lower()
        content_url = ' '.join(re.findall('[\w.’]{2,}', content_url)).lower()
        spec_chars = string.punctuation + '\n\xa0«»\t—…’”“'
        content_url = remove_chars_from_text(content_url, spec_chars)
        content_url = remove_chars_from_text(content_url, string.digits)
        text_tokens = word_tokenize(content_url)
        text = nltk.Text(text_tokens)
        fdist = FreqDist(text)
        result = dict(fdist)
        result.update(stopwords_dict)
        return FreqDist(result)


async def get_content(url):
    """
    Получение содержания странички в асинхронном виде
    :param url:Урл странички
    :return: ответ от сервера
    """
    print(url)
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.text()
    except Exception as e:
        print('что-то пошло не так', e)


async def gobaby(urls):
    """
    Подготовка-запуск асинхронного запроса по урлам, формирование итогового словаря слов
    :param urls:
    :return:
    """
    futures = [get_content(url) for url in
               urls]  # созадниае списка футур (функций, которые будут выполнены в асинхронном режиме)
    done, _ = await asyncio.wait(futures)  # Запуск ФУТУР
    result_dict = FreqDist()  # Словарь в котором будут собираться результаты
    for future in done:  # Если футура выполнена
        try:
            result_dict.update(give_me_my_dict(future.result()))
        except Exception as e:
            print('Ошибка вот такая', e)
    create_cloud(result_dict) #Создание облага слов


def main():
    """
    Получение списка урлов из гугл апи,
    Подготовка асинхронного запроса по урлам
    :return: ничего
    """
    api_key = 'dadf7ef2f99a437eb931b5924b9ea393'
    url_list = give_me_my_urls(api_key)
    print(len(url_list))
    loop = asyncio.get_event_loop()  # запуск планировщика  асинхронных задач
    loop.run_until_complete(gobaby(url_list))  # помещение в планировщик основной задачи
    loop.close()  # закрытия планировщика задач после выполнения


if __name__ == '__main__':
    main()
