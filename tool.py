import os
import sys
import warnings
import logging

from crewai_tools import BaseTool, MCPServerAdapter

warnings.filterwarnings("ignore")
logging.disable(logging.CRITICAL)

from contextlib import contextmanager
from io import StringIO


@contextmanager
def suppress_output():
    original_stderr = sys.stderr
    original_stdout = sys.stdout
    try:
        sys.stderr = StringIO()
        sys.stdout = StringIO()
        yield
    finally:
        sys.stderr = original_stderr
        sys.stdout = original_stdout


class UclMcpTool(BaseTool):
    name = "ucl_mcp_tool"
    description = "Proxy tool forwarding calls to Fastn UCL MCP server."

    def __init__(self, **data):
        super().__init__(**data)
        self.server_url = os.getenv("MCP_SERVER_URL", "http://localhost:3001")

    def _get_server_params(self):
        return {
            "url": self.server_url,
            "transport": "streamable-http"
        }

    def _run(self, *args, **kwargs):

        payload = None

        if args:
            first = args[0]

            if isinstance(first, dict):
                payload = first
            elif isinstance(first, str) and len(args) > 1:
                payload = {"tool": first, "input": args[1]}
            else:
                payload = {}
        else:
            payload = kwargs or {}

        if "argument" in payload:
            payload = payload["argument"]

        tool_name = payload.get("tool") or payload.get("name")
        input_dict = payload.get("input", {})

        if not tool_name:
            return {"error": "Missing tool name"}

        try:
            with suppress_output():
                with MCPServerAdapter(self._get_server_params()) as tools:

                    tools = list(tools)

                    target = None
                    for t in tools:
                        if t.name == tool_name:
                            target = t
                            break

                    if not target:
                        return {
                            "error": f"Tool {tool_name} not found",
                            "available": [t.name for t in tools]
                        }

                    return target._run(**input_dict)

        except Exception as e:
            return {"error": str(e)}
