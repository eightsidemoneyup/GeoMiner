import math
import geopandas as gpd

gdf = gpd.read_file("global_mining_polygons_v2.gpkg")

lat, lon, km = -7.3, 27.417, 30
dlat = km / 111
dlon = km / (111 * math.cos(math.radians(lat)))
hits = gdf.cx[lon - dlon : lon + dlon, lat - dlat : lat + dlat]

print(f"{len(hits)} polygons")
print(hits[["COUNTRY_NAME", "AREA"]])
hits.to_file("manono_check.geojson", driver="GeoJSON")