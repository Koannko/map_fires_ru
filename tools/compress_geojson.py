import json

def compress(input_file, output_file):
    # Загрузка геоданных из исходного файла
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    # Функция для уменьшения точности координат
    def round_coordinates(coordinates):
        if isinstance(coordinates, list):
            return [round_coordinates(coord) for coord in coordinates]
        elif isinstance(coordinates, float):
            return round(coordinates, 1)
        else:
            return coordinates
    # Рекурсивно обойти геоданные и уменьшить точность координат
    def round_geometry(geometry):
        if 'coordinates' in geometry:
            geometry['coordinates'] = round_coordinates(geometry['coordinates'])
        if 'geometries' in geometry:
            for sub_geometry in geometry['geometries']:
                round_geometry(sub_geometry)

    # Применить уменьшение точности координат к геоданным
    for feature in data['features']:
        if 'geometry' in feature:
            round_geometry(feature['geometry'])

    # Сохранить обновленные геоданные в целевой файл
    with open(output_file, 'w') as f:
        json.dump(data, f)


# Указать путь к исходному и целевому файлам GeoJSON
input_file = 'map_russia.geojson'
output_file = 'map_russia_compressed.geojson'

compress(input_file, output_file)