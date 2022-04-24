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

# import os

# from dynaconf import Dynaconf

# current_directory = os.path.dirname(os.path.realpath(__file__))

# settings = Dynaconf(
#     envvar_prefix="DYNACONF",
#     settings_files=[
#         f"{current_directory}/settings.toml",
#         f"{current_directory}/.secrets.toml",
#     ],
# )
