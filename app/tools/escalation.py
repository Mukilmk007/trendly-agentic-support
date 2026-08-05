from app.state.conversation_state import ConversationState


class EscalationTool:

    name = "escalate"

    def __init__(self, state: ConversationState):
        self.state = state

    def run(self, arguments: dict):

        reason = arguments.get(
            "reason",
            "Escalation requested."
        )

        order = self.state.current_order

        summary = {
            "reason": reason,
            "conversation": self.state.get_recent_history()
        }

        if order:

            summary.update({
                "order_id": order.get("order_id"),
                "customer_id": order.get("customer_id"),
                "status": order.get("status"),
                "carrier": order.get("carrier"),
                "tracking_number": order.get("tracking_number")
            })

        return {
            "success": True,
            "tool": self.name,
            "data": {
                "escalated": True,
                "summary": summary
            },
            "error": None
        }