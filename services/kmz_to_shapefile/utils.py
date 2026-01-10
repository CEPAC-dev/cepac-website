# services/kmz_to_shapefile/utils.py

import os
import shutil
import zipfile
import re
from lxml import etree
import geopandas as gpd
from shapely.geometry import Point, LineString, Polygon

KML_NAMESPACE = "http://www.opengis.net/kml/2.2"
NAMESPACES = {"kml": KML_NAMESPACE}

def extract_kml_from_kmz(kmz_path: str, extract_folder: str) -> str:
    """
    Unzip the KMZ to `extract_folder` and return the first .kml path found.
    """
    if os.path.exists(extract_folder):
        shutil.rmtree(extract_folder)
    os.makedirs(extract_folder, exist_ok=True)

    with zipfile.ZipFile(kmz_path, "r") as kmz:
        kmz.extractall(extract_folder)

    kml_path = None
    for root, _, files in os.walk(extract_folder):
        for fname in files:
            if fname.lower().endswith(".kml"):
                kml_path = os.path.join(root, fname)
                break
        if kml_path:
            break

    if not kml_path:
        raise FileNotFoundError("No .kml file found inside the KMZ.")
    return kml_path

def parse_geometries(kml_path: str) -> gpd.GeoDataFrame | None:
    """
    Read the KML, inject xmlns:xsi if missing, parse Placemarks into a GeoDataFrame.
    """
    # 1) Load raw text
    raw = open(kml_path, "rb").read().decode("utf-8", errors="ignore")

    # 2) If there's an xsi:schemaLocation but no xmlns:xsi, inject it
    if "xsi:schemaLocation" in raw and "xmlns:xsi" not in raw:
        raw = re.sub(
            r"(<[A-Za-z0-9_:]+)(\s|>)",
            r'\1 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\2',
            raw,
            count=1,
        )

    # 3) Parse
    parser = etree.XMLParser(ns_clean=True, recover=True)
    root = etree.fromstring(raw.encode("utf-8"), parser=parser)

    features = []
    for pm in root.findall(".//kml:Placemark", namespaces=NAMESPACES):
        name_el = pm.find("kml:name", namespaces=NAMESPACES)
        name = name_el.text.strip() if (name_el is not None and name_el.text) else "NoName"

        # POINT?
        p = pm.find(".//kml:Point/kml:coordinates", namespaces=NAMESPACES)
        if p is not None and p.text:
            lon, lat = map(float, p.text.strip().split(",")[:2])
            features.append({"name": name, "geometry": Point(lon, lat)})
            continue

        # LINESTRING?
        ls = pm.find(".//kml:LineString/kml:coordinates", namespaces=NAMESPACES)
        if ls is not None and ls.text:
            pts = [tuple(map(float, coord.split(",")[:2])) for coord in ls.text.strip().split()]
            features.append({"name": name, "geometry": LineString(pts)})
            continue

        # POLYGON?
        poly = pm.find(".//kml:Polygon//kml:coordinates", namespaces=NAMESPACES)
        if poly is not None and poly.text:
            pts = [tuple(map(float, coord.split(",")[:2])) for coord in poly.text.strip().split()]
            features.append({"name": name, "geometry": Polygon(pts)})

    if not features:
        return None

    return gpd.GeoDataFrame(features, crs="EPSG:4326")

def build_shapefile_archive(kml_path: str, output_zip_path: str):
    """
    Given a kml_path, parse its geometries and write out a .zip of shapefile(s).
    """
    gdf = parse_geometries(kml_path)
    if gdf is None or gdf.empty:
        raise ValueError("No valid geometries found in KML.")

    # Temp folder named after the zip (minus “.zip”)
    base = os.path.splitext(output_zip_path)[0]
    if os.path.exists(base):
        shutil.rmtree(base)
    os.makedirs(base, exist_ok=True)

    # Split by geometry type
    geom_sets = {
        "points": gdf[gdf.geometry.type == "Point"],
        "lines": gdf[gdf.geometry.type == "LineString"],
        "polygons": gdf[gdf.geometry.type == "Polygon"],
    }

    for layer, subset in geom_sets.items():
        if not subset.empty:
            subset.to_file(os.path.join(base, f"{layer}.shp"))

    # Zip up everything in that folder
    with zipfile.ZipFile(output_zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(base):
            for fname in files:
                full = os.path.join(root, fname)
                arc = os.path.relpath(full, base)
                zf.write(full, arc)

    shutil.rmtree(base, ignore_errors=True)
