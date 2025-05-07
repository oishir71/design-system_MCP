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
            name="get_softreef_overview_description",
            description="Get a description of either overview, environment or resource about Softreef design-system",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "enum": ["overview", "environment", "resource"],
                        "description": "Name of category",
                    }
                },
                "required": ["category"],
            },
        ),
        Tool(
            name="get_available_softreef_component_description_list",
            description="Get a list of available softreef component descriptions",
            inputSchema={"type": "object"},
        ),
        Tool(
            name="get_softreef_component_description",
            description="Get one of the descriptions in a series of descriptions about Softreef design-system component",
            inputSchema={
                "type": "object",
                "properties": {
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
                "required": ["component"],
            },
        ),
        Tool(
            name="get_available_softreef_design_pattern_description_list",
            description="Get a list of available softreef design-pattern descriptions",
            inputSchema={"type": "object"},
        ),
        Tool(
            name="get_softreef_design_pattern_description",
            description="Get one of the description in a series of descriptions about Softreef design-pattern",
            inputSchema={
                "type": "object",
                "properties": {
                    "pattern": {
                        "type": "string",
                        "enum": [
                            "ContentAreaLayout",
                            "BasicScreenLayout",
                            "DeleteConfirmationDialog",
                            "DetailPanelLayout",
                            "FormSubmissionPanelLayout",
                        ],
                        "description": "Name of design-pattern",
                    },
                },
                "required": ["pattern"],
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


async def call_get_softreef_overview_description(
    arguments: Any,
) -> Sequence[TextContent]:
    if not isinstance(arguments, dict) or not "category" in arguments:
        raise ValueError("Required argument 'category' not found")

    uri = f"markdown://softreef/design-system/{arguments.get("category")}"
    try:
        response = await get_storybook_resource(url=uri_2_resource.get(uri).url)
        return [TextContent(type="text", text=response)]
    except requests.HTTPError as e:
        logger.error(
            f"{str(e)} was occurred when client tried to obtain the '{arguments.get("pattern")}' description"
        )
        raise RuntimeError(
            f"{str(e)} was occurred when client tried to obtain the '{arguments.get("pattern")}' description"
        )


async def call_get_available_softreef_component_description_list() -> (
    Sequence[TextContent]
):
    tools = await list_tools()
    get_softreef_component_description_tool = None
    for tool in tools:
        if tool.name == "get_softreef_component_description":
            get_softreef_component_description_tool = tool

    components = (
        get_softreef_component_description_tool.inputSchema.get("properties")
        .get("component")
        .get("enum")
    )
    response = f"{str(components)}"
    return [TextContent(type="text", text=response)]


async def call_get_softreef_component_description(
    arguments: Any,
) -> Sequence[TextContent]:
    if not isinstance(arguments, dict) or not "component" in arguments:
        raise ValueError("Required argument 'component' not found")

    uri = f"markdown://softreef/design-system/component/{arguments.get("component")}"
    try:
        response = await get_storybook_resource(url=uri_2_resource.get(uri).url)
        return [TextContent(type="text", text=response)]
    except requests.HTTPError as e:
        logger.error(
            f"{str(e)} was occurred when client tried to obtain the '{arguments.get("component")}' component description"
        )
        raise RuntimeError(
            f"{str(e)} was occurred when client tried to obtain the '{arguments.get("component")}' component description"
        )


async def call_get_available_softreef_design_pattern_description_list() -> (
    Sequence[TextContent]
):
    tools = await list_tools()
    get_softreef_design_pattern_description_tool = None
    for tool in tools:
        if tool.name == "get_softreef_design_pattern_description":
            get_softreef_design_pattern_description_tool = tool

    patterns = (
        get_softreef_design_pattern_description_tool.inputSchema.get("properties")
        .get("pattern")
        .get("enum")
    )
    response = f"{str(patterns)}"
    return [TextContent(type="text", text=response)]


async def call_get_softreef_design_pattern_description(
    arguments: Any,
) -> Sequence[TextContent]:
    if not isinstance(arguments, dict) or not "pattern" in arguments:
        raise ValueError("Required argument 'pattern' not found")

    uri = f"markdown://softreef/design-system/design-pattern/{arguments.get("pattern")}"
    try:
        response = await get_storybook_resource(url=uri_2_resource.get(uri).url)
        return [TextContent(type="text", text=response)]
    except requests.HTTPError as e:
        logger.error(
            f"{str(e)} was occurred when client tried to obtain the '{arguments.get("pattern")}' design-pattern description"
        )
        raise RuntimeError(
            f"{str(e)} was occurred when client tried to obtain the '{arguments.get("pattern")}' design-pattern description"
        )


@app.call_tool()
async def call_tool(
    name: str, arguments: Any
) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    if name == "run_aggregation":
        return await call_run_aggregation(arguments)
    elif name == "get_softreef_overview_description":
        return await call_get_softreef_overview_description(arguments)
    elif name == "get_available_softreef_component_description_list":
        return await call_get_available_softreef_component_description_list()
    elif name == "get_softreef_component_description":
        return await call_get_softreef_component_description(arguments)
    elif name == "get_available_softreef_design_pattern_description_list":
        return await call_get_available_softreef_design_pattern_description_list()
    elif name == "get_softreef_design_pattern_description":
        return await call_get_softreef_design_pattern_description(arguments)
    else:
        raise ValueError(f"Unknown tool: {name}")


async def main():
    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
