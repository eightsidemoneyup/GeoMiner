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

def nearby(gdf, lat, lon, km):
    dlat = km / 111
    dlon = km / (111 * math.cos(math.radians(lat)))
    return gdf.cx[lon - dlon : lon + dlon, lat - dlat : lat + dlat]

def km_between(lat1, lon1, lat2, lon2):
    dlat = (lat2 - lat1) * 111
    dlon = (lon2 - lon1) * 111 * math.cos(math.radians(lat1))
    return math.hypot(dlat, dlon)

gdf = gpd.read_file("global_mining_polygons_v2.gpkg")

for name, (lat, lon) in SITES.items():
    hits = nearby(gdf, lat, lon, 50)
    print(f"\n{name}")
    if len(hits) == 0:
        print("   nothing within 50 km")
        continue
    rows = []
    for _, row in hits.iterrows():
        minx, miny, maxx, maxy = row.geometry.bounds
        d = km_between(lat, lon, (miny + maxy) / 2, (minx + maxx) / 2)
        rows.append((d, row["AREA"], row["COUNTRY_NAME"]))
    for d, area, country in sorted(rows):
        print(f"   {d:5.1f} km   {area:7.2f} km²   {country}")