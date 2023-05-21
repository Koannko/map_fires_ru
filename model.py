import folium

class MapFires():
    def __init__(self, state_geo, state_data, color, name, legend_name, bins, param):
        self.m = folium.Map(location=[70, 110], zoom_start=3)
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
        print(f'Добавлен слой {self.name} {year} год')

    def hide_legend(self, year):
        for key in self.c._children:
            if key.startswith('color_map') and year > 2018:
                del(self.c._children[key])
                print(f'Скрыта легенда слоя {self.name} {year} год')

    def add_layer_control(self):
        folium.LayerControl().add_to(self.m)
        print(f'Добавлен контроллер для слоя {self.legend_name}')

    def add_tooltip(self):
        self.tooltip = folium.GeoJsonTooltip(fields=['full_name'],
                            aliases=[''],
                            labels=True,
                            localize=True,
                            sticky=True,
                            style="""
                            background-color: #FFFFFF;
                            border: 1 solid black;
                            border-radius: 1px;
                            box-shadow: 1px;
                            font-size: 14px;
                            """,)

        g = folium.GeoJson(self.state_geo, 
            name="Показывать названия субъектов РФ",
            style_function=lambda x: {
                "fillColor": "transparent",
                "color": "transparent",
                "weight": 1,
            },
            tooltip=self.tooltip, 
            smooth_factor=1,
            highlight_function=lambda x: {"fillColor": "grey", "color": "grey", "opacity": 0.1},
        ).add_to(self.m)
        print(f'Добавлен интерактив для слоя {self.legend_name}')

    def save(self):
        self.m.save(f'maps\\{self.param}_fires.html')
        print(f'Сохранена карта {self.param}_fires.html')
    
    def add_styles(self, styles):
        # Открытие HTML файла для записи
        with open(f'maps\\{self.param}_fires.html', 'a') as f:
            # Запись строки со стилями в файл
            f.write('<style>{}</style>\n'.format(styles))
        print(f'Добавлены стили для карты {self.param}_fires.html')