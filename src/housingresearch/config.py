from pathlib import Path
from dynaconf import Dynaconf

SETTINGS_PATH = "settings.toml"
SECRETS_PATH = ".secrets.toml"
root_path = Path.cwd()

if "notebooks" in Path.cwd().parts:
    root_path = Path.cwd().parent

settings = Dynaconf(
    envvar_prefix="HOUSING",
    settings_files=[f"{SETTINGS_PATH}", f"{SECRETS_PATH}"],
    environments=True,
    root_path=root_path,
)
