from build123d import export_stl
from inspect import currentframe
from pathlib import Path

def export(output_path : Path, *parts):
    frame = currentframe()
    if not frame or not frame.f_back:
        raise Exception("Frame Error")
    callers_local_vars = frame.f_back.f_locals.items()
    part_names = [var_name for var_name, var_val in callers_local_vars if var_val in parts]

    output_path.mkdir(exist_ok=True)

    for part, part_name in zip(parts, part_names):
        export_stl(part, output_path / f"{part_name}.stl")