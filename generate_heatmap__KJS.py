#!/usr/bin/env python3
import pandas as pd
import folium
from folium.plugins import HeatMap

# open and read CSV
csv_file = 'locations.csv'
data = pd.read_csv(csv_file)

# center map on mean lat/long of data
center_lat = data['latitude'].mean()
center_lon = data['longitude'].mean()

m = folium.Map(location=[center_lat, center_lon], zoom_start=8)
# m = folium.Map(location=[center_lat, center_lon], zoom_start=12)

# load heatmap data array
heat_data = [[row['latitude'], row['longitude']] for index, row in data.iterrows()]

# add heatmap layer to the map
HeatMap(heat_data).add_to(m)

# save map to an html file
output_file = 'heatmap.html'
m.save(output_file)

print(f"Heatmap saved as {output_file}")
