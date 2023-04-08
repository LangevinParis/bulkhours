import os
import subprocess

from IPython.core.magic import Magics, cell_magic, magics_class, line_cell_magic, needs_local_scope
import IPython
import ipywidgets

from .textstyles import *
from .logins import *
from . import firebase
from . import install
from .widgets import BulkWidget


def get_data_from_file(label, on=None, subdir="data", **kwargs):
    import glob

    filename = None
    for directory in [
        "bulkhours",
        ".",
        "..",
        "../../bulkhours",
        "../../../bulkhours",
        os.environ["HOME"] + "/projects/bulkhours",
    ]:
        if len((files := glob.glob(f"{directory}/{subdir}/{label}*"))):
            filename = files[0]
    if not filename:
        print(f"No data available for {subdir}/{label}")
        return None
    return filename


def evaluate_core_cpp_project(cinfo, cell, show_solution=False):
    height = "550px"
    for o in cinfo.puppet.split(","):
        if "height=" in o:
            height = o.split("=")[1]

    filenames = cinfo.options.split(",")
    os.system("mkdir -p cache")

    files = []
    for t, f in enumerate(filenames):
        ff = f.split(":")
        if not os.path.exists(cfilename := f"cache/{cinfo.id}_{ff[0]}"):
            rfilename = get_data_from_file(f"{cinfo.id}_{ff[0]}", subdir="bulkhours/hpc")
            print(f"Generate {cfilename} from {rfilename}")

            data = open(rfilename).read()
            with open(cfilename, "w") as f:
                f.write(data)
        data = open(cfilename, "r").read()

        if show_solution:
            data1 = ipywidgets.Textarea(
                open(cfilename, "r").read(), layout=ipywidgets.Layout(height=height, width="49%")
            )
            data2 = ipywidgets.Output(layout={"height": height, "width": "49%"})
            with data2:
                IPython.display.display(IPython.display.Code(open(cfilename, "r").read()))
            data = ipywidgets.HBox([data1, data2])
        else:
            data = ipywidgets.Textarea(
                open(cfilename, "r").read(), layout=ipywidgets.Layout(height=height, width="99%")
            )

        files.append(data)

    tab = ipywidgets.Tab(children=files)
    for t, f in enumerate(filenames):
        tab.set_title(t, f)
    return tab, files
