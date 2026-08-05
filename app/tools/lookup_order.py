from app.services.order_service import OrderService


class LookupOrderTool:

    name = "lookup_order"

    def __init__(self, order_service: OrderService):
        self.order_service = order_service

    def run(self, arguments: dict):

        order_id = arguments.get("order_id", "").strip().upper()

        if not order_id:
            return {
                "success": False,
                "tool": self.name,
                "data": None,
                "error": "Missing order_id."
            }

        order = self.order_service.get_order_by_id(order_id)

        if order is None:
            return {
                "success": False,
                "tool": self.name,
                "data": None,
                "error": "Order not found."
            }

        return {
            "success": True,
            "tool": self.name,
            "data": order,
            "error": None
        }