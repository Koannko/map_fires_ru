import folium

class MapFires():
    def __init__(self, state_geo, state_data, color, name, legend_name, bins, param):
        self.m = folium.Map(location=[70, 110], zoom_start=2)
        self.state_geo = state_geo
        self.state_data = state_data
        self.color = color
        self.name = name
        self.legend_name = legend_name
        self.bins = bins
        self.param = param

    def add_choropleth(self, param, year, show):
        self.c = folium.Choropleth(
            geo_data=self.state_geo,
            name=self.name + str(year) + "год",
            data=self.state_data,
            columns=["regions", f"{param}_{year}"],
            key_on="feature.properties.name",
            fill_color=self.color,
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name=self.legend_name,
            bins=self.bins,
            show = show,
        ).add_to(self.m)
        print(f'Добавлен слой {self.name} за {year} год')

    def hide_legend(self, year):
        for key in self.c._children:
            if key.startswith('color_map') and year > 2018:
                del(self.c._children[key])
                print(f'Скрыта легенда слоя {self.name} {year} год')

    def add_layer_control(self):
        folium.LayerControl().add_to(self.m)
        print(f'Добавлен контроллер для слоя {self.legend_name}')

    def save(self):
        self.m.save(f'map_{self.param}_tooltip_fires.html')
        print(f'Сохранена карта {self.param}_fires.html')