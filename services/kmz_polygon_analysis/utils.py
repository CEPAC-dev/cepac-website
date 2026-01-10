import os
import zipfile
import shutil
from lxml import etree
from shapely.geometry import Polygon
from pyproj import Transformer

KML_NAMESPACE = "http://www.opengis.net/kml/2.2"
NAMESPACES = {"kml": KML_NAMESPACE}


def extract_kml_files_from_kmz(kmz_path, output_directory):
    kml_files = []
    with zipfile.ZipFile(kmz_path, "r") as kmz:
        kmz.extractall(output_directory)

    for root, _, files in os.walk(output_directory):
        for file in files:
            if file.lower().endswith(".kml"):
                kml_files.append(os.path.join(root, file))

    if not kml_files:
        raise FileNotFoundError("No KML files found inside KMZ archive.")
    return kml_files


def get_hierarchical_path(element):
    path = []
    while element is not None:
        name = element.find("kml:name", NAMESPACES)
        if name is not None and name.text:
            path.append(name.text.strip())
        element = element.getparent()
    return "\\".join(reversed(path))


def process_single_kml(kml_path, excel_rows, placemark_index_start):
    transformer = None
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(kml_path, parser)
    root = tree.getroot()
    placemark_index = placemark_index_start

    for placemark in root.findall(".//kml:Placemark", namespaces=NAMESPACES):
        placemark_index += 1
        name_elem = placemark.find("kml:name", namespaces=NAMESPACES)
        coords_elem = placemark.find(".//kml:Polygon/kml:outerBoundaryIs/kml:LinearRing/kml:coordinates", namespaces=NAMESPACES)

        original_name = name_elem.text.strip() if name_elem is not None and name_elem.text else f"Unknown_{placemark_index}"

        if coords_elem is not None and coords_elem.text and coords_elem.text.strip():
            coord_text = coords_elem.text.strip()
            coords = [tuple(map(float, pt.split(",")[:2])) for pt in coord_text.split() if pt.strip()]
            if coords:
                lon0, lat0 = coords[0]
                utm_zone = int((lon0 + 180) // 6) + 1
                is_northern = lat0 >= 0
                utm_epsg = 32600 + utm_zone if is_northern else 32700 + utm_zone

                if transformer is None:
                    transformer = Transformer.from_crs("EPSG:4326", f"EPSG:{utm_epsg}", always_xy=True)

                utm_coords = [transformer.transform(lon, lat) for lon, lat in coords]
                polygon = Polygon(utm_coords)
                area = polygon.area

                new_name = f"{original_name}_{area:.2f}"
                if name_elem is None:
                    name_elem = etree.SubElement(placemark, "{%s}name" % KML_NAMESPACE)
                name_elem.text = new_name

                hierarchical_path = get_hierarchical_path(placemark)

                excel_rows.append({
                    "Hierarchical Path": hierarchical_path,
                    "Original Polygon Name": original_name,
                    "Updated Polygon Name": new_name,
                    "Area (m²)": area,
                    "Has Coordinates": True
                })
        else:
            hierarchical_path = get_hierarchical_path(placemark)
            excel_rows.append({
                "Hierarchical Path": hierarchical_path,
                "Original Polygon Name": original_name,
                "Updated Polygon Name": "N/A",
                "Area (m²)": "N/A",
                "Has Coordinates": False
            })

    # overwrite modified KML with updated names
    with open(kml_path, "wb") as f:
        tree.write(f, pretty_print=True, xml_declaration=True, encoding="UTF-8")

    return placemark_index


def analyze_and_repackage(input_kmz_path, output_kmz_path, output_excel_path):
    """
    Core flow: unpack, process KML(s), repackage updated KMZ, write Excel summary.
    """
    temp_dir = os.path.join(os.path.dirname(input_kmz_path), "temp_kmz_polygon_analysis")
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir, exist_ok=True)

    try:
        kml_files = extract_kml_files_from_kmz(input_kmz_path, temp_dir)
        excel_rows = []
        placemark_index = 0

        for kml_file in kml_files:
            placemark_index = process_single_kml(kml_file, excel_rows, placemark_index)

        # Recreate KMZ with updated KMLs
        with zipfile.ZipFile(output_kmz_path, "w", zipfile.ZIP_DEFLATED) as kmz:
            for root, _, files in os.walk(temp_dir):
                for file in files:
                    full_path = os.path.join(root, file)
                    arcname = os.path.relpath(full_path, temp_dir)
                    kmz.write(full_path, arcname=arcname)

        # Export Excel summary
        try:
            import pandas as pd
        except ImportError:
            raise RuntimeError("pandas is required to write Excel summary.")

        df = pd.DataFrame(excel_rows)
        df.to_excel(output_excel_path, index=False)
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)
