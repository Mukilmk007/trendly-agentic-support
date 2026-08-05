from app.services.order_service import OrderService
from app.services.eligibility_service import EligibilityService


order_service = OrderService("data/orders.json")
order_service.initialize()

eligibility_service = EligibilityService()

# Test with a delivered order
order = order_service.get_order_by_id("TR-4527")

result = eligibility_service.check(
    order=order,
    action="return"
)

print(result)