import geopandas as gpd
import pandas as pd
import numpy as np
from shapely.geometry import Point

# ============================
#  1. LOAD SHAPEFILE (ΠΕΡΙΦΕΡΕΙΕΣ)
# ============================
import os
print(os.getcwd())
shp_path = "datathon/data/raw/shapefiles/nomoi_okxe.shp"
gdf = gpd.read_file(shp_path, encoding="cp1253")





file_path = "datathon/data/raw/excel/01. Per capita gross domestic product by Nuts II, IΙΙ (Provisional Data) ( 2000 - 2022 ).xlsx"

GPD= pd.read_excel(file_path ,skiprows=8,nrows=76)
GPD=GPD.iloc[:,[0,23]]
GPD.columns=['Νομοί','GPD']

GPD=GPD.drop([0,1,10,15,18,23,24,30,38,43,48,54,59,63,69])
GPD.reset_index(drop=True, inplace=True)
GPD


