#Επισκέψεις το 2024

import geopandas as gpd
import pandas as pd
import numpy as np
from shapely.geometry import Point

shp_path = "datathon/data/raw/shapefiles/periphereies.shp"
gdf = gpd.read_file(shp_path, encoding="cp1253")


Episkepseis = pd.read_excel("datathon/data/raw/excel/Επισκέψεις_περιφερειακά.xlsx", header=None)

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

Episkepseis = Episkepseis[Episkepseis.iloc[:,0].notna()]

Episkepseis = Episkepseis.loc[:, Episkepseis.iloc[3].notna()]
Episkepseis = Episkepseis.iloc[:,:10]
Episkepseis=Episkepseis.loc[2:,:]
Episkepseis.columns = Episkepseis.iloc[0]   # set first row as header

Episkepseis = Episkepseis[1:]               # drop that first row
Episkepseis = Episkepseis.reset_index(drop=True)
Episkepseis.loc[:, ["Περιφέρεια3",2024]]
Episkepseis['shp_name'] = Episkepseis['Περιφέρεια3'].map(mapping)
Episkepseis=Episkepseis.iloc[:13,:]

Episkepseis['Περιφέρεια3'] = Episkepseis['Περιφέρεια3'].str.strip().map(mapping)

x=gdf.merge(Episkepseis,  left_on="PER",  right_on="shp_name",    how="left")
x = x.drop('shp_name', axis=1)
c=[2016.0,2017.0,2018.0,2019.0,2020,2021,2022,2023,2024]
x[c]=x[c]*1000

x.columns = x.columns.map(str)

# τώρα ξαναγράψε
output_path = "datathon/data/processed/dedomena.gpkg"
x.to_file(output_path, layer="episkepseis", driver="GPKG", append=True)

