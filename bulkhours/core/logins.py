import os
import time
import IPython

from . import firebase
from . import contexts


def init_config(config_id, collection, config):
    if config_id not in config:
        config[config_id] = {}

    if not collection.document(config_id).get().to_dict():
        firebase.save_config(config_id, config)
    config[config_id].update(collection.document(config_id).get().to_dict())

    return config


def init_database(**kwargs):
    from . import tools

    if "from_scratch" not in kwargs:
        kwargs["from_scratch"] = True
    config = tools.get_config(**kwargs)

    if "database" not in config:
        config["database"] = "bkache@free1"

    config["notebook_id"] = "nob" if "notebook_id" not in config else config["notebook_id"]

    config = firebase.init_database(config)
    return tools.update_config(config)


def init_prems(**kwargs):
    config = init_database(**kwargs)
    db_label = config["database"].split("@")[0] + "@" if "@" in config["database"] else ""

    email, notebook_id = (config.get(v) for v in ["email", "notebook_id"])
    subject = config["global"].get("subject")

    info = f"subject/virtualroom/nb_id/user='{db_label}{subject}/{config['virtual_room']}/{notebook_id}/"

    if email is None:
        info += f"None ❌\x1b[41m\x1b[37m, email not configurd, no db connection), \x1b[0m"
        return info

    is_known_student = (
        ("virtual_room" in config and email in config["global"][config["virtual_room"]])
        or email in config["global"]["admins"]
        or email == "solution"
    )
    language = config["global"].get("language")

    config["eparams"] = False
    if not is_known_student:
        if config["global"]["restricted"]:
            raise Exception.IndexError(
                f"❌\x1b[41m\x1b[37mL'email '{email}' n'est pas configuré dans la base de données. Contacter le professeur svp\x1b[0m"
                if language == "fr"
                else f"❌\x1b[41m\x1b[37mEmail '{email}' is not configured in the database. Please contact the teacher\x1b[0m"
            )
        info += (
            f"{email}❌ (\x1b[41m\x1b[37memail inconnu: contacter le professeur svp\x1b[0m), "
            if language == "fr"
            else f"{email}❌ (\x1b[41m\x1b[37munknown email: please contact the teacher\x1b[0m), "
        )
    else:
        admin = "🎓" if email in config["global"]["admins"] else "✅"
        info += f"{email}{admin}', "

    return info


def init_env(packages=None, **kwargs):
    from . import installer
    from . import tools
    from . import colors as c

    info = init_prems(**kwargs)
    start_time = time.time()

    if ipp := IPython.get_ipython():
        from .evaluation import Evaluation
        from ..hpc.compiler import CCPPlugin

        ipp.register_magics(CCPPlugin(ipp))
        ipp.register_magics(Evaluation(ipp))

    if packages is not None and "BLK_PACKAGES_STATUS" not in os.environ:
        installer.install_dependencies(packages, start_time)
        os.environ["BLK_PACKAGES_STATUS"] = f"INITIALIZED"

    config = tools.get_config()
    c.set_plt_style()
    version = open(tools.abspath("bulkhours/__version__.py")).readlines()[0].split('"')[1]

    einfo = f", ⚠️\x1b[31m\x1b[41m\x1b[37m in admin/teacher🎓 mode\x1b[0m⚠️" if tools.is_admin(config=config) else ""
    print(f"Import BULK Helper cOURSe (\x1b[0m\x1b[36mversion='{version}'\x1b[0m🚀'{einfo}):\n{info})")
    if "bkloud" not in config["database"]:
        print(
            f"⚠️\x1b[41m\x1b[37mDatabase is not replicated on the cloud. Persistency is not garantee outside the notebook\x1b[0m⚠️"
        )

    return contexts.CellContext(), contexts.CellContext()
