CONFIG_INIT = {
    "BASE_URL": "https://apidf-preprod.cerema.fr",
    "TOKEN": None,
    "PROXY": None,
    "PROGRESS_BAR": True,
}
CONFIG = CONFIG_INIT.copy()


def configure(**kwargs):
    global CONFIG
    CONFIG.update(kwargs)


def get_param(value):
    global CONFIG
    return CONFIG.get(value)


def reset():
    global CONFIG
    CONFIG = CONFIG_INIT.copy()
