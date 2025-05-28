import os
import sys
import json
import asyncio
from pathlib import Path
from typing import Any
from contextlib import AsyncExitStack

from openai import AsyncAzureOpenAI
from dotenv import load_dotenv

sys.path.append(str(Path(__file__).parent.parent / "utils"))
from color_print import user_input, llm_print, event_print, error_print

sys.path.append(str(Path(__file__).parent.parent / "client"))
from stdio_client_light import MCPClient

load_dotenv()

OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")
OPENAI_API_VERSION = os.getenv("OPENAI_API_VERSION")
OPENAI_DEPLOYMENT_ID = os.getenv("OPENAI_DEPLOYMENT_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class MCPHost:
    def __init__(self, servers: dict[str, dict]):
        self.servers = servers
        self.clients = {}
        self.tools = {}

        self.client_context_stack = AsyncExitStack()

        self.session_name = "host"
        self.session_dir = Path(__file__).parent / "sessions"
        self.session_dir.mkdir(parents=True, exist_ok=True)

        self.openai_client = AsyncAzureOpenAI(
            azure_endpoint=OPENAI_API_BASE,
            azure_deployment=OPENAI_DEPLOYMENT_ID,
            api_key=OPENAI_API_KEY,
        )

    async def __aenter__(self):
        for server_name, server_parameters in self.servers.items():
            client = await self.client_context_stack.enter_async_context(
                MCPClient(server_parameters)
            )
            tools = await client._get_tools()

            self.clients[server_name] = client
            self.tools[server_name] = tools

        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.client_context_stack.aclose()

    def _save_session(self, messages: list[dict[str, Any]]):
        with (self.session_dir / f"{self.session_name}.json").open("w") as f:
            json.dump(messages, f, ensure_ascii=False, indent=4)

    def _read_session(self) -> list[dict[str, Any]]:
        session_file = self.session_dir / f"{self.session_name}.json"
        if not session_file.exists():
            return []
        with session_file.open("r") as f:
            return json.load(f)

    async def execute(self, message: dict[str, Any]):
        event_print("Taskを開始します")
        messages = self._read_session()
        messages.append(message)
        flatten_tools = [item for sublist in self.tools.values() for item in sublist]

        while True:
            event_print("LLMによる推論中です")
            response = await self.openai_client.chat.completions.create(
                model=OPENAI_DEPLOYMENT_ID,
                messages=messages,
                tools=flatten_tools,
            )
            event_print("LLMによる推論が完了しました")
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
            self._save_session(messages=messages)

            if response_message.tool_calls:
                for tool_call in response_message.tool_calls:
                    tool_name = tool_call.function.name
                    tool_arguments = json.loads(tool_call.function.arguments)
                    for server_name in self.tools:
                        server_tool_names = [
                            server_tool.get("function").get("name")
                            for server_tool in self.tools[server_name]
                        ]
                        if tool_name in server_tool_names:
                            event_print(
                                f"{tool_name = }を{tool_arguments = }で実行します"
                            )
                            contents = await self.clients[server_name].execute_tool(
                                name=tool_name, arguments=tool_arguments
                            )
                            messages.append(
                                {
                                    "role": "tool",
                                    "content": contents,
                                    "tool_call_id": tool_call.id,
                                }
                            )
                            self._save_session(messages=messages)
                            event_print(f"{tool_name = }の実行が完了しました")
            else:
                break

    async def chat_loop(self):
        event_print("\n以下のMCP Serverの読み込みが完了しました")
        for server_name in self.clients.keys():
            event_print(f"  - {server_name}")
        event_print("質問を入力するか'quit'を入力して終了してください")

        while True:
            try:
                query = user_input("\nユーザー入力: ")
                if query.lower() == "quit":
                    break

                message = {"role": "user", "content": query}
                await self.execute(message=message)
            except Exception as e:
                error_print(f"\nエラーが発生しました: {str(e)}")


async def main(servers: dict[str, Any]):
    async with MCPHost(servers=servers) as host:
        await host.chat_loop()


if __name__ == "__main__":
    with open("./config.json") as f:
        servers = json.load(f)
    asyncio.run(main(servers=servers))
