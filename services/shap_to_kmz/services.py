import os
import tempfile                        # ← add this
from django.conf import settings
from .utils import extract_compressed_file, allowed_file
import geopandas as gpd
import simplekml
import shutil

def handle_shap_to_kmz(uploaded_file, base_name):
    uploads_dir = os.path.join(settings.MEDIA_ROOT, "uploads")
    converted_dir = os.path.join(settings.MEDIA_ROOT, "converted")
    os.makedirs(uploads_dir, exist_ok=True)
    os.makedirs(converted_dir, exist_ok=True)

    input_archive_path = os.path.join(uploads_dir, uploaded_file.name)
    with open(input_archive_path, "wb+") as dest:
        for chunk in uploaded_file.chunks():
            dest.write(chunk)

    if not allowed_file(input_archive_path):
        raise ValueError("Archive must be .zip or .rar containing shapefile.")

    # <-- tempfile now available
    with tempfile.TemporaryDirectory() as tmpdir:
        extract_compressed_file(input_archive_path, tmpdir)

        # find .shp files
        shp_paths = []
        for root, _, files in os.walk(tmpdir):
            for f in files:
                if f.lower().endswith(".shp"):
                    shp_paths.append(os.path.join(root, f))

        if not shp_paths:
            raise ValueError("No .shp file found inside archive.")

        # build KML
        kml = simplekml.Kml()
        for shp in shp_paths:
            gdf = gpd.read_file(shp).to_crs("EPSG:4326")
            layer_name = os.path.splitext(os.path.basename(shp))[0]
            for _, row in gdf.iterrows():
                geom = row.geometry
                name = str(row.get("name", layer_name))
                if geom.geom_type == "Point":
                    kml.newpoint(name=name, coords=[(geom.x, geom.y)])
                elif geom.geom_type == "LineString":
                    kml.newlinestring(name=name, coords=list(geom.coords))
                elif geom.geom_type == "Polygon":
                    kml.newpolygon(name=name, outerboundaryis=list(geom.exterior.coords))
                elif geom.geom_type.startswith("Multi"):
                    for part in geom.geoms:
                        if part.geom_type == "Point":
                            kml.newpoint(name=name, coords=[(part.x, part.y)])
                        elif part.geom_type == "LineString":
                            kml.newlinestring(name=name, coords=list(part.coords))
                        elif part.geom_type == "Polygon":
                            kml.newpolygon(name=name, outerboundaryis=list(part.exterior.coords))

        output_kml_path = os.path.join(converted_dir, f"{base_name}.kml")
        kml.save(output_kml_path)

        return output_kml_path
