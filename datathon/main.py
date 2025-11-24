import matplotlib.pyplot as plt
import pandas as pd
import re
import geopandas as gpd
from matplotlib.patches import Patch
import os
import numpy as np
import h3
from shapely.geometry import Polygon

print(os.getcwd())
file_path = "datathlon\Εισπράξεις_περιφερειακά.xlsx"

df = pd.read_excel(file_path, sheet_name="ΠΕΡΙΦΕΡΕΙΑΚΑ", skiprows=3)

region_col = [col for col in df.columns if "Περιφέρεια" in str(col)][0]

print(f"Using column: {region_col}")

region_mask = df[region_col].astype(str).str.contains(r"\(EL\d+\)")

df_regions = df[region_mask]

year_cols = [col for col in df_regions.columns if str(col).isdigit()]

# Create a list of columns to keep

cols_to_keep = [region_col] + year_cols

# Filter the dataframe to keep only these columns
Eisprakseis = df_regions[cols_to_keep]

res,k= 8,6
center = h3.latlng_to_cell(38.0, 23.7, 8)

#υπολογιζει ολα τα κεντρα
cells = h3.k_ring(center, k)

boundary = h3.cell_to_boundary(h)       # δίνει λίστα από (lat, lon)

poly = Polygon([(lon, lat) for lat, lon in boundary])




