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
from storybook_resources import (
    uri_2_resource as sb_uri_2_resources,
    overviews as sb_overviews,
    components as sb_components,
    form_components as sb_form_components,
    checkbox_components as sb_checkbox_components,
    dialog_components as sb_dialog_components,
    card_components as sb_card_components,
    dropdownmenu_components as sb_dropdownmenu_components,
    dropzone_components as sb_dropzone_components,
    paging_components as sb_paging_components,
    toggle_components as sb_toggle_components,
    layout_components as sb_layout_components,
    basic_elements as sb_basic_elements,
    design_patterns as sb_design_patterns,
)
from design_system_file_path_resources import uri_2_resource as ds_uri_2_resources
from storybook_prompts import prompts

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("softreef")


async def get_storybook_resource(url: str):
    try:
        markdown = await markdown_format_text(url)
        return markdown
    except httpx.HTTPError as e:
        raise RuntimeError(
            f"{str(e)} was occurred during fetching storybook resource from the url: ({url})"
        )


app = Server("softreef")


@app.list_prompts()
async def list_prompts() -> list[Prompt]:
    return prompts


@app.get_prompt()
async def get_prompt(
    name: str, arguments: dict[str, str] | None = None
) -> GetPromptResult:
    if name == "softreef-design-system-overview":
        category = arguments.get("category")
        uri = f"markdown://softreef/design-system/{category}"
        response = await get_storybook_resource(url=sb_uri_2_resources[uri].url)
        return GetPromptResult(
            messages=[
                PromptMessage(
                    role="user",
                    content=TextContent(
                        type="text",
                        text=(
                            f"Softreefのdesign-systemの{category}について以下の情報を参照して教えてください。"
                            f"\n\n{response}"
                        ),
                    ),
                )
            ]
        )
    elif name == "softreef-design-system-component":
        component = arguments.get("component")
        uri = f"markdown://softreef/design-system/component/{component}"
        response = await get_storybook_resource(url=sb_uri_2_resources[uri].url)
        return GetPromptResult(
            messages=[
                PromptMessage(
                    role="user",
                    content=TextContent(
                        type="text",
                        text=(
                            f"Softreefのdesign-systemの{component}コンポーネントについて以下の情報を参照して教えてください。"
                            f"\n\n{response}"
                        ),
                    ),
                )
            ]
        )
    elif name == "softreef-design-system-basic-element":
        element = arguments.get("element")
        uri = f"markdown://softreef/design-system/basic-element/{element}"
        response = await get_storybook_resource(url=sb_uri_2_resources[uri].url)
        return GetPromptResult(
            messages=[
                PromptMessage(
                    role="user",
                    content=TextContent(
                        type="text",
                        text=(
                            f"Softreefのdesign-systemの基本要素の1つである{element}について以下の情報を参照して教えてください。"
                            f"\n\n{response}"
                        )
                    )
                )
            ]
        )
    elif name == "softreef-design-system-design-pattern":
        pattern = arguments.get("pattern")
        uri = f"markdown://softreef/design-system/design-pattern/{pattern}"
        response = await get_storybook_resource(url=sb_uri_2_resources[uri].url)
        return GetPromptResult(
            messages=[
                PromptMessage(
                    role="user",
                    content=TextContent(
                        type="text",
                        text=(
                            f"Softreefのdesign-systemの{pattern} design-patternについて以下の情報を参照して教えてください。"
                            f"\n\n{response}"
                        ),
                    ),
                )
            ]
        )
    else:
        raise ValueError(f"Prompt not found: {name}")


@app.list_resources()
async def list_resources() -> list[Resource]:
    return [
        *[
            Resource(
                uri=key,
                name=value.name,
                description=value.description,
                mimeType="text/markdown",
            )
            for key, value in sb_uri_2_resources.items()
        ],
        *[
            Resource(
                uri=key,
                name=value.name,
                description=value.description,
                mimeType="text/plain",
            )
            for key, value in ds_uri_2_resources.items()
        ],
    ]


@app.read_resource()
async def read_resource(uri: AnyUrl) -> str:
    uri = str(uri)
    if uri in sb_uri_2_resources:
        return await get_storybook_resource(url=sb_uri_2_resources[uri].url)
    elif uri in ds_uri_2_resources:
        return await ds_uri_2_resources[uri].path
    else:
        logger.error(f"URI: {uri} was not defined.")
        raise RuntimeError(f"Not defined URI was given: {uri}")


