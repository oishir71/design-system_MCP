import os
import logging
import urllib3
from urllib3.exceptions import (
    HTTPError,
    MaxRetryError,
    NewConnectionError,
    ConnectTimeoutError,
    ReadTimeoutError,
    SSLError,
    ProxyError,
)
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


overviews = [
    (
        "Overview",
        "概要・利用方法",
        "Softreef / デザインシステムの概要と利用方法について",
    ),
    (
        "Environment",
        "対応環境",
        "Softreefがサポートしている動作環境について",
    ),
    (
        "Resource",
        "リソース",
        "Softreefで利用されているリソースについて",
    ),
]

components = [
    (
        "Accordion",
        "アコーディオン",
        "情報量が多い箇所をコンパクト見せる目的で利用するコンポーネント",
    ),
    (
        "Breadcrumbs",
        "パンくずリスト",
        "ユーザーがサイト内のどの階層にいるかを把握しやすくするために、ページ上部に現在位置を表示する際に利用するコンポーネント",
    ),
    (
        "Button",
        "ボタン",
        "ユーザーがデータの操作やページ遷移などのアクションを起こす際に使用するコンポーネント",
    ),
    (
        "ButtonGroup",
        "ボタングループ",
        "関連する複数のボタンを1つのグループとして一括りにし、ユーザーが同じコンテキスト内で複数のアクションを選択できるようにするために利用するコンポーネント",
    ),
    (
        "Chip",
        "チップ",
        "タグや属性、選択された値をコンパクトに表示するためのコンポーネント。ユーザーが選択したアイテムをChipとして表示することで、直感的・明示的に示すことができる。",
    ),
    (
        "DateTimePicker",
        "デートタイムピッカー",
        "ユーザーが日付と時刻を選択し、指定した形式でそれらを入力できるようにするために使用するコンポーネント",
    ),
    (
        "Divider",
        "ディバイダー",
        "複数要素が並んだときに、似ている要素ごとにグルーピングする際に利用するコンポーネント",
    ),
    (
        "KeyValue",
        "キーバリュー",
        "Key-Value形式のデータを表示するためのコンポーネント",
    ),
    (
        "List",
        "リスト",
        "情報をリスト形式で表示する場合に利用するコンポーネント",
    ),
    (
        "Loader",
        "ローダー",
        "処理中であることをユーザーに伝えるために利用するコンポーネント",
    ),
    ("Logo", "ロゴ", "Softreefのロゴ"),
    (
        "Notification",
        "通知バー",
        "ユーザーに処理成功・エラーなどを通知する際に使用するコンポーネント",
    ),
    (
        "Slider",
        "スライダー",
        "ユーザーが範囲内の値を選択または調整するために利用するコンポーネント",
    ),
    (
        "Status",
        "ステータス",
        "特定の処理に関する現在のステータスをユーザーに表示する場合に使用するコンポーネント",
    ),
    (
        "Stepper",
        "ステッパー",
        "プロセスまたはワークフローを段階的に表示するために使用するコンポーネント。ユーザーは自分がプロセスのどこにいて、どのステップが残っているのか把握できるようになる。",
    ),
    (
        "SwitchTableAndCardView",
        "",
        "テーブルとカードリストを切り替えて表示したい場合に使用するコンポーネント",
    ),
    (
        "Tab",
        "タブ",
        "重要度が同じ、または関連性のある情報などを画面遷移せずに簡単に切り替えたい場合に使用するコンポーネント。操作後の結果が予想したすいので、タブ項目だけでユーザーは情報の全体像を把握できることがメリット。",
    ),
    (
        "Table",
        "テーブル",
        "表形式でデータを表示、操作したい場合に使用するコンポーネント",
    ),
    (
        "Tooltip",
        "ツールチップ",
        "スペースが限られている場所で、補足テキストを一時的に表示するためのコンポーネント",
    ),
]

