from app.services.order_service import OrderService

service = OrderService("data/orders.json")
service.initialize()

print("Customers:", len(service.customers))
print("Orders:", len(service.orders))

print(service.get_order_by_id("TR-4521"))
print(service.get_customer_by_id("C-100"))
print(service.get_orders_by_customer("C-100"))
print(service.order_exists("TR-4521"))
print(service.order_exists("TR-9999"))