import os
import sys
import json
import asyncio
from dataclasses import dataclass
from collections.abc import AsyncGenerator
from pathlib import Path
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.types import EmbeddedResource, ImageContent, TextContent

from openai import AsyncAzureOpenAI
from dotenv import load_dotenv

sys.path.append(str(Path(__file__).parent.parent / "utils"))
from color_print import user_input, llm_print, event_print

load_dotenv()

OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")
OPENAI_API_VERSION = os.getenv("OPENAI_API_VERSION")
OPENAI_DEPLOYMENT_ID = os.getenv("OPENAI_DEPLOYMENT_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


@dataclass
class StdioServerParameterArgs:
    command: str
    args: list[str]
    env: dict[str, str] | None = None


class MCPClient:
    def __init__(self, session_name: str, parameters: StdioServerParameterArgs):
        self.session_name = session_name
        self.parameters = parameters

        self.session_dir = Path(__file__).parent / "sessions"
        self.session_dir.mkdir(parents=True, exist_ok=True)

        self.openai_client = AsyncAzureOpenAI(
            azure_endpoint=OPENAI_API_BASE,
            azure_deployment=OPENAI_DEPLOYMENT_ID,
            api_key=OPENAI_API_KEY,
        )

    def _save_session(self, session_name: str, messages: list[dict[str, Any]]):
        with (self.session_dir / f"{session_name}.json").open("w") as f:
            json.dump(messages, f, ensure_ascii=False, indent=4)

    def _read_session(self, session_name: str) -> list[dict[str, Any]]:
        session_file = self.session_dir / f"{session_name}.json"
        if not session_file.exists():
            return []
        with session_file.open("r") as f:
            return json.load(f)

    async def _get_tools(
        self, mcp_client_session: ClientSession
    ) -> list[dict[str, Any]]:
        list_tools_response = await mcp_client_session.list_tools()
        tools = [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.inputSchema,
                },
            }
            for tool in list_tools_response.tools
        ]
        event_print("ツール一覧を取得しました")
        return tools

    def _encode_tool_content(
        self, content: TextContent | ImageContent | EmbeddedResource
    ):
        if isinstance(content, TextContent):
            return {"type": "text", "text": content.text}
        elif isinstance(content, ImageContent):
            return {"type": "image_url", "image_url": {"url": content.url}}
        else:
            raise Exception(f"Unsupported content type: {type(content)}")

    async def _execute_tool(
        self, session: ClientSession, name: str, arguments: dict[str, Any]
    ):
        result = await session.call_tool(name=name, arguments=arguments)
        return [self._encode_tool_content(c) for c in result.content]

    async def execute(
        self, message: dict[str, Any], session_name: str
    ) -> AsyncGenerator:
        event_print("taskを開始します")
        messages = self._read_session(session_name)
        messages.append(
            {
                "role": message.get("role", "user"),
                "content": [{"type": "text", "text": message.get("content")}],
            }
        )

        server_params = StdioServerParameters(
            command=self.parameters.command,
            args=self.parameters.args,
            env=self.parameters.env,
        )
        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()

                tools = await self._get_tools(session)

                while True:
                    event_print("LLMによる推論中です")
                    response = await self.openai_client.chat.completions.create(
                        model=OPENAI_DEPLOYMENT_ID,
                        messages=messages,
                        tools=tools,
                    )
                    event_print("LLMにより推論が完了しました")
                    response_message = response.choices[0].message
                    input_required = False
                    if response_message.content:
                        llm_print(response_message.content)
                        if response_message.content.endswith("<INPUT_REQUIRED>"):
                            input_required = True
                            response_message.content = response_message.content.rstrip(
                                "<INPUT_REQUIRED>"
                            )
                    messages.append(
                        response_message.model_dump(mode="json", exclude_defaults=True)
                    )
                    self._save_session(session_name=session_name, messages=messages)

                    if response_message.tool_calls:
                        for tool_call in response_message.tool_calls:
                            tool_name = tool_call.function.name
                            tool_arguments = json.loads(tool_call.function.arguments)
                            event_print(
                                f"{tool_name = }を{tool_arguments = }で実行します"
                            )
                            contents = await self._execute_tool(
                                session=session,
                                name=tool_name,
                                arguments=tool_arguments,
                            )
                            messages.append(
                                {
                                    "role": "tool",
                                    "content": contents,
                                    "tool_call_id": tool_call.id,
                                }
                            )
                            self._save_session(
                                session_name=session_name, messages=messages
                            )
                            event_print(f"{tool_name = }の実行が完了しました")
                    else:
                        break

    async def chat_loop(self):
        event_print("\nMCP Clientが起動しました")
        event_print("質問を入力するか'quit'を入力して終了してください")

        while True:
            try:
                query = user_input("\nユーザー入力: ")
                if query.lower() == "quit":
                    break

                message = {"role": "user", "content": query}
                await self.execute(message=message, session_name=self.session_name)
            except Exception as e:
                event_print(f"\nエラーが発生しました: {str(e)}")


async def main():
    client = MCPClient()
    await client.chat_loop()


if __name__ == "__main__":
    session_name = "softreef"
    parameters = StdioServerParameterArgs(
        command="/Users/oishir71/.local/bin/uv",
        args=[
            "--directory",
            "/Users/oishir71/Desktop/SoftBank/R_D/MCP/design-system_MCP/server",
            "run",
            "storybook_server.py",
        ],
        env={
            "https_proxy": "http://10.35.227.1:8080",
            "http_proxy": "http://10.35.227.1:8080",
            "all_proxy": "http://10.35.227.1:8080",
            "no_proxy": "127.0.*,192.168.*,localhost,10.144.42.153",
            "ALL_PROXY": "http://10.35.227.1:8080",
            "HTTPS_PROXY": "http://10.35.227.1:8080",
            "HTTP_PROXY": "http://10.35.227.1:8080",
        },
    )

    asyncio.run(main(session_name=session_name, parameters=parameters))