form_components = [
    (
        "Autocomplete",
        "オートコンプリート",
        "ユーザー入力から自動保管を行いつつ、複数項目から1つ以上の項目を選択するために利用するコンポーネント",
    ),
    (
        "SelectBox",
        "セレクトボックス",
        "ユーザーが複数の項目から1つを選択するための入力手段として利用するコンポーネント",
    ),
    (
        "TextBox",
        "テキストボックス",
        "ユーザーがテキスト情報を入力する手段として使用するコンポーネント",
    ),
    (
        "RadioButton",
        "ラジオボタン",
        "ユーザーが複数の項目から1つを選択するための入力手段として使用するコンポーネント。主にアンケートなど少数の選択肢から選ぶ場合に適している。",
    ),
]

checkbox_components = [
    (
        "CheckBox",
        "チェックボックス",
        "ユーザーが複数項目から複数を選択するための入力手段として使用するコンポーネント",
    ),
    (
        "AllSelectCheckBox",
        "全選択チェックボックス",
        "複数のチャックボックスを一括選択 / 解除するために利用するコンポーネント",
    ),
]

dialog_components = [
    (
        "ActionDialog",
        "アクションダイアログ",
        "ユーザーの操作を要求する画面をダイアログ形式で表示する際に利用するコンポーネント",
    ),
    (
        "DisplayDialog",
        "表示用ダイアログ",
        "ユーザーの操作が必要ない情報をダイアログ形式で表示するために利用するコンポーネント",
    ),
    (
        "StepperDialog",
        "ステッパーダイアログ",
        "ダイアログ形式でユーザーに複数のステップで操作を求める場合に利用するコンポーネント",
    ),
]

card_components = [
    (
        "Card",
        "カード",
        "1つのトピックに対して、コンテンツやアクションを表示したい場合に使用するコンポーネント",
    ),
    (
        "CardForGalleryView",
        "ギャラリービュー用カード",
        "データをギャラリービューで表示したい婆に利用するコンポーネント",
    ),
    (
        "CardList",
        "カードリスト",
        "複数のCardForGalleryViewを一覧で表示したい場合に使用するコンポーネント",
    ),
]

chart_components = [
    (
        "BarChart",
        "棒グラフ",
        "同じ観点から複数データを比較するさいに利用するグラフコンポーネント",
    ),
]

dropdownmenu_components = [
    (
        "DropdownMenuButton",
        "ドロップダウンメニュー",
        "使用頻度が低い・ボタンの配置に余裕がない場合に使用するコンポーネント",
    ),
    (
        "EllipsisDropdownMenuButton",
        "省略形ドロップダウンメニュー",
        "使用頻度が低い・ボタンの配置に余裕がない場合に使用するコンポーネント、複数のボタンが3点リーダーにまとめられる。",
    ),
]

dropzone_components = [
    (
        "ImageDropZone",
        "画像用ドロップゾーン",
        "画像のアップロード特化の機能を利用する際に使用するコンポーネント",
    ),
]

paging_components = [
    (
        "FullPaging",
        "ページング",
        "原則テーブルの下部に配置するページング用のコンポーネント",
    ),
    (
        "SimplePaging",
        "簡略型ページング",
        "原則テーブルの上部に配置するページング用のコンポーネント",
    ),
]

toggle_components = [
    (
        "ToggleButton",
        "トグルボタン",
        "ユーザーからの入力を受け取り、表示やステータスを即座に切り替えたい場合に使用するコンポーネント",
    ),
    (
        "ToggleSwitch",
        "トグルスイッチ",
        "ユーザーからの入力を受け取り、表示やステータスなどを即座に切り替えたい場合に使用するコンポーネント。選択肢がBoolean(True / False)の時に限られる。",
    ),
]

layout_components = [
    (
        "GridLayout",
        "グリッドレイアウト",
        "グリッドデザインを実現するために利用するコンポーネント",
    ),
]

