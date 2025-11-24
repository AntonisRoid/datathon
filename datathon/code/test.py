import geopandas as gpd

# if os.path.exists(gpkg):
#     os.remove(gpkg)
# os.remove("data/processed/dedomena.gpkg")

#print(gdf1.head())

import subprocess
subprocess.run(["python", "datathon/code/build_eisprakseis_gpkg.py"])#print(gdf1.layers)

subprocess.run(["python", "datathon/code/build_natura_gpkg.py"])#print(gdf1.layers)
subprocess.run(["python", "datathon/code/build_episkepseis.py"])#print(gdf1.layers)
subprocess.run(["python", "datathon/code/build_gpd_nuts2.py"])#print(gdf1.layers)
subprocess.run(["python", "datathon/code/build_employment.py"])#print(gdf1.layers)

gdf1 = gpd.read_file("datathon/data/processed/dedomena.gpkg",layer= 'episkepseis')
