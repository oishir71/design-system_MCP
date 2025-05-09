# 概要

こちらのrespositoryはSoftreefのdesign-systemの内容をLLMに伝える役割を持つMCP Serverが実装されています。
S3上にデプロイされているstorybookの内容を取得し、それをLLMに伝えることでLLMがあたかもdesign-systemを把握しているように動作させています。

# 環境構築

ローカルのMac上で以下を実行し、repositoryをクローンします。

```bash
git clone git@github.com:oishir71/Softreef_DesignSystem_MCP_Server.git softreef-mcp-server
cd softreef-mcp-server
```

MCP ClientにクローンしたMCP Serverを認識させます。
その際に、proxyの設定を`env`に記載する必要があります。

Claude desktopをMCP Clientとして利用する場合は`clande_desktop_config.json`に以下を記載します。

```json:claude_desktop_config.json
{
  "mcpServers": {
    "softreef": {
      "command": "/Users/oishir71/.local/bin/uv",
      "args": [
        "--directory",
        "/Users/yourname/path/to/respository/design_system_mcp_server",
        "run",
        "storybook_server.py"
      ],
      "env": {
        "https_proxy": "http://10.35.227.1:8080",
        "http_proxy": "http://10.35.227.1:8080",
        "all_proxy": "http://10.35.227.1:8080",
        "no_proxy": "127.0.*,192.168.*,localhost,10.144.42.153",
        "ALL_PROXY": "http://10.35.227.1:8080",
        "HTTPS_PROXY": "http://10.35.227.1:8080",
        "HTTP_PROXY": "http://10.35.227.1:8080"
      }
    }
  }
}
```

VS CodeをMCP Clientとして利用する場合は`settings.json`に上記と同様の設定を行う必要があります。

```json:settings.json
...
  "mcp": {
    "inputs": [],
    "servers": {
      "softreef": {
        "command": "/Users/oishir71/.local/bin/uv",
        "args": [
          "--directory",
          "/Users/oishir71/Desktop/SoftBank/R_D/MCP/softreef",
          "run",
          "storybook_server.py"
        ],
        "env": {
          "https_proxy": "http://10.35.227.1:8080",
          "http_proxy": "http://10.35.227.1:8080",
          "all_proxy": "http://10.35.227.1:8080",
          "no_proxy": "127.0.*,192.168.*,localhost,10.144.42.153",
          "ALL_PROXY": "http://10.35.227.1:8080",
          "HTTPS_PROXY": "http://10.35.227.1:8080",
          "HTTP_PROXY": "http://10.35.227.1:8080"
        }
      },
    }
  }
...
```

# API

## Resource

- `markdown://softreef/design-system/{category}`
  - `category`には`overview`, `environment`, `resource`のいずれか
  - design-systemの基本的な説明
- `markdown://softreef/design-system/component/{component}`
  - `component`にはdesign-systemで提供されているcomponent名が入る
  - design-systemのocmponentの基本的な説明
- `markdown://softreef/design-system/design-pattern/{pattern}`
  - `pattern`にはdesign-patternで提供されているpattern名が入る
  - design-patterの基本的な説明

## Tool

- `get_overview_description`
  - `markdown://softreef/design-system/{category}`の説明を取得する
- `get_component_list`
  - `markdown://softreef/design-system/component/{component}` resourceで取得できる説明の一覧を取得する
- `ge_component_description`
  - `markdown://softreef/design-system/component/{component}`の説明を取得する
- `get_design_pattern_list`
  - `markdown://softreef/design-system/design-pattern/{pattern}` resourceで取得できる説明の一覧を取得する
- `get_design_pattern_description`
  - `markdown://softreef/design-system/design-pattern/{pattern}`の説明を取得する

## Prompt

- `softreef_overview`
  - `markdown://softreef/design-system/{category}` resourceをpromptに埋め込むことができる。
  - `category`は必須で与える必要がある
- `softreef_component`
  - `markdown://softreef/design-system/component/{component}` resourceをpromptに埋め込むことができる。
  - `component`は必須で与える必要がある
- `softreef_design_pattern`
  - `markdown://softreef/design-system/design-pattern/{pattern}` resourceをpromptに埋め込むことができる。
  - `pattern`は必須で与える必要がある

# Tips

エラーに遭遇したら`/Users/yourname/Library/Logs/Claude`配下のログファイルを確認する。
