import os
from pathlib import Path
import logging
from dataclasses import dataclass
from dotenv import load_dotenv
from typing import Literal

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("design_system_file_path_resources")

SOFTREEF_DESIGN_SYSTEM_FILE_BASE_PATH = os.getenv(
    "SOFTREEF_DESIGN_SYSTEM_FILE_BASE_PATH"
)


@dataclass(frozen=True)
class Resource:
    path: str
    name: str
    description: str


def list_tsx_files(directory: str) -> list[Path]:
    return [
        path
        for path in Path(directory).rglob("*.tsx")
        if not path.name.endswith(".stories.tsx") and not path.stem in ["index"]
    ]


def convert_path_to_resource(
    path: Path, type: Literal["component", "design-pattern"]
) -> dict[str, Resource]:
    component = path.stem
    return {
        f"filepath://softreef/design-system/{type}/{component}": Resource(
            path=str(path),
            name=f"Path to {component} {type} file",
            description=f"{component} {type}の実装ファイルパス",
        )
    }


def check_file_exists(path) -> bool:
    if os.path.exists(path):
        return True
    else:
        logger.warning(f"{path} was not found")
        return False


uri_2_resource: dict[str, Resource] = {}
for directory in ["components", "design-patterns"]:
    for path in list_tsx_files(
        directory=SOFTREEF_DESIGN_SYSTEM_FILE_BASE_PATH + directory
    ):
        uri_2_resource.update(convert_path_to_resource(path, directory[0:-1]))


def main():
    for uri in uri_2_resource:
        _ = check_file_exists(path=uri_2_resource[uri].path)


if __name__ == "__main__":
    import pprint

    main()
    pprint.pprint(uri_2_resource)
