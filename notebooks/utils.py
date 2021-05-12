from pathlib import Path
import os

import geopandas as gpd
import pyproj
from shapely.geometry import Polygon


def read_config(fname):
    if Path(fname).exists():
        with open(fname, "r") as f:
            inputs = filter(None, (line.rstrip() for line in f))
            inputs = [line for line in inputs if not line.lstrip()[0] == "#"]
        keys = [f.strip().partition(";")[0].split("=")[0].strip() for f in inputs]
        values = [f.strip().partition(";")[0].split("=")[1].strip() for f in inputs]
        for i in range(len(values)):
            try:
                values[i] = float(values[i])
            except ValueError:
                continue

        config = dict(zip(keys, values))
        if "class" in config:
            config["class"] = int(config["class"])
    else:
        raise FileNotFoundError(f"info file was not found: {fname}")

    return config

def get_path(scenario, class_no, root):
    case = get_case(class_no, scenario)
    return Path(root, case, "FlowFM_map.nc")

def get_case(class_no, scenario=None):
    scenarios = {
        "Ref": f"C{class_no}_A8_S1",
        "R20": f"C{class_no}_A8_S2_1",
        "R30": f"C{class_no}_A8_S2_2",
        "D90": f"C{class_no}_A8_S4_1",
        "D570": f"C{class_no}_A8_S4_2",
        "S07": f"C{class_no}_A8_S5_1",
        "S31": f"C{class_no}_A8_S5_2",
    }
    if scenario is None:
        return scenarios
    return scenarios[scenario]


def clip_geom(geodf, geom, crs, clip_name, root):
    if not geodf.crs.is_exact_same(pyproj.CRS.from_user_input(crs)):
        geodf = geodf.to_crs(crs)

    cfile = Path(root, f"{clip_name}.gpkg")
    if not cfile.exists():
        clipped = gpd.clip(geodf, geom).reset_index(drop=True)
        clipped.to_file(cfile)
    else:
        clipped = gpd.read_file(cfile)

    return clipped


def geo_census(data_name, geom, crs, clip_name, root):
    os.makedirs(Path(root), exist_ok=True)
    cfile = Path(root, f"us_{data_name}.gpkg")
    if not cfile.exists():
        census = gpd.read_file(
            f"https://www2.census.gov/geo/tiger/TIGER2020/{data_name.upper()}/tl_2020_us_{data_name}.zip"
        )
        census.to_file(cfile)
    else:
        census = gpd.read_file(cfile)
    return clip_geom(census, geom, crs, clip_name, root)
