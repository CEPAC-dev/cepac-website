import os
import zipfile
import shutil
from lxml import etree
from shapely.geometry import Polygon, Point, LineString
from pyproj import Transformer
import pandas as pd

KML_NAMESPACE = "http://www.opengis.net/kml/2.2"
NAMESPACES = {"kml": KML_NAMESPACE}

def extract_kml_from_kmz(kmz_path, output_directory):
    if os.path.exists(output_directory):
        shutil.rmtree(output_directory)
    os.makedirs(output_directory, exist_ok=True)

    with zipfile.ZipFile(kmz_path, "r") as kmz:
        kmz.extractall(output_directory)

    kmls = []
    for root, _, files in os.walk(output_directory):
        for f in files:
            if f.lower().endswith(".kml"):
                kmls.append(os.path.join(root, f))

    if not kmls:
        raise FileNotFoundError("No KML file found inside KMZ.")
    return kmls

def parse_geometries_from_kml(kml_path):
    # Read raw bytes so we can patch missing xsi namespace if needed
    with open(kml_path, 'rb') as f:
        content = f.read()

    # If the document uses xsi:schemaLocation but doesn't define xmlns:xsi, inject it
    if b'xsi:schemaLocation' in content and b'xmlns:xsi=' not in content:
        content = content.replace(
            b'<kml',
            b'<kml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"',
            1
        )

    # Parse the (possibly patched) KML
    parser = etree.XMLParser(remove_blank_text=True)
    root = etree.fromstring(content, parser)

    features = []
    for placemark in root.findall('.//kml:Placemark', namespaces=NAMESPACES):
        name_elem = placemark.find('kml:name', namespaces=NAMESPACES)
        name = name_elem.text.strip() if name_elem is not None and name_elem.text else 'NoName'

        # Point
        pt = placemark.find('.//kml:Point/kml:coordinates', namespaces=NAMESPACES)
        if pt is not None and pt.text:
            lon, lat = map(float, pt.text.strip().split(',')[:2])
            features.append({
                'Name': name,
                'Geometry Type': 'Point',
                'Coordinates': f"{lat}, {lon}",
                'Area (m²)': '',
                'Perimeter (m)': '',
            })
            continue

        # LineString
        ls = placemark.find('.//kml:LineString/kml:coordinates', namespaces=NAMESPACES)
        if ls is not None and ls.text:
            raw = ls.text.strip().split()
            coords = [(float(c.split(',')[0]), float(c.split(',')[1])) for c in raw]
            line = LineString(coords)
            features.append({
                'Name': name,
                'Geometry Type': 'LineString',
                'Coordinates': '; '.join([f"({lat},{lon})" for lon, lat in coords]),
                'Area (m²)': '',
                'Perimeter (m)': line.length,
            })
            continue

        # Polygon
        poly = placemark.find('.//kml:Polygon//kml:coordinates', namespaces=NAMESPACES)
        if poly is not None and poly.text:
            raw = poly.text.strip().split()
            coords = [(float(c.split(',')[0]), float(c.split(',')[1])) for c in raw]
            if len(coords) >= 3:
                lon0, lat0 = coords[0]
                zone = int((lon0 + 180) // 6) + 1
                is_north = lat0 >= 0
                epsg = 32600 + zone if is_north else 32700 + zone
                transformer = Transformer.from_crs("EPSG:4326", f"EPSG:{epsg}", always_xy=True)
                utm_coords = [transformer.transform(lon, lat) for lon, lat in coords]
                polygon = Polygon(utm_coords)
                area = polygon.area
                perimeter = polygon.length
            else:
                area = perimeter = 0
            features.append({
                'Name': name,
                'Geometry Type': 'Polygon',
                'Coordinates': '; '.join([f"({lat},{lon})" for lon, lat in coords]),
                'Area (m²)': area,
                'Perimeter (m)': perimeter,
            })

    if not features:
        return None

    return pd.DataFrame(features)

def convert_kmz_to_excel(input_kmz_path, output_excel_path):
    temp_dir = os.path.join(os.path.dirname(input_kmz_path), "temp_kmz_to_excel")
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir, exist_ok=True)

    try:
        kml_paths = extract_kml_from_kmz(input_kmz_path, temp_dir)
        dfs = []
        for kml in kml_paths:
            df = parse_geometries_from_kml(kml)
            if df is not None:
                dfs.append(df)
        if not dfs:
            raise ValueError("No geometry could be parsed from KML(s).")
        result_df = pd.concat(dfs, ignore_index=True)
        result_df.to_excel(output_excel_path, index=False)
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)
