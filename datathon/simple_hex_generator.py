import h3
import pprint
import pandas as pd

import geopandas as gpd
from shapely.geometry import Polygon

from branca.colormap import linear
import folium
start_lat = 37.9838  # Γεωγραφικό πλάτος (Latitude)
start_lon = 23.7275  # Γεωγραφικό μήκος (Longitude)

# Η ανάλυση του πλέγματος (Resolution).
# Resolution 9: περίπου 700 μέτρα πλευρά-πλευρά (ιδανικό για 1 χλμ. περιοχή).
RESOLUTION = 9

K_RING_SIZE = 3 # Η "ακτίνα" (k-ring) των γειτονικών εξαγώνων. K=3 σημαίνει το κεντρικό + 3 δακτύλιοι γύρω του.

# --- 2. Ορισμός της Συνάρτησης Υπολογισμού Τιμής ---
def calculate_value(lat, lon):
    value = lat-lon
    return round(value, 2)


# --- 3. Υπολογισμός H3 Index του αρχικού σημείου ---
initial_h3_index = h3.latlng_to_cell(start_lat, start_lon, RESOLUTION)

# --- 4. Δημιουργία του Πλέγματος (grid_disk) ---
h3_grid_indices = h3.grid_disk(initial_h3_index, K_RING_SIZE)

# --- 5. Εξαγωγή Δεδομένων και Υπολογισμός Τιμών ---
polygon_data = []

for h3_index in h3_grid_indices:
    # 5α. Συντεταγμένες Κέντρου του Εξαγώνου (cell_to_latlng)
    center_lat, center_lon = h3.cell_to_latlng(h3_index)
    # 5β. Συντεταγμένες Κορυφών του Εξαγώνου (cell_to_boundary)
    # Η προεπιλογή είναι (lat, lon)
    boundary_coordinates = h3.cell_to_boundary(h3_index)

    # 5γ. Υπολογισμός της Τιμής
    value = calculate_value(center_lat, center_lon)

    # Αποθήκευση των δεδομένων
    polygon_data.append({
        'h3_index': h3_index,
        'center_lat': center_lat,
        'center_lon': center_lon,
        'boundary': boundary_coordinates,  # Λίστα με ζεύγη (lat, lon)
        'calculated_value': value
    })

# --- 6. Αποτελέσματα ---
print("✅ Η Δημιουργία του Εξαγωνικού Πλέγματος Ολοκληρώθηκε")
print(f"Ανάλυση H3: {RESOLUTION}")
print(f"Συνολικά Εξάγωνα: {len(polygon_data)}")

print("\n--- Δεδομένα Πρώτου Εξαγώνου (Παράδειγμα) ---")
pprint.pprint(polygon_data[0])

df = pd.DataFrame(polygon_data)


print("\n3. Μετατροπή σε GeoDataFrame και Αποθήκευση GeoJSON...")

# 1. Δημιουργία της στήλης "geometry"
# Κάθε στοιχείο στη στήλη 'boundary' είναι μια λίστα με (lat, lon) ζεύγη.
# Η shapely χρειάζεται (lon, lat) ζεύγη για σωστό GeoJSON/GeoPandas.
def create_polygon(boundary_coords):
    # Επιστρέφει τη λίστα με (lon, lat)
    coords_lon_lat = [(lon, lat) for lat, lon in boundary_coords]
    return Polygon(coords_lon_lat)

df['geometry'] = df['boundary'].apply(create_polygon)

# 2. Δημιουργία GeoDataFrame
# Ορίζουμε το CRS (Σύστημα Αναφοράς Συντεταγμένων) ως WGS84 (EPSG:4326)
# που είναι το standard για γεωγραφικές συντεταγμένες.
gdf = gpd.GeoDataFrame(df, geometry='geometry', crs="EPSG:4326")

# 3. Αποθήκευση σε GeoJSON
output_geojson_file = 'h3_hex_grid_data.geojson'
gdf.to_file(output_geojson_file, driver='GeoJSON')

print(f"✅ Τα γεωχωρικά δεδομένα αποθηκεύτηκαν επιτυχώς στο: {output_geojson_file}")
print("   Μπορείτε να ανοίξετε αυτό το αρχείο σε οποιοδήποτε GIS λογισμικό (π.χ. QGIS).")



# m = folium.Map(location=[start_lat, start_lon], zoom_start=12)
#
# min_val = df['calculated_value'].min()
# max_val = df['calculated_value'].max()
# colormap = linear.YlOrRd_09.scale(min_val, max_val)
# m.add_child(colormap)
#
#
# for _, row in df.iterrows():
#     # Παίρνουμε το χρώμα με βάση την τιμή
#     fill_color = colormap(row['calculated_value'])
#
#     # Το boundary είναι μια λίστα με (lat, lon) ζεύγη
#     polygon_boundary = row['boundary']
#
#     folium.Polygon(
#         locations=polygon_boundary,
#         weight=1,
#         fill_color=fill_color,
#         fill_opacity=0.6,
#         tooltip=f"Value: {row['calculated_value']}"
#     ).add_to(m)
#
# output_file = 'h3_hexagonal_grid_map.html'
# m.save(output_file)
# print(f"Ο χάρτης αποθηκεύτηκε στο: {output_file}")

