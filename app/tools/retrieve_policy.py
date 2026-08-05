from app.services.policy_service import PolicyService


class RetrievePolicyTool:

    name = "retrieve_policy"

    def __init__(self, policy_service: PolicyService):
        self.policy_service = policy_service

    def run(self, arguments: dict):

        section = arguments.get("section")

        if not section:
            return {
                "success": False,
                "tool": self.name,
                "data": None,
                "error": "Missing policy section."
            }

        policy = self.policy_service.get_section(section)

        if policy is None:
            return {
                "success": False,
                "tool": self.name,
                "data": None,
                "error": "Policy section not found."
            }

        return {
            "success": True,
            "tool": self.name,
            "data": {
                "section": section,
                "content": policy
            },
            "error": None
        }