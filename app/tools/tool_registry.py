class ToolRegistry:

    def __init__(self):
        self.tools = {}

    def register(self, tool):

        self.tools[tool.name] = tool

    def get_tool(self, tool_name):

        return self.tools.get(tool_name)

    def has_tool(self, tool_name):

        return tool_name in self.tools

    def list_tools(self):

        return list(self.tools.keys())