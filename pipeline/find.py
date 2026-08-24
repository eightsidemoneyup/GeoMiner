import math
import geopandas as gpd

SITES = {
    "Rubaya Mines":     (-1.5580,  28.8840),
    "Kenticha":          (5.5167,  39.0333),
    "Tanco":            (50.4300, -95.4465),
    "Greenbushes":     (-33.8680, 116.0650),
    "Volta Grande":    (-21.0807, -44.6156),
    "Manono-Kitotolo":  (-7.3000,  27.4170),
    "Pitinga":          (-0.7569, -60.1056),
    "Kamativi":        (-18.5330,  27.1170),
}

def nearby(gdf, lat, lon, km=15):
    # 1 degree of latitude is ~111 km everywhere. 1 degree of longitude
    # shrinks toward the poles, so scale it by cos(latitude).
    dlat = km / 111
    dlon = km / (111 * math.cos(math.radians(lat)))
    return gdf.cx[lon - dlon : lon + dlon, lat - dlat : lat + dlat]

gdf = gpd.read_file("global_mining_polygons_v2.gpkg")

for name, (lat, lon) in SITES.items():
    hits = nearby(gdf, lat, lon)
    countries = ", ".join(sorted(hits["COUNTRY_NAME"].unique())) or "—"
    print(f"{name:20} {len(hits):3} polygons   {countries}")