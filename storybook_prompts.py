from mcp.types import Prompt, PromptArgument

prompts: list[Prompt] = [
    Prompt(
        name="design-system_storybook",
        description="Generate a description of design-system",
        arguments=[
            PromptArgument(
                name="category",
                description="type of major category",
                required=True,
            ),
            PromptArgument(
                name="component",
                description="type of component",
                required=False,
            )
        ]
    )
]