
def get_pct_change_by_point(lon, lat):

    point = gpd.GeoSeries([Point(lon, lat)], crs="EPSG:4326")
    point_transformed = point.to_crs(Eisprakseis_gdf.crs)
    point_df = gpd.GeoDataFrame(geometry=point_transformed)

    result = gpd.sjoin(point_df, Eisprakseis_gdf, how="inner", predicate="within")

    if not result.empty:
        return result["pct_change"].iloc[0]
    else:
        return None
