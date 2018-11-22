import pandas as pd
from yandex_geocoder import Client
from tqdm import tqdm

# Path to csv with data
# Need fields:  'street' -> address, example "ул. Кутузова 163",
#               'longitude' -> longitude,
#               'latitude' -> latitude,
csv_path = ""
# City name in Russian. Example: Тула
city = ""

raw_data = pd.read_csv(csv_path)
raw_data['is_was_checked'] = False

print("Items for processing: ", len(raw_data))

for index, row in tqdm(raw_data.iterrows()):
    try:
        if row['street']:
            address = city + " " + row['street']
            true_coordinates = Client.coordinates(address)
            raw_data.loc[index, 'longitude'] = true_coordinates[0]
            raw_data.loc[index, 'latitude'] = true_coordinates[1]
            raw_data.loc[index, 'is_was_checked'] = True
    except:
        print("Not found: ", address)

raw_data.to_csv('data_with_correct_coordinates.csv')
