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

file_path = "datathon/data/raw/excel/Employment by Nuts I, ΙΙ and industry (Provisional Data) ( 2000 - 2022 ).xlsx"

Employment= pd.read_excel(file_path ,skiprows=432,nrows=17)
Employment=Employment.iloc[:,[0,4,11]]
Employment.columns=['Περιφέρεια','tourism_employment','total_employment']
Employment['tourism_employment_pct']=Employment['tourism_employment']/Employment['total_employment']*100


mapping = {
    "Αττική": "Π. ΑΤΤΙΚΗΣ",
    "Βόρειο Αιγαίο": "Π. ΒΟΡΕΙΟΥ ΑΙΓΑΙΟΥ",
    "Νότιο Αιγαίο": "Π. ΝΟΤΙΟΥ ΑΙΓΑΙΟΥ",
    "Κρήτη": "Π. ΚΡΗΤΗΣ",
    "Ανατολική Μακεδονία, Θράκη": "Π. ΑΝΑΤΟΛΙΚΗΣ ΜΑΚΕΔΟΝΙΑΣ - ΘΡΑΚΗΣ",
    "Κεντρική Μακεδονία": "Π. ΚΕΝΤΡΙΚΗΣ ΜΑΚΕΔΟΝΙΑΣ",
    "Δυτική Μακεδονία": "Π. ΔΥΤΙΚΗΣ ΜΑΚΕΔΟΝΙΑΣ",
    "Ήπειρος": "Π. ΗΠΕΙΡΟΥ",
    "Θεσσαλία": "Π. ΘΕΣΣΑΛΙΑΣ",
    "Ιόνια Νησιά": "Π. ΙΟΝΙΩΝ ΝΗΣΩΝ",
    "Δυτική Ελλάδα": "Π. ΔΥΤΙΚΗΣ ΕΛΛΑΔΑΣ",
    "Στερεά Ελλάδα": "Π. ΣΤΕΡΕΑΣ ΕΛΛΑΔΑΣ",
    "Πελοπόννησος": "Π. ΠΕΛΟΠΟΝΝΗΣΟΥ"
}

Employment = Employment.drop(index=[1, 5, 10])
Employment.reset_index(drop=True, inplace=True)

Employment = Employment.copy()
Employment["shp_name"] = Employment["Περιφέρεια"].map(mapping)


Employment_gdf = gdf.merge(
    Employment,
    right_on="shp_name",
    left_on="PER",
    how="left"
)

Employment_gdf = Employment_gdf.drop(["Περιφέρεια", "shp_name"], axis=1)

output_path = "datathon/data/processed/dedomena.gpkg"
Employment_gdf.to_file(output_path, layer="employment", driver="GPKG")