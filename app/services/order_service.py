import json
from pathlib import Path


class OrderService:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

        # Raw data
        self.orders = []
        self.customers = []

        # Indexes
        self.orders_by_id = {}
        self.customers_by_id = {}
        self.orders_by_customer = {}

    def load_data(self):
        """Load customers and orders from the JSON file."""
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            self.customers = data["customers"]
            self.orders = data["orders"]

        except FileNotFoundError:
            raise FileNotFoundError(
                f"Could not find data file: {self.file_path}"
            )

        except json.JSONDecodeError:
            raise ValueError(
                f"Invalid JSON in {self.file_path}"
            )

    def build_indexes(self):
        """Build dictionaries for fast O(1) lookups."""

        # Order ID -> Order
        self.orders_by_id = {
            order["order_id"]: order
            for order in self.orders
        }

        # Customer ID -> Customer
        self.customers_by_id = {
            customer["customer_id"]: customer
            for customer in self.customers
        }

        # Customer ID -> List of Orders
        self.orders_by_customer = {}

        for order in self.orders:
            customer_id = order["customer_id"]

            if customer_id not in self.orders_by_customer:
                self.orders_by_customer[customer_id] = []

            self.orders_by_customer[customer_id].append(order)

    def initialize(self):
        """Load data and build indexes."""
        self.load_data()
        self.build_indexes()

    def get_order_by_id(self, order_id: str):
        return self.orders_by_id.get(order_id)

    def get_customer_by_id(self, customer_id: str):
        return self.customers_by_id.get(customer_id)

    def get_orders_by_customer(self, customer_id: str):
        return self.orders_by_customer.get(customer_id, [])

    def order_exists(self, order_id: str):
        return order_id in self.orders_by_id