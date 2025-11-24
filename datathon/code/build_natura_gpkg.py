import geopandas as gpd

natura = gpd.read_file("datathon/data/raw/shapefiles/natura.shp", encoding='utf-8')

natura = natura.to_crs(epsg=2100)
#os.remove(output_path)

output_path = "datathon/data/processed/dedomena.gpkg"
natura.to_file(output_path, layer="natura", driver="GPKG", append=True)
