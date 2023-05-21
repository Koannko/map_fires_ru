import pandas as pd
import requests
from model import MapFires


def load_data(url, filename, file_type):
    r = requests.get(url)
    with open(filename, 'w') as f:
        f.write(r.content.decode("utf-8"))
    with open(filename, 'r') as f:
        return file_type(f)

state_geo = "geojson\\map_ru_compr_with_full_names.geojson"
file_path = "static_data\\dataset.csv"
state_data = pd.read_csv(file_path)

bins = [[0, 300, 600, 900, 1200, 1500, 2100],
        [0, 500, 1000, 3000, 5000, 7400],
        [0, 500, 1500, 3000, 4000, 5000],]

names = ["Показать число лесных пожаров за ",
         "Показать площадь, охваченную лесными пожарами за ",
         "Показать расходы на охрану лесов от лесных пожаров за "]

legend_names = ["Число лесных пожаров (единицы)",
                "Площадь лесных пожаров (тыс. гектар)",
                "Расходы на охрану лесов от лесных пожаров (млн. руб.)"]

parameters = ["num", "area", "cost"]
colors = ["YlOrBr", "Greys", "YlGnBu"]

for i, param in enumerate(parameters):
    m = MapFires(state_geo, state_data, colors[i], names[i], legend_names[i], bins[i], param)

    for year in range(2018, 2022):
        show = year == 2018

        #Добавить слой
        m.add_choropleth(param, year, show)

        #Скрыть легенду, если это необходимо
        m.hide_legend(year)
    
    # Добавить слой с именами субъектов
    m.add_tooltip()

    #Добавление переключения между слоями
    m.add_layer_control()

    # Сохранение карты в HTML с минимизацией HTML-кода
    m.save()

    styles = '.caption { font-weight: 500; font-size: 14px; }\
                .tick {font-size: 14px;}'
    m.add_styles(styles)