from app.services.eligibility_service import EligibilityService


class EligibilityTool:

    name = "check_eligibility"

    def __init__(self, conversation_state):
        self.state = conversation_state
        self.service = EligibilityService()

    def run(self, arguments):

        action = arguments.get("action")

        if action is None:
            return {
                "success": False,
                "tool": self.name,
                "data": None,
                "error": "Missing action."
            }

        order = self.state.current_order

        if order is None:
            return {
                "success": False,
                "tool": self.name,
                "data": None,
                "error": "No order available in conversation state."
            }

        result = self.service.check(
            order=order,
            action=action
        )

        return {
            "success": True,
            "tool": self.name,
            "data": result,
            "error": None
        }