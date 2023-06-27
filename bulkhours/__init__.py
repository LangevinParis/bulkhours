import os
import datetime
import zoneinfo

from .core.tools import get_config, get_value  # noqa
from .core.timeit import timeit  # noqa
from .core import geo  # noqa
from .core.geo import geo_plot_country  # noqa
from .core import tools  # noqa

# from . import data  # noqa
# from .data import get_data, get_image  # noqa

from .core.gpt import ask_chat_gpt, ask_dall_e  # noqa
from .core.equals import is_equal  # noqa

from .core import colors as c  # noqa

from .core import installer  # noqa
from . import admin  # noqa
from . import rl  # noqa
from . import hpc  # noqa
from . import ecox  # noqa
from . import beaut  # noqa
from . import boids  # noqa
from . import phyu  # noqa
from .phyu.constants import constants  # noqa
from .phyu.formulas import formulas  # noqa

from .ecox.trading import *  # noqa


class CellContext:
    """This context cell contains cell executions:
    - Two are defined by default: 'student' or 'teacher'
    When using the correction code, the stdout and answer are filled
    """

    @property
    def stdout(self):
        return False

    @property
    def answer(self):
        return False


def init_env(from_scratch=False, database=None, packages=None, **kwargs):
    import IPython

    config = core.tools.get_config(do_update=True, from_scratch=from_scratch, database=database, **kwargs)

    from .core.logins import init_prems

    info_core = init_prems()

    start_time = time.time()
    stime = datetime.datetime.now(tz=zoneinfo.ZoneInfo("Europe/Paris"))

    if ipp := IPython.get_ipython():
        from .core.evaluation import Evaluation
        from .hpc.compiler import CCPPlugin

        ipp.register_magics(CCPPlugin(ipp))
        ipp.register_magics(Evaluation(ipp))

    if packages is not None and "BLK_STATUS" not in os.environ:
        installer.install_dependencies(packages, start_time)

    set_style()
    vfile = os.path.abspath(os.path.dirname(__file__)) + "/__version__.py"
    versions = open(vfile).readlines()
    version, _, _ = [versions[i].split('"')[1] for i in range(3)]

    ts = ", time='%s'" % stime.strftime("%H:%M:%S")
    print(f"Import BULK Helper cOURSe (\x1b[0m \x1b[36mversion='{version}{ts}'\x1b[0m🚀'):")

    info = info_core
    if core.tools.is_admin(config):
        info = f"\x1b[31m{info}⚠️\x1b[41m\x1b[37mfor teachers only🎓\x1b[0m"

    print(f"{info})")
    if "bkloud" not in database:
        print(
            f"⚠️\x1b[41m\x1b[37mDatabase is not replicated on the cloud. Persistency is not garantee outside the notebook\x1b[0m⚠️"
        )

    os.environ["BLK_STATUS"] = f"INITIALIZED"
    return CellContext(), CellContext()


def get_color(discipline):
    colors = {"swimming": "#581845", "cycling": "#C70039", "running": "#FF5733", "axis": "#4F77AA"}
    return colors[discipline] if discipline in colors else "black"


def set_style():
    import matplotlib.pyplot as plt

    background_color = "#F0FDFA11"  # cdcdcd
    axis_color = "#4F77AA"  # cdcdcd

    def get_color(discipline):
        colors = {"swimming": "#581845", "cycling": "#C70039", "running": "#FF5733", "axis": "#4F77AA"}
        return colors[discipline] if discipline in colors else "black"

    plt.rcParams["axes.grid"] = True
    plt.rcParams["axes.edgecolor"] = axis_color
    plt.rcParams["axes.labelcolor"] = axis_color
    plt.rcParams["axes.titlecolor"] = axis_color
    plt.rcParams["axes.facecolor"] = background_color
    plt.rcParams["figure.edgecolor"] = axis_color
    plt.rcParams["figure.facecolor"] = background_color
    plt.rcParams["grid.color"] = "white"
    plt.rcParams["legend.facecolor"] = background_color
    plt.rcParams["legend.edgecolor"] = background_color
    plt.rcParams["xtick.color"] = axis_color
    plt.rcParams["ytick.color"] = axis_color

    plt.rcParams["font.size"] = 14
    plt.rcParams["lines.linewidth"] = 4

    # ax.grid(True, axis="y", color="white")

    from cycler import cycler

    # mpl.rcParams['axes.prop_cycle'] = cycler(color='bgrcmyk')
    plt.rcParams["axes.prop_cycle"] = cycler(
        color=[get_color(c) for c in ["swimming", "cycling", "running", "The end"]]
    )


def geo_plot(data=None, timeopt="last", **kwargs):
    """
    data: geopandas dataframe (world.mappoverty)
    timeopt: year the estimation (last by default)
    """
    if type(data) is str:
        data = get_data(data, timeopt=timeopt)
    return geo.geo_plot(data, timeopt=timeopt, **kwargs)


def html(label, display=True, style="raw"):
    import IPython

    if style == "title":
        data = IPython.display.HTML(f"<b><font face='FiraCode Nerd Font' size=6 color='black'>{label}<font></b>")
    else:
        data = IPython.display.HTML(label)
    if display:
        IPython.display.display(data)
