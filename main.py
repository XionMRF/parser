import requests
import json
import pandas as pd
import glob 
import os

url = "https://www.mos.ru/api/stats/v1/frontend/json/evp?page=1&per-page=50&sort=-visits_CURRENT_MONTH" # ссылка получена путем анализа сайта, вручную
response = requests.get(url).text # посредством библиотеки requests получаем JSON в виде строки
data = json.loads(response) # c пощью библиотеки json преобразуем данные к питоновскому словарю
df = pd.DataFrame(data['items']) # создаем дата фрейм и помещаем наши полученные данные в него

for i in range(2,14): # создадим цикл для парсинга остальных страниц с информацией
   link = f'https://www.mos.ru/api/stats/v1/frontend/json/evp?page={i}&per-page=50&sort=-visits_CURRENT_MONTH'
   response = requests.get(link.strip()).text # strip() приводим ссылку к ее нормальному виду, а не с \n
   data = json.loads(response)
   df2 = pd.DataFrame(data['items']) # создаем "переменный df" для данных из цикла для удобства
   df = pd.concat([df, df2],ignore_index=True) # добавляем строки в исходный df получаемые из "переменного df"
   df.to_excel('/content/drive/MyDrive/Colab Notebooks/report.xlsx', sheet_name ='Sheet_1') # записываем данные в эксель таблицу

report = glob.glob('/content/drive/MyDrive/Colab Notebooks/report*.xlsx')[0] # поиск по названию файла
os.replace(report, os.path.join('/content/drive/MyDrive/Colab Notebooks/archive', os.path.basename(report + '.backup'))) # отправление данных в архив