@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="get_softreef_overview_description",
            description="Softreefのdesign-systemの概要に関する情報を取得する",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "enum": [overview[0] for overview in sb_overviews],
                        "description": "概要の種類",
                    }
                },
                "required": ["category"],
            },
        ),
        Tool(
            name="get_available_softreef_component_description_list",
            description="Softreefのdesign-systemが提供しているコンポーネントの一覧を取得する",
            inputSchema={"type": "object"},
        ),
        Tool(
            name="get_softreef_component_description",
            description="Softreefのdesign-systemが提供しているコンポーネントに関する情報を取得する",
            inputSchema={
                "type": "object",
                "properties": {
                    "component": {
                        "type": "string",
                        "enum": [component[0] for component in [
                            *sb_components,
                            *sb_form_components,
                            *sb_checkbox_components,
                            *sb_dialog_components,
                            *sb_dropdownmenu_components,
                            *sb_card_components,
                            *sb_dropzone_components,
                            *sb_paging_components,
                            *sb_toggle_components,
                            *sb_layout_components]],
                        "description": "コンポーネント名",
                    },
                },
                "required": ["component"],
            },
        ),
        Tool(
            name="get_available_softreef_basic_element_description_list",
            description="Softreefのdesign-systemが提供する基本要素の一覧を取得する",
            inputSchema={"type": "object"},
        ),
        Tool(
            name="get_softreef_basic_element_description",
            description="Softreefのdesign-systemが提供する基本要素に関する情報を取得する",
            inputSchema={
                "type": "object",
                "properties": {
                    "element": {
                        "type": "string",
                        "enum": [element[0] for element in sb_basic_elements],
                        "description": "基本要素名",
                    },
                },
                "required": ["element"]
            },
        ),
        Tool(
            name="get_available_softreef_design_pattern_description_list",
            description="Softreefのdesign-systemが提供するデザインパターンの一覧を取得する",
            inputSchema={"type": "object"},
        ),
        Tool(
            name="get_softreef_design_pattern_description",
            description="Softreefのdesign-systemが提供するデザインパターンに関する情報を取得する",
            inputSchema={
                "type": "object",
                "properties": {
                    "pattern": {
                        "type": "string",
                        "enum": [pattern[0] for pattern in sb_design_patterns],
                        "description": "デザインパターン名",
                    },
                },
                "required": ["pattern"],
            },
        ),
        Tool(
            name="get_softreef_component_file_path",
            description="Softreefのdesign-systemが提供するコンポーネントの実装ファイルの絶対パスを取得する",
            inputSchema={
                "type": "object",
                "properties": {
                    "component": {
                        "type": "string",
                        "enum": [component[0] for component in [
                            *sb_components,
                            *sb_form_components,
                            *sb_checkbox_components,
                            *sb_dialog_components,
                            *sb_dropdownmenu_components,
                            *sb_card_components,
                            *sb_dropzone_components,
                            *sb_paging_components,
                            *sb_toggle_components,
                            *sb_layout_components]],
                        "description": "コンポーネント名",
                    },
                },
                "required": ["component"],
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
    response = await get_storybook_resource(url=sb_uri_2_resources.get(uri).url)
    return [TextContent(type="text", text=response)]


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
    response = await get_storybook_resource(url=sb_uri_2_resources.get(uri).url)
    return [TextContent(type="text", text=response)]


async def call_get_available_softreef_basic_element_description_list() -> Sequence[TextContent]:
    tools = await list_tools()
    get_softreef_basic_element_description_tool = None
    for tool in tools:
        if tool.name == "get_softreef_basic_element_description":
            get_softreef_basic_element_description_tool = tool

    elements = (
        get_softreef_basic_element_description_tool.inputSchema.get("properties")
        .get("element")
        .get("enum")
    )
    response = f"{str(elements)}"
    return [TextContent(type="text", text=response)]

async def call_get_softreef_basic_element_description(arguments) -> Sequence[TextContent]:
    if not isinstance(arguments, dict) or not "element" in arguments:
        raise ValueError("Required argument 'element' not found")

    uri = f"markdown://softreef/design-system/basic-element/{arguments.get("element")}"
    response = await get_storybook_resource(url=sb_uri_2_resources.get(uri).url)
    return [TextContent(type="text", text=response)]

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
    response = await get_storybook_resource(url=sb_uri_2_resources.get(uri).url)
    return [TextContent(type="text", text=response)]


async def call_get_softreef_component_file_path(
    arguments: Any,
) -> Sequence[TextContent]:
    if not isinstance(arguments, dict) or not "component" in arguments:
        raise ValueError("Required argument 'component' not found")

    uri = f"filepath://softreef/design-system/component/{arguments.get("component")}"
    response = ds_uri_2_resources.get(uri).path
    return [TextContent(type="text", text=response)]


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
    elif name == "get_available_softreef_basic_element_description_list":
        return await call_get_available_softreef_basic_element_description_list()
    elif name == "get_softreef_basic_element_description":
        return await call_get_softreef_basic_element_description(arguments)
    elif name == "get_available_softreef_design_pattern_description_list":
        return await call_get_available_softreef_design_pattern_description_list()
    elif name == "get_softreef_design_pattern_description":
        return await call_get_softreef_design_pattern_description(arguments)
    elif name == "get_softreef_component_file_path":
        return await call_get_softreef_component_file_path(arguments)
    else:
        raise ValueError(f"Unknown tool: {name}")


async def main():
    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
