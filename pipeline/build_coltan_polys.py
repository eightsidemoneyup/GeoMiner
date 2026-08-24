"""Add mined-land footprints for GeoMiner's coltan sites."""
import json
import math
import re

import geopandas as gpd

GPKG = "global_mining_polygons_v2.gpkg"
PAGE = "GeoMiner.html"
TOLERANCE = 0.0002        # ~22 m, matches GeoMiner's 4-dp coords

# name: (lat, lon, search radius in km)
# Radii are per-site because the published coordinates vary in precision —
# Tanco and Greenbushes are on the workings, the others are nearby towns.
# Rubaya: absent from the dataset entirely (see notes).
# Manono: nearest polygon is 25 km away, too far to attribute confidently.
SITES = {
    "Manono-Kitotolo":  ( -7.3000,  27.4170, 30),
    "Kenticha":        (  5.5167,  39.0333, 10),
    "Tanco":           ( 50.4300, -95.4465,  5),
    "Greenbushes":     (-33.8680, 116.0650,  5),
    "Volta Grande":    (-21.0807, -44.6156,  8),
    "Pitinga":         ( -0.7569, -60.1056, 10),
    "Kamativi":        (-18.5330,  27.1170, 12),
}


def nearby(gdf, lat, lon, km):
    dlat = km / 111
    dlon = km / (111 * math.cos(math.radians(lat)))
    return gdf.cx[lon - dlon : lon + dlon, lat - dlat : lat + dlat]


def rings_of(geom):
    parts = geom.geoms if geom.geom_type == "MultiPolygon" else [geom]
    out = []
    for part in parts:
        flat = []
        for lon, lat in part.exterior.coords:
            flat += [round(lat, 4), round(lon, 4)]
        out.append(flat)
    return out


gdf = gpd.read_file(GPKG)
html = open(PAGE, encoding="utf-8").read()

match = re.search(r"const MINES_RAW = (\[.*?\]);\n", html, re.S)
mines = json.loads(match.group(1))
index_of = {row[0]: i for i, row in enumerate(mines)}

records = []
for name, (lat, lon, km) in SITES.items():
    if name not in index_of:
        print(f"  !  {name}: not in MINES_RAW — check the spelling")
        continue

    fi = index_of[name]
    hits = nearby(gdf, lat, lon, km)
    print(f"  ·  {name:16} r={km:2} km   {len(hits):2} polygons")

    for _, row in hits.iterrows():
        simple = row.geometry.simplify(TOLERANCE, preserve_topology=True)
        if simple.is_empty:
            continue
        records.append([fi, round(row["AREA"], 2), *rings_of(simple)])

print(f"\n{len(records)} records ready")
json.dump(records, open("coltan_polys.json", "w"))