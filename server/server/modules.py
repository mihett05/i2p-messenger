import importlib
import os
from pathlib import Path
from typing import List

blacklist = ["alembic", "server"]


def attach_modules() -> List[str]:
    modules = []
    for entry in os.scandir(Path(os.path.basename(__file__)) / ".."):
        entry: os.DirEntry
        if entry.is_dir() and not entry.name.startswith(".") and entry.name not in blacklist:
            importlib.import_module(f"{entry.name}.controllers")
            importlib.import_module(f"{entry.name}.models")
            modules.append(entry.name)
    return modules
