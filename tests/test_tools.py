from app.services.order_service import OrderService
from app.services.policy_service import PolicyService

from app.tools.lookup_order import LookupOrderTool
from app.tools.retrieve_policy import RetrievePolicyTool


order_service = OrderService("data/orders.json")
order_service.initialize()

policy_service = PolicyService("data/trendly_policy.md")
policy_service.initialize()

lookup_tool = LookupOrderTool(order_service)
policy_tool = RetrievePolicyTool(policy_service)

print(lookup_tool.run("TR-4521"))
print(policy_tool.run("shipping"))