from mcp.types import Prompt, PromptArgument

prompts: list[Prompt] = [
    Prompt(
        name="softreef-design-system-overview",
        description="Softreefの概要に関する情報を取得するためのプロンプト",
        arguments=[
            PromptArgument(
                name="category",
                description="概要の種類",
                required=True,
            )
        ],
    ),
    Prompt(
        name="softreef-design-system-component",
        description="Softreefのコンポーネントに関する情報を取得するためのプロンプト",
        arguments=[
            PromptArgument(
                name="component",
                description="コンポーネントの種類",
                required=True,
            )
        ],
    ),
    Prompt(
        name="softreef-design-system-basic-element",
        description="Softreefの基本要素に関する情報を取得するためのプロンプト",
        arguments=[
            PromptArgument(name="element", description="基本要素の種類", required=True)
        ],
    ),
    Prompt(
        name="softreef-design-system-design-pattern",
        description="Softreefのデザインパターンに関する情報を取得するためのプロンプト",
        arguments=[
            PromptArgument(
                name="pattern",
                description="デザインパターンの種類",
                required=True,
            )
        ],
    ),
]
