import asyncio
from typing import Optional, Any
from contextlib import AsyncExitStack
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.types import EmbeddedResource, ImageContent, TextContent


class MCPClient:
    def __init__(self, session_parameters: dict[str, Any]):
        self.session_parameters = session_parameters
        self.session: Optional[ClientSession] = None

        self.session_dir = Path(__file__).parent / "sessions"
        self.session_dir.mkdir(parents=True, exist_ok=True)

        self.exit_stack = AsyncExitStack()

    async def connect_to_server(self):
        server_params = StdioServerParameters(
            command=self.session_parameters.get("command"),
            args=self.session_parameters.get("args"),
            env=self.session_parameters.get("env", None),
        )

        stdio_transport = await self.exit_stack.enter_async_context(
            stdio_client(server_params)
        )
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(self.stdio, self.write)
        )

        await self.session.initialize()

    async def _get_tools(self):
        list_tools_response = await self.session.list_tools()
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

    async def execute_tool(self, name: str, arguments: dict[str, Any]):
        result = await self.session.call_tool(name=name, arguments=arguments)
        return [self._encode_tool_content(c) for c in result.content]

    async def cleanup(self):
        await self.exit_stack.aclose()


async def main():
    session_parameters = {
        "command": "/Users/oishir71/.local/bin/uv",
        "args": [
            "--directory",
            "/Users/oishir71/Desktop/SoftBank/R_D/MCP/design-system_MCP/server",
            "run",
            "storybook_server.py",
        ],
        "env": {
            "https_proxy": "http://10.35.227.1:8080",
            "http_proxy": "http://10.35.227.1:8080",
            "all_proxy": "http://10.35.227.1:8080",
            "no_proxy": "127.0.*,192.168.*,localhost,10.144.42.153",
            "ALL_PROXY": "http://10.35.227.1:8080",
            "HTTPS_PROXY": "http://10.35.227.1:8080",
            "HTTP_PROXY": "http://10.35.227.1:8080",
        },
    }

    client = MCPClient(session_parameters=session_parameters)
    await client.connect_to_server()
    await client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
