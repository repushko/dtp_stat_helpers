import pandas as pd
import numpy as np
import osmnx as ox
import networkx as nx
from shapely.geometry import Point
from shapely.geometry import LineString
from tqdm import tqdm

# Path to csv with data
# Need fields:  'street' -> address, example "ул. Кутузова 163",
#               'longitude' -> longitude,
#               'latitude' -> latitude,
csv = ""

# City name abd country (in Englisth). Example: Tula, Russia
city_and_country = ""


# Helpers
# Calculate projection of point to line
def calculate_projection(p, ls):
    point = Point(p[0], p[1])
    line = LineString(ls)

    x = np.array(point.coords[0])

    u = np.array(line.coords[0])
    v = np.array(line.coords[len(line.coords) - 1])

    n = v - u
    n /= np.linalg.norm(n, 2)

    return u + n * np.dot(x - u, n)


# Get nearest projection of point
def nearest_projection(G, point):
    nearest_node = ox.geo_utils.get_nearest_node(G, point, method='haversine', return_dist=False)
    nearest_node_info = G.nodes[nearest_node]
    neighbors = nx.all_neighbors(G, nearest_node)
    lines = []
    for i in neighbors:
        current_node_info = G.nodes[i]
        lines.append(
            [(current_node_info['y'], current_node_info['x']), (nearest_node_info['y'], nearest_node_info['x'])])
    projections = []
    for i in lines:
        projections.append(calculate_projection(point, i))
    final_projection = []
    min_distance = 1000
    for i in projections:
        new_min_distance = ox.utils.euclidean_dist_vec(i[0], i[1], point[0], point[1])
        if new_min_distance < min_distance:
            min_distance = new_min_distance
            final_projection = i
    return final_projection, min_distance


# Main pipeline
# Loading graph of street and data
G = ox.graph_from_place(city_and_country, network_type='drive')

data = pd.read_csv(csv)
data['projection_lat'] = 0
data['projection_lon'] = 0

print("Items for processing: ", len(data))

for index, row in tqdm(data.iterrows()):
    try:
        projection = nearest_projection(G, [row['latitude'], row['longitude']])
        data.loc[index, 'projection_lat'] = projection[0][0]
        data.loc[index, 'projection_lon'] = projection[0][1]
    except:
        print("Error with projection address:", row['street'])

data.to_csv('addresses_to_street_projections.csv')
