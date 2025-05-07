import os
import logging
import asyncio
import httpx
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("softreef_resources")

SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL = os.getenv(
    "SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL"
)


@dataclass(frozen=True)
class Resource:
    url: str
    name: str
    description: str


uri_2_resource: dict[str, Resource] = {
    "markdown://softreef/design-system/overview": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-概要・利用方法--docs",
        name="Overview of Softreef design-system",
        description="Softreef / デザインシステムの概要と利用方法について",
    ),
    "markdown://softreef/design-system/environment": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-対応環境--docs",
        name="Overview of Softreef environment",
        description="Softreefがサポートしている動作環境について",
    ),
    "markdown://softreef/design-system/resource": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-リソース--docs",
        name="Overview of Softreef resource",
        description="Softreefで利用されているリソースについて",
    ),
    "markdown://softreef/design-system/component/Accordion": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-accordion（アコーディオン）--docs",
        name="Softreef Accordion component",
        description="情報量が多い箇所をコンパクト見せる目的で利用するコンポーネント",
    ),
    "markdown://softreef/design-system/component/Autocomplete": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-autocomplete（オートコンプリート）--docs",
        name="Softreef Autocomplete component",
        description="ユーザー入力から自動保管を行いつつ、複数項目から1つ以上の項目を選択するために利用するコンポーネント",
    ),
    "markdown://softreef/design-system/component/Breadcrumbs": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-breadcrumbs（パンくずリスト）--docs",
        name="Softreef Breadcrumbs component",
        description=(
            "ユーザーがサイト内のどの階層にいるかを把握しやすくするために、"
            "ページ上部に現在位置を表示する際に利用するコンポーネント"
        ),
    ),
    "markdown://softreef/design-system/component/Button": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-button（ボタン）--docs",
        name="Softreef Button component",
        description="ユーザーがデータの操作やページ遷移などのアクションを起こす際に使用するコンポーネント",
    ),
    "markdown://softreef/design-system/component/ButtonGroup": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-buttongroup（ボタングループ）--docs",
        name="Softreef ButtonGroup component",
        description=(
            "関連する複数のボタンを1つのグループとして一括りにし。"
            "ユーザーが同じコンテキスト内で複数のアクションを選択できるようにするために利用するコンポーネント"
        ),
    ),
    "markdown://softreef/design-system/component/CardOverview": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-card（カード）--docs",
        name="Overview of Softreef Card component",
        description="1つのトピックに対して、コンテンツやアクションを表示したい場合に使用する。",
    ),
    "markdown://softreef/design-system/component/Card": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-card（カード）-card（カード）--docs",
        name="Softreef Card component",
        description="1つのトピックに対して、コンテンツやアクションを表示したい場合に使用するコンポーネント",
    ),
    "markdown://softreef/design-system/component/CardForGalleryView": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-card（カード）-cardforgalleryview（ギャラリービュー用カード）--docs",
        name="Softreef CardForGalleryView component",
        description="データをギャラリービューで表示したい婆に利用するコンポーネント",
    ),
    "markdown://softreef/design-system/component/CardList": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-card（カード）-cardlist（カードリスト）--docs",
        name="Softreef CardList component",
        description="複数のCardForGalleryViewを一覧で表示したい場合に使用するコンポーネント",
    ),
    "markdown://softreef/design-system/component/BarChart": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-chart（チャート）-bar-chart（棒グラフ）--docs",
        name="Softreef BarChart component",
        description="同じ観点から複数データを比較するさいに利用するグラフコンポーネント",
    ),
    "markdown://softreef/design-system/component/AllSelectCheckBox": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-checkbox（チェックボックス）-allselectcheckbox（全選択チェックボックス）--docs",
        name="Softreef AllSelectCheckBox component",
        description="複数のチャックボックスを一括選択 / 解除するために利用するコンポーネント",
    ),
    "markdown://softreef/design-system/component/CheckBox": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-checkbox（チェックボックス）-checkbox（チェックボックス）--docs",
        name="Softreef Check box component",
        description="ユーザーが複数項目から複数を選択するための入力手段として使用するコンポーネント",
    ),
    "markdown://softreef/design-system/component/Chip": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-chip（チップ）--docs",
        name="Softreef Chip component",
        description=(
            "タグや属性、選択された値をコンパクトに表示するためのコンポーネント。"
            "ユーザーが選択したアイテムをChipとして表示することで、直感的・明示的に示すことができる。"
        ),
    ),
    "markdown://softreef/design-system/component/DateTimePicker": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-datetimepicker（デートタイムピッカー）--docs",
        name="Softreef DateTimePicker component",
        description="ユーザーが日付と時刻を選択し、指定した形式でそれらを入力できるようにするために使用するコンポーネント",
    ),
    "markdown://softreef/design-system/component/DialogOverview": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-dialog（ダイアログ）--docs",
        name="Overview of Softreef Dialog",
        description="ダイアログに関する基本情報",
    ),
    "markdown://softreef/design-system/component/ActionDialog": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-dialog（ダイアログ）-actiondialog--docs",
        name="Softreef ActionDialog component",
        description="ユーザーの操作を要求する画面をダイアログ形式で表示する際に利用するコンポーネント",
    ),
    "markdown://softreef/design-system/component/DisplayDialog": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-dialog（ダイアログ）-displaydialog--docs",
        name="Softreef DisplayDialog component",
        description="ユーザーの操作が必要ない情報をダイアログ形式で表示するために利用するコンポーネント",
    ),
    "markdown://softreef/design-system/component/StepperDialog": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-dialog（ダイアログ）-stepperdialog--docs",
        name="Softreef StepperDialog component",
        description="ダイアログ形式でユーザーに複数のステップで操作を求める場合に利用するコンポーネント",
    ),
    "markdown://softreef/design-system/component/Divider": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-divider（ディバイダー）--docs",
        name="Softreef Divider component",
        description="複数要素が並んだときに、似ている要素ごとにグルーピングする際に利用するコンポーネント",
    ),
    "markdown://softreef/design-system/component/DropdownMenuButton": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-dropdownmenu（ドロップダウンメニュー）-dropdownmenubutton--docs",
        name="Softreef DropdownMenuButton component",
        description="使用頻度が低い・ボタンの配置に余裕がない場合に使用するコンポーネント",
    ),
    "markdown://softreef/design-system/component/EllipsisDropdownMenuButton": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-dropdownmenu（ドロップダウンメニュー）-ellipsisdropdownmenubutton--docs",
        name="Softreef EllipsisDropdownMenuButton component",
        description=(
            "使用頻度が低い・ボタンの配置に余裕がない場合に使用するコンポーネント"
            "複数のボタンが3点リーダーにまとめられる。"
        ),
    ),
    "markdown://softreef/design-system/component/DropZoneOverview": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-dropzone（ドロップゾーン）--docs",
        name="Softreef DropZone component",
        description="ファイルをアップロードする際に利用するコンポーネント",
    ),
    "markdown://softreef/design-system/component/ImageDropZone": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-dropzone（ドロップゾーン）-imagedropzone--docs",
        name="Softreef ImageDropZone component",
        description="画像のアップロード特化の機能を利用する際に使用するコンポーネント",
    ),
    "markdown://softreef/design-system/component/GridLayout": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-gridlayout（グリッドレイアウト）--docs",
        name="Softreef GridLayout component",
        description="グリッドデザインを実現するために利用するコンポーネント",
    ),
    "markdown://softreef/design-system/component/Icon": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-icon（アイコン）--docs",
        name="Softreef Icon component",
        description="操作を直感的・視覚的にわかりやすくするために利用するコンポーネント",
    ),
    "markdown://softreef/design-system/component/List": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-list-リスト--docs",
        name="Softreef List component",
        description="情報をリスト形式で表示する場合に利用するコンポーネント",
    ),
    "markdown://softreef/design-system/component/Loader": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-loader（ローダー）--docs",
        name="Softreef Loader component",
        description="処理中であることをユーザーに伝えるために利用するコンポーネント",
    ),
    "markdown://softreef/design-system/component/Logo": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-logo（ロゴ）--docs",
        name="Softreef Logo component",
        description="Softreefのロゴ",
    ),
    "markdown://softreef/design-system/component/Notification": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-notification（通知バー）--docs",
        name="Softreef Notification component",
        description="ユーザーに処理成功・エラーなどを通知する際に使用するコンポーネント",
    ),
    "markdown://softreef/design-system/component/PagingOverview": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-paging（ページネーション）--docs",
        name="Overview of Paging component",
        description="テーブル形式のデータを複数ページで表示する際に利用する。",
    ),
    "markdown://softreef/design-system/component/FullPaging": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-paging（ページネーション）-fullpaging--docs",
        name="Softreef FullPaging component",
        description="原則テーブルの下部に配置するページング用のコンポーネント",
    ),
    "markdown://softreef/design-system/component/SimplePaging": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-paging（ページネーション）-simplepaging--docs",
        name="Softreef SimplePaging component",
        description="原則テーブルの上部に配置するページング用のコンポーネント",
    ),
    "markdown://softreef/design-system/component/RadioButton": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-radiobutton（ラジオボタン）--docs",
        name="Softreef RadioButton component",
        description=(
            "ユーザーが複数の項目から1つを選択するための入力手段として使用するコンポーネント。"
            "主にアンケートなど少数の選択肢から選ぶ場合に適している。"
        ),
    ),
    "markdown://softreef/design-system/component/SelectBox": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-selectbox（セレクトボックス）--docs",
        name="Softreef SelectBox component",
        description="ユーザーが複数の項目から1つを選択するための入力手段として利用するコンポーネント",
    ),
    "markdown://softreef/design-system/component/Slider": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-slider（スライダー）--docs",
        name="Softreef Slider component",
        description="ユーザーが範囲内の値を選択または調整するために利用するコンポーネント",
    ),
    "markdown://softreef/design-system/component/Status": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-status（ステータス）--docs",
        name="Softreef Status component",
        description="特定の処理に関する現在のステータスをユーザーに表示する場合に使用するコンポーネント",
    ),
    "markdown://softreef/design-system/component/Stepper": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-stepper（ステッパー）--docs",
        name="Softreef Stepper component",
        description=(
            "プロセスまたはワークフローを段階的に表示するために使用するコンポーネント。"
            "ユーザーは自分がプロセスのどこにいて、どのステップが残っているのか把握できるようになる。"
        ),
    ),
    "markdown://softreef/design-system/component/SwitchTableAndCardView": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-switchtableandcardview--docs",
        name="Softreef SwitchTableAndCardView component",
        description="テーブルとカードリストを切り替えて表示したい場合に使用するコンポーネント",
    ),
    "markdown://softreef/design-system/component/Tab": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-tab（タブ）--docs",
        name="Softreef Tab component",
        description=(
            "重要度が同じ、または関連性のある情報などを画面遷移せずに簡単に切り替えたい場合に使用するコンポーネント。"
            "操作後の結果が予想したすいので、タブ項目だけでユーザーは情報の全体像を把握できることがメリット。"
        ),
    ),
    "markdown://softreef/design-system/component/Table": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-table（テーブル）--docs",
        name="Softreef Table component",
        description="表形式でデータを表示、操作したい場合に使用するコンポーネント",
    ),
    "markdown://softreef/design-system/component/Text": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-text（テキスト）--docs",
        name="Softreef Text component",
        description="画面上にテキストを表示する際に使用するコンポーネント",
    ),
    "markdown://softreef/design-system/component/TextBox": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-textbox（テキストボックス）--docs",
        name="Softreef TextBox component",
        description="ユーザーがテキスト情報を入力する手段として使用するコンポーネント",
    ),
    "markdown://softreef/design-system/component/ToggleOverview": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-toggle（トグル）--docs",
        name="Softreef Toggle component",
        description=(
            "ユーザーからの入力を受け取り、表示やステータスなどを即座位に切り替えたい場合に使用する。詳細は"
            "詳細は、ToggleButtonまたはToggleSwitchを参照してください。"
        ),
    ),
    "markdown://softreef/design-system/component/ToggleButton": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-toggle（トグル）-togglebutton（トグルボタン）--docs",
        name="Softreef ToggleButton component",
        description="ユーザーからの入力を受け取り、表示やステータスを即座に切り替えたい場合に使用するコンポーネント",
    ),
    "markdown://softreef/design-system/component/ToggleSwitch": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-toggle（トグル）-toggleswitch（トグルスイッチ）--docs",
        name="Softreef ToggleSwitch component",
        description=(
            "ユーザーからの入力を受け取り、表示やステータスなどを即座に切り替えたい場合に使用するコンポーネント。"
            "選択肢がBoolean(True / False)の時に限られる。"
        ),
    ),
    "markdown://softreef/design-system/component/Tooltip": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-tooltip（ツールチップ）--docs",
        name="Softreef Tooltip component",
        description="スペースが限られている場所で、補足テキストを一時的に表示するためのコンポーネント",
    ),
    "markdown://softreef/design-system/component/KeyValue": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-keyvalue-キーバリュー--docs",
        name="Softreef KeyValue component",
        description="Key-Value形式のデータを表示するためのコンポーネント",
    ),
    "markdown://softreef/design-system/design-pattern/ContentAreaLayout": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-デザインパターン-コンテンツエリア--docs",
        name="Softreef ContentArea design-pattern",
        description="ヘッダーやナビゲーション、パンくずリスト以外の案件特化画面で遵守されるべきデザインルール",
    ),
    "markdown://softreef/design-system/design-pattern/BasicScreenLayout": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-デザインパターン-基本画面構成-overview--docs",
        name="Softreef BasicScreenLayout design-pattern",
        description="ヘッダーやナビゲーション、パンくずリストなどの全画面で共通で利用される画面要素のデザインルール",
    ),
    "markdown://softreef/design-system/design-pattern/DeleteConfirmationDialog": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-デザインパターン-汎用削除確認画面-overview--docs",
        name="Softreef DeleteConfirmationDialog design-pattern",
        description="何かしらのオブジェクトを削除する際に汎用的に使用される画面のデザインルール",
    ),
    "markdown://softreef/design-system/design-pattern/DetailPanelLayout": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-デザインパターン-汎用詳細画面--docs",
        name="Softreef DetailPanelLayout design-pattern",
        description="何かしらのオブジェクトの詳細を確認する際に汎用的に使用される画面のデザインルール",
    ),
    "markdown://softreef/design-system/design-pattern/FormSubmissionPanelLayout": Resource(
        url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-デザインパターン-汎用入力画面--docs",
        name="Softreef FormSubmissionPanelLayout design-pattern",
        description="ユーザーが情報を新規登録したり、編集するための画面として使用される画面のデザインルール",
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


def utf8_decode(url: str) -> str:
    from urllib.parse import unquote

    return unquote(url)


if __name__ == "__main__":
    asyncio.run(main())
