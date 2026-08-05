from datetime import datetime, timezone

class EligibilityService:

    REFERENCE_DATE = datetime(2026, 8, 1, tzinfo=timezone.utc)

    NON_RETURNABLE_CATEGORIES = {
        "innerwear",
        "jewellery",
        "beauty",
        "fragrance",
        "gift_cards",
        "face_masks",
        "socks"
    }

    RETURN_WINDOW_DAYS = 30

    def check(self, order: dict, action: str):

        if result := self._is_cancelled(order, action):
            return result

        if result := self._is_delivered(order, action):
            return result

        if result := self._is_within_window(order, action):
            return result

        if result := self._is_non_returnable(order, action):
            return result

        if result := self._is_final_sale(order, action):
            return result

        if action == "exchange":
            if result := self._is_exchange_allowed(order):
                return result

        return {
            "eligible": True,
            "action": action,
            "reason": f"Order is eligible for {action}."
        }

    def _is_cancelled(self, order, action):

        if order["status"] == "cancelled":
            return {
                "eligible": False,
                "action": action,
                "reason": "Cancelled orders cannot be returned or exchanged."
            }

        return None

    def _is_delivered(self, order, action):

        if order["status"] != "delivered":
            return {
                "eligible": False,
                "action": action,
                "reason": "Only delivered orders are eligible for returns or exchanges."
            }

        return None

    def _is_within_window(self, order, action):

        delivered_at = order.get("delivered_at")

        if not delivered_at:
            return {
                "eligible": False,
                "action": action,
                "reason": "Delivery date is unavailable."
            }

        delivered_date = datetime.fromisoformat(
            delivered_at.replace("Z", "+00:00")
        )

        today = self.REFERENCE_DATE

        days = (today - delivered_date).days

        if days > self.RETURN_WINDOW_DAYS:
            return {
                "eligible": False,
                "action": action,
                "reason": "Return window has expired."
            }

        return None

    def _is_non_returnable(self, order, action):

        for item in order["items"]:

            category = item["category"].lower()

            if category in self.NON_RETURNABLE_CATEGORIES:

                return {
                    "eligible": False,
                    "action": action,
                    "reason": f"{category.title()} items cannot be returned or exchanged."
                }

        return None

    def _is_final_sale(self, order, action):

        for item in order["items"]:

            if item.get("final_sale"):

                if action == "return":

                    return {
                        "eligible": False,
                        "action": action,
                        "reason": "Final sale items cannot be returned."
                    }

        return None

    def _is_exchange_allowed(self, order):

        if order.get("exchange_completed"):

            return {
                "eligible": False,
                "action": "exchange",
                "reason": "This order has already been exchanged once."
            }

        return None