import geopandas as gpd
import pandas as pd
import numpy as np
from shapely.geometry import Point

# ============================
#  1. LOAD SHAPEFILE (ΠΕΡΙΦΕΡΕΙΕΣ)
# ============================
import os
print(os.getcwd())
shp_path = "datathon/data/raw/shapefiles/periphereies.shp"
gdf = gpd.read_file(shp_path, encoding="cp1253")

#  2. LOAD ΕΙΣΠΡΑΞΕΙΣ EXCEL

file_path = "datathon/data/raw/excel/Εισπράξεις_περιφερειακά.xlsx"

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
# mapping για αντιστοίχιση excel ↔ shp
mapping = {
    "ΑΤΤΙΚΗ (EL3)": "Π. ΑΤΤΙΚΗΣ",
    "ΒΟΡΕΙΟ ΑΙΓΑΙΟ (EL41)": "Π. ΒΟΡΕΙΟΥ ΑΙΓΑΙΟΥ",
    "ΝΟΤΙΟ ΑΙΓΑΙΟ (EL42)": "Π. ΝΟΤΙΟΥ ΑΙΓΑΙΟΥ",
    "ΚΡΗΤΗ (EL43)": "Π. ΚΡΗΤΗΣ",
    "ΑΝΑΤΟΛ. ΜΑΚΕΔΟΝΙΑ ΚΑΙ ΘΡΑΚΗ (EL51)": "Π. ΑΝΑΤΟΛΙΚΗΣ ΜΑΚΕΔΟΝΙΑΣ - ΘΡΑΚΗΣ",
    "ΚΕΝΤΡΙΚΗ ΜΑΚΕΔΟΝΙΑ (EL52)": "Π. ΚΕΝΤΡΙΚΗΣ ΜΑΚΕΔΟΝΙΑΣ",
    "ΔΥΤΙΚΗ ΜΑΚΕΔΟΝΙΑ (EL53)": "Π. ΔΥΤΙΚΗΣ ΜΑΚΕΔΟΝΙΑΣ",
    "ΗΠΕΙΡΟΣ (EL54)": "Π. ΗΠΕΙΡΟΥ",
    "ΘΕΣΣΑΛΙΑ (EL61)": "Π. ΘΕΣΣΑΛΙΑΣ",
    "ΙΟΝΙΑ ΝΗΣΙΑ (EL62)": "Π. ΙΟΝΙΩΝ ΝΗΣΩΝ",
    "ΔΥΤΙΚΗ ΕΛΛΑΔΑ (EL63)": "Π. ΔΥΤΙΚΗΣ ΕΛΛΑΔΑΣ",
    "ΣΤΕΡΕΑ ΕΛΛΑΔΑ (EL64)": "Π. ΣΤΕΡΕΑΣ ΕΛΛΑΔΑΣ",
    "ΠΕΛΟΠΟΝΝΗΣΟΣ (EL65)": "Π. ΠΕΛΟΠΟΝΝΗΣΟΥ"
}

# νέα στήλη με το όνομα του shapefile
Eisprakseis = Eisprakseis.copy()
Eisprakseis["shp_name"] = Eisprakseis["Περιφέρεια2"].map(mapping)

#  3. MERGE SHP + EXCEL

Eisprakseis_gdf = gdf.merge(
    Eisprakseis,
    left_on="PER",
    right_on="shp_name",
    how="left"
)

#  4. ΥΠΟΛΟΓΙΣΜΟΣ % ΜΕΤΑΒΟΛΗΣ

year_prev = 2023
year_curr = 2024

Eisprakseis_gdf["pct_change"] = np.nan

mask = Eisprakseis_gdf[year_prev].notna() & (Eisprakseis_gdf[year_prev] != 0)
Eisprakseis_gdf[year_curr] = Eisprakseis_gdf[year_curr].astype(float)
Eisprakseis_gdf[year_prev] = Eisprakseis_gdf[year_prev].astype(float)

Eisprakseis_gdf.loc[mask, "pct_change"] = (
    (Eisprakseis_gdf.loc[mask, year_curr] - Eisprakseis_gdf.loc[mask, year_prev])
    / Eisprakseis_gdf.loc[mask, year_prev] * 100
)

#  5. ΚΡΑΤΑΜΕ ΜΟΝΟ Ο,ΤΙ ΧΡΕΙΑΖΕΤΑΙ
Eisprakseis_gdf = Eisprakseis_gdf[["PER", "pct_change", "geometry"]].copy()
Eisprakseis_gdf = gpd.GeoDataFrame(Eisprakseis_gdf, geometry="geometry", crs=gdf.crs)

print("Tourinvest table created successfully.")


Eisprakseis_gdf = gpd.GeoDataFrame(Eisprakseis_gdf, geometry='geometry', crs=gdf.crs)
Eisprakseis_gdf['pct_change'] = Eisprakseis_gdf['pct_change'].astype('float64')

output_path = "datathon/data/processed/dedomena.gpkg"
Eisprakseis_gdf.to_file(output_path, layer="eisprakseis", driver="GPKG")
print("GPKG saved:", output_path)
