import pandas as pd
import requests
import folium


def load_data(url, filename, file_type):
    r = requests.get(url)
    with open(filename, 'w') as f:
        f.write(r.content.decode("utf-8"))
    with open(filename, 'r') as f:
        return file_type(f)

state_geo = "map_russia_compressed.geojson"
file_path = "dataset.csv"
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
    m = folium.Map(location=[60, 100], zoom_start=3)

    for year in range(2018, 2022):
        name = names[i] + str(year) + " год"
        legend_name = legend_names[i]
        
        c = folium.Choropleth(
            geo_data=state_geo,
            name=name,
            data=state_data,
            columns=["regions", f"{param}_{year}"],
            key_on="feature.properties.name",
            fill_color=colors[i],
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name=legend_name,
            bins=bins[i],
            show = (year == 2018),
        )

        for key in c._children:
            if key.startswith('color_map') and year > 2018:
                del(c._children[key])

        c.add_to(m)

    #Добавление переключения между слоями
    folium.LayerControl().add_to(m)

    # Сохранение карты в HTML с минимизацией HTML-кода
    m.save(f'map_{param}_fires.html')
