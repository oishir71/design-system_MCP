from mcp.types import Prompt, PromptArgument

prompts: list[Prompt] = [
    Prompt(
        name="softreef_overview",
        description="Generate a description of design-system overview",
        arguments=[
            PromptArgument(
                name="category",
                description="type of major category",
                required=True,
            )
        ],
    ),
    Prompt(
        name="softreef_component",
        description="Generate a description of design-system component",
        arguments=[
            PromptArgument(
                name="component",
                description="type of component",
                required=True,
            )
        ],
    ),
    Prompt(
        name="softreef_design_pattern",
        description="Generate a description of design-pattern",
        arguments=[
            PromptArgument(
                name="pattern",
                description="type of design-pattern",
                required=True,
            )
        ],
    ),
]
