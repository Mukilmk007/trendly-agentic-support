class ConversationState:

    def __init__(self):

        # Last referenced order
        self.current_order = None

        # Last retrieved policy
        self.current_policy = None

        # Tool outputs
        self.observations = []

        # Conversation history
        self.history = []

    def set_current_order(self, order):
        self.current_order = order

    def set_current_policy(self, policy):
        self.current_policy = policy

    def add_observation(self, observation):
        self.observations.append(observation)

    def add_history(self, role: str, message: str):
        self.history.append({
            "role": role,
            "message": message
        })

    def clear_observations(self):
        self.observations = []

    def get_planner_context(self):

        order = None

        if self.current_order:

            order = {
                "order_id": self.current_order.get("order_id"),
                "status": self.current_order.get("status"),
                "delivered_at": self.current_order.get("delivered_at"),
                "expected_delivery": self.current_order.get("expected_delivery"),
                "carrier": self.current_order.get("carrier"),
                "tracking_number": self.current_order.get("tracking_number"),
                "shipping_city": self.current_order.get("shipping_city"),
                "payment_method": self.current_order.get("payment_method"),
                "items": [
                    item.get("name")
                    for item in self.current_order.get("items", [])
                ]
            }

        return {
            "history": self.history[-6:],
            "current_order": order,
            "current_policy": self.current_policy
        }

    def get_recent_history(self, limit: int = 6):
        return self.history[-limit:]