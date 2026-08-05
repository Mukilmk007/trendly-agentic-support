from app.services.gemini_service import GeminiService
from app.services.order_service import OrderService
from app.services.policy_service import PolicyService

from app.tools.lookup_order import LookupOrderTool
from app.tools.retrieve_policy import RetrievePolicyTool
from app.tools.eligibility import EligibilityTool
from app.tools.escalation import EscalationTool
from app.tools.tool_registry import ToolRegistry
from app.state.conversation_state import ConversationState
import time


class ReActController:

    def __init__(self):

        self.state = ConversationState()

        # AI Service
        self.gemini = GeminiService()

        # Data Services
        self.order_service = OrderService("data/orders.json")
        self.order_service.initialize()

        self.policy_service = PolicyService("data/trendly_policy.md")
        self.policy_service.initialize()

        # Tools
        self.lookup_tool = LookupOrderTool(self.order_service)
        self.policy_tool = RetrievePolicyTool(self.policy_service)
        self.eligibility_tool = EligibilityTool(self.state)
        self.escalation_tool = EscalationTool(self.state)

        # Tool Registry
        self.registry = ToolRegistry()

        self.registry.register(self.lookup_tool)
        self.registry.register(self.policy_tool)
        self.registry.register(self.eligibility_tool)
        self.registry.register(self.escalation_tool)

    def handle_message(self, user_message: str):

            self.state.clear_observations()

            self.state.add_history(
                "user",
                user_message
            )

            plan = self._create_plan(user_message)

            observations = self._execute_plan(plan)

            response = self._generate_response(
                user_message,
                observations
            )

            self.state.add_history(
                "assistant",
                response
            )

            return response

    def _create_plan(self, user_message: str):

        plan = self.gemini.plan(
            user_message,
            self.state
        )

        print("PLAN:", plan)

        return plan

    def _execute_plan(self, plan):

        observations = []

        actions = plan.get("actions", [])

        for action in actions:

            tool_name = action.get("tool")
            arguments = action.get("arguments", {})

            tool = self.registry.get_tool(tool_name)

            if tool is None:

                result = {
                    "success": False,
                    "tool": tool_name,
                    "data": None,
                    "error": f"Unknown tool: {tool_name}"
                }

            else:

                try:

                    result = tool.run(arguments)
                    print("Tool Result:", result)

                    if (
                        tool_name == "lookup_order"
                        and result["success"]
                    ):
                        self.state.set_current_order(
                            result["data"]
                        )

                    elif (
                        tool_name == "retrieve_policy"
                        and result["success"]
                    ):
                        self.state.set_current_policy(
                            result["data"]
                        )

                except Exception as e:

                    result = {
                        "success": False,
                        "tool": tool_name,
                        "data": None,
                        "error": str(e)
                    }

            observations.append(result)
            self.state.add_observation(result)

        return observations

    def _generate_response(
        self,
        user_message: str,
        observations
    ):

        return self.gemini.generate_response(
            user_message,
            observations,
            self.state
        )
    def reset_conversation(self):

        self.state = ConversationState()

        self.eligibility_tool.state = self.state
        self.escalation_tool.state = self.state