import geopandas as gpd

gdf = gpd.read_file("global_mining_polygons_v2.gpkg")

print(f"{len(gdf):,} polygons")
print("coordinate system:", gdf.crs)
print(gdf.head())
