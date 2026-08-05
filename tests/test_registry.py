from app.tools.tool_registry import ToolRegistry

from app.tools.lookup_order import LookupOrderTool

registry = ToolRegistry()

registry.register(
    LookupOrderTool(None)
)

print(
    registry.list_tools()
)