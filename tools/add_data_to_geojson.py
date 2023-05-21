import csv
import json

def add_data(input_file, output_file, full_names_file):
    # Загрузка геоданных из исходного файла
    with open(input_file, 'r') as f:
        data = json.load(f)

    # Загрузка данных о столицах из CSV файла
    full_names = {}
    with open(full_names_file, 'r', encoding='cp1251') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            subject_name = row['regions']
            full_name = row['name']
            full_names[subject_name] = full_name

    # Добавление имени столицы каждого субъекта
    for feature in data['features']:
        properties = feature.get('properties', {})
        subject_name = properties.get('name')
        full_name = full_names.get(subject_name)
        properties['full_name'] = full_name

    # Сохранение обновленных геоданных в целевой файл
    with open(output_file, 'w') as f:
        json.dump(data, f)

# Пример использования
input_file = 'map_russia_compressed.geojson'
output_file = 'map_ru_compr_with_full_names.geojson'
full_names_file = 'dataset.csv'

add_data(input_file, output_file, full_names_file)