component_overviews = [
    (
        "Icon",
        "アイコン",
        "操作を直感的・視覚的にわかりやすくするために利用するコンポーネント",
    ),
    (
        "Text",
        "テキスト",
        "画面上にテキストを表示する際に使用するコンポーネント",
    ),
    (
        "Card",
        "カード",
        "1つのトピックに対して、コンテンツやアクションを表示したい場合に使用する。",
    ),
    (
        "Dialog",
        "ダイアログ",
        "ダイアログに関する基本情報",
    ),
    (
        "DropZone",
        "ドロップゾーン",
        "ファイルをアップロードする際に利用するコンポーネント",
    ),
    (
        "Paging",
        "ページネーション",
        "テーブル形式のデータを複数ページで表示する際に利用する。",
    ),
    (
        "Toggle",
        "トグル",
        "ユーザーからの入力を受け取り、表示やステータスなどを即座位に切り替えたい場合に使用する。詳細はToggleButtonまたはToggleSwitchを参照してください。",
    ),
]

basic_elements = [
    (
        "Illustrations",
        "イラストレーション",
        "文字ではなくイラストレーションを使用して直感的に情報を伝えたい場合に使用する要素に関する説明",
    ),
    (
        "GridSystem",
        "グリッドシステム",
        "コンテンツのレイアウト時に一貫性を持たせるために使用コンポーネントに関するルールや適応例",
    ),
    (
        "ShadowAndLayout",
        "シャドウと高度",
        "コンテンツに与える影(shadow)や高度(zIndex)の使用ルールに関する説明",
    ),
    ("Writing", "ライティング", "SoftReefで使用する言語に関しての指針説明"),
    (
        "ResponsiveDesign",
        "レスポンシブデザイン",
        "デバイスサイズに応じた適切な画面レイアウトを提供するためのルールや適応例の説明",
    ),
    ("Opacity", "不透明度", "要素の不透明度に関するルールの説明"),
    ("Margin", "余白", "マージンやパディングなどの余白パターンの基本とルール説明"),
    ("Color", "色", "SoftReefで使用可能な色に関するルール説明"),
    ("Radius", "角丸", "要素の境界の外側の角を丸める際に準拠するべきルール説明"),
]

design_patterns = [
    (
        "ContentAreaLayout",
        "コンテンツエリア",
        "ヘッダーやナビゲーション、パンくずリスト以外の案件特化画面で遵守されるべきデザインルール",
    ),
    (
        "BasicScreenLayout",
        "基本画面構成-overview",
        "ヘッダーやナビゲーション、パンくずリストなどの全画面で共通で利用される画面要素のデザインルール",
    ),
    (
        "DeleteConfirmationDialog",
        "汎用削除確認画面-overview",
        "何かしらのオブジェクトを削除する際に汎用的に使用される画面のデザインルール",
    ),
    (
        "DetailPanelLayout",
        "汎用詳細画面",
        "何かしらのオブジェクトの詳細を確認する際に汎用的に使用される画面のデザインルール",
    ),
    (
        "FormSubmissionPanelLayout",
        "汎用入力画面",
        "ユーザーが情報を新規登録したり、編集するための画面として使用される画面のデザインルール",
    ),
]

