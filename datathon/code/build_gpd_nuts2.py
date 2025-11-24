import pandas as pd
import geopandas as gpd

from numpy.distutils.system_info import gdk_pixbuf_2_info

path = "datathon/data/raw/excel/nama_10r_2gdp__custom_19015809_page_spreadsheet.xlsx"

shp_path = "datathon/data/raw/shapefiles/periphereies.shp"
gdf = gpd.read_file(shp_path, encoding="cp1253")

df = pd.read_excel(path, sheet_name=1,skiprows=8, nrows=13)
df=df.iloc[:,:2]

df=df.rename(columns={'Unnamed: 1':'gdk',"GEO (Labels)":'Περιφέρεια'})
df['gdk']=df['gdk']*1000000

mapping = {
    "Attiki": "Π. ΑΤΤΙΚΗΣ",
    "Voreio Aigaio": "Π. ΒΟΡΕΙΟΥ ΑΙΓΑΙΟΥ",
    "Notio Aigaio": "Π. ΝΟΤΙΟΥ ΑΙΓΑΙΟΥ",
    "Kriti": "Π. ΚΡΗΤΗΣ",
    "Anatoliki Makedonia, Thraki": "Π. ΑΝΑΤΟΛΙΚΗΣ ΜΑΚΕΔΟΝΙΑΣ - ΘΡΑΚΗΣ",
    "Kentriki Makedonia": "Π. ΚΕΝΤΡΙΚΗΣ ΜΑΚΕΔΟΝΙΑΣ",
    "Dytiki Makedonia": "Π. ΔΥΤΙΚΗΣ ΜΑΚΕΔΟΝΙΑΣ",
    "Ipeiros": "Π. ΗΠΕΙΡΟΥ",
    "Thessalia": "Π. ΘΕΣΣΑΛΙΑΣ",
    "Ionia Nisia": "Π. ΙΟΝΙΩΝ ΝΗΣΩΝ",
    "Dytiki Elláda": "Π. ΔΥΤΙΚΗΣ ΕΛΛΑΔΑΣ",
    "Sterea Elláda": "Π. ΣΤΕΡΕΑΣ ΕΛΛΑΔΑΣ",
    "Peloponnisos": "Π. ΠΕΛΟΠΟΝΝΗΣΟΥ"
}
df = df.copy()
df["shp_name"] = df["Περιφέρεια"].map(mapping)



df_gdf = gdf.merge(
    df,
    left_on="PER",
    right_on="shp_name",
    how="left"
)
df_gdf = df_gdf.drop(columns=["Περιφέρεια", "shp_name"])

output_path = "datathon/data/processed/dedomena.gpkg"
df_gdf.to_file(output_path, layer="gpd_nuts2", driver="GPKG", append=True)
