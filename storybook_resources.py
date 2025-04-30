import os
import logging
import asyncio
import httpx
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("softreef_resources")

SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL=os.getenv("SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL")
@dataclass(frozen=True)
class Resource:
    url: str
    name: str
    description: str

uri_2_resource: dict[str, Resource] = {
    "markdown://softreef/design-system/overview": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-概要・利用方法--docs",
        name="Overview of Softreef design-system",
        description="Overview of Softreef design-system",
    ),
    "markdown://softreef/design-system/environment": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-対応環境--docs",
        name="Overview of Softreef environment",
        description="Overview of Softreef environment",
    ),
    "markdown://softreef/design-system/resource": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-リソース--docs",
        name="Overview of Softreef resource",
        description="Overview of Softreef resource",
    ),
    "markdown://softreef/design-system/component/Accordion": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-accordion（アコーディオン）--docs",
        name="Softreef Accordion component",
        description="Softreef Accordion component",
    ),
    "markdown://softreef/design-system/component/Autocomplete": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-autocomplete（オートコンプリート）--docs",
        name="Softreef Autocomplete component",
        description="Softreef Autocomplete component",
    ),
    "markdown://softreef/design-system/component/Breadcrumbs": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-breadcrumbs（パンくずリスト）--docs",
        name="Softreef Breadcrumbs component",
        description="Softreef Breadcrumbs component",
    ),
    "markdown://softreef/design-system/component/Button": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-button（ボタン）--docs",
        name="Softreef Button component",
        description="Softreef Button component",
    ),
    "markdown://softreef/design-system/component/ButtonGroup": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-buttongroup（ボタングループ）--docs",
        name="Softreef ButtonGroup component",
        description="Softreef ButtonGroup component",
    ),
    "markdown://softreef/design-system/component/CardOverview": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-card（カード）--docs",
        name="Overview of Softreef Card component",
        description="Overview of Card component",
    ),
    "markdown://softreef/design-system/component/Card": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-card（カード）-card（カード）--docs",
        name="Softreef Card component",
        description="Softreef Card component",
    ),
    "markdown://softreef/design-system/component/CardForGalleryView": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-card（カード）-cardforgalleryview（ギャラリービュー用カード）--docs",
        name="Softreef CardForGalleryView component",
        description="Softreef CardForGalleryView component",
    ),
    "markdown://softreef/design-system/component/CardList": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-card（カード）-cardlist（カードリスト）--docs",
        name="Softreef CardList component",
        description="Softreef CardList component",
    ),
    "markdown://softreef/design-system/component/BarChart": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-chart（チャート）-bar-chart（棒グラフ）--docs",
        name="Softreef BarChart component",
        description="Softreef BarChart component",
    ),
    "markdown://softreef/design-system/component/AllSelectCheckBox": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-checkbox（チェックボックス）-allselectcheckbox（全選択チェックボックス）--docs",
        name="Softreef AllSelectCheckBox component",
        description="Softreef AllSelectCheckBox component",
    ),
    "markdown://softreef/design-system/component/CheckBox": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-checkbox（チェックボックス）-checkbox（チェックボックス）--docs",
        name="Softreef Check box component",
        description="Softreef check box component",
    ),
    "markdown://softreef/design-system/component/Chip": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-chip（チップ）--docs",
        name="Softreef Chip component",
        description="Softreef Chip component",
    ),
    "markdown://softreef/design-system/component/DateTimePicker": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-datetimepicker（デートタイムピッカー）--docs",
        name="Softreef DateTimePicker component",
        description="Softreef DateTimePicker component",
    ),
    "markdown://softreef/design-system/component/DialogOverview": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-dialog（ダイアログ）--docs",
        name="Overview of Softreef Dialog",
        description="Overview of Softreef Dialog",
    ),
    "markdown://softreef/design-system/component/ActionDialog": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-dialog（ダイアログ）-actiondialog--docs",
        name="Softreef ActionDialog component",
        description="Softreef ActionDialog component",
    ),
    "markdown://softreef/design-system/component/DisplayDialog": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-dialog（ダイアログ）-displaydialog--docs",
        name="Softreef DisplayDialog component",
        description="Softreef DisplayDialog component",
    ),
    "markdown://softreef/design-system/component/StepperDialog": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-dialog（ダイアログ）-stepperdialog--docs",
        name="Softreef StepperDialog component",
        description="Softreef StepperDialog component",
    ),
    "markdown://softreef/design-system/component/Divider": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-divider（ディバイダー）--docs",
        name="Softreef Divider component",
        description="Softreef Divider component",
    ),
    "markdown://softreef/design-system/component/DropdownMenuButton": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-dropdownmenu（ドロップダウンメニュー）-dropdownmenubutton--docs",
        name="Softreef DropdownMenuButton component",
        description="Softreef DropdownMenuButton component",
    ),
    "markdown://softreef/design-system/component/EllipsisDropdownMenuButton": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-dropdownmenu（ドロップダウンメニュー）-ellipsisdropdownmenubutton--docs",
        name="Softreef EllipsisDropdownMenuButton component",
        description="Softreef EllipsisDropdownMenuButton component",
    ),
    "markdown://softreef/design-system/component/DropZoneOverview": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-dropzone（ドロップゾーン）--docs",
        name="Softreef DropZone component",
        description="Softreef DropZone component",
    ),
    "markdown://softreef/design-system/component/ImageDropZone": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-dropzone（ドロップゾーン）-imagedropzone--docs",
        name="Softreef ImageDropZone component",
        description="Softreef ImageDropZone component",
    ),
    "markdown://softreef/design-system/component/GridLayout": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-gridlayout（グリッドレイアウト）--docs",
        name="Softreef GridLayout component",
        description="Softreef GridLayout component",
    ),
    "markdown://softreef/design-system/component/Icon": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-icon（アイコン）--docs",
        name="Softreef Icon component",
        description="Softreef Icon component",
    ),
    "markdown://softreef/design-system/component/List": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-list-リスト--docs",
        name="Softreef List component",
        description="Softreef List component",
    ),
    "markdown://softreef/design-system/component/Loader": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-loader（ローダー）--docs",
        name="Softreef Loader component",
        description="Softreef Loader component",
    ),
    "markdown://softreef/design-system/component/Logo": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-logo（ロゴ）--docs",
        name="Softreef Logo component",
        description="Softreef Logo component",
    ),
    "markdown://softreef/design-system/component/Notification": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-notification（通知バー）--docs",
        name="Softreef Notification component",
        description="Softreef Notification component",
    ),
    "markdown://softreef/design-system/component/PagingOverview": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-paging（ページネーション）--docs",
        name="Overview of Paging component",
        description="Overview of Paging component",
    ),
    "markdown://softreef/design-system/component/FullPaging": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-paging（ページネーション）-fullpaging--docs",
        name="Softreef FullPaging component",
        description="Softreef FullPaging component",
    ),
    "markdown://softreef/design-system/component/SimplePaging": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-paging（ページネーション）-simplepaging--docs",
        name="Softreef SimplePaging component",
        description="Softreef SimplePaging component",
    ),
    "markdown://softreef/design-system/component/RadioButton": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-radiobutton（ラジオボタン）--docs",
        name="Softreef RadioButton component",
        description="Softreef RadioButton component",
    ),
    "markdown://softreef/design-system/component/SelectBox": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-selectbox（セレクトボックス）--docs",
        name="Softreef SelectBox component",
        description="Softreef SelectBox component",
    ),
    "markdown://softreef/design-system/component/Slider": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-slider（スライダー）--docs",
        name="Softreef Slider component",
        description="Softreef Slider component",
    ),
    "markdown://softreef/design-system/component/Status": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-status（ステータス）--docs",
        name="Softreef Status component",
        description="Softreef Status component",
    ),
    "markdown://softreef/design-system/component/Stepper": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-stepper（ステッパー）--docs",
        name="Softreef Stepper component",
        description="Softreef Stepper component",
    ),
    "markdown://softreef/design-system/component/SwitchTableAndCardView": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-switchtableandcardview--docs",
        name="Softreef SwitchTableAndCardView component",
        description="Softreef SwitchTableAndCardView component",
    ),
    "markdown://softreef/design-system/component/Tab": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-tab（タブ）--docs",
        name="Softreef Tab component",
        description="Softreef Tab component",
    ),
    "markdown://softreef/design-system/component/Table": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-table（テーブル）--docs",
        name="Softreef Table component",
        description="Softreef Table component",
    ),
    "markdown://softreef/design-system/component/Text": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-text（テキスト）--docs",
        name="Softreef Text component",
        description="Softreef Text component",
    ),
    "markdown://softreef/design-system/component/TextBox": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-textbox（テキストボックス）--docs",
        name="Softreef TextBox component",
        description="Softreef TextBox component",
    ),
    "markdown://softreef/design-system/component/ToggleOverview": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-toggle（トグル）--docs",
        name="Softreef Toggle component",
        description="Softreef Toggle component",
    ),
    "markdown://softreef/design-system/component/ToggleButton": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-toggle（トグル）-togglebutton（トグルボタン）--docs",
        name="Softreef ToggleButton component",
        description="Softreef ToggleButton component",
    ),
    "markdown://softreef/design-system/component/ToggleSwitch": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-toggle（トグル）-toggleswitch（トグルスイッチ）--docs",
        name="Softreef ToggleSwitch component",
        description="Softreef ToggleSwitch component",
    ),
    "markdown://softreef/design-system/component/Tooltip": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-tooltip（ツールチップ）--docs",
        name="Softreef Tooltip component",
        description="Softreef Tooltip component",
    ),
    "markdown://softreef/design-system/component/KeyValue": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-keyvalue-キーバリュー--docs",
        name="Softreef KeyValue component",
        description="Softreef KeyValue component",
    ),
}

async def check_reachable_url(url: str) -> bool:
    try:
        async with httpx.AsyncClient() as client:
            _ = await client.get(url)
            return True
    except Exception as e:
        logger.error(f'"{str(e)}" was occurred when trying to access "{url}"')
        return False

async def main():
    for uri in uri_2_resource:
        _ = await check_reachable_url(url=uri_2_resource[uri].url)

if __name__ == "__main__":
    asyncio.run(main())