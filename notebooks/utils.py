from pathlib import Path


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