uri_2_resource: dict[str, Resource] = {
    **{
        f"markdown://softreef/design-system/{en}": Resource(
            url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-{ja}--docs",
            name=f"{en} of Softreef design-system",
            description=description,
        )
        for (en, ja, description) in overviews
    },
    **{
        f"markdown://softreef/design-system/component/{en}": Resource(
            url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-{en.lower()}（{ja}）--docs",
            name=f"Softreef {en} component",
            description=description,
        )
        for (en, ja, description) in [
            *components,
            *form_components,
            *layout_components,
            *component_overviews,
        ]
    },
    **{
        f"markdown://softreef/design-system/component/{en}": Resource(
            url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-checkbox（チェックボックス）-{en.lower()}（{ja}）--docs",
            name=f"Softreef {en} component",
            description=description,
        )
        for (en, ja, description) in checkbox_components
    },
    **{
        f"markdown://softreef/design-system/component/{en}": Resource(
            url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-dialog（ダイアログ）-{en.lower()}--docs",
            name=f"Softreef {en} component",
            description=description,
        )
        for (en, _, description) in dialog_components
    },
    **{
        f"markdown://softreef/design-system/component/{en}": Resource(
            url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-card（カード）-{en.lower()}（{ja}）--docs",
            name=f"Softreef {en} component",
            description=description,
        )
        for (en, ja, description) in card_components
    },
    **{
        f"markdown://softreef/design-system/component/{en}": Resource(
            url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-chart（チャート）-{en.lower()}（{ja}）--docs",
            name=f"Softreef {en} component",
            description=description,
        )
        for (en, ja, description) in chart_components
    },
    **{
        f"markdown://softreef/design-system/component/{en}": Resource(
            url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-dropdownmenu（ドロップダウンメニュー）-{en.lower()}--docs",
            name=f"Softreef {en} component",
            description=description,
        )
        for (en, _, description) in dropdownmenu_components
    },
    **{
        f"markdown://softreef/design-system/component/{en}": Resource(
            url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-dropzone（ドロップゾーン）-{en.lower()}--docs",
            name=f"Softreef {en} component",
            description=description,
        )
        for (en, _, description) in dropzone_components
    },
    **{
        f"markdown://softreef/design-system/component/{en}": Resource(
            url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-paging（ページネーション）-{en.lower()}--docs",
            name=f"Softreef {en} component",
            description=description,
        )
        for (en, _, description) in paging_components
    },
    **{
        f"markdown://softreef/design-system/component/{en}": Resource(
            url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-コンポーネント-toggle（トグル）-{en.lower()}（{ja}）--docs",
            name=f"Softreef {en} component",
            description=description,
        )
        for (en, ja, description) in toggle_components
    },
    **{
        f"markdown://softreef/design-system/basic-element/{en}": Resource(
            url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-基本要素-{ja}--docs",
            name=f"Softreef {en} basic-element",
            description=description,
        )
        for (en, ja, description) in basic_elements
    },
    **{
        f"markdown://softreef/design-system/design-pattern/{en}": Resource(
            url=f"{SOFTREEF_DESIGN_SYSTEM_STORYBOOK_BASE_URL}-デザインパターン-{ja}--docs",
            name=f"Softreef {en} design-pattern",
            description=description,
        )
        for (en, ja, description) in design_patterns
    },
}


def main():
    http = urllib3.PoolManager()
    for uri in uri_2_resource:
        url = uri_2_resource[uri].url
        logger.info(f"Check if the following URL is reachable. URL: {url}")
        try:
            _ = http.request("HEAD", url, timeout=5.0, retries=False)
        except ConnectTimeoutError as e:
            logger.error(f"ConnectTimeoutError（接続タイムアウト）: {e}\n{url}")
        except ReadTimeoutError as e:
            logger.error(f"ReadTimeoutError（読み込みタイムアウト）: {e}\n{url}")
        except SSLError as e:
            logger.error(f"SSLError（SSLエラー）: {e}\n{url}")
        except NewConnectionError as e:
            logger.error(f"NewConnectionError（新規接続失敗、DNSエラー等）: {e}\n{url}")
        except ProxyError as e:
            logger.error(f"ProxyError（プロキシ関連のエラー）: {e}\n{url}")
        except MaxRetryError as e:
            logger.error(f"MaxRetryError（最大リトライ回数に到達）: {e}\n{url}")
        except HTTPError as e:
            logger.error(f"HTTPError（一般的なHTTPエラー）: {e}\n{url}")
        except Exception as e:
            logger.error(f"Error（その他のエラー）: {e}\n{url}")


def utf8_decode(url: str) -> str:
    from urllib.parse import unquote

    return unquote(url)


if __name__ == "__main__":
    main()
