import os
import logging
from dataclasses import dataclass
from dotenv import load_dotenv

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


uri_2_resource: dict[str, Resource] = {
    **{
        f"filepath://softreef/design-system/component/{component}": Resource(
            path=f"{SOFTREEF_DESIGN_SYSTEM_FILE_BASE_PATH}/{component}/{component}.tsx",
            name=f"Path to {component} component file",
            description=f"{component}コンポーネントの実装ファイルパス",
        )
        for component in [
            "Accordion",
            "Breadcrumbs",
            "Button",
            "ButtonGroup",
            "Card",
            "CardForGalleryView",
            "CardList",
            "Chip",
            "DateTimePicker",
            "Divider",
            "KeyValue",
            "List",
            "Loader",
            "Logo",
            "Notification",
            "Slider",
            "Status",
            "Stepper",
            "SwitchTableAndCardView",
            "Tab",
            "Table",
            "ToggleButton",
            "TOggleSwitch",
            "Tooltip",
        ]
    },
    **{
        f"filepath://softreef/design-system/component/{component}": Resource(
            path=f"{SOFTREEF_DESIGN_SYSTEM_FILE_BASE_PATH}/form/{component}.tsx",
            name=f"Path to {component} component file",
            description=f"{component}コンポーネントの実装ファイル",
        )
        for component in [
            "Autocomplete",
            "AllSelectCheckBox",
            "CheckBox",
            "RadioButton",
            "SelectBox",
            "TextBox",
        ]
    },
    **{
        f"filepath://softreef/design-system/component/{component}": Resource(
            path=f"{SOFTREEF_DESIGN_SYSTEM_FILE_BASE_PATH}/Chart/{component}/{component}.tsx",
            name=f"Path to {component} component file",
            description=f"{component}コンポーネントの実装ファイル",
        )
        for component in ["BarChart"]
    },
    **{
        f"filepath://softreef/design-system/component/{component}": Resource(
            path=f"{SOFTREEF_DESIGN_SYSTEM_FILE_BASE_PATH}/dialog/{component}/{component}.tsx",
            name=f"Path to {component} component file",
            description=f"{component}コンポーネントの実装ファイル",
        )
        for component in ["ActionDialog", "StepperDialog"]
    },
    **{
        f"filepath://softreef/design-system/component/{component}": Resource(
            path=f"{SOFTREEF_DESIGN_SYSTEM_FILE_BASE_PATH}/DropdownMenu/{component}/{component}.tsx",
            name=f"Path to {component} component file",
            description=f"{component}コンポーネントの実装ファイル",
        )
        for component in ["DropdownMenuButton", "EllipsisDropdownMenuButton"]
    },
    **{
        f"filepath://softreef/design-system/component/{component}": Resource(
            path=f"{SOFTREEF_DESIGN_SYSTEM_FILE_BASE_PATH}/dropzone/{component}/{component}.tsx",
            name=f"Path to {component} component file",
            description=f"{component}コンポーネントの実装ファイル",
        )
        for component in ["DropZone", "ImageDropZone"]
    },
    **{
        f"filepath://softreef/design-system/component/{component}": Resource(
            path=f"{SOFTREEF_DESIGN_SYSTEM_FILE_BASE_PATH}/layout/{component}.tsx",
            name=f"Path to {component} component file",
            description=f"{component}コンポーネントの実装ファイル",
        )
        for component in ["GridLayout"]
    },
    **{
        f"filepath://softreef/design-system/component/{component}": Resource(
            path=f"{SOFTREEF_DESIGN_SYSTEM_FILE_BASE_PATH}/paging/{component}/{component}.tsx",
            name=f"Path to {component} component file",
            description=f"{component}コンポーネントの実装ファイル",
        )
        for component in ["FullPaging", "SimplePaging"]
    },
    **{
        f"filepath://softreef/design-system/component/{component}": Resource(
            path=f"{SOFTREEF_DESIGN_SYSTEM_FILE_BASE_PATH}/Text/{component}/{component}.tsx",
            name=f"Path to {component} component file",
            description=f"{component}コンポーネントの実装ファイル",
        )
        for component in [
            "TitleH1Text",
            "TitleH2Text",
            "CaptionText",
            "NormalText",
            "SmallText",
            "NotesText",
            "LinkText",
        ]
    },
}


def check_file_exists(path) -> bool:
    if os.path.exists(path):
        return True
    else:
        logger.warning(f"{path} was not found")
        False


def main():
    for uri in uri_2_resource:
        _ = check_file_exists(path=uri_2_resource[uri].path)


if __name__ == "__main__":
    main()
