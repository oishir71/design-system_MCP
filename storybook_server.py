import json
import logging
from collections.abc import Sequence
from typing import Any
import requests
import httpx
from dotenv import load_dotenv
from pydantic import AnyUrl
from mcp.server import Server
from mcp.types import (
    Prompt,
    GetPromptResult,
    PromptMessage,
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)

from storybook_async_fetcher import markdown_format_text
from storybook_resources import uri_2_resource
from storybook_prompts import prompts

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("softreef")


async def get_storybook_resource(url: str):
    markdown = await markdown_format_text(url)
    return markdown


app = Server("softreef")


@app.list_prompts()
async def list_prompts() -> list[Prompt]:
    return prompts


@app.get_prompt()
async def get_prompt(
    name: str, arguments: dict[str, str] | None = None
) -> GetPromptResult:
    if not name in [prompt.name for prompt in prompts]:
        raise ValueError(f"Prompt not found: {name}")

    if name == "design-system_storybook":
        uri = "markdown://softreef/design-system/"
        category = arguments.get("category")
        component = arguments.get("component", "")
        if category == "component":
            uri += f"{category}/{component}"
            response = await get_storybook_resource(url=uri_2_resource[uri].url)
            return GetPromptResult(
                messages=[
                    PromptMessage(
                        role="user",
                        content=TextContent(
                            type="text",
                            text=(
                                f"Softreefのdesign-systemの{component}コンポーネントについて知りたいです。\n"
                                f"以下の内容を参照して教えてください。\n\n{response}"
                            ),
                        ),
                    )
                ]
            )
        else:
            uri += category
            if uri in uri_2_resource:
                response = await get_storybook_resource(url=uri_2_resource[uri].url)
                return GetPromptResult(
                    messages=[
                        PromptMessage(
                            role="user",
                            content=TextContent(
                                type="text",
                                text=(
                                    f"Softreefの{category}について知りたいです。\n"
                                    f"以下の内容を参照して教えてください。\n\n{response}"
                                ),
                            ),
                        )
                    ]
                )
            else:
                return GetPromptResult(
                    messages=[
                        PromptMessage(
                            role="user",
                            content=TextContent(
                                type="text",
                                text=(f"Softreefの{category}について教えてください。"),
                            ),
                        )
                    ]
                )

    raise ValueError(f"Prompt implementation not found: {name}")


@app.list_resources()
async def list_resources() -> list[Resource]:
    return [
        Resource(
            uri=key,
            name=value.name,
            description=value.description,
            mimeType="text/markdown",
        )
        for key, value in uri_2_resource.items()
    ]


@app.read_resource()
async def read_resource(uri: AnyUrl) -> str:
    uri = str(uri)
    if not uri in uri_2_resource:
        logger.error(f"URI: {uri} was not defined.")
        raise RuntimeError(f"Not defined URI was given: {uri}")

    try:
        content = await get_storybook_resource(url=uri_2_resource[uri].url)
        return content
    except httpx.HTTPError as e:
        raise RuntimeError(f"Fetch softreef design-system content error: {str(e)}")


@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="get_storybook_as_markdown",
            description="Get description of Softreef design-system",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "enum": ["overview", "environment", "resource", "component"],
                        "description": "type of major category",
                    },
                    "component": {
                        "type": "string",
                        "enum": [
                            "Accordion",
                            "Autocomplete",
                            "Breadcrumbs",
                            "Button",
                            "ButtonGroup",
                            "CardOverview",
                            "Card",
                            "CardForGalleryView",
                            "CardList",
                            "BarChart",
                            "AllSelectCheckBox",
                            "CheckBox",
                            "Chip",
                            "DateTimePicker",
                            "DialogOverview",
                            "ActionDialog",
                            "StepperDialog",
                            "Divider",
                            "DropdownMenuButton",
                            "EllipsisDropdownMenuButton",
                            "DropZoneOverview",
                            "ImageDropZone",
                            "GridLayout",
                            "Icon",
                            "List",
                            "Loader",
                            "Logo",
                            "Notification",
                            "PagingOverview",
                            "FullPaging",
                            "SimplePaging",
                            "RadioButton",
                            "SelectBox",
                            "Slider",
                            "Status",
                            "Stepper",
                            "SwitchTableAndCardView",
                            "Tab",
                            "Table",
                            "Text",
                            "TextBox",
                            "ToggleOverview",
                            "ToggleButton",
                            "ToggleSwitch",
                            "Tooltip",
                            "KeyValue",
                        ],
                        "description": "Name of component",
                    },
                },
                "required": ["category"],
            },
        ),
    ]


async def call_run_aggregation(arguments: Any) -> Sequence[TextContent]:
    if not isinstance(arguments, dict) or "aggregation" not in arguments:
        raise ValueError("Required argument 'aggregation' not found")

    aggregation = arguments.get("aggregation")
    data = {"aggregation": {"column": "0", "aggs": aggregation}}

    try:
        response = "Thi is an example."
        return [TextContent(type="text", text=json.dumps(response, indent=2))]
    except requests.HTTPError as e:
        logger.error(f"{str(e)} was occurred during calling run aggregation")
        raise RuntimeError(f"{str(e)} was occurred during calling run aggregation")


async def call_get_storybook_as_markdown_tool(arguments: Any) -> Sequence[TextContent]:
    if not isinstance(arguments, dict) or "category" not in arguments:
        raise ValueError("Required argument 'category' not found")

    uri = "markdown://softreef/design-system/"
    category = arguments.get("category")
    component = arguments.get("component", "")
    if category == "component":
        uri += f"{category}/{component}"
    else:
        uri += category

    try:
        response = await get_storybook_resource(url=uri_2_resource[uri].url)
        return [TextContent(type="text", text=response)]
    except requests.HTTPError as e:
        logger.error(f"{str(e)} was occurred during calling get storybook resource")
        raise RuntimeError(
            f"{str(e)} was occurred during calling get storybook resource"
        )


@app.call_tool()
async def call_tool(
    name: str, arguments: Any
) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    if name == "run_aggregation":
        return await call_run_aggregation(arguments)
    elif name == "get_storybook_as_markdown":
        return await call_get_storybook_as_markdown_tool(arguments)
    else:
        raise ValueError(f"Unknown tool: {name}")


async def main():
    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
